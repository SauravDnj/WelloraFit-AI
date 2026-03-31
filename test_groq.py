"""
Test script for Groq API integration
"""
import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.groq_service import groq_service

def test_text_analysis():
    """Test text-based meal analysis"""
    print("Testing text-based meal analysis...")
    print("=" * 50)
    
    test_meals = [
        "2 scrambled eggs with toast and butter",
        "Grilled chicken breast with rice and broccoli",
        "Banana and protein shake"
    ]
    
    for meal in test_meals:
        print(f"\nMeal: {meal}")
        try:
            result = groq_service.analyze_meal_text(meal)
            print(f"✓ Calories: {result.get('calories', 0)}")
            print(f"✓ Protein: {result.get('protein_g', 0)}g")
            print(f"✓ Carbs: {result.get('carbs_g', 0)}g")
            print(f"✓ Fat: {result.get('fat_g', 0)}g")
            print(f"✓ Confidence: {result.get('confidence', 'unknown')}")
        except Exception as e:
            print(f"✗ Error: {e}")

def test_insights():
    """Test nutrition insights generation"""
    print("\n\nTesting nutrition insights...")
    print("=" * 50)
    
    sample_data = {
        'calories': 1800,
        'calorie_goal': 2000,
        'protein': 120,
        'protein_goal': 150,
        'carbs': 180,
        'carbs_goal': 200,
        'fat': 55,
        'fat_goal': 65
    }
    
    try:
        insights = groq_service.generate_nutrition_insights(sample_data)
        print(f"\n{insights}")
        print("\n✓ Insights generated successfully")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    if not groq_service:
        print("ERROR: Groq service not initialized. Please set GROQ_API_KEY in .env file")
        sys.exit(1)
    
    print("🚀 Groq API Integration Test\n")
    test_text_analysis()
    test_insights()
    print("\n" + "=" * 50)
    print("✓ All tests completed!")
