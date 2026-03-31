"""
Day-by-Day History View
"""
import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
from utils.database_utils import get_connection, delete_entry
from services.nutrition_service import calculate_net_carbs
import json

def show_history(user):
    """Display day-by-day history with all entries"""
    st.title("📅 Day-by-Day History")
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        days_back = st.selectbox(
            "View History",
            options=[7, 14, 30, 60, 90],
            format_func=lambda x: f"Last {x} days",
            index=0
        )
    
    with col2:
        filter_type = st.selectbox(
            "Filter By",
            options=["all", "meal", "workout"],
            format_func=lambda x: "All" if x == "all" else x.capitalize()
        )
    
    with col3:
        sort_order = st.selectbox(
            "Sort",
            options=["newest", "oldest"],
            format_func=lambda x: "Newest First" if x == "newest" else "Oldest First"
        )
    
    st.divider()
    
    # Get entries for date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT * FROM entries
        WHERE user_id = ?
        AND DATE(timestamp) BETWEEN DATE(?) AND DATE(?)
    """
    params = [user['id'], start_date.isoformat(), end_date.isoformat()]
    
    if filter_type != "all":
        query += " AND entry_type = ?"
        params.append(filter_type)
    
    query += f" ORDER BY timestamp {'DESC' if sort_order == 'newest' else 'ASC'}"
    
    cursor.execute(query, params)
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not entries:
        st.info(f"No {filter_type if filter_type != 'all' else ''} entries found in the last {days_back} days.")
        return
    
    # Group entries by date
    entries_by_date = {}
    for entry in entries:
        entry_date = entry['timestamp'][:10]  # Get YYYY-MM-DD
        if entry_date not in entries_by_date:
            entries_by_date[entry_date] = []
        entries_by_date[entry_date].append(entry)
    
    # Display summary stats
    total_entries = len(entries)
    total_calories = sum(e['calories'] for e in entries)
    total_protein = sum(e['protein_g'] for e in entries)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Entries", total_entries)
    col2.metric("Total Calories", f"{total_calories:.0f}")
    col3.metric("Total Protein", f"{total_protein:.0f}g")
    col4.metric("Days Tracked", len(entries_by_date))
    
    st.divider()
    
    # Display entries grouped by date
    for entry_date in sorted(entries_by_date.keys(), reverse=(sort_order == "newest")):
        day_entries = entries_by_date[entry_date]
        
        # Calculate daily totals
        day_calories = sum(e['calories'] for e in day_entries)
        day_protein = sum(e['protein_g'] for e in day_entries)
        day_carbs = sum(e['carbs_g'] for e in day_entries)
        day_fat = sum(e['fat_g'] for e in day_entries)
        
        # Date header with daily totals
        date_obj = datetime.strptime(entry_date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A, %B %d, %Y")
        
        with st.expander(
            f"📅 **{day_name}** - "
            f"{len(day_entries)} entries | "
            f"{day_calories:.0f} cal | "
            f"{day_protein:.0f}g protein",
            expanded=(entry_date == str(date.today()))  # Expand today by default
        ):
            # Show daily summary
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Calories", f"{day_calories:.0f}")
            col2.metric("Protein", f"{day_protein:.0f}g")
            col3.metric("Carbs", f"{day_carbs:.0f}g")
            col4.metric("Fat", f"{day_fat:.0f}g")
            
            st.divider()
            
            # Display each entry
            for entry in day_entries:
                display_entry_card(entry, user)

def display_entry_card(entry, user):
    """Display a single entry as a card"""
    # Parse vitamins if present
    vitamins = {}
    if entry['vitamins']:
        try:
            vitamins = json.loads(entry['vitamins'])
        except:
            pass
    
    # Entry type icon
    icon = "🍽️" if entry['entry_type'] == 'meal' else "💪"
    time_str = entry['timestamp'][11:16]  # Get HH:MM
    
    with st.container():
        st.markdown(f"### {icon} {entry['description']}")
        st.caption(f"⏰ {time_str}")
        
        # Main nutrition metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.write(f"🔥 **{entry['calories']:.0f}** kcal")
        col2.write(f"🥩 **{entry['protein_g']:.1f}g** protein")
        col3.write(f"🍞 **{entry['carbs_g']:.1f}g** carbs")
        col4.write(f"🥑 **{entry['fat_g']:.1f}g** fat")
        
        # Additional details in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"🌾 Fiber: {entry['fiber_g']:.1f}g")
            st.write(f"🍬 Sugar: {entry['sugar_g']:.1f}g")
        
        with col2:
            net_carbs = calculate_net_carbs(entry['carbs_g'], entry['fiber_g'])
            st.write(f"📊 Net Carbs: {net_carbs:.1f}g")
        
        with col3:
            if entry['photo_path']:
                st.write("📷 Has photo")
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 2, 6])
        
        with col1:
            if st.button("🗑️ Delete", key=f"del_entry_{entry['id']}", use_container_width=True):
                if delete_entry(entry['id'], user['id']):
                    st.success("Deleted!")
                    st.rerun()
        
        with col2:
            if st.button("⭐ Favorite", key=f"fav_entry_{entry['id']}", use_container_width=True):
                save_as_favorite(entry, user)
                st.success("Saved to favorites!")
                st.rerun()
        
        st.divider()

def save_as_favorite(entry, user):
    """Save an entry as a favorite"""
    from utils.database_utils import save_favorite
    
    nutrition_data = {
        'calories': entry['calories'],
        'protein_g': entry['protein_g'],
        'carbs_g': entry['carbs_g'],
        'fat_g': entry['fat_g'],
        'fiber_g': entry['fiber_g'],
        'sugar_g': entry['sugar_g']
    }
    
    save_favorite(user['id'], entry['description'], nutrition_data)
