#!/usr/bin/env python3
"""
Test script for Wikipedia.org redesign
"""

import json
import requests
import sys

def test_wikipedia_redesign():
    """Test the redesign API with wikipedia.org"""
    
    url = "http://localhost:8000/api/redesign"
    payload = {
        "url": "https://www.wikipedia.org",
        "style_preferences": {
            "theme": "modern",
            "colors": "vibrant"
        }
    }
    
    print("🚀 Testing Wikipedia.org Redesign API")
    print(f"📍 Endpoint: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    print("\n⏳ Sending request (this may take 1-2 minutes)...\n")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        
        if response.status_code == 200:
            print("✅ SUCCESS! Redesign completed.")
            data = response.json()
            
            print("\n" + "="*60)
            print("📊 RESPONSE SUMMARY")
            print("="*60)
            print(f"Original URL: {data['original_url']}")
            print(f"Screenshot Size: {len(data['original_screenshot'])} bytes (base64)")
            print(f"\n📝 Design Analysis:")
            print(json.dumps(data['analysis'], indent=2))
            print(f"\n💻 TSX Code Length: {len(data['tsx_code'])} characters")
            print(f"\n🎨 TSX Code Preview (first 500 chars):")
            print("-" * 60)
            print(data['tsx_code'][:500])
            print("-" * 60)
            
            # Save full response to file
            with open('wikipedia_redesign_result.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n💾 Full response saved to: wikipedia_redesign_result.json")
            
            # Save TSX code separately
            with open('wikipedia_redesign.tsx', 'w') as f:
                f.write(data['tsx_code'])
            print(f"💾 TSX code saved to: wikipedia_redesign.tsx")
            
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 5 minutes")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_wikipedia_redesign()
