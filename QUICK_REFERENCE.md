# 🚀 Quick Reference Guide

## Essential Commands

### Run Complete Pipeline
```bash
cd /home/dt-nyx/ai-scheme-explainer/scripts
bash run_pipeline.sh
```

### View Dataset
```bash
# View all schemes
python3 view_dataset.py

# View specific scheme (e.g., scheme #1)
python3 view_dataset.py 1
```

### Test Individual Components
```bash
# Scrape data
python3 scraper_myscheme.py
python3 scraper_indiagov.py

# Clean data
python3 data_cleaner.py

# Validate data
python3 validator.py

# Setup RAG
python3 rag_pipeline.py

# Store in database
python3 database_storage.py

# Test integration
python3 scheme_integration.py
```

## Key Files

### Main Dataset
```
data/processed/schemes_cleaned.json
```

### Database
```
data/schemes.db
```

### Vector Store
```
data/embeddings/chromadb/
```

## Python Usage Examples

### Query with RAG
```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
results = rag.query("schemes for farmers", n_results=3)
print(results)
```

### Check Eligibility
```python
from scheme_integration import SchemeExplainer

explainer = SchemeExplainer()
user_profile = {
    'age': 25,
    'gender': 'Female',
    'occupation': 'Student',
    'income': 200000
}
result = explainer.check_eligibility("AICTE Pragati Scholarship for Girls", user_profile)
print(result)
```

### Search Schemes
```python
from scheme_integration import SchemeExplainer

explainer = SchemeExplainer()
schemes = explainer.search_schemes("health insurance", n_results=3)
for scheme in schemes:
    print(scheme['scheme_name'])
```

### Query Database
```python
from database_storage import DatabaseStorage

db = DatabaseStorage()
schemes = db.query_schemes({'occupation': 'Farmer'})
print(f"Found {len(schemes)} schemes for farmers")
db.close()
```

## Documentation Files

- **DATA_PIPELINE_README.md** - Full technical documentation
- **QUICKSTART.md** - 5-minute setup guide
- **PIPELINE_SUMMARY.md** - Implementation summary
- **EXECUTION_LOG.md** - Pipeline execution log
- **IMPLEMENTATION_COMPLETE.md** - Final summary
- **PROJECT_STRUCTURE.txt** - File structure overview

## Installation

```bash
pip3 install --break-system-packages requests beautifulsoup4 lxml chromadb sentence-transformers
```

## Troubleshooting

### Module not found
```bash
pip3 install --break-system-packages <module-name>
```

### Permission denied
```bash
chmod +x run_pipeline.sh
```

### ChromaDB slow download
First run downloads ~80MB model. Subsequent runs use cached model.

## Dataset Statistics

- Total Schemes: 20
- Data Sources: 2
- Validation: 100% pass
- Embeddings: 60 chunks
- Query Time: <100ms

## Support

Check the documentation files for detailed information or examine the code comments.
