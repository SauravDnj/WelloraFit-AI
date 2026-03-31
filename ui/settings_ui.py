"""
Settings UI Component - Goals and preferences
"""
import streamlit as st
from auth.authentication import update_user_goals

def show_settings(user):
    """Display user settings and goals configuration"""
    st.title("⚙️ Settings & Goals")
    
    st.subheader("🎯 Daily Goals")
    st.write("Set your daily nutrition targets")
    
    with st.form("goals_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            daily_calories = st.number_input(
                "Daily Calorie Goal",
                min_value=1000,
                max_value=5000,
                value=user.get('daily_calorie_goal', 2000),
                step=50
            )
            
            daily_protein = st.number_input(
                "Daily Protein Goal (g)",
                min_value=50,
                max_value=500,
                value=user.get('daily_protein_goal', 150),
                step=5
            )
            
            daily_carbs = st.number_input(
                "Daily Carbs Goal (g)",
                min_value=50,
                max_value=500,
                value=user.get('daily_carbs_goal', 200),
                step=5
            )
        
        with col2:
            daily_fat = st.number_input(
                "Daily Fat Goal (g)",
                min_value=20,
                max_value=200,
                value=user.get('daily_fat_goal', 65),
                step=5
            )
            
            daily_water = st.number_input(
                "Daily Water Goal (ml)",
                min_value=1000,
                max_value=5000,
                value=user.get('daily_water_goal', 2000),
                step=100
            )
        
        st.divider()
        
        st.subheader("⚖️ Weight Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_weight = st.number_input(
                "Current Weight (kg)",
                min_value=30.0,
                max_value=300.0,
                value=float(user.get('current_weight', 70.0)) if user.get('current_weight') else 70.0,
                step=0.1
            )
        
        with col2:
            target_weight = st.number_input(
                "Target Weight (kg)",
                min_value=30.0,
                max_value=300.0,
                value=float(user.get('target_weight', 70.0)) if user.get('target_weight') else 70.0,
                step=0.1
            )
        
        submitted = st.form_submit_button("💾 Save Goals", use_container_width=True)
        
        if submitted:
            success = update_user_goals(
                user['id'],
                daily_calorie_goal=daily_calories,
                daily_protein_goal=daily_protein,
                daily_carbs_goal=daily_carbs,
                daily_fat_goal=daily_fat,
                daily_water_goal=daily_water,
                current_weight=current_weight,
                target_weight=target_weight
            )
            
            if success:
                st.success("✅ Goals updated successfully!")
                # Update session state
                st.session_state.user['daily_calorie_goal'] = daily_calories
                st.session_state.user['daily_protein_goal'] = daily_protein
                st.session_state.user['daily_carbs_goal'] = daily_carbs
                st.session_state.user['daily_fat_goal'] = daily_fat
                st.session_state.user['daily_water_goal'] = daily_water
                st.session_state.user['current_weight'] = current_weight
                st.session_state.user['target_weight'] = target_weight
                st.rerun()
            else:
                st.error("Failed to update goals")
    
    # Account info
    st.divider()
    st.subheader("👤 Account Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
    with col2:
        st.write(f"**Member since:** {user.get('created_at', 'Unknown')[:10]}")
