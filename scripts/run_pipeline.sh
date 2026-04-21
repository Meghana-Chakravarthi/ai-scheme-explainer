#!/bin/bash

echo "=========================================="
echo "Indian Government Schemes Data Pipeline"
echo "=========================================="
echo ""

# Step 1: Install dependencies
echo "Step 1: Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 2: Scrape MyScheme Portal
echo "Step 2: Scraping MyScheme Portal..."
python scraper_myscheme.py
echo "✅ MyScheme data scraped"
echo ""

# Step 3: Scrape India.gov.in
echo "Step 3: Scraping India.gov.in..."
python scraper_indiagov.py
echo "✅ India.gov.in data scraped"
echo ""

# Step 4: Clean and merge data
echo "Step 4: Cleaning and merging data..."
python data_cleaner.py
echo "✅ Data cleaned and merged"
echo ""

# Step 5: Validate data
echo "Step 5: Validating data..."
python validator.py
echo "✅ Data validated"
echo ""

# Step 6: Generate embeddings and setup RAG
echo "Step 6: Setting up RAG pipeline..."
python rag_pipeline.py
echo "✅ RAG pipeline ready"
echo ""

echo "=========================================="
echo "Pipeline execution completed!"
echo "=========================================="
echo ""
echo "Output files:"
echo "  - data/raw/myscheme_raw.json"
echo "  - data/raw/indiagov_raw.json"
echo "  - data/processed/schemes_cleaned.json"
echo "  - data/embeddings/chromadb/"
echo ""
