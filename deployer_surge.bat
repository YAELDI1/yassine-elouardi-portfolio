@echo off
title Deploiement Portfolio - Yassine EL OUARDI
echo =============================================================
echo   Deploiement Gratuit & Immediat de Votre Portfolio
echo =============================================================
echo.
echo Votre site va etre deploye en ligne sur l'adresse :
echo   https://yassine-elouardi.surge.sh
echo.
echo (Lors du premier lancement, Surge vous demandera simplement
echo  votre email et un mot de passe pour securiser votre domaine).
echo.
pause
cd /d "%~dp0"
npx --yes surge . yassine-elouardi.surge.sh
echo.
echo =============================================================
echo Deploiement termine !
echo Votre portfolio est en ligne.
echo =============================================================
pause
