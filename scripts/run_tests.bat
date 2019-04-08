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

set PROJ_MAIN_DIR=%~dp0..

pushd %PROJ_MAIN_DIR%

set PACKAGE_ROOT=oz_property_parser

set PYTHONPATH=%PYTHONPATH%;%PACKAGE_ROOT%

rem Test directories are specified in Pytest.ini
pytest --cov=%PACKAGE_ROOT%
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Issues Found
    goto exit_ok
) else (
    echo *** Some Issues Found
    goto exit_error
)

rem Some pytest resources
rem https://hackingthelibrary.org/posts/2018-02-09-code-coverage/
rem https://code.activestate.com/pypm/pytest-cov/
rem https://docs.pytest.org/en/latest/usage.html
rem http://blog.thedigitalcatonline.com/blog/2018/07/05/useful-pytest-command-line-options/
rem https://www.patricksoftwareblog.com/python-unit-testing-structuring-your-project/

:exit_error
popd
endlocal
exit /B 1

:exit_ok
popd
endlocal
exit /B 0
