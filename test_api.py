#!/usr/bin/env python3
"""
Quick test script to verify the RAG API is working correctly.
Run this after starting the server with: python app.py
"""
import requests
import json
import sys

BASE_URL = "http://localhost:10000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("status") == "ok"
        print("✓ Health check passed")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_query(query, expected_keywords=None):
    """Test query endpoint"""
    print(f"\nTesting query: '{query}'...")
    try:
        payload = {"query": query, "top_k": 3}
        resp = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
        assert resp.status_code == 200
        data = resp.json()
        
        # Verify response structure
        assert "answer" in data, "Response missing 'answer' field"
        assert "contexts" in data, "Response missing 'contexts' field"
        assert isinstance(data["contexts"], list), "contexts must be a list"
        
        print(f"Answer: {data['answer']}")
        print(f"Contexts ({len(data['contexts'])}): {data['contexts'][:2]}...")
        
        # Optionally check for expected keywords
        if expected_keywords:
            answer_lower = data["answer"].lower()
            found = any(kw.lower() in answer_lower for kw in expected_keywords)
            if found:
                print(f"✓ Found expected keyword in answer")
            else:
                print(f"⚠ Expected keywords not found: {expected_keywords}")
        
        print("✓ Query test passed")
        return True
    except Exception as e:
        print(f"✗ Query test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("MedInSight RAG API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    results.append(test_health())
    
    # Test 2: Diabetes query
    results.append(test_query(
        "What is diabetes?",
        expected_keywords=["diabetes", "blood sugar", "glucose"]
    ))
    
    # Test 3: Hypertension query
    results.append(test_query(
        "What is hypertension?",
        expected_keywords=["hypertension", "blood pressure"]
    ))
    
    # Test 4: Heart attack query
    results.append(test_query(
        "What are symptoms of heart attack?",
        expected_keywords=["chest", "pain", "myocardial"]
    ))
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
