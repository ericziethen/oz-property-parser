
@echo off

setlocal

rem This selfwrapper calls itself again to avoid closing the command window when exiting
IF "%selfWrapped%"=="" (
  REM this is necessary so that we can use "exit" to terminate the batch file,
  REM and all subroutines, but not the original cmd.exe
  SET selfWrapped=true
  %ComSpec% /s /c ""%~0" %*"
  GOTO :EOF
)

set SCRIPT_DIR=%~dp0
set LINTER_DIR=%SCRIPT_DIR%Linting
set ERROR_FOUND=

echo ### Start Linting ###
call:run_linter "%LINTER_DIR%\RunBandit.bat"
call:run_linter "%LINTER_DIR%\RunMyPy.bat"
call:run_linter "%LINTER_DIR%\RunPycodestyle.bat"
call:run_linter "%LINTER_DIR%\RunPydocstyle.bat"
call:run_linter "%LINTER_DIR%\RunPylint.bat"
echo ### Linting finished ###

if defined ERROR_FOUND (
    call:error
) else (
    call:end
)


: #########################################
: ##### START OF FUNCTION DEFINITIONS #####
: #########################################
:run_linter
set LINDER_SCRIPT=%~1

echo ### LINTER START - '%LINDER_SCRIPT%' ###
call "%LINDER_SCRIPT%"

set return_code=%errorlevel%
if %return_code% gtr 0 (
    set ERROR_FOUND=TRUE
    echo   Issues Found
) else (
    echo   No Issues
)
echo ### LINTER END - '%LINDER_SCRIPT%' ###
echo[
goto:eof
: #######################################
: ##### END OF FUNCTION DEFINITIONS #####
: #######################################


:error
echo !!! SOME LINTING ISSUE FOUND, CHECK OUTPUT
popd
endlocal
exit 1

:end
echo !!! NO LINTING ISSUE FOUND
popd
endlocal
exit 0
