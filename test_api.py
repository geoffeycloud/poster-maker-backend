#!/usr/bin/env python3
"""
Test script for the AI Poster Maker API
Run this to test all the endpoints and generate sample posters
"""

import requests
import json
import time
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_poster_generation():
    """Test poster generation with different themes and sizes"""
    
    print("🎨 Testing AI Poster Generation...")
    
    # Test cases
    test_cases = [
        {
            "name": "Business Poster",
            "data": {
                "title": "Grand Opening Sale",
                "description": "50% off everything in store!",
                "theme": "corporate",
                "size": "A4",
                "background_prompt": "modern business storefront with elegant lighting",
                "include_logo": True,
                "additional_text": "Visit us at 123 Main Street | Call: (555) 123-4567"
            }
        },
        {
            "name": "Social Media Post",
            "data": {
                "title": "Follow Your Dreams",
                "description": "Motivational quote of the day",
                "theme": "modern",
                "size": "SOCIAL_MEDIA",
                "background_prompt": "inspiring sunset over mountains",
                "additional_text": "#motivation #dreams #success"
            }
        },
        {
            "name": "Event Flyer",
            "data": {
                "title": "Tech Conference 2025",
                "description": "The Future of AI and Innovation",
                "theme": "professional",
                "size": "LETTER",
                "background_prompt": "futuristic tech conference hall with holographic displays",
                "include_logo": True,
                "additional_text": "December 15-16, 2025 | Register at techconf2025.com"
            }
        },
        {
            "name": "Creative Poster",
            "data": {
                "title": "Art Exhibition",
                "description": "Contemporary Digital Art Showcase",
                "theme": "creative",
                "size": "A4",
                "background_prompt": "abstract digital art with vibrant colors",
                "additional_text": "Opening Night: July 20, 2025 | Gallery Downtown"
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📝 Generating {test_case['name']}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/generate-poster",
                json=test_case['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "name": test_case['name'],
                    "poster_id": result['poster_id'],
                    "image_url": result['image_url'],
                    "success": True
                })
                print(f"✅ Success! Poster ID: {result['poster_id']}")
                print(f"🖼️  Preview: {BASE_URL}{result['image_url']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                results.append({
                    "name": test_case['name'],
                    "success": False,
                    "error": response.text
                })
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            results.append({
                "name": test_case['name'],
                "success": False,
                "error": str(e)
            })
    
    return results

def test_text_generation():
    """Test AI text generation"""
    
    print("\n📝 Testing AI Text Generation...")
    
    test_prompts = [
        {
            "prompt": "Write a catchy tagline for a coffee shop",
            "tone": "friendly",
            "max_length": 100
        },
        {
            "prompt": "Create a motivational quote for entrepreneurs",
            "tone": "inspiring",
            "max_length": 150
        },
        {
            "prompt": "Write a professional announcement for a product launch",
            "tone": "professional",
            "max_length": 200
        }
    ]
    
    for i, prompt_data in enumerate(test_prompts, 1):
        print(f"\n🔤 Test {i}: {prompt_data['prompt']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/generate-text",
                json=prompt_data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Generated: {result['text']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")

def test_api_endpoints():
    """Test other API endpoints"""
    
    print("\n🔍 Testing API Endpoints...")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test templates
    try:
        response = requests.get(f"{BASE_URL}/api/templates")
        if response.status_code == 200:
            templates = response.json()
            print(f"✅ Templates endpoint working - {len(templates.get('templates', []))} templates available")
        else:
            print(f"❌ Templates endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Templates endpoint error: {e}")
    
    # Test themes
    try:
        response = requests.get(f"{BASE_URL}/api/themes")
        if response.status_code == 200:
            themes = response.json()
            print(f"✅ Themes endpoint working - {len(themes.get('themes', []))} themes available")
            print(f"📋 Available themes: {', '.join(themes.get('themes', []))}")
        else:
            print(f"❌ Themes endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Themes endpoint error: {e}")

def main():
    """Main test function"""
    
    print("🚀 AI Poster Maker API Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the server first:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("✅ Server is running!")
    
    # Run tests
    test_api_endpoints()
    test_text_generation()
    poster_results = test_poster_generation()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    successful_posters = [r for r in poster_results if r['success']]
    failed_posters = [r for r in poster_results if not r['success']]
    
    print(f"✅ Successful poster generations: {len(successful_posters)}")
    print(f"❌ Failed poster generations: {len(failed_posters)}")
    
    if successful_posters:
        print("\n🎨 Generated Posters:")
        for result in successful_posters:
            print(f"  • {result['name']}: {BASE_URL}{result['image_url']}")
    
    if failed_posters:
        print("\n❌ Failed Generations:")
        for result in failed_posters:
            print(f"  • {result['name']}: {result.get('error', 'Unknown error')}")
    
    print(f"\n🗂️  Check the 'generated_posters' folder for your poster files!")
    print(f"📖 View API documentation at: {BASE_URL}/docs")
    print(f"🏥 View health check at: {BASE_URL}/health")

if __name__ == "__main__":
    main()
