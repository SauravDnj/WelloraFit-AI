# 🚀 Quick Start Guide

## Step 1: Get Your Free Groq API Key

1. Visit https://console.groq.com/keys
2. Sign up for a free account (if you don't have one)
3. Click "Create API Key"
4. Copy your API key

## Step 2: Configure the Application

1. Create a `.env` file in the project root:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` and add your API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

## Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at http://localhost:8501

## Step 4: Create Your Account

1. Click the "Sign Up" tab
2. Enter your details:
   - Username
   - Email
   - Password (at least 6 characters)
3. Click "Sign Up"
4. Log in with your new credentials

## What's Working Now (Phase 1 Complete ✅)

- ✅ User registration and authentication
- ✅ Secure password hashing
- ✅ Database with all tables created
- ✅ Groq AI integration ready
- ✅ Basic app structure with navigation

## Coming Next (Phase 2)

- 💬 Chat interface for logging meals
- 🤖 AI-powered nutrition analysis from text
- 📝 Save meals to your journal
- 📊 View your entries

## Testing Groq API (Optional)

To test if your API key is working:

```bash
python test_groq.py
```

This will analyze sample meals and show nutritional data.

## Troubleshooting

**"GROQ_API_KEY not configured" error:**
- Make sure you created the `.env` file
- Check that your API key is correct
- Restart the Streamlit app after adding the key

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**Database errors:**
- Delete `data/journable.db` and restart the app to recreate it

## Project Structure

```
Code/
├── app.py                 # Main application (RUN THIS)
├── requirements.txt       # Dependencies
├── .env                   # Your API key (CREATE THIS)
├── config/               # Configuration
├── auth/                 # Authentication
├── services/             # AI services
├── data/                 # Database & uploads
└── test_groq.py          # API test script
```

---

🎉 **You're all set!** Run `streamlit run app.py` to start tracking your nutrition!
