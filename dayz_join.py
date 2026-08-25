#!/usr/bin/env python3
"""
DayZ Linux Toolkit

Abre o DayZ diretamente pela Steam e conecta a um servidor,
sem depender do launcher oficial.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


TOOLKIT = Path(__file__).resolve().parent

OFFICIAL_SERVERS = TOOLKIT / "servers" / "official"
LEGACY_SERVERS = TOOLKIT / "servers"

LOCAL_CONFIG = (
    Path.home()
    / ".config/dayz-linux-toolkit"
)

LOCAL_SERVERS = LOCAL_CONFIG / "servers"

LOGS = (
    Path.home()
    / ".local/state/dayz-linux-toolkit/logs"
)

DAYZ_DIRECTORY = (
    Path.home()
    / ".local/share/Steam/steamapps/common/DayZ"
)

WORKSHOP_DIRECTORY = (
    Path.home()
    / ".local/share/Steam/steamapps/workshop/content/221100"
)

STEAM_COMMAND = "steam"
DAYZ_APP_ID = "221100"


class DayZJoinError(RuntimeError):
    """Erro ao preparar ou iniciar o DayZ."""


def load_server(server_name: str) -> dict[str, Any]:
    filename = f"{server_name}.json"

    candidates = (
        LOCAL_SERVERS / filename,
        OFFICIAL_SERVERS / filename,
        LEGACY_SERVERS / filename,
    )

    path = next(
        (
            candidate
            for candidate in candidates
            if candidate.is_file()
        ),
        None,
    )

    if path is None:
        searched = "\n".join(
            f"  - {candidate}"
            for candidate in candidates
        )

        raise DayZJoinError(
            "Configuração não encontrada. "
            "Locais pesquisados:\n"
            f"{searched}"
        )

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    required = (
        "name",
        "address",
        "port",
        "player_name",
        "mods",
    )

    for field in required:
        if field not in data:
            raise DayZJoinError(
                f"Campo ausente em {path.name}: {field}"
            )

    if not isinstance(data["mods"], list):
        raise DayZJoinError(
            "O campo 'mods' deve ser uma lista."
        )

    return data


def validate_directories() -> None:
    if not DAYZ_DIRECTORY.is_dir():
        raise DayZJoinError(
            f"Pasta do DayZ não encontrada: {DAYZ_DIRECTORY}"
        )

    if not WORKSHOP_DIRECTORY.is_dir():
        raise DayZJoinError(
            f"Workshop do DayZ não encontrado: {WORKSHOP_DIRECTORY}"
        )


def create_mod_links(
    mods: list[list[str]],
) -> tuple[list[str], list[str]]:
    """
    Cria links como:

        DayZ/@ws_2691041685
            ->
        workshop/content/221100/2691041685
    """

    mod_arguments: list[str] = []
    missing: list[str] = []

    for entry in mods:
        if not isinstance(entry, list) or len(entry) != 2:
            raise DayZJoinError(
                f"Entrada de mod inválida: {entry!r}"
            )

        workshop_id = str(entry[0])
        display_name = str(entry[1])

        source = WORKSHOP_DIRECTORY / workshop_id
        link_name = f"@ws_{workshop_id}"
        destination = DAYZ_DIRECTORY / link_name

        if not source.is_dir():
            missing.append(
                f"{display_name} ({workshop_id})"
            )
            continue

        if destination.is_symlink():
            current_target = destination.resolve()

            if current_target != source.resolve():
                destination.unlink()
                destination.symlink_to(
                    source,
                    target_is_directory=True,
                )

        elif destination.exists():
            raise DayZJoinError(
                f"Existe um arquivo/pasta que não é link: {destination}"
            )

        else:
            destination.symlink_to(
                source,
                target_is_directory=True,
            )

        mod_arguments.append(link_name)

    return mod_arguments, missing


def write_log(
    server_name: str,
    command: list[str],
    mods: list[list[str]],
) -> Path:
    LOGS.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    path = LOGS / f"{server_name}_{timestamp}.log"

    lines = [
        f"Servidor: {server_name}",
        f"Data: {timestamp}",
        "",
        "Comando:",
        " ".join(command),
        "",
        "Mods:",
    ]

    for workshop_id, display_name in mods:
        lines.append(
            f"{workshop_id} | {display_name}"
        )

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return path


def build_command(
    config: dict[str, Any],
    mod_arguments: list[str],
) -> list[str]:
    address = config["address"]
    port = int(config["port"])
    player_name = config["player_name"]
    password = str(config.get("password", "")).strip()

    command = [
        STEAM_COMMAND,
        "-applaunch",
        DAYZ_APP_ID,
        f"-connect={address}:{port}",
        "-nolauncher",
        "-nosplash",
        "-skipintro",
        f"-name={player_name}",
        f"-mod={';'.join(mod_arguments)}",
    ]

    if password:
        command.append(f"-password={password}")

    return command


def print_summary(
    config: dict[str, Any],
    mods: list[list[str]],
) -> None:
    print("=" * 68)
    print(" DayZ Linux Toolkit")
    print("=" * 68)
    print()
    print("Servidor:", config["name"])
    print(
        "Endereço:",
        f"{config['address']}:{config['port']}",
    )
    print("Jogador:", config["player_name"])
    print("Mods:", len(mods))
    print()


def main() -> int:
    try:
        if len(sys.argv) != 2:
            print(
                f"Uso: {Path(sys.argv[0]).name} SERVIDOR",
                file=sys.stderr,
            )
            print(
                "Exemplo: python3 dayz_join.py infinity",
                file=sys.stderr,
            )
            return 2

        server_name = sys.argv[1].strip()

        validate_directories()
        config = load_server(server_name)

        print_summary(config, config["mods"])

        mod_arguments, missing = create_mod_links(
            config["mods"]
        )

        if missing:
            print("Mods ausentes:", file=sys.stderr)

            for mod in missing:
                print(f"  - {mod}", file=sys.stderr)

            print()
            print(
                "Abra a Steam e baixe os mods ausentes antes de continuar.",
                file=sys.stderr,
            )
            return 1

        print("Todos os mods foram encontrados.")
        print("Links locais preparados.")

        command = build_command(
            config,
            mod_arguments,
        )

        log_path = write_log(
            server_name,
            command,
            config["mods"],
        )

        print("Log:", log_path)
        print()
        print("Iniciando DayZ...")

        subprocess.Popen(
            command,
            cwd=DAYZ_DIRECTORY,
            start_new_session=True,
        )

        return 0

    except (
        DayZJoinError,
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
        ValueError,
    ) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
