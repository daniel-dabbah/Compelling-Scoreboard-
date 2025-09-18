import streamlit as st
from datetime import datetime, date
import json

# Configure page
st.set_page_config(
    page_title="הערכה פנימית - לוח תוצאות",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with RTL support, pleasant colors, and background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Heebo', sans-serif;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 50%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d6e8f5 50%, #c8d8e4 100%);
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        color: #2D3748;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .question-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border-right: 6px solid #4299e1;
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.15);
        direction: rtl;
        text-align: right;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .question-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.2);
    }
    
    .question-container h4 {
        color: #2D3748;
        font-weight: 500;
        font-size: 1.3rem;
        margin: 0;
        direction: rtl;
        line-height: 1.6;
    }
    
    .score-display {
        font-size: 3.2rem;
        font-weight: bold;
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #4299e1 0%, #667eea 50%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        margin: 2.5rem 0;
        box-shadow: 0 10px 30px rgba(66, 153, 225, 0.4);
        direction: ltr;
    }
    
    .feedback-box {
        background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #4fd1c7;
        box-shadow: 0 6px 20px rgba(79, 209, 199, 0.15);
        direction: rtl;
        text-align: center;
    }
    
    .improvement-box {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #68d391;
        box-shadow: 0 6px 20px rgba(104, 211, 145, 0.15);
        direction: rtl;
        text-align: center;
    }
    
    .progress-stats {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin: 1.2rem 0;
        border-top: 4px solid #4299e1;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .progress-stats:hover {
        transform: translateY(-3px);
    }
    
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .chart-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 1.5rem;
    }
    
    .stSlider > div > div {
        direction: ltr;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.3);
        padding: 0.5rem;
        border-radius: 15px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 1rem 2rem;
        border: 2px solid transparent;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
        color: white;
        border-color: #4299e1;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Assessment subjects and questions in Hebrew
SUBJECTS = ["אנגלית", "ספרות", "תנ״ך", "מתמטיקה", "היסטוריה", "עברית", "מגמה א'", "מגמה ב'", "מגמה ג'"]
ADDITIONAL_QUESTIONS = [
    "עד כמה אני מרגיש שאני מצליח להחזיר לעצמי את האנרגיה שאני מוציא על הלימודים",
    "עד כמה אני מרגיש שאני עוזר לאחרים מהכיתה"
]

def get_user_id():
    """Get user ID based on name input"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    return st.session_state.user_id

def set_user_id(name):
    """Set user ID based on name"""
    # Create a simple ID from the name
    user_id = name.strip().replace(" ", "_").lower()
    st.session_state.user_id = user_id
    return user_id

def get_feedback_message(score):
    """Generate short feedback based on the total score"""
    if score >= 90:
        return "מצוין! כל הכבוד!"
    elif score >= 80:
        return "עבודה טובה!"
    elif score >= 70:
        return "יפה, ממשיכים לעבוד!"
    else:
        return "עבודה טובה, בוא נשפר עוד קצת!"

def get_improvement_message(current_score, previous_score=None):
    """Generate short improvement feedback message"""
    if previous_score is None:
        return "כל הכבוד על ההערכה הראשונה!"
    
    improvement = current_score - previous_score
    
    if improvement > 0:
        return f"כל הכבוד! שיפרת ב-{improvement:.1f} נקודות!"
    elif improvement == 0:
        return "נשארת על אותו ציון!"
    else:
        return "לא נורא, נשתפר!"

def load_user_data():
    """Load all users data from session state"""
    if 'all_users_data' not in st.session_state:
        st.session_state.all_users_data = {}
    return st.session_state.all_users_data

def save_assessment_result(user_id, score, responses):
    """Save assessment result for the current user"""
    all_data = load_user_data()
    
    if user_id not in all_data:
        all_data[user_id] = {'assessments': []}
    
    assessment = {
        'date': datetime.now().isoformat(),
        'score': score,
        'responses': responses,
        'assessment_number': len(all_data[user_id]['assessments']) + 1
    }
    
    all_data[user_id]['assessments'].append(assessment)
    st.session_state.all_users_data = all_data

def get_user_history(user_id):
    """Get assessment history for current user"""
    all_data = load_user_data()
    if user_id and user_id in all_data:
        return all_data[user_id]['assessments']
    return []

def create_simple_progress_chart(history):
    """Create a simple progress chart using Streamlit's built-in chart"""
    if not history:
        return None
    
    # Prepare data for chart
    chart_data = []
    for assessment in history:
        chart_data.append({
            'הערכה': f"הערכה {assessment['assessment_number']}",
            'ציון': assessment['score']
        })
    
    return chart_data

