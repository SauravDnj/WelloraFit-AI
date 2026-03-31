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
        prompt = f"""You are a professional nutritionist and certified dietitian with expertise in food composition analysis. Analyze this meal/food with high accuracy using standard USDA nutrition database values.

Meal description: "{description}"

IMPORTANT INSTRUCTIONS:
1. Use actual USDA nutrition data for common foods
2. Consider realistic portion sizes (e.g., "1 apple" = medium apple ~180g, "2 eggs" = large eggs ~100g total)
3. Be precise with calculations - don't round excessively
4. If portion not specified, assume standard serving size
5. For homemade/cooked items, account for cooking methods
6. Include ALL macronutrients and micronutrients when data is available

Provide your response in this exact JSON format (numbers only, no units):
{{
    "description": "Detailed description with estimated portions",
    "calories": total calories (precise number, e.g., 156 not 150),
    "protein_g": protein in grams (decimal precision, e.g., 12.6),
    "carbs_g": total carbohydrates in grams (decimal precision),
    "fat_g": total fat in grams (decimal precision),
    "fiber_g": dietary fiber in grams (decimal precision),
    "sugar_g": total sugars in grams (decimal precision),
    "vitamins": {{
        "vitamin_a": amount in mcg RAE or "unknown",
        "vitamin_c": amount in mg or "unknown",
        "vitamin_d": amount in mcg or "unknown",
        "calcium": amount in mg or "unknown",
        "iron": amount in mg or "unknown"
    }},
    "confidence": "high/medium/low",
    "notes": "Source of nutrition data, assumptions about portions, or cooking methods considered"
}}

Examples for reference:
- "2 boiled eggs" = ~156 calories, 12.6g protein, 1.1g carbs, 10.6g fat
- "1 medium apple" = ~95 calories, 0.5g protein, 25g carbs, 0.3g fat, 4.4g fiber
- "1 cup cooked white rice" = ~205 calories, 4.3g protein, 45g carbs, 0.4g fat

Respond ONLY with valid JSON, no additional text."""

        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a certified nutritionist with access to USDA FoodData Central. Provide accurate, evidence-based nutrition analysis. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,  # Lower temperature for more consistent, accurate responses
                max_tokens=1200
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
        Analyze food photo and extract nutritional information with high accuracy
        Returns dict with calories, protein, carbs, fat, etc.
        """
        try:
            # Read and encode image
            with open(image_path, 'rb') as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Determine image type
            ext = image_path.lower().split('.')[-1]
            mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
            
            prompt = """You are a professional nutritionist and certified dietitian analyzing a food photo. Use your expertise to provide highly accurate nutrition data.

ANALYZE THE IMAGE:
1. IDENTIFY all food items visible
2. ESTIMATE portion sizes using visual cues (plate size, utensils, hand for scale)
3. DETECT cooking methods if visible (grilled, fried, steamed, etc.)
4. CALCULATE nutrition using USDA standard values

BE PRECISE:
- Use realistic portion estimates (e.g., "1 medium chicken breast ~200g")
- Consider plate/bowl size as reference
- If multiple items, analyze each separately
- Account for visible cooking oil, sauce, toppings
- Use decimal precision for accuracy

Respond in this exact JSON format (numbers only, no units):
{
    "description": "Detailed list of identified foods with portions (e.g., '1 grilled chicken breast ~200g, 1 cup steamed broccoli, 1/2 cup brown rice')",
    "calories": total calories (precise number, e.g., 487),
    "protein_g": protein in grams (decimal precision, e.g., 54.3),
    "carbs_g": total carbohydrates in grams (decimal precision),
    "fat_g": total fat in grams (decimal precision),
    "fiber_g": dietary fiber in grams (decimal precision),
    "sugar_g": total sugars in grams (decimal precision),
    "vitamins": {
        "vitamin_a": amount in mcg RAE or "unknown",
        "vitamin_c": amount in mg or "unknown",
        "vitamin_d": amount in mcg or "unknown",
        "calcium": amount in mg or "unknown",
        "iron": amount in mg or "unknown"
    },
    "portion_estimate": "Method used for estimation (e.g., 'Based on standard dinner plate size')",
    "confidence": "high/medium/low (based on image clarity)",
    "notes": "Cooking method observed, any assumptions made, USDA reference if applicable"
}

Examples for reference:
- Grilled chicken breast (200g): ~330 cal, 62g protein, 0g carbs, 7g fat
- Steamed broccoli (1 cup/156g): ~55 cal, 3.7g protein, 11g carbs, 0.6g fat, 5g fiber
- Brown rice (1/2 cup cooked/98g): ~108 cal, 2.5g protein, 22g carbs, 0.9g fat

Respond ONLY with valid JSON, no additional text."""

            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a certified nutritionist with expertise in visual portion estimation and USDA nutrition data. Provide accurate, evidence-based analysis."
                    },
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
                temperature=0.2,  # Lower for more accurate results
                max_tokens=1500
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
