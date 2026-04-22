#!/bin/bash

set -e

echo "🚀 Automated Vercel Deployment"
echo "=============================="
echo ""

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm i -g vercel
fi

# Check if logged in
echo "📝 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel:"
    vercel login
fi

echo ""
echo "✅ Authenticated as: $(vercel whoami)"
echo ""

# Deploy Backend (API)
echo "🔧 Step 1/2: Deploying Backend API..."
echo "─────────────────────────────────────"
vercel --prod --yes

echo ""
echo "✅ Backend deployed!"
echo ""
echo "📋 Copy your backend URL from above and paste it when prompted."
echo ""
read -p "Enter Backend URL (e.g., https://your-project.vercel.app): " BACKEND_URL

# Deploy Frontend
echo ""
echo "🎨 Step 2/2: Deploying Frontend..."
echo "─────────────────────────────────────"
cd frontend

# Create .env for build
echo "VITE_API_URL=$BACKEND_URL" > .env

# Deploy frontend
vercel --prod --yes

cd ..

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  🎉 DEPLOYMENT COMPLETE! 🎉              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🔧 Backend API:  $BACKEND_URL"
echo "🎨 Frontend App: Check the URL above"
echo ""
echo "✅ Your app is now live!"
echo ""
echo "⚠️  Important: Set VITE_API_URL in Vercel dashboard:"
echo "   1. Go to your frontend project on vercel.com"
echo "   2. Settings → Environment Variables"
echo "   3. Add: VITE_API_URL = $BACKEND_URL"
echo "   4. Redeploy if needed"
echo ""
