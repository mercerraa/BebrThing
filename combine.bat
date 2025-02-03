@echo off
setlocal enabledelayedexpansion

:: Set the source folder and the output file
set source_folder=.\
set output_file=.\BebrData.js

:: Initialize the output file by creating it or clearing it
> "%output_file%" echo.

:: Loop through each file in the source folder
for %%f in (%source_folder%\*) do (
    if not "%%~xff"==".js" (
        echo Concatenating %%f
        type "%%f" >> "%output_file%"
    )
)

echo Done.
pause
