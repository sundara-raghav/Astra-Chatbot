import google.generativeai as genai
import sys

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyC6a1bunkC6P8cTFYva3FIBVi-xspXhnms"

def list_available_models(api_key=None):
    if api_key:
        genai.configure(api_key=api_key)
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        
    try:
        print("Fetching available models...")
        models = genai.list_models()
        
        # Group models by type
        model_groups = {
            "gemini-1.5": [],
            "gemini-2.0": [],
            "gemini-2.5": [],
            "embedding": [],
            "other": []
        }
        
        for model in models:
            name = model.name
            if "gemini-1.5" in name:
                model_groups["gemini-1.5"].append(model)
            elif "gemini-2.0" in name:
                model_groups["gemini-2.0"].append(model)
            elif "gemini-2.5" in name:
                model_groups["gemini-2.5"].append(model)
            elif "embedding" in name:
                model_groups["embedding"].append(model)
            else:
                model_groups["other"].append(model)
        
        # Print models by group
        print("\n=== AVAILABLE MODELS ===")
        for group_name, group_models in model_groups.items():
            if group_models:
                print(f"\n## {group_name.upper()} MODELS:")
                for model in group_models:
                    print(f"- {model.name}")
                    print(f"  Supported methods: {', '.join(model.supported_generation_methods)}")
        
        # Print recommended models for chat
        print("\n=== RECOMMENDED MODELS FOR CHAT ===")
        print("These models are recommended for use in the chat application:")
        
        recommended = []
        for model in models:
            if "generateContent" in model.supported_generation_methods and "gemini" in model.name:
                if "flash" in model.name:  # Flash models typically have higher quotas
                    recommended.append((model.name, "⭐⭐⭐ (Higher quota limit)"))
                else:
                    recommended.append((model.name, "⭐⭐ (Standard)"))
        
        # Sort by rating (more stars first)
        recommended.sort(key=lambda x: x[1], reverse=True)
        
        for name, rating in recommended[:5]:  # Show top 5
            print(f"- {name} {rating}")
        
        print("\n=== QUOTA INFORMATION ===")
        print("Free tier limits for Gemini API:")
        print("- Limited number of requests per minute")
        print("- Limited total requests per day")
        print("- 'Flash' models typically have higher quota limits than 'Pro' models")
        print("\nIf you encounter quota errors:")
        print("1. Try using a 'Flash' model instead of a 'Pro' model")
        print("2. Wait a few minutes before trying again")
        print("3. Get your own API key from Google AI Studio (https://ai.google.dev/)")
        
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        if "quota" in str(e).lower() or "429" in str(e).lower():
            print("\nYou've exceeded the API quota. Please try again later or use a different API key.")

if __name__ == "__main__":
    # Check if an API key was provided as a command-line argument
    if len(sys.argv) > 1:
        list_available_models(sys.argv[1])
    else:
        list_available_models()