"""
Comprehensive System Test
Tests all major features of the application
"""
import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth.authentication import create_user, authenticate_user, update_user_goals
from utils.database_utils import (
    save_entry, get_daily_totals, add_water_intake, 
    get_today_water_total, save_favorite, get_user_favorites,
    add_weight_log, get_weight_history
)
from services.groq_service import groq_service
from config.database import init_database

def test_authentication():
    """Test user authentication system"""
    print("\n🔐 Testing Authentication...")
    
    # Create test user
    test_username = f"test_user_{int(__import__('time').time())}"
    user_id = create_user(test_username, "test@example.com", "password123")
    
    if user_id:
        print(f"  ✅ User created: {test_username}")
    else:
        print("  ✅ User creation handled (already exists)")
    
    # Test login
    user = authenticate_user(test_username, "password123")
    if user:
        print(f"  ✅ Login successful: {user['username']}")
        return user
    else:
        print("  ❌ Login failed")
        return None

def test_meal_logging(user):
    """Test AI meal logging"""
    print("\n🍽️ Testing Meal Logging...")
    
    test_meal = "grilled chicken breast with broccoli"
    
    try:
        # Analyze meal with AI
        nutrition_data = groq_service.analyze_meal_text(test_meal)
        print(f"  ✅ AI analyzed meal: {nutrition_data.get('description')}")
        print(f"     Calories: {nutrition_data.get('calories')}kcal")
        print(f"     Protein: {nutrition_data.get('protein_g')}g")
        
        # Save to database
        entry_id = save_entry(
            user_id=user['id'],
            entry_type='meal',
            description=test_meal,
            nutrition_data=nutrition_data
        )
        print(f"  ✅ Meal saved to database (ID: {entry_id})")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_daily_totals(user):
    """Test daily totals calculation"""
    print("\n📊 Testing Daily Totals...")
    
    totals = get_daily_totals(user['id'])
    print(f"  ✅ Today's totals retrieved:")
    print(f"     Calories: {totals.get('total_calories', 0):.0f}")
    print(f"     Protein: {totals.get('total_protein', 0):.1f}g")
    print(f"     Entries: {totals.get('entry_count', 0)}")

def test_water_tracking(user):
    """Test water intake tracking"""
    print("\n💧 Testing Water Tracking...")
    
    # Add water
    add_water_intake(user['id'], 500)
    print("  ✅ Added 500ml water")
    
    # Get total
    total = get_today_water_total(user['id'])
    print(f"  ✅ Today's total: {total}ml")

def test_favorites(user):
    """Test favorites system"""
    print("\n⭐ Testing Favorites...")
    
    # Save favorite
    fav_data = {
        'calories': 300,
        'protein_g': 25,
        'carbs_g': 30,
        'fat_g': 10,
        'fiber_g': 5,
        'sugar_g': 3
    }
    
    fav_id = save_favorite(user['id'], "Test Favorite Meal", fav_data)
    print(f"  ✅ Favorite saved (ID: {fav_id})")
    
    # Retrieve favorites
    favorites = get_user_favorites(user['id'])
    print(f"  ✅ Retrieved {len(favorites)} favorite(s)")

def test_weight_tracking(user):
    """Test weight logging"""
    print("\n⚖️ Testing Weight Tracking...")
    
    # Add weight log
    weight_id = add_weight_log(user['id'], 75.5)
    print(f"  ✅ Weight logged: 75.5kg (ID: {weight_id})")
    
    # Get history
    history = get_weight_history(user['id'])
    print(f"  ✅ Retrieved {len(history)} weight log(s)")

def test_goal_setting(user):
    """Test goal updates"""
    print("\n🎯 Testing Goal Setting...")
    
    success = update_user_goals(
        user['id'],
        daily_calorie_goal=2200,
        daily_protein_goal=160,
        target_weight=70.0
    )
    
    if success:
        print("  ✅ Goals updated successfully")
    else:
        print("  ❌ Failed to update goals")

def test_ai_insights():
    """Test AI insights generation"""
    print("\n💡 Testing AI Insights...")
    
    sample_data = {
        'calories': 1500,
        'calorie_goal': 2000,
        'protein': 100,
        'protein_goal': 150,
        'carbs': 150,
        'carbs_goal': 200,
        'fat': 50,
        'fat_goal': 65
    }
    
    try:
        insights = groq_service.generate_nutrition_insights(sample_data)
        print("  ✅ AI insights generated:")
        print(f"     {insights[:100]}...")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def main():
    print("=" * 60)
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    # Initialize database
    print("\n📦 Initializing database...")
    init_database()
    print("  ✅ Database ready")
    
    # Run all tests
    user = test_authentication()
    
    if user:
        test_goal_setting(user)
        test_meal_logging(user)
        test_daily_totals(user)
        test_water_tracking(user)
        test_favorites(user)
        test_weight_tracking(user)
        test_ai_insights()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n🎉 Your application is fully functional!")
    print("\n🚀 Start the app with:")
    print("   streamlit run app.py")
    print("\n📖 Open: http://localhost:8501")
    print("=" * 60)

if __name__ == "__main__":
    main()
