#!/bin/bash

echo "Installing required packages..."
pip install -r requirements.txt

echo ""
echo "Choose an option:"
echo "1. Start Gemini Chat Application"
echo "2. Check Available Models"
echo "3. Check Models with Custom API Key"
echo ""
read -p "Enter option (1, 2, or 3): " option

if [ "$option" = "1" ]; then
    echo "Starting Gemini Chat Application..."
    python app.py
elif [ "$option" = "2" ]; then
    echo "Checking available models..."
    python check_models.py
    read -p "Press Enter to continue..."
elif [ "$option" = "3" ]; then
    echo ""
    read -p "Enter your Gemini API key: " api_key
    echo "Checking available models with your API key..."
    python check_models.py "$api_key"
    read -p "Press Enter to continue..."
else
    echo "Invalid option. Starting Gemini Chat Application by default..."
    python app.py
fi