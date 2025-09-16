# Simple GitHub Repository Replacement Script

Write-Host "Replacing GitHub Repository Content" -ForegroundColor Cyan

# Check Git installation
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check project directory
if (-not (Test-Path "langchain_helper.py")) {
    Write-Host "Please run this script from your project directory" -ForegroundColor Red
    exit 1
}

Write-Host "Project directory detected" -ForegroundColor Green

# Get repository details
$username = Read-Host "Enter your GitHub username"
$reponame = Read-Host "Enter repository name (e.g., Chatbot_With_RAG)"

$repoUrl = "https://github.com/$username/$reponame.git"
Write-Host "Repository URL: $repoUrl" -ForegroundColor Blue

# Initialize Git if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Blue
    git init
}

# Set up remote
git remote remove origin 2>$null
git remote add origin $repoUrl

# Add and commit files
Write-Host "Adding files..." -ForegroundColor Blue
git add .

Write-Host "Committing files..." -ForegroundColor Blue
git commit -m "Replace with Portfolio Q&A System - OpenAI GPT-4 integration with modern LangChain"

# Push with force to replace existing content
Write-Host "This will REPLACE existing repository content" -ForegroundColor Red
$confirm = Read-Host "Continue? (yes/no)"

if ($confirm -eq "yes") {
    Write-Host "Pushing to GitHub..." -ForegroundColor Blue
    git branch -M main
    git push -f origin main
    
    Write-Host "Repository updated successfully!" -ForegroundColor Green
    Write-Host "Visit: $repoUrl" -ForegroundColor Cyan
} else {
    Write-Host "Operation cancelled" -ForegroundColor Yellow
}