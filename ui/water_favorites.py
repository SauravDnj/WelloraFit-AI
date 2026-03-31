"""
Water Tracker and Favorites UI Components
"""
import streamlit as st
from datetime import datetime
from utils.database_utils import (
    add_water_intake, get_today_water_total,
    get_user_favorites, save_favorite, delete_favorite,
    save_entry
)
from utils.charts import create_progress_bar_chart

def show_water_tracker(user):
    """Display water intake tracking"""
    st.title("💧 Water Tracker")
    
    # Get today's total
    today_total = get_today_water_total(user['id'])
    goal = user.get('daily_water_goal', 2000)
    
    # Progress display
    st.subheader("Today's Hydration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Progress bar
        progress_chart = create_progress_bar_chart(today_total, goal, "Water", "#4ECDC4")
        st.plotly_chart(progress_chart, use_container_width=True)
    
    with col2:
        st.metric(
            "Total Today",
            f"{today_total} ml",
            f"{(today_total/goal*100):.0f}% of goal"
        )
    
    st.divider()
    
    # Quick add buttons
    st.subheader("💧 Log Water")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🥤 250 ml\nGlass", use_container_width=True):
            add_water_intake(user['id'], 250)
            st.success("Added 250ml!")
            st.rerun()
    
    with col2:
        if st.button("🫗 500 ml\nBottle", use_container_width=True):
            add_water_intake(user['id'], 500)
            st.success("Added 500ml!")
            st.rerun()
    
    with col3:
        if st.button("💧 750 ml\nLarge Bottle", use_container_width=True):
            add_water_intake(user['id'], 750)
            st.success("Added 750ml!")
            st.rerun()
    
    with col4:
        if st.button("🚰 1000 ml\nLiter", use_container_width=True):
            add_water_intake(user['id'], 1000)
            st.success("Added 1000ml!")
            st.rerun()
    
    # Custom amount
    st.subheader("Custom Amount")
    
    with st.form("custom_water"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            custom_amount = st.number_input(
                "Enter amount (ml)",
                min_value=1,
                max_value=5000,
                value=250,
                step=50
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            submitted = st.form_submit_button("Add", use_container_width=True)
        
        if submitted:
            add_water_intake(user['id'], custom_amount)
            st.success(f"Added {custom_amount}ml!")
            st.rerun()
    
    # Hydration tips
    st.divider()
    st.info("""
    💡 **Hydration Tips:**
    - Drink water regularly throughout the day
    - Increase intake during exercise
    - Listen to your body's thirst signals
    - Aim for clear or light yellow urine
    """)

def show_favorites(user):
    """Display and manage favorite foods"""
    st.title("⭐ Favorite Foods")
    
    # Get favorites
    favorites = get_user_favorites(user['id'])
    
    # Add new favorite section
    with st.expander("➕ Add New Favorite", expanded=False):
        with st.form("add_favorite"):
            name = st.text_input("Food Name")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                calories = st.number_input("Calories", min_value=0, max_value=5000, step=10)
                protein = st.number_input("Protein (g)", min_value=0.0, max_value=500.0, step=0.5)
            
            with col2:
                carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=500.0, step=0.5)
                fat = st.number_input("Fat (g)", min_value=0.0, max_value=200.0, step=0.5)
            
            with col3:
                fiber = st.number_input("Fiber (g)", min_value=0.0, max_value=100.0, step=0.5)
                sugar = st.number_input("Sugar (g)", min_value=0.0, max_value=200.0, step=0.5)
            
            submitted = st.form_submit_button("💾 Save Favorite", use_container_width=True)
            
            if submitted and name:
                nutrition_data = {
                    'calories': calories,
                    'protein_g': protein,
                    'carbs_g': carbs,
                    'fat_g': fat,
                    'fiber_g': fiber,
                    'sugar_g': sugar
                }
                save_favorite(user['id'], name, nutrition_data)
                st.success(f"Added '{name}' to favorites!")
                st.rerun()
    
    st.divider()
    
    # Display favorites
    if favorites:
        st.subheader(f"Your Favorites ({len(favorites)})")
        
        # Grid layout
        cols = st.columns(2)
        
        for idx, fav in enumerate(favorites):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"### ⭐ {fav['name']}")
                    
                    # Nutrition info
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"🔥 **{fav['calories']:.0f}** cal")
                        st.write(f"🥩 **{fav['protein_g']:.1f}g** protein")
                        st.write(f"🍞 **{fav['carbs_g']:.1f}g** carbs")
                    
                    with col2:
                        st.write(f"🥑 **{fav['fat_g']:.1f}g** fat")
                        st.write(f"🌾 **{fav['fiber_g']:.1f}g** fiber")
                        st.write(f"🍬 **{fav['sugar_g']:.1f}g** sugar")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📝 Quick Log", key=f"log_{fav['id']}", use_container_width=True):
                            # Log as entry
                            nutrition_data = {
                                'description': fav['name'],
                                'calories': fav['calories'],
                                'protein_g': fav['protein_g'],
                                'carbs_g': fav['carbs_g'],
                                'fat_g': fav['fat_g'],
                                'fiber_g': fav['fiber_g'],
                                'sugar_g': fav['sugar_g'],
                                'vitamins': {}
                            }
                            save_entry(user['id'], 'meal', fav['name'], nutrition_data)
                            st.success(f"Logged '{fav['name']}'!")
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️ Delete", key=f"del_{fav['id']}", use_container_width=True):
                            delete_favorite(fav['id'], user['id'])
                            st.success("Deleted!")
                            st.rerun()
                    
                    st.divider()
    else:
        st.info("No favorites yet! Add your frequently eaten meals above for quick logging.")
