@echo off
title Publication GitHub - YAELDI1
echo =============================================================
echo   Publication Automatique sur GitHub : https://github.com/YAELDI1
echo =============================================================
echo.
echo Choisissez le nom de votre depot GitHub :
echo   [1] YAELDI1.github.io  (URL directe d'elite : https://yaeldi1.github.io)
echo   [2] portfolio          (URL : https://yaeldi1.github.io/portfolio/)
echo.
set /p choice="Votre choix (1 ou 2, defaut: 1) : "
if "%choice%"=="2" (
    set REPONAME=portfolio
) else (
    set REPONAME=YAELDI1.github.io
)

echo.
echo Configuration du remote vers https://github.com/YAELDI1/%REPONAME%.git ...
git remote remove origin 2>nul
git remote add origin https://github.com/YAELDI1/%REPONAME%.git
git branch -M main

echo.
echo Envoi des fichiers vers GitHub...
git push -u origin main

echo.
echo =============================================================
if %errorlevel% equ 0 (
    echo SUCCES ! Fichiers envoyes avec succes sur GitHub.
    echo.
    echo Pour activer l'hebergement gratuit :
    echo 1. Ouvrez : https://github.com/YAELDI1/%REPONAME%/settings/pages
    echo 2. Sous 'Build and deployment', choisissez Source: 'Deploy from a branch'
    echo 3. Selectionnez la branche 'main' et cliquez sur 'Save'.
    echo.
    if "%REPONAME%"=="YAELDI1.github.io" (
        echo Votre site sera accessible sur : https://yaeldi1.github.io
    ) else (
        echo Votre site sera accessible sur : https://yaeldi1.github.io/portfolio/
    )
) else (
    echo NOTE : Si le push a echoue, creez d'abord le depot sur :
    echo   https://github.com/new
    echo en lui donnant exactement le nom : %REPONAME%
    echo puis relancez ce script !
)
echo =============================================================
pause
