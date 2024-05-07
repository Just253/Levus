@echo off
for /f %%i in ('powershell -Command "Get-Content config.json | ConvertFrom-Json | % jar.jarFilePath"') do set jarFilePath=%%i
for /f %%i in ('powershell -Command "Get-Content config.json | ConvertFrom-Json | % jar.options"') do set jarOptions=%%i
for /f %%i in ('powershell -Command "Get-Content config.json | ConvertFrom-Json | % py.pyFilePath"') do set pyFilePath=%%i
for /f %%i in ('powershell -Command "Get-Content config.json | ConvertFrom-Json | % py.args"') do set pyArgs=%%i

start /b java %jarOptions% -jar "%jarFilePath%"
start /b python "%pyFilePath%" %pyArgs%