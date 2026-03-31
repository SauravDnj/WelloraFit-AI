"""
Dashboard UI Component
"""
import streamlit as st
from datetime import datetime, date
from utils.database_utils import get_daily_totals, get_recent_entries, delete_entry
from utils.charts import create_macro_donut_chart, create_progress_bar_chart
from services.groq_service import groq_service
from services.nutrition_service import calculate_net_carbs

def show_dashboard(user):
    """Display main dashboard with daily summary and insights"""
    st.title("📊 Dashboard")
    
    # Get today's data
    today_totals = get_daily_totals(user['id'])
    recent_entries = get_recent_entries(user['id'], limit=10)
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Calories",
            f"{today_totals.get('total_calories', 0):.0f}",
            f"Goal: {user.get('daily_calorie_goal', 2000)}"
        )
    
    with col2:
        st.metric(
            "Protein",
            f"{today_totals.get('total_protein', 0):.0f}g",
            f"Goal: {user.get('daily_protein_goal', 150)}g"
        )
    
    with col3:
        st.metric(
            "Carbs",
            f"{today_totals.get('total_carbs', 0):.0f}g",
            f"Goal: {user.get('daily_carbs_goal', 200)}g"
        )
    
    with col4:
        st.metric(
            "Fat",
            f"{today_totals.get('total_fat', 0):.0f}g",
            f"Goal: {user.get('daily_fat_goal', 65)}g"
        )
    
    st.divider()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Recent Entries")
        
        if recent_entries:
            for entry in recent_entries:
                with st.expander(
                    f"{'🍽️' if entry['entry_type'] == 'meal' else '💪'} {entry['description']} - "
                    f"{entry['calories']:.0f} cal",
                    expanded=False
                ):
                    entry_col1, entry_col2 = st.columns([3, 1])
                    
                    with entry_col1:
                        st.write(f"**Time:** {entry['timestamp']}")
                        st.write(f"**Protein:** {entry['protein_g']:.1f}g | "
                                f"**Carbs:** {entry['carbs_g']:.1f}g | "
                                f"**Fat:** {entry['fat_g']:.1f}g")
                        st.write(f"**Fiber:** {entry['fiber_g']:.1f}g | "
                                f"**Sugar:** {entry['sugar_g']:.1f}g")
                        
                        # Net carbs
                        net_carbs = calculate_net_carbs(entry['carbs_g'], entry['fiber_g'])
                        st.write(f"**Net Carbs:** {net_carbs:.1f}g")
                    
                    with entry_col2:
                        if st.button("🗑️ Delete", key=f"del_{entry['id']}"):
                            if delete_entry(entry['id'], user['id']):
                                st.success("Deleted!")
                                st.rerun()
        else:
            st.info("No entries yet. Go to 'Chat & Log' to start tracking!")
    
    with col2:
        st.subheader("🥗 Macro Breakdown")
        
        # Macro donut chart
        macro_chart = create_macro_donut_chart(
            today_totals.get('total_protein', 0),
            today_totals.get('total_carbs', 0),
            today_totals.get('total_fat', 0)
        )
        st.plotly_chart(macro_chart, use_container_width=True)
        
        # Progress bars
        st.subheader("📈 Today's Progress")
        
        # Calories progress
        cal_current = today_totals.get('total_calories', 0)
        cal_goal = user.get('daily_calorie_goal', 2000)
        cal_chart = create_progress_bar_chart(cal_current, cal_goal, "Calories")
        st.plotly_chart(cal_chart, use_container_width=True)
        
        # Protein progress
        protein_current = today_totals.get('total_protein', 0)
        protein_goal = user.get('daily_protein_goal', 150)
        protein_chart = create_progress_bar_chart(protein_current, protein_goal, "Protein", "#FF6B6B")
        st.plotly_chart(protein_chart, use_container_width=True)
    
    # AI Insights section
    if today_totals.get('entry_count', 0) > 0:
        st.divider()
        st.subheader("💡 AI Nutrition Insights")
        
        if st.button("Generate Insights", use_container_width=True):
            with st.spinner("Analyzing your nutrition..."):
                insights_data = {
                    'calories': today_totals.get('total_calories', 0),
                    'calorie_goal': user.get('daily_calorie_goal', 2000),
                    'protein': today_totals.get('total_protein', 0),
                    'protein_goal': user.get('daily_protein_goal', 150),
                    'carbs': today_totals.get('total_carbs', 0),
                    'carbs_goal': user.get('daily_carbs_goal', 200),
                    'fat': today_totals.get('total_fat', 0),
                    'fat_goal': user.get('daily_fat_goal', 65)
                }
                
                insights = groq_service.generate_nutrition_insights(insights_data)
                st.info(insights)
