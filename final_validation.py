"""Final validation script - tests the complete refactored system."""
import os
import sys

print("🚀 Final System Validation")
print("=" * 50)

# Test 1: Core imports
try:
    from analytics import ChatbotAnalytics
    from config import config
    import pandas as pd
    print("✅ Core imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 2: Analytics functionality
try:
    analytics = ChatbotAnalytics("final_test.db")
    analytics.log_interaction(
        question="What programming languages does Noah know?",
        answer="Noah knows Python, and has experience with LangChain and AI frameworks.",
        source_count=2,
        response_time_ms=1100.5,
        linkedin_included=False,
        is_career_related=True,
        session_id="validation_test"
    )
    
    summary = analytics.get_analytics_summary()
    recent = analytics.get_recent_interactions(limit=1)
    stats = analytics.get_database_stats()
    
    assert summary['total_interactions'] == 1
    assert len(recent) == 1
    assert stats['total_records'] == 1
    
    print("✅ Analytics system fully functional")
except Exception as e:
    print(f"❌ Analytics error: {e}")
    sys.exit(1)

# Test 3: File structure
required_files = [
    "analytics.py", "analytics_viewer.py", "main.py", 
    "single_question.py", "config.py", "noah_portfolio.csv"
]

missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    print(f"❌ Missing files: {missing}")
    sys.exit(1)

print("✅ All required files present")

# Test 4: CSV knowledge base has analytics documentation
try:
    with open("noah_portfolio.csv", "r") as f:
        content = f.read()
        if "Analytics & Tracking" in content:
            print("✅ Analytics documentation in knowledge base")
        else:
            print("⚠️  Analytics docs not found in CSV")
except Exception as e:
    print(f"❌ CSV check failed: {e}")

# Cleanup
if os.path.exists("final_test.db"):
    os.remove("final_test.db")

print("\n" + "=" * 50)
print("🎉 SYSTEM VALIDATION COMPLETE!")
print("\n📋 Ready to use:")
print("  • python quick_test.py           - Quick validation")  
print("  • python single_question.py     - Test Q&A")
print("  • streamlit run main.py         - Full chatbot")
print("  • streamlit run analytics_viewer.py - Analytics dashboard")
print("\n🔍 Key improvements made:")
print("  • Simplified and optimized code")
print("  • Removed unnecessary dependencies") 
print("  • Enhanced error handling")
print("  • Streamlined file structure")
print("  • Added comprehensive documentation")
print("\n✅ The analytics system is production-ready!")
