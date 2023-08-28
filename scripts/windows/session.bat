:: Raven - UserBot


@echo off
cls
:::  ██████╗   █████╗  ██╗   ██╗ ███████╗ ███╗   ██╗
:::  ██╔══██╗ ██╔══██╗ ██║   ██║ ██╔════╝ ████╗  ██║
:::  ██████╔╝ ███████║ ██║   ██║ █████╗   ██╔██╗ ██║
:::  ██╔══██╗ ██╔══██║ ╚██╗ ██╔╝ ██╔══╝   ██║╚██╗██║
:::  ██║  ██║ ██║  ██║  ╚████╔╝  ███████╗ ██║ ╚████║
:::  ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚══════╝ ╚═╝  ╚═══╝

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

echo Starting dependency installation in $sec seconds...

echo Installing Dependencies.
if exist resources/session/ssgen.py goto sessionStart
echo Fetching ssgen.py from GitHub...
curl https://raw.githubusercontent.com/itzNightmare17/Raven/main/resources/session/ssgen.py -o resources/session/ssgen.py

:sessionStart
cls
python resources/session/ssgen.py

exit /b 1
