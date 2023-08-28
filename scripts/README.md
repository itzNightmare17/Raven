
## Scripts

This directory contains the various shellscripts for Raven.<br>Do not run them directly, instead, use the ```raven``` file with arguments.

## Shell scripts
* `installer.sh` - Script to install Raven
* `install-termux` - Script to install Raven in termux
* `session` - Script to generator String Session
* `startup` - Script to start Raven

## `installer.sh`
Installs Raven in machine. Use custom flags to define installation configs or don't provide any flags to use default configs

```bash
./raven install [Options]
```
### Options
```
    --help: Show message containing usage of the script
    --dir: Install Raven in a custom or specified directory, Default is current directory/Raven
    --branch: Clone custom or specificed Raven repo branch like main or dev, Default is main
    --env-file: Path to .env file, required only if using any env file other than .env
    --no-root: Install Raven without root access
```

## `install-termux`
```bash
./raven termux
```
Installs Raven in termux.

## `session`
Generates string session of telethon or pyrogram.
```bash
./raven session
```

## `start`
Starts the bot.
```bash
./raven start [Options]
```

### Options
```
    --help: Show the help message
    --http-server: Start a http server serving files over http, default port: 8000
```
