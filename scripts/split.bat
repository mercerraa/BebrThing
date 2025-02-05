@echo off
setlocal enabledelayedexpansion

:: Define the input file and output files
set inputFile=BebrData.js
set outputFile1=BebrByggnad.js
set outputFile2=BebrMinne.js

:: Initialize a flag to track when we find "let polygon"
set foundPolygon=0

:: Create/clear output files initially
> %outputFile1% echo.
> %outputFile2% echo.

:: Open the input file and process it line by line
(for /f "delims=" %%a in (%inputFile%) do (
    if !foundPolygon! equ 0 (
        echo %%a>>%outputFile1%
        echo %%a | findstr /c:"let polygon" >nul
        if !errorlevel! equ 0 (
            set foundPolygon=1
        )
    ) else (
        echo %%a>>%outputFile2%
    )
)) 

echo File has been split successfully.
