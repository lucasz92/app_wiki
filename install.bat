@echo off
echo ========================================
echo    WikiApp - Instalador Automatico
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Instalando dependencias basicas...
pip install PyQt6 python-dateutil

echo.
echo ¿Deseas instalar WeasyPrint para exportacion PDF mejorada? (s/n)
set /p install_weasy=

if /i "%install_weasy%"=="s" (
    echo Instalando WeasyPrint...
    pip install weasyprint
    if errorlevel 1 (
        echo ADVERTENCIA: No se pudo instalar WeasyPrint
        echo La exportacion PDF usara el motor basico de Qt
    ) else (
        echo WeasyPrint instalado correctamente!
    )
)

echo.
echo Creando directorios necesarios...
if not exist "config" mkdir config
if not exist "styles" mkdir styles

echo.
echo ========================================
echo    Instalacion completada!
echo ========================================
echo.
echo Para ejecutar WikiApp:
echo   python main.py
echo.
echo O haz doble clic en run.bat
echo.
pause