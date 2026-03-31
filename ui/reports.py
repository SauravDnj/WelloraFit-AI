"""
Reports UI Component - Weekly summaries and progress
"""
import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
from utils.database_utils import get_daily_totals, get_weight_history
from utils.charts import create_weekly_calorie_chart, create_weight_progress_chart

def show_reports(user):
    """Display weekly reports and progress"""
    st.title("📊 Weekly Reports")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        weeks_back = st.selectbox(
            "Select Week",
            options=[0, 1, 2, 3, 4],
            format_func=lambda x: f"This Week" if x == 0 else f"{x} Week{'s' if x > 1 else ''} Ago"
        )
    
    # Calculate date range
    today = date.today()
    week_start = today - timedelta(days=today.weekday() + (weeks_back * 7))
    week_end = week_start + timedelta(days=6)
    
    st.write(f"**Week of {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}**")
    
    # Collect daily data for the week
    daily_data = []
    weekly_totals = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'entries': 0
    }
    
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_totals = get_daily_totals(user['id'], day)
        
        daily_data.append({
            'date': day.strftime('%a %m/%d'),
            'calories': day_totals.get('total_calories', 0),
            'protein': day_totals.get('total_protein', 0),
            'carbs': day_totals.get('total_carbs', 0),
            'fat': day_totals.get('total_fat', 0),
            'entries': day_totals.get('entry_count', 0)
        })
        
        weekly_totals['calories'] += day_totals.get('total_calories', 0)
        weekly_totals['protein'] += day_totals.get('total_protein', 0)
        weekly_totals['carbs'] += day_totals.get('total_carbs', 0)
        weekly_totals['fat'] += day_totals.get('total_fat', 0)
        weekly_totals['entries'] += day_totals.get('entry_count', 0)
    
    # Calculate averages
    days_with_data = sum(1 for d in daily_data if d['entries'] > 0)
    
    # Summary metrics
    st.subheader("📈 Weekly Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Calories",
            f"{weekly_totals['calories']:.0f}",
            f"Avg: {weekly_totals['calories']/7:.0f}/day"
        )
    
    with col2:
        st.metric(
            "Total Protein",
            f"{weekly_totals['protein']:.0f}g",
            f"Avg: {weekly_totals['protein']/7:.0f}g/day"
        )
    
    with col3:
        st.metric(
            "Total Carbs",
            f"{weekly_totals['carbs']:.0f}g",
            f"Avg: {weekly_totals['carbs']/7:.0f}g/day"
        )
    
    with col4:
        st.metric(
            "Total Fat",
            f"{weekly_totals['fat']:.0f}g",
            f"Avg: {weekly_totals['fat']/7:.0f}g/day"
        )
    
    st.divider()
    
    # Daily calorie chart
    st.subheader("📊 Daily Breakdown")
    calorie_chart = create_weekly_calorie_chart(daily_data)
    st.plotly_chart(calorie_chart, use_container_width=True)
    
    # Daily data table
    with st.expander("📋 View Daily Details"):
        df = pd.DataFrame(daily_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": "Date",
                "calories": st.column_config.NumberColumn("Calories", format="%.0f"),
                "protein": st.column_config.NumberColumn("Protein (g)", format="%.1f"),
                "carbs": st.column_config.NumberColumn("Carbs (g)", format="%.1f"),
                "fat": st.column_config.NumberColumn("Fat (g)", format="%.1f"),
                "entries": st.column_config.NumberColumn("Entries", format="%d")
            }
        )
    
    st.divider()
    
    # Weight progress
    st.subheader("⚖️ Weight Progress")
    weight_history = get_weight_history(user['id'], limit=30)
    
    if weight_history:
        weight_chart = create_weight_progress_chart(weight_history)
        st.plotly_chart(weight_chart, use_container_width=True)
        
        # Weight stats
        latest_weight = weight_history[0]['weight']
        target_weight = user.get('target_weight')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Weight", f"{latest_weight:.1f} kg")
        
        with col2:
            if target_weight:
                st.metric("Target Weight", f"{target_weight:.1f} kg")
        
        with col3:
            if target_weight and len(weight_history) > 1:
                weight_change = weight_history[0]['weight'] - weight_history[-1]['weight']
                st.metric("Progress", f"{weight_change:+.1f} kg")
    else:
        st.info("No weight data yet. Go to Settings to log your weight!")
    
    # Export section
    st.divider()
    st.subheader("💾 Export Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download CSV", use_container_width=True):
            df = pd.DataFrame(daily_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download",
                data=csv,
                file_name=f"nutrition_report_{week_start}_{week_end}.csv",
                mime="text/csv"
            )
    
    with col2:
        st.info("PDF export coming soon!")
