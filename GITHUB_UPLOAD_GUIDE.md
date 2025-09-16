# GitHub Upload Instructions

## Prerequisites
1. Install Git: https://git-scm.com/downloads
2. Create GitHub account if you don't have one
3. Create a new repository on GitHub.com

## Steps to Upload

### 1. Initialize Git Repository
```bash
cd "c:\Users\ndelacalzada\Downloads\langchain-main - Copy\langchain-main\3_project_codebasics_q_and_a"
git init
```

### 2. Configure Git (first time only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
```

### 3. Add Files to Git
```bash
git add .
git commit -m "Initial commit: Portfolio Q&A system with OpenAI integration"
```

### 4. Connect to GitHub Repository
Replace `YOUR_USERNAME` and `REPO_NAME` with your actual GitHub username and repository name:
```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Important: Security Check
Before uploading, verify your .env file is NOT included:
```bash
git status
```
Make sure `.env` is NOT listed (should be ignored by .gitignore)

## Recommended Repository Name
- `portfolio-qa-system`
- `noah-portfolio-chatbot`
- `ai-portfolio-assistant`

## Repository Description Suggestion
"AI-powered Q&A system for professional portfolio using OpenAI GPT-4, LangChain, and FAISS vector search. Allows hiring managers to ask questions about professional background and experience."