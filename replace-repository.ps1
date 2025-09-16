# Replace Existing GitHub Repository Content
# This script will replace the content in your Chatbot_With_RAG repository

Write-Host "🔄 Replacing GitHub Repository Content" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

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

# Security check for .env file
if (Test-Path ".env") {
    Write-Host "🔒 Security Check:" -ForegroundColor Yellow
    Write-Host "   Your .env file contains API keys and will NOT be uploaded (protected by .gitignore)" -ForegroundColor Yellow
}

# Get repository URL (assuming it's Chatbot_With_RAG based on the screenshot)
Write-Host ""
Write-Host "📝 Repository Setup:" -ForegroundColor Cyan
$username = Read-Host "Enter your GitHub username (from screenshot appears to be 'NoahCodeGuy')"
if ([string]::IsNullOrWhiteSpace($username)) {
    $username = "NoahCodeGuy"
}

$reponame = Read-Host "Enter repository name (press Enter for 'Chatbot_With_RAG')"
if ([string]::IsNullOrWhiteSpace($reponame)) {
    $reponame = "Chatbot_With_RAG"
}

$repoUrl = "https://github.com/$username/$reponame.git"

Write-Host ""
Write-Host "🌐 Repository URL: $repoUrl" -ForegroundColor Blue

# Initialize Git if needed
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Blue
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Add remote if not exists
$remoteExists = git remote | Where-Object { $_ -eq "origin" }
if (-not $remoteExists) {
    Write-Host "🔗 Adding remote origin..." -ForegroundColor Blue
    git remote add origin $repoUrl
} else {
    Write-Host "🔗 Updating remote origin..." -ForegroundColor Blue
    git remote set-url origin $repoUrl
}

# Configure Git user if not set
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if ([string]::IsNullOrWhiteSpace($gitUser)) {
    $userName = Read-Host "Enter your name for Git commits"
    git config --global user.name "$userName"
}

if ([string]::IsNullOrWhiteSpace($gitEmail)) {
    $userEmail = Read-Host "Enter your email for Git commits"
    git config --global user.email "$userEmail"
}

# Add all files
Write-Host ""
Write-Host "📋 Adding files to Git..." -ForegroundColor Blue
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Yellow
} else {
    Write-Host "💾 Committing files..." -ForegroundColor Blue
    git commit -m "Replace repository with Portfolio Q&A System

Features:
- AI-powered Q&A using OpenAI GPT-4
- Vector search with FAISS  
- Professional portfolio data management
- Modern LangChain integration
- Configurable environment setup
- Jupyter notebook examples
- Best practices implementation

This replaces the previous chatbot implementation with a more
sophisticated portfolio Q&A system for professional use."
}

# Push to GitHub (force push to replace existing content)
Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Blue
Write-Host "⚠️  This will REPLACE the existing repository content" -ForegroundColor Red

$confirm = Read-Host "Are you sure you want to replace the existing repository? (yes/no)"
if ($confirm -eq "yes" -or $confirm -eq "y") {
    git branch -M main
    git push -f origin main
    
    Write-Host ""
    Write-Host "🎉 Repository content replaced successfully!" -ForegroundColor Green
    Write-Host "Your repository is now available at:" -ForegroundColor Green
    Write-Host "   $repoUrl" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "📋 What was updated:" -ForegroundColor Yellow
    Write-Host "✅ Modern LangChain implementation" -ForegroundColor White
    Write-Host "✅ OpenAI GPT-4 integration" -ForegroundColor White
    Write-Host "✅ Professional portfolio Q&A system" -ForegroundColor White
    Write-Host "✅ Improved configuration management" -ForegroundColor White
    Write-Host "✅ Better documentation and setup" -ForegroundColor White
    Write-Host "✅ Security best practices" -ForegroundColor White
    
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Update repository description on GitHub" -ForegroundColor White
    Write-Host "2. Add topics: ai, portfolio, openai, langchain, python" -ForegroundColor White
    Write-Host "3. Consider updating the repository name if needed" -ForegroundColor White
    
} else {
    Write-Host "❌ Operation cancelled" -ForegroundColor Red
}