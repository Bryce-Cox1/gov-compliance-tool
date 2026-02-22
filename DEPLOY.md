# Quick Deployment Guide

## Option 1: Deploy to Render (Recommended - Free Tier)

### Step 1: Push to GitHub
```bash
# Login to GitHub CLI
gh auth login

# Create GitHub repo and push
cd gov-compliance-tool
gh repo create gov-compliance-tool --public --source=. --push
```

### Step 2: Deploy on Render
1. Go to https://render.com and sign in with GitHub
2. Click "New +" → "Web Service"
3. Connect your `gov-compliance-tool` repo
4. Render will auto-detect the `render.yaml` config
5. Add environment variable:
   - `OPENAI_API_KEY` = your OpenAI API key
6. Click "Create Web Service"

**Done!** Your app will be live at `https://gov-compliance-tool.onrender.com` (or similar)

---

## Option 2: Deploy to Railway

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway
1. Go to https://railway.app and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `gov-compliance-tool`
4. Railway will auto-detect Python
5. Add environment variable:
   - `OPENAI_API_KEY` = your OpenAI API key
6. Railway will deploy automatically

**Done!** Your app will be live at a Railway URL.

---

## Option 3: Quick Deploy via CLI

If you have the Railway CLI installed:
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

---

## Environment Variables Required

- `OPENAI_API_KEY` - Your OpenAI API key for text rewriting

---

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env file with your API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run locally
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000
