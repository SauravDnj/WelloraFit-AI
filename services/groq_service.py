"""
Groq AI Service for nutrition analysis and insights
"""
import json
import base64
from typing import Dict, Optional, Any
from groq import Groq
from config.settings import settings

class GroqService:
    """Service for interacting with Groq AI API"""
    
    def __init__(self):
        """Initialize Groq client"""
        # Get API key
        api_key = settings.GROQ_API_KEY
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not configured. Add to Streamlit secrets or .env file.")
        
        self.client = Groq(api_key=api_key)
        self.text_model = settings.GROQ_TEXT_MODEL
        self.vision_model = settings.GROQ_VISION_MODEL
    
    def analyze_meal_text(self, description: str) -> Dict[str, Any]:
        """
        Analyze meal description and extract nutritional information
        Returns dict with calories, protein, carbs, fat, fiber, sugar, etc.
        """
        prompt = f"""You are a nutrition expert. Analyze this meal/food description and provide detailed nutritional information.

Meal description: "{description}"

Provide your response in this exact JSON format (numbers only, no units):
{{
    "description": "Cleaned up description of the meal",
    "calories": estimated total calories (number),
    "protein_g": protein in grams (number),
    "carbs_g": total carbohydrates in grams (number),
    "fat_g": total fat in grams (number),
    "fiber_g": fiber in grams (number),
    "sugar_g": sugar in grams (number),
    "vitamins": {{
        "vitamin_a": amount in mcg or "unknown",
        "vitamin_c": amount in mg or "unknown",
        "vitamin_d": amount in mcg or "unknown",
        "calcium": amount in mg or "unknown",
        "iron": amount in mg or "unknown"
    }},
    "confidence": "high/medium/low",
    "notes": "Any additional nutritional notes or assumptions made"
}}

Respond ONLY with valid JSON, no additional text."""

        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise nutrition analyst. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Extract and parse JSON response
            content = response.choices[0].message.content
            
            # Try to extract JSON if there's extra text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            nutrition_data = json.loads(content)
            return nutrition_data
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {content}")
            # Return default structure with zeros
            return {
                "description": description,
                "calories": 0,
                "protein_g": 0,
                "carbs_g": 0,
                "fat_g": 0,
                "fiber_g": 0,
                "sugar_g": 0,
                "vitamins": {},
                "confidence": "low",
                "notes": "Failed to parse nutrition data"
            }
        except Exception as e:
            print(f"Error analyzing meal: {e}")
            raise
    
    def analyze_food_photo(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze food photo and extract nutritional information
        Returns dict with calories, protein, carbs, fat, etc.
        """
        try:
            # Read and encode image
            with open(image_path, 'rb') as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Determine image type
            ext = image_path.lower().split('.')[-1]
            mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
            
            prompt = """Analyze this food photo and provide detailed nutritional information.

Identify the food items, estimate portion sizes, and provide nutritional breakdown.

Respond in this exact JSON format (numbers only, no units):
{
    "description": "Description of foods visible in the image",
    "calories": estimated total calories (number),
    "protein_g": protein in grams (number),
    "carbs_g": total carbohydrates in grams (number),
    "fat_g": total fat in grams (number),
    "fiber_g": fiber in grams (number),
    "sugar_g": sugar in grams (number),
    "vitamins": {
        "vitamin_a": amount in mcg or "unknown",
        "vitamin_c": amount in mg or "unknown",
        "vitamin_d": amount in mcg or "unknown",
        "calcium": amount in mg or "unknown",
        "iron": amount in mg or "unknown"
    },
    "portion_estimate": "Description of estimated portion size",
    "confidence": "high/medium/low",
    "notes": "Any additional observations or assumptions"
}

Respond ONLY with valid JSON, no additional text."""

            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Extract and parse JSON response
            content = response.choices[0].message.content
            
            # Try to extract JSON if there's extra text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            nutrition_data = json.loads(content)
            return nutrition_data
            
        except Exception as e:
            print(f"Error analyzing photo: {e}")
            raise
    
    def generate_nutrition_insights(self, daily_data: Dict) -> str:
        """
        Generate personalized nutrition insights based on daily intake
        daily_data should include: calories, protein, carbs, fat, goals
        """
        prompt = f"""As a nutrition expert, analyze this daily nutrition data and provide 2-3 brief, actionable insights or recommendations.

Daily intake:
- Calories: {daily_data.get('calories', 0)} / {daily_data.get('calorie_goal', 2000)} goal
- Protein: {daily_data.get('protein', 0)}g / {daily_data.get('protein_goal', 150)}g goal
- Carbs: {daily_data.get('carbs', 0)}g / {daily_data.get('carbs_goal', 200)}g goal
- Fat: {daily_data.get('fat', 0)}g / {daily_data.get('fat_goal', 65)}g goal

Provide insights in 2-3 short, friendly paragraphs. Focus on what's going well and constructive suggestions."""

        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly, encouraging nutrition coach."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return "Keep up the great work tracking your nutrition! Stay consistent with your logging for the best results."

# Initialize global service instance with error handling
try:
    groq_service = GroqService()
except Exception as e:
    print(f"⚠️ GroqService init failed: {e}")
    print("Add GROQ_API_KEY to Streamlit secrets or .env file")
    groq_service = None
