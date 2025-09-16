# GitHub Upload PowerShell Script
# Run this script from PowerShell in your project directory

Write-Host "🚀 GitHub Upload Helper Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if Git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "❌ Git is not installed. Please install Git first:" -ForegroundColor Red
    Write-Host "   https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git is installed" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "langchain_helper.py")) {
    Write-Host "❌ Please run this script from your project directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Project directory detected" -ForegroundColor Green

# Check if .env file exists and warn about security
if (Test-Path ".env") {
    Write-Host "🔒 Security Check:" -ForegroundColor Yellow
    Write-Host "   Your .env file contains API keys and will NOT be uploaded (protected by .gitignore)" -ForegroundColor Yellow
}

# Initialize Git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Blue
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Get user input for GitHub repository
Write-Host ""
Write-Host "📝 GitHub Repository Setup:" -ForegroundColor Cyan
$username = Read-Host "Enter your GitHub username"
$reponame = Read-Host "Enter your repository name (e.g., portfolio-qa-system)"

# Add and commit files
Write-Host ""
Write-Host "📋 Adding files to Git..." -ForegroundColor Blue
git add .

Write-Host "💾 Committing files..." -ForegroundColor Blue
git commit -m "Initial commit: Portfolio Q&A system with OpenAI integration

Features:
- AI-powered Q&A using OpenAI GPT-4
- Vector search with FAISS
- Professional portfolio data management
- Configurable environment setup
- Jupyter notebook examples"

# Add remote and push
Write-Host ""
Write-Host "🌐 Connecting to GitHub..." -ForegroundColor Blue
$repoUrl = "https://github.com/$username/$reponame.git"
git remote add origin $repoUrl

Write-Host "🚀 Uploading to GitHub..." -ForegroundColor Blue
git branch -M main
git push -u origin main

Write-Host ""
Write-Host "🎉 Upload complete!" -ForegroundColor Green
Write-Host "Your repository is now available at:" -ForegroundColor Green
Write-Host "   $repoUrl" -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit your GitHub repository" -ForegroundColor White
Write-Host "2. Add a repository description" -ForegroundColor White
Write-Host "3. Consider making it public to showcase your work" -ForegroundColor White
Write-Host "4. Add topics/tags like 'ai', 'portfolio', 'openai', 'langchain'" -ForegroundColor White