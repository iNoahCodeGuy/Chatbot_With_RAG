# Analytics System - Quick Start Guide

## Overview
The Noah Portfolio Chatbot includes a streamlined SQLite-based analytics system that automatically tracks every interaction with detailed metrics.

## ✨ Key Features
- **Automatic Tracking**: All interactions logged transparently
- **Performance Metrics**: Response times and source utilization
- **Smart Classification**: Career vs. technical questions  
- **LinkedIn Integration Tracking**: Professional URL inclusion monitoring
- **Zero Configuration**: Works out of the box
- **Lightweight**: Efficient SQLite storage

## 🚀 Quick Start

### 1. Test Basic Functionality
```bash
python quick_test.py          # Validate core system
python single_question.py     # Test Q&A with analytics
```

### 2. Run Full Applications
```bash
streamlit run main.py                # Main chatbot interface
streamlit run analytics_viewer.py    # Analytics dashboard
```

## 📊 What Gets Tracked
- **Complete Interactions**: Questions, answers, timestamps
- **Performance Data**: Response times in milliseconds
- **Content Analysis**: Knowledge base sources used per query
- **Behavioral Insights**: Career-related vs. technical questions
- **LinkedIn Integration**: When professional URLs are auto-included
- **Session Data**: Grouped interactions with session IDs

## 🔍 Analytics Dashboard Features
- **Key Metrics**: Total interactions, response times, categorization
- **Recent Activity**: Timeline of latest interactions
- **Performance Charts**: Response time and source usage analysis
- **Data Export**: CSV export for external analysis
- **Database Stats**: Storage utilization and record counts

## 📁 File Structure
```
analytics.py           # Core analytics system
analytics_viewer.py    # Streamlit analytics dashboard  
main.py               # Main chatbot with embedded analytics
single_question.py    # Test script with analytics
quick_test.py         # Simple system validation
```

## 💾 Database Details
- **File**: `chatbot_analytics.db` (SQLite)
- **Schema**: Indexed for performance (timestamp, career questions)
- **Size**: ~83MB for 5 years typical usage
- **Backup**: Single file for easy backup/restore

## 🛠️ System Requirements
- Python 3.11+
- Core dependencies: streamlit, pandas, langchain, sqlite3
- Optional: plotly (for enhanced visualizations)

## 📈 Sample Output
```
📊 Analytics Summary
Total interactions: 23
Career-related: 12 (52.2%)
LinkedIn included: 10 (83.3% of career questions)
Average response time: 1,247ms
```

The analytics system is production-ready and provides comprehensive insights into chatbot usage patterns!
