# Zellno DayZ Linux Toolkit

An open-source Linux utility that launches DayZ through Steam, loads the
mods declared in a JSON profile, and connects directly to a server without
depending on the official launcher's mod-loading workflow.

The project was originally created for the **Zellno DayZ Server | Full PvE**,
but it also supports personal profiles for other DayZ servers.

## Current status

- Linux only
- Tested on Linux Mint 22.2
- Steam and Proton
- Official Zellno server profile
- Automatic symbolic links for Workshop mods
- Mod validation before launch
- Direct server connection
- Personal JSON profiles
- Local execution logs

The Toolkit does not download or subscribe to mods. Required mods must
already be installed through the Steam Workshop.

## Requirements

- Linux
- Python 3
- Steam for Linux
- DayZ installed through Steam
- Proton configured for DayZ
- Required Workshop mods already downloaded

The current version expects the default Steam library at
`~/.local/share/Steam/steamapps`.

## Installation

Run `git clone https://github.com/Zellno/dayz-linux-toolkit.git`, enter the
new directory with `cd dayz-linux-toolkit`, and execute `./install.sh`.

The installer creates the command `~/.local/bin/dayz-join`.

## Official Steam Workshop collection

Subscribe to all required mods through the official collection and wait for
Steam to finish downloading them:

https://steamcommunity.com/sharedfiles/filedetails/?id=3790094607

The collection references the original Workshop publications. It does not
repack, reupload, modify, or redistribute third-party mods.

## Join the Zellno server

Run:

    dayz-join zellno

The Toolkit validates the mods, prepares local links, builds the `-mod=`
argument, writes a log, launches DayZ through Steam, and connects directly.

- Server: Zellno DayZ Server | Full PvE
- Map: Chernarus
- Game Port: 89.43.106.164:20400
- Query Port: 89.43.106.164:20410
- BattleMetrics: https://www.battlemetrics.com/servers/dayz/40889989

## Personal server profiles

Store personal profiles in:

    ~/.config/dayz-linux-toolkit/servers/

For example:

    ~/.config/dayz-linux-toolkit/servers/my-server.json

Then run:

    dayz-join my-server

See `servers/examples/example-server.json` for the supported JSON format.

Profiles are searched in this order:

1. personal profiles in `~/.config/dayz-linux-toolkit/servers`
2. official profiles distributed with the project
3. legacy profiles in the root `servers` directory

The mod order declared in the JSON file is preserved in the DayZ `-mod=`
argument.

## Logs

Execution logs are stored in:

    ~/.local/state/dayz-linux-toolkit/logs/

Logs contain the selected server, launch command, and ordered mod list.

## Limitações e uso em português

O Toolkit foi criado para jogadores de DayZ no Linux que enfrentam problemas
com o fluxo do launcher oficial.

Após instalar o projeto e baixar os mods necessários pela Steam Workshop,
entre no servidor Zellno com:

    dayz-join zellno

Perfis particulares de outros servidores podem ser colocados em:

    ~/.config/dayz-linux-toolkit/servers/

Limitações atuais:

- somente Linux
- não baixa nem assina mods automaticamente
- não gerencia inscrições da Steam Workshop
- não consulta automaticamente a lista de mods do servidor
- não possui interface gráfica
- Steam Deck ainda não homologado
- utiliza atualmente o caminho padrão da Steam

Windows não faz parte do escopo atual, pois já possui outras ferramentas
disponíveis e não é o ambiente que originou este projeto.

## Security and privacy

Public profiles must not contain administrative passwords, RCon passwords,
API keys, credentials, personal paths, or private server information.

A normal server access password may be placed in a personal profile, but that
file must not be committed to a public repository.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

The license covers only the source code of this project. It does not grant
rights over DayZ, Steam, Workshop mods, or third-party content.

## Disclaimer

This is an independent and unofficial project. It is not affiliated with
Bohemia Interactive or Valve Corporation. DayZ, Steam, and other trademarks
belong to their respective owners.
