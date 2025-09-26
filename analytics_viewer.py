"""Analytics Dashboard - Interactive Streamlit dashboard for chatbot analytics."""
import streamlit as st
import pandas as pd
from analytics import ChatbotAnalytics
import os

st.set_page_config(
    page_title="Noah's Chatbot Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

# Initialize analytics
@st.cache_resource
def get_analytics():
    return ChatbotAnalytics()

def create_metrics_row(summary: dict) -> None:
    """Create the main metrics display."""
    col1, col2, col3, col4 = st.columns(4)
    
    total = summary.get('total_interactions', 0)
    career = summary.get('career_questions', 0)
    linkedin = summary.get('linkedin_included_count', 0)
    
    with col1:
        st.metric("Total Interactions", total, help="Total questions asked")
    
    with col2:
        career_pct = (career / max(total, 1)) * 100
        st.metric("Career Questions", f"{career_pct:.1f}%", help="Career-related questions")
    
    with col3:
        avg_time = summary.get('avg_response_time', 0)
        st.metric("Avg Response Time", f"{avg_time:.0f}ms", help="Average response time")
    
    with col4:
        linkedin_pct = (linkedin / max(career, 1)) * 100
        st.metric("LinkedIn Integration", f"{linkedin_pct:.1f}%", help="LinkedIn URL inclusion rate")

def create_recent_interactions_table(recent: list) -> None:
    """Create recent interactions table."""
    if not recent:
        st.info("No recent interactions found.")
        return
    
    df = pd.DataFrame([
        {
            'Time': r[1],
            'Question': r[2][:80] + "..." if len(r[2]) > 80 else r[2],
            'Sources': r[4],
            'Response Time': f"{r[5]:.0f}ms" if r[5] else "N/A",
            'Career Related': "✅" if r[7] else "❌",
            'LinkedIn Included': "✅" if r[6] else "❌"
        }
        for r in recent
    ])
    
    st.dataframe(df, use_container_width=True)

def create_simple_charts(recent: list, summary: dict) -> None:
    """Create simple text-based analytics displays."""
    if not recent:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Response Time Analysis")
        response_times = [r[5] for r in recent if r[5] is not None]
        if response_times:
            st.write(f"📊 **Response Time Stats:**")
            st.write(f"- Average: {sum(response_times)/len(response_times):.0f}ms")
            st.write(f"- Fastest: {min(response_times):.0f}ms")
            st.write(f"- Slowest: {max(response_times):.0f}ms")
        
        st.bar_chart(pd.DataFrame({'Response Times (ms)': response_times}))
    
    with col2:
        st.subheader("Source Usage")
        source_counts = [r[4] for r in recent if r[4] is not None]
        if source_counts:
            st.write(f"📚 **Source Usage Stats:**")
            st.write(f"- Average sources: {sum(source_counts)/len(source_counts):.1f}")
            st.write(f"- Most sources used: {max(source_counts)}")
            st.write(f"- Least sources used: {min(source_counts)}")
        
        st.bar_chart(pd.DataFrame({'Sources Used': source_counts}))

def create_category_display(summary: dict) -> None:
    """Create question categorization display."""
    career = summary.get('career_questions', 0)
    total = summary.get('total_interactions', 0)
    technical = total - career
    
    if total > 0:
        st.write("📊 **Question Categories:**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Career Questions", career, f"{(career/total)*100:.1f}%")
        with col2:
            st.metric("Technical Questions", technical, f"{(technical/total)*100:.1f}%")

# Main app
st.title("📊 Chatbot Analytics Dashboard")
st.markdown("*Real-time insights into chatbot performance and usage patterns*")

analytics = get_analytics()

# Sidebar controls
st.sidebar.header("Analytics Controls")
days_filter = st.sidebar.slider("Days to analyze", 1, 365, 30)
show_raw_data = st.sidebar.checkbox("Show raw interaction data", False)

# Export functionality
st.sidebar.markdown("---")
if st.sidebar.button("📥 Export to CSV"):
    try:
        export_path = analytics.export_data()
        st.sidebar.success(f"Exported: {os.path.basename(export_path)}")
    except Exception as e:
        st.sidebar.error(f"Export failed: {e}")

try:
    # Get analytics data
    summary = analytics.get_analytics_summary(days=days_filter)
    
    if summary.get('total_interactions', 0) == 0:
        st.warning("No interactions found. Start using the chatbot to see analytics!")
        st.stop()
    
    # Main metrics
    st.subheader("📈 Key Metrics")
    create_metrics_row(summary)
    
    # Recent interactions
    st.subheader("🕒 Recent Activity")
    recent = analytics.get_recent_interactions(limit=10)
    create_recent_interactions_table(recent)
    
    # Performance analysis
    st.subheader("⚡ Performance Analysis")
    create_simple_charts(recent, summary)
    
    # Question categorization
    st.subheader("📊 Question Categories")
    create_category_display(summary)
    
    # Raw data (optional)
    if show_raw_data and recent:
        st.subheader("🔍 Raw Interaction Data")
        raw_df = pd.DataFrame([
            {
                'ID': r[0], 'Timestamp': r[1], 'Question': r[2],
                'Answer': r[3][:200] + "..." if len(r[3]) > 200 else r[3],
                'Source Count': r[4], 'Response Time (ms)': r[5],
                'LinkedIn Included': r[6], 'Career Related': r[7],
                'Session ID': r[9] if len(r) > 9 else 'N/A'
            }
            for r in recent
        ])
        st.dataframe(raw_df, use_container_width=True)
    
    # Database statistics
    st.subheader("💾 Database Statistics")
    db_stats = analytics.get_database_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Database Size", f"{db_stats.get('size_mb', 0):.2f} MB")
    with col2:
        st.metric("Total Records", db_stats.get('total_records', 0))
    with col3:
        st.metric("Database File", os.path.basename(analytics.db_path))

except Exception as e:
    st.error(f"Failed to load analytics: {e}")
    st.info("Ensure you've used the chatbot to generate analytics data.")

st.markdown("---")
st.caption("Analytics Dashboard - Real-time insights into chatbot performance")
