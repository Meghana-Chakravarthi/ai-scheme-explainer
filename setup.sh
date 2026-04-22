#!/bin/bash

echo "🚀 AI Scheme Explainer - Quick Start"
echo "===================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo ""

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Create frontend/.env file with:"
echo "   VITE_API_URL=http://localhost:3001"
echo ""
echo "2. Start development server:"
echo "   npm run dev:frontend"
echo ""
echo "3. Open browser at: http://localhost:3000"
echo ""
echo "📚 For deployment instructions, see DEPLOYMENT.md"
