::!/usr/bin/env bash
:: Raven - UserBot


@echo off

:::  ██████╗   █████╗  ██╗   ██╗ ███████╗ ███╗   ██╗
:::  ██╔══██╗ ██╔══██╗ ██║   ██║ ██╔════╝ ████╗  ██║
:::  ██████╔╝ ███████║ ██║   ██║ █████╗   ██╔██╗ ██║
:::  ██╔══██╗ ██╔══██║ ╚██╗ ██╔╝ ██╔══╝   ██║╚██╗██║
:::  ██║  ██║ ██║  ██║  ╚████╔╝  ███████╗ ██║ ╚████║
:::  ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚══════╝ ╚═╝  ╚═══╝
:::
:::      Visit @TheRaven for updates!!

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

pip show telethon >nul 2>&1 || goto install

:install
pip install -r requirements.txt
pip install -r resources/extras/optional-requirements.txt
echo Installed all dependencies
echo Starting Raven.

python -m core