#!/bin/bash
# Quick script to enable mock mode (bypasses rate limits for testing)

echo "Enabling mock mode in .env..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Add or update USE_MOCK_IMAGES
if grep -q "USE_MOCK_IMAGES" .env; then
    # Update existing line
    sed -i '' 's/USE_MOCK_IMAGES=.*/USE_MOCK_IMAGES=true/' .env
    echo "✅ Updated USE_MOCK_IMAGES=true"
else
    # Add new line
    echo "" >> .env
    echo "USE_MOCK_IMAGES=true" >> .env
    echo "✅ Added USE_MOCK_IMAGES=true"
fi

echo ""
echo "Mock mode enabled! This bypasses HERE API rate limits."
echo "The comparison will work but show a placeholder reference image."
echo ""
echo "To disable mock mode later, run:"
echo "  sed -i '' 's/USE_MOCK_IMAGES=true/USE_MOCK_IMAGES=false/' .env"
echo ""
echo "Now restart your backend:"
echo "  python3 -m uvicorn main:app --reload --port 8000"
