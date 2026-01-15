"""
Time Travel Chat - Redirect Module
"""
from agents.time_travel import run_time_travel

if __name__ == "__main__":
    import os
    import google.generativeai as genai
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Please set the GEMINI_API_KEY environment variable")
        exit(1)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    run_time_travel(model)
