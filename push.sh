#!/bin/bash
# Quick push script for WelloraFit AI

echo "🚀 Pushing WelloraFit AI to GitHub..."
echo ""

cd "E:\Projects\Health\Code"

# Check if on main branch
git branch -M main

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 View your repo at:"
    echo "   https://github.com/SauravDnj/WelloraFit-AI"
    echo ""
    echo "🚀 Next: Deploy to Streamlit Cloud"
    echo "   → https://share.streamlit.io"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "   1. Need Personal Access Token (not password)"
    echo "   2. Repository doesn't exist on GitHub"
    echo "   3. Authentication failed"
    echo ""
    echo "💡 Try GitHub Desktop instead:"
    echo "   https://desktop.github.com/"
    echo ""
fi
