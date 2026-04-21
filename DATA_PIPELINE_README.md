# Indian Government Schemes Data Pipeline

A complete, production-ready data pipeline for collecting, cleaning, structuring, and storing Indian government scheme data for RAG-based AI applications.

## Overview

This pipeline extracts scheme information from multiple government portals, cleans and structures the data, validates it, and prepares it for RAG (Retrieval-Augmented Generation) applications.

## Pipeline Architecture

```
Data Sources → Scrapers → Cleaner → Validator → Storage (JSON/SQLite) → RAG (ChromaDB)
```

## Features

- **Multi-source scraping**: MyScheme Portal, India.gov.in
- **Intelligent data cleaning**: Removes HTML noise, duplicates, and inconsistencies
- **Structured schema**: Consistent JSON format with eligibility criteria
- **Validation**: Ensures data quality and completeness
- **Dual storage**: JSON files and SQLite database
- **RAG-ready**: ChromaDB embeddings with semantic search
- **Production-ready**: Error handling, logging, and scalability

## Dataset Schema

```json
{
  "scheme_name": "PM Kisan Samman Nidhi",
  "description": "Income support scheme for farmers...",
  "benefits": "₹6000 per year in three installments...",
  "eligibility": {
    "age": "18-100 years",
    "income": "Landholding farmers",
    "gender": "All",
    "category": "General",
    "state": "All India",
    "occupation": "Farmer"
  },
  "documents_required": [
    "Aadhaar Card",
    "Bank Account Details",
    "Land Ownership Documents"
  ],
  "source_url": "https://pmkisan.gov.in"
}
```

## Directory Structure

```
ai-scheme-explainer/
├── data/
│   ├── raw/                          # Raw scraped data
│   │   ├── myscheme_raw.json
│   │   └── indiagov_raw.json
│   ├── processed/                    # Cleaned and validated data
│   │   └── schemes_cleaned.json
│   ├── embeddings/                   # Vector embeddings
│   │   └── chromadb/
│   └── schemes.db                    # SQLite database
├── scripts/
│   ├── scraper_myscheme.py          # MyScheme portal scraper
│   ├── scraper_indiagov.py          # India.gov.in scraper
│   ├── data_cleaner.py              # Data cleaning and merging
│   ├── validator.py                 # Data validation
│   ├── rag_pipeline.py              # RAG setup with ChromaDB
│   ├── database_storage.py          # SQLite storage
│   ├── run_pipeline.sh              # Complete pipeline execution
│   └── requirements.txt             # Python dependencies
└── DATA_PIPELINE_README.md          # This file
```

## Installation

```bash
cd scripts
pip install -r requirements.txt
```

## Usage

### Run Complete Pipeline

```bash
cd scripts
bash run_pipeline.sh
```

### Run Individual Components

**1. Scrape Data**
```bash
python3 scraper_myscheme.py
python3 scraper_indiagov.py
```

**2. Clean Data**
```bash
python3 data_cleaner.py
```

**3. Validate Data**
```bash
python3 validator.py
```

**4. Setup RAG**
```bash
python3 rag_pipeline.py
```

**5. Store in Database**
```bash
python3 database_storage.py
```

## Data Sources

### 1. MyScheme Portal
- **URL**: https://www.myscheme.gov.in
- **Schemes**: 12 major central government schemes
- **Coverage**: PM Kisan, Ayushman Bharat, PMAY, NSP, etc.

### 2. India.gov.in
- **URL**: https://www.india.gov.in
- **Schemes**: 8 additional welfare schemes
- **Coverage**: MGNREGA, Atal Pension, PMKVY, etc.

## Current Dataset Statistics

- **Total Schemes**: 20
- **Categories**: Farmer, Student, Worker, Women, General
- **States**: All India coverage
- **Validation**: 100% pass rate
- **Embeddings**: 60 semantic chunks

## Schemes Included

### Farmer Schemes
- PM Kisan Samman Nidhi
- Pradhan Mantri Fasal Bima Yojana

### Health & Insurance
- Ayushman Bharat (PM-JAY)
- PM Jeevan Jyoti Bima Yojana
- PM Suraksha Bima Yojana

### Housing
- Pradhan Mantri Awas Yojana

### Education
- National Scholarship Portal
- AICTE Pragati Scholarship for Girls

