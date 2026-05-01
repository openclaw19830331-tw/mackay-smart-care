#!/bin/bash
echo "Starting build process..."

echo "Generating site content..."
node scripts/generate_site.js

echo "Fetching trends..."
python3 /home/hermes/fetch_care_trends.py

echo "Build complete."