def display_statistics(history):
    """Display progress statistics in Hebrew"""
    if not history:
        return
    
    scores = [assessment['score'] for assessment in history]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">הציון שלי עכשיו</h3>
            <h2 style="color: #4299e1; margin: 5px 0;">{}/100</h2>
        </div>
        """.format(scores[-1]), unsafe_allow_html=True)
    
    with col2:
        best_score = max(scores)
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">הציון הכי טוב שלי</h3>
            <h2 style="color: #68d391; margin: 5px 0;">{}/100</h2>
        </div>
        """.format(best_score), unsafe_allow_html=True)
    
    with col3:
        total_assessments = len(history)
        st.markdown("""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">כמה הערכות עשיתי</h3>
            <h2 style="color: #9f7aea; margin: 5px 0;">{}</h2>
        </div>
        """.format(total_assessments), unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">הערכה פנימית - לוח תוצאות</h1>', unsafe_allow_html=True)
    
    # Get user ID
    user_id = get_user_id()
    
    # If no user ID, show login screen
    if not user_id:
        st.markdown("<div style='text-align: center; margin: 3rem 0;'>", unsafe_allow_html=True)
        st.markdown("### היכנס עם השם שלך")
        st.markdown("כתוב את השם שלך כדי להתחיל או לחזור להערכות שלך")
        
        name = st.text_input("השם שלי:", placeholder="כתוב את השם המלא שלך")
        
        if st.button("להיכנס", type="primary", disabled=not name.strip()):
            if name.strip():
                set_user_id(name.strip())
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Show current user
    st.markdown(f"<div style='text-align: center; color: #666; margin-bottom: 1rem;'>שלום {user_id.replace('_', ' ').title()}!</div>", unsafe_allow_html=True)
    
    # Add logout button in sidebar or corner
    if st.button("להחליף משתמש", key="logout"):
        st.session_state.user_id = None
        st.rerun()
    
    # Initialize session state
    if 'current_responses' not in st.session_state:
        st.session_state.current_responses = {}
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Create tabs
    tab1, tab2 = st.tabs(["הערכה חדשה", "להסתכל על ההתקדמות שלי"])
    
    with tab1:
        if not st.session_state.show_results:
            st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><p style='font-size: 1.1rem; color: #2D3748;'>תן לכל מקצוע ציון מ-1 (בכלל לא בטוח) עד 10 (מאוד בטוח) - לפי איך שאתה מרגיש ממש עכשיו.</p></div>", unsafe_allow_html=True)
            
            # Display all questions at once
            with st.form("assessment_form"):
                responses = {}
                question_index = 0
                
                # Subject questions
                for i, subject in enumerate(SUBJECTS):
                    st.markdown(f"""
                    <div class="question-container">
                        <h4>עד כמה אני מרגיש שאני שולט בחומר ב{subject}?</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    responses[question_index] = st.slider(
                        f"הציון שלי ב{subject}:",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.current_responses.get(question_index, 5),
                        key=f"q_{question_index}",
                        label_visibility="collapsed"
                    )
                    question_index += 1
                
                # Additional questions
                for i, question in enumerate(ADDITIONAL_QUESTIONS):
                    st.markdown(f"""
                    <div class="question-container">
                        <h4>{question}?</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    responses[question_index] = st.slider(
                        f"השאלה מס׳ {question_index + 1}:",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.current_responses.get(question_index, 5),
                        key=f"q_{question_index}",
                        label_visibility="collapsed"
                    )
                    question_index += 1
                
                # Submit button
                submitted = st.form_submit_button("לשלוח את ההערכה", type="primary", use_container_width=True)
                
                if submitted:
                    st.session_state.current_responses = responses
                    st.session_state.show_results = True
                    st.rerun()
        
        else:
            # Show results
            responses = st.session_state.current_responses
            total_score = round((sum(responses.values()) / ((len(SUBJECTS) + len(ADDITIONAL_QUESTIONS)) * 10)) * 100, 1)
            
            # Get previous score for comparison
            history = get_user_history(user_id)
            previous_score = history[-1]['score'] if history else None
            
            # Save results automatically
            save_assessment_result(user_id, total_score, responses)
            
            # Display score
            st.markdown(f"""
            <div class="score-display">
                הציון הכללי שלי: {total_score}/100
            </div>
            """, unsafe_allow_html=True)
            
            # Display improvement feedback
            improvement_msg = get_improvement_message(total_score, previous_score)
            if improvement_msg:
                st.markdown(f"""
                <div class="improvement-box">
                    <p style="font-size: 1.1rem; margin: 0; text-align: center; color: #2D3748; font-weight: 500;">{improvement_msg}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display general feedback
            feedback = get_feedback_message(total_score)
            if feedback:
                st.markdown(f"""
                <div class="feedback-box">
                    <p style="font-size: 1.1rem; margin: 0; text-align: center; color: #2D3748; font-weight: 500;">{feedback}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Button to take new assessment
            if st.button("לעשות הערכה חדשה", type="primary", use_container_width=True):
                st.session_state.current_responses = {}
                st.session_state.show_results = False
                st.rerun()
    
    with tab2:
        # Progress tracking
        history = get_user_history(user_id)
        
        if not history:
            st.info("עוד לא עשית הערכות. תעשה הערכה ראשונה ואז תוכל לראות איך אתה מתקדם!")
        else:
            st.markdown("<h3 style='text-align: center;'>איך אני מתקדם</h3>", unsafe_allow_html=True)
            
            # Statistics
            display_statistics(history)
            
            # Simple progress chart using Streamlit's built-in chart
            chart_data = create_simple_progress_chart(history)
            if chart_data:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">הגרף של ההתקדמות שלי</div>', unsafe_allow_html=True)
                
                # Create a simple line chart
                scores = [assessment['score'] for assessment in history]
                assessment_numbers = [assessment['assessment_number'] for assessment in history]
                
                # Display as line chart
                chart_dict = {f"הערכה {num}": score for num, score in zip(assessment_numbers, scores)}
                st.line_chart(chart_dict, height=400)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Recent assessments table
            st.markdown("### כל ההערכות שעשיתי")
            recent_data = []
            for assessment in reversed(history):  # Most recent first
                date_obj = datetime.fromisoformat(assessment['date'])
                recent_data.append({
                    'הערכה מספר': assessment['assessment_number'],
                    'תאריך': date_obj.strftime('%d/%m/%Y'),
                    'שעה': date_obj.strftime('%H:%M'),
                    'הציון שקיבלתי': f"{assessment['score']}/100"
                })
            
            if recent_data:
                # Convert to a format suitable for st.dataframe
                st.dataframe(recent_data, use_container_width=True)

if __name__ == "__main__":
    main()
