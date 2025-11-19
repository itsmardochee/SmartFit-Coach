# Script PowerShell pour tester le comptage sur plusieurs vidéos
# Usage: .\test_all_videos.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SmartFit Coach - Test Batch Videos" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Activation de l'environnement virtuel
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERREUR: Environnement virtuel non trouve!" -ForegroundColor Red
    Write-Host "Creez-le d'abord avec: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Configuration
$squatVideos = @(
    "data\raw\squat\squat_1.MOV",
    "data\raw\squat\squat_10.mp4",
    "data\raw\squat\squat_20.mp4"
)

$results = @()

Write-Host "`n📊 Test de $($squatVideos.Count) videos de squats...`n" -ForegroundColor Green

foreach ($video in $squatVideos) {
    if (Test-Path $video) {
        Write-Host "`n----------------------------------------" -ForegroundColor Cyan
        Write-Host "Testing: $video" -ForegroundColor Yellow
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        
        # Lancer le test sans affichage (plus rapide)
        $output = python test_video_counting.py --video $video --exercise squat --no-display 2>&1 | Out-String
        
        # Extraire le nombre de répétitions (exemple basique)
        if ($output -match "Répétitions détectées: (\d+)") {
            $reps = $Matches[1]
            $results += [PSCustomObject]@{
                Video = (Split-Path $video -Leaf)
                Repetitions = $reps
                Status = "✅"
            }
        } else {
            $results += [PSCustomObject]@{
                Video = (Split-Path $video -Leaf)
                Repetitions = "N/A"
                Status = "❌"
            }
        }
    } else {
        Write-Host "⚠️  Video non trouvee: $video" -ForegroundColor Yellow
    }
}

# Affichage du résumé
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RÉSUMÉ DES TESTS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$results | Format-Table -AutoSize

Write-Host "`n✅ Tests terminés!`n" -ForegroundColor Green
