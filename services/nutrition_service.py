"""
Nutrition service for parsing and calculating nutrition data
"""
from typing import Dict, Any

def calculate_net_carbs(carbs_g: float, fiber_g: float) -> float:
    """Calculate net carbs (total carbs - fiber)"""
    return max(0, carbs_g - fiber_g)

def calculate_macro_percentages(protein_g: float, carbs_g: float, fat_g: float) -> Dict[str, float]:
    """
    Calculate macro percentages based on calories
    Protein: 4 cal/g, Carbs: 4 cal/g, Fat: 9 cal/g
    """
    protein_cal = protein_g * 4
    carbs_cal = carbs_g * 4
    fat_cal = fat_g * 9
    
    total_cal = protein_cal + carbs_cal + fat_cal
    
    if total_cal == 0:
        return {'protein': 0, 'carbs': 0, 'fat': 0}
    
    return {
        'protein': round((protein_cal / total_cal) * 100, 1),
        'carbs': round((carbs_cal / total_cal) * 100, 1),
        'fat': round((fat_cal / total_cal) * 100, 1)
    }

def validate_nutrition_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean nutrition data"""
    cleaned = {
        'description': str(data.get('description', 'Unknown')),
        'calories': max(0, float(data.get('calories', 0))),
        'protein_g': max(0, float(data.get('protein_g', 0))),
        'carbs_g': max(0, float(data.get('carbs_g', 0))),
        'fat_g': max(0, float(data.get('fat_g', 0))),
        'fiber_g': max(0, float(data.get('fiber_g', 0))),
        'sugar_g': max(0, float(data.get('sugar_g', 0))),
        'vitamins': data.get('vitamins', {}),
        'confidence': data.get('confidence', 'unknown'),
        'notes': data.get('notes', '')
    }
    
    return cleaned

def format_nutrition_summary(nutrition: Dict) -> str:
    """Format nutrition data as readable text"""
    return (
        f"📊 **Nutrition Summary**\n\n"
        f"🔥 Calories: {nutrition.get('calories', 0):.0f} kcal\n"
        f"🥩 Protein: {nutrition.get('protein_g', 0):.1f}g\n"
        f"🍞 Carbs: {nutrition.get('carbs_g', 0):.1f}g\n"
        f"🥑 Fat: {nutrition.get('fat_g', 0):.1f}g\n"
        f"🌾 Fiber: {nutrition.get('fiber_g', 0):.1f}g\n"
        f"🍬 Sugar: {nutrition.get('sugar_g', 0):.1f}g"
    )
