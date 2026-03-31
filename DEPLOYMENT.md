# 🚀 Deployment Guide - WelloraFit AI

## ⚠️ IMPORTANT: Vercel Deployment Issue

**The error you're seeing is because:**
- **Vercel** is designed for **Next.js, React, Vue** applications
- **Your app is built with Streamlit (Python)**
- Streamlit apps **cannot be deployed to Vercel**

## ✅ Correct Deployment Options for Streamlit

### Option 1: Streamlit Community Cloud (RECOMMENDED - FREE)

**Best for**: Easy, free, official Streamlit hosting

1. **Push your code to GitHub:**
   ```bash
   cd E:\Projects\Health\Code
   git init
   git add .
   git commit -m "Initial commit - WelloraFit AI"
   git remote add origin https://github.com/YOUR_USERNAME/wellorafit-ai.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect your GitHub repository
   - Select: `app.py` as main file
   - Add secrets (your GROQ_API_KEY) in settings
   - Click "Deploy"!

3. **Add secrets in Streamlit Cloud:**
   - In your app dashboard, go to "Settings" → "Secrets"
   - Add:
     ```toml
     GROQ_API_KEY = "your_groq_api_key_here"
     ```
   - Replace with your actual Groq API key from https://console.groq.com/keys

**Result:** Your app will be live at `https://your-app-name.streamlit.app`

---

### Option 2: Heroku (FREE TIER)

1. **Install Heroku CLI:**
   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Create required files:**

**Procfile:**
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. **Deploy:**
```bash
heroku login
heroku create wellorafit-ai
git push heroku main
heroku config:set GROQ_API_KEY="your_api_key"
```

---

### Option 3: Railway.app (EASY & FREE)

1. Go to https://railway.app
2. Connect your GitHub repository
3. Add environment variable: `GROQ_API_KEY`
4. Railway auto-detects Python and deploys!

---

### Option 4: Render.com (FREE)

1. Go to https://render.com
2. Create new "Web Service"
3. Connect your repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Add environment variable: `GROQ_API_KEY`

---

## 📝 Pre-Deployment Checklist

### 1. Create `.gitignore`
```
.env
__pycache__/
*.pyc
*.db
data/uploads/*
!data/uploads/.gitkeep
.streamlit/secrets.toml
```

### 2. Update `requirements.txt` (already done ✅)

### 3. Create `.streamlit/config.toml` for deployment:
```toml
[theme]
primaryColor = "#00D9A3"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

### 4. Update database for production:
For production, consider using **PostgreSQL** instead of SQLite:
- Railway, Heroku, Render provide free PostgreSQL databases
- Update `config/database.py` to support PostgreSQL

---

## 🔧 Local Testing Before Deployment

```bash
cd E:\Projects\Health\Code

# Test that everything works
streamlit run app.py

# Check that GROQ_API_KEY is loaded from .env
python -c "from config.settings import settings; print('API Key loaded:', bool(settings.GROQ_API_KEY))"
```

---

## 🎯 Recommended: Streamlit Community Cloud

**Why?**
- ✅ Free forever
- ✅ Official Streamlit hosting
- ✅ Easy GitHub integration
- ✅ Automatic HTTPS
- ✅ No server management
- ✅ Built-in secrets management

**Steps:**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add API key in secrets
4. Deploy in 1 click!

Your app will be live at: `https://wellorafit-ai.streamlit.app`

---

## ❌ Why Vercel Doesn't Work

Vercel expects:
- `package.json` with Next.js dependencies
- Node.js application
- React/Next.js framework

Your app has:
- `requirements.txt` with Python dependencies
- Python application
- Streamlit framework

**Solution:** Use Streamlit Cloud, Heroku, Railway, or Render instead!

---

## 📧 Need Help?

If you want to deploy:
1. Choose a platform above (Streamlit Cloud recommended)
2. Follow the specific steps
3. Add your GROQ_API_KEY as environment variable
4. Deploy!

Your app will work perfectly on any of these platforms! 🚀
