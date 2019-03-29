@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..

pushd %PROJ_MAIN_DIR%

for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a

set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set datetimef=%Yr%.%Mon%.%Day%_%Hr%-%Min%-%Sec%

!!! CONFIGURE SOURCE ROOT HERE !!!
set SOURCE_ROOT=oz-property-parser
set PYTHON_PROG=#PYTHON_PROG_NAME#

pushd %SOURCE_ROOT%
python -m pyinstrument "%PYTHON_PROG%" ..\test_files > ..\profiling\profile_%datetimef%.txt
popd

:end

popd

endlocal
