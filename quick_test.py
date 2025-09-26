#!/usr/bin/env python3
"""Quick test to validate analytics without external dependencies."""

def test_analytics():
    try:
        # Test basic analytics import and functionality
        from analytics import ChatbotAnalytics
        
        # Create temp analytics instance
        analytics = ChatbotAnalytics("quick_test.db")
        
        # Log a test interaction
        analytics.log_interaction(
            question="What are Noah's skills?",
            answer="Noah has skills in Python, AI, and sales.",
            source_count=2,
            response_time_ms=1500.0,
            linkedin_included=False,
            is_career_related=True,
            session_id="quick_test"
        )
        
        # Get summary
        summary = analytics.get_analytics_summary()
        print(f"✅ Analytics working! Total interactions: {summary['total_interactions']}")
        
        # Get recent
        recent = analytics.get_recent_interactions(limit=1)
        print(f"✅ Recent interactions: {len(recent)} found")
        
        # Clean up
        import os
        if os.path.exists("quick_test.db"):
            os.remove("quick_test.db")
        
        return True
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False

def test_config():
    try:
        from config import Config
        cfg = Config()
        print("✅ Config system working!")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Quick System Test")
    print("=" * 20)
    
    results = [
        test_config(),
        test_analytics()
    ]
    
    if all(results):
        print("\n🎉 Core system is working!")
    else:
        print("\n⚠️  Some issues found.")