### Women Empowerment
- Sukanya Samriddhi Yojana
- PM Ujjwala Yojana
- Stand Up India Scheme
- Beti Bachao Beti Padhao
- PM Matru Vandana Yojana

### Employment & Skills
- MGNREGA
- e-Shram Portal
- PM Kaushal Vikas Yojana

### Pension
- PM Shram Yogi Maandhan
- Atal Pension Yojana

### Business & Entrepreneurship
- PM Mudra Yojana
- Stand Up India

### Sanitation
- Swachh Bharat Mission

## RAG Integration

### ChromaDB Setup

The pipeline automatically:
1. Chunks scheme data into semantic units (overview, eligibility, documents)
2. Generates embeddings using `all-MiniLM-L6-v2` model
3. Stores in ChromaDB for fast semantic search
4. Enables retrieval for LLM queries

### Query Examples

```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
results = rag.query("What schemes are available for farmers?", n_results=5)
```

### Sample Queries Tested

- "What schemes are available for farmers?"
- "Health insurance schemes for poor families"
- "Education scholarships for girl students"
- "Pension schemes for workers"

## Database Schema (SQLite)

### Tables

**schemes**
- id (PRIMARY KEY)
- scheme_name (UNIQUE)
- description
- benefits
- source_url
- created_at

**eligibility**
- id (PRIMARY KEY)
- scheme_id (FOREIGN KEY)
- age, income, gender, category, state, occupation

**documents**
- id (PRIMARY KEY)
- scheme_id (FOREIGN KEY)
- document_name

### Query Example

```python
from database_storage import DatabaseStorage

db = DatabaseStorage()
schemes = db.query_schemes({'occupation': 'Farmer', 'gender': 'Female'})
```

## Data Quality

### Validation Checks

✅ Required fields present  
✅ No missing data  
✅ Consistent schema  
✅ Clean readable text  
✅ No HTML artifacts  
✅ No duplicate schemes  
✅ Valid eligibility structure  
✅ Document lists populated  

### Cleaning Process

1. **Text Normalization**: Remove extra whitespace, special characters
2. **Deduplication**: Remove duplicate schemes by normalized name
3. **Field Extraction**: Parse eligibility criteria into structured fields
4. **Validation**: Ensure all required fields are present and valid

## Extending the Pipeline

### Add New Data Source

1. Create new scraper: `scraper_newsource.py`
2. Follow the schema format
3. Add to `data_cleaner.py` input files
4. Run pipeline

### Add New Fields

1. Update schema in scrapers
2. Modify `data_cleaner.py` to handle new fields
3. Update `validator.py` validation rules
4. Update database schema if using SQLite

## Performance

- **Scraping**: ~2-3 seconds per source
- **Cleaning**: <1 second for 20 schemes
- **Validation**: <1 second
- **Embedding Generation**: ~20 seconds (first run with model download)
- **Database Storage**: <1 second

## Error Handling

- Network timeouts: Retry logic with exponential backoff
- Missing fields: Logged as warnings, scheme skipped if critical
- Duplicate schemes: Automatically deduplicated
- Invalid data: Validation errors logged with scheme name

## Production Considerations

### Scalability
- Batch processing for large datasets
- Async scraping for multiple sources
- Incremental updates (only new/changed schemes)

### Monitoring
- Log all scraping activities
- Track validation pass/fail rates
- Monitor embedding generation time

### Maintenance
- Regular updates from source portals
- Schema version control
- Data backup and recovery

## API Integration

The cleaned data can be integrated with:

- **FastAPI/Flask**: REST API for scheme queries
- **LangChain**: RAG chains for conversational AI
- **Streamlit**: Interactive web interface
- **Telegram/WhatsApp Bots**: Scheme information delivery

## Future Enhancements

- [ ] Add more data sources (state government portals)
- [ ] Implement incremental updates
- [ ] Add multilingual support (Hindi, regional languages)
- [ ] Create API endpoints for real-time queries
- [ ] Add scheme comparison features
- [ ] Implement user feedback loop for data quality

## License

MIT License

## Contributing

1. Fork the repository
2. Create feature branch
3. Add new scrapers or improve existing ones
4. Submit pull request

## Support

For issues or questions:
- Open GitHub issue
- Check validation logs in console output
- Review data quality in `schemes_cleaned.json`

---

**Last Updated**: April 2026  
**Dataset Version**: 1.0  
**Total Schemes**: 20  
**Coverage**: All India
