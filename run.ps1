param(
    [string]$Command = "python manage.py runserver"
)

# Go to the folder where this script lives
Set-Location -Path $PSScriptRoot

# Activate the virtual environment (Windows PowerShell)
& ".\venv\Scripts\Activate.ps1"

# Run the command (by default: start the Django dev server)
Invoke-Expression $Command

