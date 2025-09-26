#!/usr/bin/env python3
"""
Quick test to validate the analytics system is working
"""
import sys
import os
from analytics import ChatbotAnalytics

try:
    print("🧪 Testing Analytics System...")
    
    # Test 1: Create analytics instance
    analytics = ChatbotAnalytics("test_analytics.db")
    print("✅ Analytics instance created")
    
    # Test 2: Log a sample interaction
    analytics.log_interaction(
        question="Test question about Noah's career",
        answer="Test answer with professional information",
        source_count=2,
        response_time_ms=1250.5,
        linkedin_included=True,
        is_career_related=True,
        session_id="test_session"
    )
    print("✅ Sample interaction logged")
    
    # Test 3: Get analytics summary
    summary = analytics.get_analytics_summary()
    print(f"✅ Analytics summary retrieved: {summary['total_interactions']} total interactions")
    
    # Test 4: Get recent interactions
    recent = analytics.get_recent_interactions(limit=5)
    print(f"✅ Recent interactions retrieved: {len(recent)} interactions")
    
    # Test 5: Database stats
    db_stats = analytics.get_database_stats()
    size = db_stats.get('database_size_mb')
    print(f"✅ Database stats: {db_stats['total_records']} records, {size:.2f}MB")
    
    print("\n🎉 All analytics tests passed!")
    print("Analytics system is fully functional!")
    
    # Clean up test database
    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")
        print("🧹 Test database cleaned up")

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
