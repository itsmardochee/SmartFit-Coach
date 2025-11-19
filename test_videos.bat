@echo off
REM Script batch pour tester facilement le comptage sur les vidéos du dataset
REM Usage: test_videos.bat [squat|push-up] [numero_video]

echo.
echo ========================================
echo   SmartFit Coach - Test sur Videos
echo ========================================
echo.

REM Activation de l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
) else (
    echo ERREUR: Environnement virtuel non trouve!
    echo Creez-le d'abord avec: python -m venv venv
    pause
    exit /b 1
)

REM Déterminer l'exercice et la vidéo
set EXERCISE=%1
set VIDEO_NUM=%2

if "%EXERCISE%"=="" (
    set EXERCISE=squat
)

if "%VIDEO_NUM%"=="" (
    set VIDEO_NUM=1
)

REM Construction du chemin de la vidéo
if "%EXERCISE%"=="squat" (
    set VIDEO_PATH=data\raw\squat\squat_%VIDEO_NUM%.mp4
    if not exist "%VIDEO_PATH%" (
        set VIDEO_PATH=data\raw\squat\squat_%VIDEO_NUM%.MOV
    )
) else if "%EXERCISE%"=="push-up" (
    set VIDEO_PATH=data\raw\push up\push up_g%VIDEO_NUM%.jpg
)

REM Vérifier que la vidéo existe
if not exist "%VIDEO_PATH%" (
    echo.
    echo ERREUR: Video non trouvee: %VIDEO_PATH%
    echo.
    echo Videos squats disponibles:
    dir /b "data\raw\squat\*.mp4" 2>nul
    dir /b "data\raw\squat\*.MOV" 2>nul
    echo.
    echo Videos push-ups disponibles:
    dir /b "data\raw\push up\*.jpg" 2>nul | findstr "push up_g"
    echo.
    pause
    exit /b 1
)

echo.
echo Traitement de: %VIDEO_PATH%
echo Exercice: %EXERCISE%
echo.

REM Lancer le test
python test_video_counting.py --video "%VIDEO_PATH%" --exercise %EXERCISE%

echo.
echo ========================================
echo Test termine!
echo ========================================
echo.
pause
