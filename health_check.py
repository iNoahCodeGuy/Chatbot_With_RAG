"""Health check script for Portfolio Q&A (FAISS backend).
Run: python health_check.py
"""
import sys
from config import config
from langchain_helper import create_vector_db, vector_db_exists, get_qa_chain


def main():
    print("== Health Check (FAISS) ==")
    # API Key
    if not config.OPENAI_API_KEY:
        print("[FAIL] OPENAI_API_KEY missing")
        return 1
    print(f"[OK] OpenAI key present (length={len(config.OPENAI_API_KEY)})")
    # CSV
    try:
        import os
        if not os.path.exists(config.CSV_FILE_PATH):
            print(f"[FAIL] CSV file missing: {config.CSV_FILE_PATH}")
            return 1
        print(f"[OK] CSV found: {config.CSV_FILE_PATH}")
    except Exception as e:
        print(f"[FAIL] CSV validation error: {e}")
        return 1
    # Vector DB
    try:
        if not vector_db_exists():
            print("[INFO] FAISS index not found. Creating...")
            create_vector_db()
            print("[OK] FAISS index created")
        else:
            print("[OK] FAISS index present")
    except Exception as e:
        print(f"[FAIL] FAISS index error: {e}")
        return 1
    # QA Chain
    try:
        chain = get_qa_chain()
        result = chain.invoke({"query": "What technical skills does Noah have?"})
        answer = result.get("result", "")
        print(f"[OK] QA chain responded (chars={len(answer)})")
    except Exception as e:
        print(f"[FAIL] QA chain error: {e}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
