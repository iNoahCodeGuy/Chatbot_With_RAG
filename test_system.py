#!/usr/bin/env python3
"""Simple system test - validates core functionality."""
import os
import sys

def test_basic_functionality():
    """Test the basic analytics system."""
    print("🧪 Testing Analytics System...")
    
    try:
        # Import core modules
        from analytics import ChatbotAnalytics
        from config import Config
        
        # Ensure a clean test database
        test_db = "test_temp.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        
        # Test analytics creation
        analytics = ChatbotAnalytics(test_db)
        
        # Test logging
        analytics.log_interaction(
            question="Test career question about Noah",
            answer="Test answer about Noah's professional background.",
            source_count=3,
            response_time_ms=1200.0,
            linkedin_included=True,
            is_career_related=True,
            session_id="test"
        )
        
        # Test summary
        summary = analytics.get_analytics_summary()
        assert summary['total_interactions'] == 1, "Should log 1 interaction"
        assert summary['career_questions'] == 1, "Should detect career question"
        
        # Test recent interactions
        recent = analytics.get_recent_interactions()
        assert len(recent) == 1, "Should have 1 recent interaction"
        
        # Cleanup
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print("✅ Analytics system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_file_structure():
    """Check required files exist."""
    print("🧪 Testing File Structure...")
    
    required_files = [
        "analytics.py", "main.py", "single_question.py", 
        "config.py", "noah_portfolio.csv", "analytics_viewer.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing: {file}")
            return False
    
    print("✅ All required files present!")
    return True

def main():
    """Run tests."""
    print("🚀 Running System Validation")
    print("=" * 40)
    
    tests = [test_file_structure, test_basic_functionality]
    results = [test() for test in tests]
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 System is ready!")
        print("\n💡 Quick Start:")
        print("1. python single_question.py  # Test basic Q&A")
        print("2. streamlit run main.py      # Full chatbot interface") 
        print("3. streamlit run analytics_viewer.py  # Analytics dashboard")
    else:
        print("⚠️  Some issues found. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
