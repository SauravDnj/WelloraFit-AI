"""
Chat Interface UI Component - Enhanced with persistent storage
"""
import streamlit as st
from datetime import datetime
import os
from services.groq_service import groq_service
from services.nutrition_service import validate_nutrition_data, format_nutrition_summary
from utils.database_utils import save_entry, get_today_entries
from config.settings import settings

def show_chat_interface(user):
    """Display chat interface for logging meals and workouts"""
    st.title("💬 Chat & Log")
    
    # Entry type selector at top
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        entry_type = st.selectbox(
            "What are you logging?",
            ["meal", "workout"],
            format_func=lambda x: "🍽️ Meal" if x == "meal" else "💪 Workout"
        )
    
    with col2:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col3:
        today_entries = get_today_entries(user['id'])
        st.metric("Today's Logs", len(today_entries))
    
    st.divider()
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat display area with scrollable container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for idx, message in enumerate(st.session_state.chat_history):
                if message['role'] == 'user':
                    with st.chat_message("user", avatar="👤"):
                        st.write(message['content'])
                        if message.get('timestamp'):
                            st.caption(message['timestamp'])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(message['content'])
                        if 'nutrition' in message:
                            # Display nutrition in a nice card
                            nutrition = message['nutrition']
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Calories", f"{nutrition.get('calories', 0):.0f}")
                            with col2:
                                st.metric("Protein", f"{nutrition.get('protein_g', 0):.1f}g")
                            with col3:
                                st.metric("Carbs", f"{nutrition.get('carbs_g', 0):.1f}g")
                            with col4:
                                st.metric("Fat", f"{nutrition.get('fat_g', 0):.1f}g")
                            
                            # Show additional details in expander
                            with st.expander("📊 See full nutrition details"):
                                st.write(f"**Fiber:** {nutrition.get('fiber_g', 0):.1f}g")
                                st.write(f"**Sugar:** {nutrition.get('sugar_g', 0):.1f}g")
                                net_carbs = nutrition.get('carbs_g', 0) - nutrition.get('fiber_g', 0)
                                st.write(f"**Net Carbs:** {max(0, net_carbs):.1f}g")
                                if nutrition.get('notes'):
                                    st.info(nutrition['notes'])
        else:
            st.info("👋 Hi! I'm your AI health assistant. Tell me what you ate or did for exercise, and I'll track it for you!")
            st.markdown("""
            **Examples:**
            - "I had 2 scrambled eggs with toast"
            - "Did 30 minutes of running"
            - Upload a photo of your meal
            """)
    
    st.divider()
    
    # Input area
    col1, col2 = st.columns([5, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "📷 Photo",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed",
            key=f"photo_upload_{len(st.session_state.chat_history)}"
        )
    
    with col1:
        user_input = st.chat_input(
            "Type your meal or workout here..." if entry_type == "meal" 
            else "Describe your workout..."
        )
    
    # Process text input
    if user_input:
        process_text_input(user, user_input, entry_type)
    
    # Process photo upload
    if uploaded_file:
        process_photo_input(user, uploaded_file, entry_type)

def process_text_input(user, text: str, entry_type: str):
    """Process text-based meal/workout logging with DB storage"""
    # Check if Groq service is available
    if not groq_service:
        st.error("⚠️ AI service not available. GROQ_API_KEY not configured.")
        st.info("**Streamlit Cloud:** App Settings → Secrets → Add GROQ_API_KEY")
        st.info("**Local Development:** Add GROQ_API_KEY to .env file")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add user message to chat
    st.session_state.chat_history.append({
        'role': 'user',
        'content': text,
        'timestamp': timestamp
    })
    
    # Show processing message
    with st.spinner(f"🤖 Analyzing your {entry_type}..."):
        try:
            # Get nutrition data from AI
            if entry_type == "workout":
                # For workouts, estimate calories burned
                nutrition_data = groq_service.analyze_meal_text(
                    f"Estimate calories burned and nutrients for this workout activity: {text}"
                )
            else:
                nutrition_data = groq_service.analyze_meal_text(text)
            
            nutrition_data = validate_nutrition_data(nutrition_data)
            
            # Save to database
            entry_id = save_entry(
                user_id=user['id'],
                entry_type=entry_type,
                description=text,
                nutrition_data=nutrition_data
            )
            
            # Add AI response to chat
            emoji = "🍽️" if entry_type == "meal" else "💪"
            response_text = f"{emoji} Great! I've logged your {entry_type}!"
            if nutrition_data.get('confidence'):
                response_text += f"\n\n**Confidence:** {nutrition_data['confidence']}"
            if nutrition_data.get('notes'):
                response_text += f"\n\n💡 **Note:** {nutrition_data['notes']}"
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response_text,
                'nutrition': nutrition_data,
                'entry_id': entry_id
            })
            
            st.success(f"✅ {entry_type.capitalize()} logged successfully!")
            st.rerun()
            
        except Exception as e:
            error_msg = f"Sorry, I couldn't analyze that. Error: {str(e)}"
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"❌ {error_msg}"
            })
            st.error(error_msg)

def process_photo_input(user, uploaded_file, entry_type: str):
    """Process photo-based meal logging with DB storage"""
    # Check if Groq service is available
    if not groq_service:
        st.error("⚠️ AI service not available. GROQ_API_KEY not configured.")
        st.info("**Streamlit Cloud:** App Settings → Secrets → Add GROQ_API_KEY")
        st.info("**Local Development:** Add GROQ_API_KEY to .env file")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_filename = f"{user['id']}_{timestamp}_{uploaded_file.name}"
    photo_path = os.path.join(settings.UPLOAD_FOLDER, photo_filename)
    
    # Save photo
    with open(photo_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    # Add user message to chat
    st.session_state.chat_history.append({
        'role': 'user',
        'content': f"📷 [Photo: {uploaded_file.name}]",
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Show processing message
    with st.spinner("🤖 Analyzing your photo..."):
        try:
            # Get nutrition data from AI vision
            nutrition_data = groq_service.analyze_food_photo(photo_path)
            nutrition_data = validate_nutrition_data(nutrition_data)
            
            # Save to database
            entry_id = save_entry(
                user_id=user['id'],
                entry_type=entry_type,
                description=nutrition_data.get('description', 'Photo meal'),
                nutrition_data=nutrition_data,
                photo_path=photo_path
            )
            
            # Add AI response to chat
            response_text = f"📷 Great photo! I've analyzed and logged it!\n\n**Identified:** {nutrition_data.get('description', 'Food item')}"
            if nutrition_data.get('portion_estimate'):
                response_text += f"\n\n**Portion:** {nutrition_data['portion_estimate']}"
            if nutrition_data.get('confidence'):
                response_text += f"\n\n**Confidence:** {nutrition_data['confidence']}"
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response_text,
                'nutrition': nutrition_data,
                'entry_id': entry_id
            })
            
            st.success("✅ Photo analyzed and logged!")
            st.rerun()
            
        except Exception as e:
            error_msg = f"Sorry, I couldn't analyze the photo. Error: {str(e)}"
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"❌ {error_msg}"
            })
            st.error(error_msg)
            # Clean up photo on error
            if os.path.exists(photo_path):
                os.remove(photo_path)
