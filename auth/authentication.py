"""
User Authentication System
"""
import bcrypt
import yaml
from typing import Optional, Dict
from config.database import get_connection
from config.settings import settings

class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username: str, email: str, password: str) -> Optional[int]:
    """
    Create a new user
    Returns user_id if successful, None if user already exists
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (username, email, password_hash,
                             daily_calorie_goal, daily_protein_goal, 
                             daily_carbs_goal, daily_fat_goal, daily_water_goal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, 
            email, 
            password_hash,
            settings.DEFAULT_DAILY_CALORIES,
            settings.DEFAULT_DAILY_PROTEIN,
            settings.DEFAULT_DAILY_CARBS,
            settings.DEFAULT_DAILY_FAT,
            settings.DEFAULT_DAILY_WATER_ML
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return None
        raise e

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate user with username and password
    Returns user data if successful, None otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user['password_hash']):
        # Convert to dict and remove password hash
        user_dict = dict(user)
        del user_dict['password_hash']
        return user_dict
    
    return None

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_dict = dict(user)
        del user_dict['password_hash']
        return user_dict
    
    return None

def update_user_goals(user_id: int, **kwargs) -> bool:
    """
    Update user goals
    Accepts: current_weight, target_weight, daily_calorie_goal, 
             daily_protein_goal, daily_carbs_goal, daily_fat_goal, daily_water_goal
    """
    valid_fields = {
        'current_weight', 'target_weight', 'daily_calorie_goal',
        'daily_protein_goal', 'daily_carbs_goal', 'daily_fat_goal', 
        'daily_water_goal'
    }
    
    # Filter to only valid fields
    updates = {k: v for k, v in kwargs.items() if k in valid_fields}
    
    if not updates:
        return False
    
    # Build update query
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [user_id]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success

def get_all_usernames() -> list:
    """Get list of all usernames (for streamlit-authenticator)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users")
    usernames = [row['username'] for row in cursor.fetchall()]
    
    conn.close()
    return usernames
