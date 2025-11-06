#!/usr/bin/env python3
"""
Script to test OpenAI API connection and check quota status.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        print("💡 Make sure you have created a .env file with: OPENAI_API_KEY=your_key_here")
        exit(1)
    
    print("🔑 API Key found in .env file")
    print(f"   Key starts with: {api_key[:10]}...")
    print()
    
    # Initialize client
    client = OpenAI(api_key=api_key)
    
    print("🧪 Testing API connection...")
    print()
    
    # Try a simple API call
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API is working' if you can read this."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print("✅ SUCCESS: API is working!")
        print(f"   Response: {result}")
        print()
        print("✅ Your API quota is active and working!")
        print("   You can now use the docstring generator in the Streamlit app.")
        
    except Exception as e:
        error_msg = str(e)
        print("❌ ERROR: API call failed")
        print()
        
        if "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
            print("⚠️  QUOTA EXCEEDED")
            print("   Your OpenAI API quota has been exceeded.")
            print()
            print("💡 To fix this:")
            print("   1. Go to: https://platform.openai.com/account/billing")
            print("   2. Add a payment method")
            print("   3. Add credits to your account")
            print("   4. Check your usage limits")
            
        elif "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            print("⚠️  AUTHENTICATION ERROR")
            print("   Your API key is invalid or incorrect.")
            print()
            print("💡 To fix this:")
            print("   1. Check your API key in the .env file")
            print("   2. Get a new key from: https://platform.openai.com/api-keys")
            print("   3. Make sure the key starts with 'sk-'")
            
        elif "rate_limit" in error_msg.lower():
            print("⚠️  RATE LIMIT EXCEEDED")
            print("   You're making too many requests too quickly.")
            print()
            print("💡 To fix this:")
            print("   Wait a few minutes and try again.")
            
        else:
            print(f"⚠️  ERROR DETAILS:")
            print(f"   {error_msg}")
            print()
            print("💡 Check:")
            print("   - Your internet connection")
            print("   - OpenAI API status: https://status.openai.com/")
            print("   - Your API key is correct")
        
        exit(1)
        
except ImportError:
    print("❌ ERROR: OpenAI package not installed")
    print()
    print("💡 To fix this:")
    print("   pip3 install openai")
    exit(1)

except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

