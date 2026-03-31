# WelloraFit AI - AI-Powered Health & Fitness Tracker

<div align="center">

![WelloraFit AI](https://img.shields.io/badge/WelloraFit-AI-00D9A3?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Your Personal AI Health Assistant for Nutrition & Fitness Tracking**

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Deployment](#deployment)

</div>

---

## 🌟 Overview

WelloraFit AI is an intelligent health and fitness tracking application that uses AI to make nutrition and workout logging effortless. Simply chat with the AI about your meals or upload photos - it does the rest!

### ✨ Key Features

- 🤖 **AI-Powered Logging**: Natural language meal and workout tracking
- 📷 **Photo Analysis**: Upload food photos for instant nutrition breakdown
- 📊 **Complete Nutrition**: Track calories, macros, micronutrients, net carbs
- 💧 **Hydration Tracking**: Monitor daily water intake with quick-add buttons
- 📅 **Day-by-Day History**: View detailed nutrition logs with filtering
- ⭐ **Favorites System**: Save and quick-log frequently eaten meals
- 📈 **Progress Tracking**: Weight tracking, goal setting, weekly reports
- 🔐 **Privacy First**: All data stored locally, secure authentication

---

## 🚀 Features

### 💬 Chat-Based Tracking
- Type what you ate: "I had 2 eggs and toast"
- Describe workouts: "30 minutes of running"
- AI extracts complete nutritional information
- All data saves automatically to database

### 📷 Photo Analysis
- Upload food photos
- AI identifies foods and estimates portions
- Instant nutritional breakdown
- Photo storage and retrieval

### 📊 Comprehensive Tracking
- **Macros**: Protein, Carbs, Fat
- **Micronutrients**: Fiber, Sugar, Vitamins, Minerals
- **Calculated Values**: Net carbs, calorie percentages
- **Daily Totals**: Real-time aggregation

### 📅 History & Analytics
- Day-by-day entry view (7-90 days)
- Filter by meal or workout
- Daily nutrition summaries
- Delete or save to favorites
- Export capabilities

### 🎯 Goal Setting & Progress
- Customizable daily targets
- Weight tracking with charts
- Weekly progress reports
- AI-generated insights
- CSV export for sharing

---

## 🛠️ Tech Stack

- **Framework**: Streamlit (Python web framework)
- **AI/LLM**: Groq API (LLaMA 3.3 for text, LLaMA 3.2 Vision for photos)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Visualization**: Plotly (interactive charts)
- **Authentication**: bcrypt (secure password hashing)

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (free at [console.groq.com](https://console.groq.com/keys))

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/SauravDnj/WelloraFit-AI.git
cd WelloraFit-AI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
- Navigate to: `http://localhost:8501`
- Create your account
- Start tracking!

---

## 🎯 Usage

### First Time Setup

1. **Create Account**
   - Click "Sign Up" tab
   - Enter username, email, password
   - Click "Sign Up"

2. **Set Goals** (⚙️ Settings)
   - Daily calorie target
   - Protein, carbs, fat goals
   - Water intake goal
   - Current and target weight

3. **Start Logging** (💬 Chat & Log)
   - Type meals or workouts
   - Upload food photos
   - AI analyzes and logs automatically

### Daily Workflow

```
Morning:
1. Log breakfast via chat or photo
2. Track morning water intake

Throughout Day:
3. Log meals as you eat
4. Log workouts after exercise
5. Update water intake

Evening:
6. Review dashboard
7. Check progress toward goals
8. Generate AI insights
```

---

## 📱 Features Overview

### 🏠 Dashboard
- Today's calorie and macro totals
- Progress bars for goals
- Macro breakdown donut chart
- Recent entries with actions
- AI nutrition insights

### 💬 Chat & Log
- Natural language meal logging
- Workout activity tracking
- Photo upload and analysis
- Real-time nutrition display
- Chat history with timestamps

### 📅 History
- 7-90 day entry history
- Filter by meal/workout
- Daily nutrition summaries
- Quick actions (delete, favorite)
- Detailed nutrition view

### ⭐ Favorites
- Save frequently eaten meals
- One-tap quick logging
- Manual entry with full nutrition
- Edit and delete favorites

### 💧 Water Tracker
- Quick-add buttons (250ml, 500ml, 750ml, 1L)
- Custom amount entry
- Daily goal progress
- Hydration tips

### 📊 Reports
- Weekly nutrition summaries
- Daily breakdown charts
- Weight progress graphs
- CSV export
- Multi-week history

### ⚙️ Settings
- Customize daily goals
- Weight goal tracking
- Account information
- Goal progress calculation

---

## 🌐 Deployment

### Streamlit Community Cloud (Recommended - FREE)

1. **Push to GitHub** (if not already done)
```bash
git push origin main
```

2. **Deploy**
   - Visit: [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Add secret in Settings:
     ```
     GROQ_API_KEY = "your_actual_api_key"
     ```
   - Click "Deploy"!

3. **Your app will be live at:**
   - `https://wellorafit-ai.streamlit.app`

For other deployment options (Heroku, Railway, Render), see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📁 Project Structure

```
WelloraFit-AI/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── config/
│   ├── settings.py            # App configuration
│   └── database.py            # Database schema
├── auth/
│   └── authentication.py      # User authentication
├── services/
│   ├── groq_service.py        # AI integration
│   └── nutrition_service.py   # Nutrition calculations
├── ui/
│   ├── dashboard.py           # Dashboard view
│   ├── chat_interface.py      # Chat interface
│   ├── history.py             # History view
│   ├── water_favorites.py     # Water & favorites
│   ├── reports.py             # Reports view
│   └── settings_ui.py         # Settings page
├── utils/
│   ├── database_utils.py      # Database operations
│   └── charts.py              # Chart generation
└── data/
    ├── journable.db           # SQLite database (gitignored)
    └── uploads/               # Photo storage (gitignored)
```

---

## 🔐 Security & Privacy

- **Password Security**: bcrypt hashing (industry standard)
- **Local Data**: All data stored on your device
- **API Security**: Environment variables for API keys
- **No Tracking**: Your data stays with you
- **Secure Sessions**: Streamlit session management

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** for providing free AI API access
- **Streamlit** for the amazing Python web framework
- **LLaMA** models for powerful AI capabilities
- All contributors and users of WelloraFit AI

---

## 📧 Contact

**Developer**: Saurav Danej  
**Email**: sauravdanej24@gmail.com  
**GitHub**: [@SauravDnj](https://github.com/SauravDnj)

---

## 🌟 Show Your Support

If you find WelloraFit AI helpful, please give it a ⭐️!

---

<div align="center">

**Made with ❤️ by Saurav Danej**

[⬆ Back to Top](#wellorafit-ai---ai-powered-health--fitness-tracker)

</div>
