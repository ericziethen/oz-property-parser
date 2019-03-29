@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0..

pushd %PROJ_MAIN_DIR%

set PACKAGE_ROOT=oz-property-parser

set PYTHONPATH=%PYTHONPATH%;%PACKAGE_ROOT%

rem Test directories are specified in Pytest.ini
pytest --cov=%PACKAGE_ROOT%


rem Some pytest resources
rem https://hackingthelibrary.org/posts/2018-02-09-code-coverage/
rem https://code.activestate.com/pypm/pytest-cov/
rem https://docs.pytest.org/en/latest/usage.html
rem http://blog.thedigitalcatonline.com/blog/2018/07/05/useful-pytest-command-line-options/
rem https://www.patricksoftwareblog.com/python-unit-testing-structuring-your-project/

:error

:end

popd

endlocal
