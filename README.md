# WelloraFit AI - AI-Powered Health & Fitness Tracker

An AI-powered nutrition and fitness tracking application built with Streamlit and Groq AI.

## Features

- 💬 **Chat-based Tracking**: Log meals and workouts through natural conversation
- 📷 **Photo Analysis**: Upload food photos for instant nutritional estimates
- 📊 **Complete Nutrition**: Track calories, macros, and micronutrients
- 💧 **Water Tracking**: Monitor daily hydration goals
- ⭐ **Favorite Foods**: Quick-log frequently eaten meals
- 📈 **Progress Reports**: Weekly summaries and weight tracking
- 🎯 **Goal Setting**: Personalized calorie and macro targets

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   - Copy `.env.example` to `.env`
   - Get your free API key from [Groq Console](https://console.groq.com/keys)
   - Add your key to `.env`:
     ```
     GROQ_API_KEY=your_actual_key_here
     ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Create Your Account**
   - Open the app in your browser
   - Sign up with username and password
   - Start tracking your nutrition!

## Technology Stack

- **Streamlit**: Web framework
- **Groq AI**: Natural language processing and vision
- **SQLite**: Local database
- **Plotly**: Interactive charts
- **Python 3.8+**: Programming language

## Usage

1. **Log a Meal**: Type what you ate (e.g., "I had 2 eggs and toast for breakfast")
2. **Upload Photo**: Click camera icon and upload a food photo
3. **View Dashboard**: See your daily calorie and macro totals
4. **Track Water**: Log water intake throughout the day
5. **Set Goals**: Configure your target weight and daily nutrition goals
6. **View Reports**: Check weekly progress and insights

## Privacy

All data is stored locally on your device. Your API key and personal information are never shared with third parties.

## License

MIT License - See LICENSE file for details
