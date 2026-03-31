"""
Database utility functions for CRUD operations
"""
from typing import List, Dict, Optional
from datetime import datetime, date
import json
from config.database import get_connection

def save_entry(user_id: int, entry_type: str, description: str, 
               nutrition_data: Dict, photo_path: Optional[str] = None) -> int:
    """
    Save a meal or workout entry
    Returns entry_id
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Extract vitamins as JSON string
    vitamins_json = json.dumps(nutrition_data.get('vitamins', {}))
    
    cursor.execute("""
        INSERT INTO entries (
            user_id, entry_type, description, 
            calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g,
            vitamins, photo_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        entry_type,
        nutrition_data.get('description', description),
        nutrition_data.get('calories', 0),
        nutrition_data.get('protein_g', 0),
        nutrition_data.get('carbs_g', 0),
        nutrition_data.get('fat_g', 0),
        nutrition_data.get('fiber_g', 0),
        nutrition_data.get('sugar_g', 0),
        vitamins_json,
        photo_path
    ))
    
    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return entry_id

def get_today_entries(user_id: int) -> List[Dict]:
    """Get all entries for today"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM entries
        WHERE user_id = ? 
        AND DATE(timestamp) = DATE('now')
        ORDER BY timestamp DESC
    """, (user_id,))
    
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse vitamins JSON
    for entry in entries:
        if entry['vitamins']:
            entry['vitamins'] = json.loads(entry['vitamins'])
    
    return entries

def get_recent_entries(user_id: int, limit: int = 20) -> List[Dict]:
    """Get recent entries"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM entries
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))
    
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    for entry in entries:
        if entry['vitamins']:
            entry['vitamins'] = json.loads(entry['vitamins'])
    
    return entries

def get_daily_totals(user_id: int, target_date: Optional[date] = None) -> Dict:
    """Get nutrition totals for a specific day"""
    if target_date is None:
        target_date = date.today()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COALESCE(SUM(calories), 0) as total_calories,
            COALESCE(SUM(protein_g), 0) as total_protein,
            COALESCE(SUM(carbs_g), 0) as total_carbs,
            COALESCE(SUM(fat_g), 0) as total_fat,
            COALESCE(SUM(fiber_g), 0) as total_fiber,
            COALESCE(SUM(sugar_g), 0) as total_sugar,
            COUNT(*) as entry_count
        FROM entries
        WHERE user_id = ?
        AND DATE(timestamp) = DATE(?)
    """, (user_id, target_date.isoformat()))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}

def delete_entry(entry_id: int, user_id: int) -> bool:
    """Delete an entry (with user ownership check)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM entries
        WHERE id = ? AND user_id = ?
    """, (entry_id, user_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

# Water tracking functions
def add_water_intake(user_id: int, amount_ml: int) -> int:
    """Add water intake entry"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO water_intake (user_id, amount_ml)
        VALUES (?, ?)
    """, (user_id, amount_ml))
    
    water_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return water_id

def get_today_water_total(user_id: int) -> int:
    """Get total water intake for today in ml"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COALESCE(SUM(amount_ml), 0) as total
        FROM water_intake
        WHERE user_id = ?
        AND DATE(timestamp) = DATE('now')
    """, (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return row['total'] if row else 0

# Favorites functions
def save_favorite(user_id: int, name: str, nutrition_data: Dict) -> int:
    """Save a favorite food"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO favorites (
            user_id, name, calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        name,
        nutrition_data.get('calories', 0),
        nutrition_data.get('protein_g', 0),
        nutrition_data.get('carbs_g', 0),
        nutrition_data.get('fat_g', 0),
        nutrition_data.get('fiber_g', 0),
        nutrition_data.get('sugar_g', 0)
    ))
    
    fav_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return fav_id

def get_user_favorites(user_id: int) -> List[Dict]:
    """Get all favorites for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM favorites
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    
    favorites = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return favorites

def delete_favorite(favorite_id: int, user_id: int) -> bool:
    """Delete a favorite"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM favorites
        WHERE id = ? AND user_id = ?
    """, (favorite_id, user_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

# Weight tracking functions
def add_weight_log(user_id: int, weight: float) -> int:
    """Add a weight log entry"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO weight_logs (user_id, weight)
        VALUES (?, ?)
    """, (user_id, weight))
    
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return log_id

def get_weight_history(user_id: int, limit: int = 30) -> List[Dict]:
    """Get weight history"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM weight_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))
    
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return logs

def get_latest_weight(user_id: int) -> Optional[float]:
    """Get most recent weight"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT weight FROM weight_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return row['weight'] if row else None
