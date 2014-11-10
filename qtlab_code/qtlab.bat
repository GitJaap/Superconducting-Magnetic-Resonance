:: qtlab.bat
:: Runs QTlab on Windows
::
:: QTlab needs gnuplot, Console2 and GTK to exist in the system PATH.
:: They can be defined globally in "configuration_panel => system =>
:: advanced => system_variables", or on the commandline just before
:: execution of QTlab. The latter is done below with the "SET PATH"
:: statements. Comment or uncomment these lines as needed.

@ECHO OFF

:: Add gnuplot to PATH ("binary" folder for >= 4.4.0, "bin" folder for 4.3)
SET PATH=%CD%\3rd_party\gnuplot\binary;%PATH%

:: Add Console2 to PATH
SET PATH=%CD%\3rd_party\Console2\;%PATH%

:: Add GTK to PATH and set GTK_BASEPATH (not needed if using
:: pygtk-all-in-one installer).
::SET GTK_BASEPATH=%CD%\3rd_party\gtk
::SET PATH=%CD%\3rd_party\gtk\bin;%CD%\3rd_party\gtk\lib;%PATH%

:: Check for version of python
IF EXIST c:\Python27\python.exe (
    SET PYTHON_PATH=c:\Python27
    GOTO mark1
)
IF EXIST c:\python26\python.exe (
    SET PYTHON_PATH=c:\python26
    GOTO mark1
)
:mark1

:: Run QTlab
IF EXIST %PYTHON_PATH%\Scripts\ipython.exe (
	start Console -w "QTLab" -r "/k %PYTHON_PATH%\python.exe %PYTHON_PATH%\Scripts\ipython.exe --gui=gtk -i source/qtlab_shell.py -- %*"
	GOTO EOF
)

echo Failed to run qtlab.bat %PYTHON_PATH%
pause
:EOF
