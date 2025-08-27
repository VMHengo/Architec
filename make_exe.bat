@echo off
REM Activate your venv
call .qtcreator\Python_3_10_10venv\Scripts\activate.bat

REM Build the exe
pyinstaller --onefile --noconsole mainwindow.py

REM Deactivate venv
call deactivate

REM Show where the exe ended up
echo.
echo Build complete! Your EXE is at: dist\mainwindow.exe
pause
