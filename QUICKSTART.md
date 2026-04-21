# Quick Start Guide - Data Pipeline

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd scripts
pip3 install --break-system-packages requests beautifulsoup4 lxml chromadb sentence-transformers
```

### Step 2: Run the Pipeline

```bash
bash run_pipeline.sh
```

This will:
- ✅ Scrape 20 government schemes
- ✅ Clean and validate data
- ✅ Generate embeddings
- ✅ Create SQLite database

### Step 3: View the Data

```bash
# View all schemes
python3 view_dataset.py

# View specific scheme
python3 view_dataset.py 1
```

### Step 4: Query with RAG

```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
results = rag.query("schemes for farmers", n_results=3)
print(results)
```

## 📊 Output Files

After running the pipeline, you'll have:

```
data/
├── raw/
│   ├── myscheme_raw.json          # 12 schemes from MyScheme
│   └── indiagov_raw.json          # 8 schemes from India.gov.in
├── processed/
│   └── schemes_cleaned.json       # 20 cleaned & validated schemes
├── embeddings/
│   └── chromadb/                  # Vector database (60 chunks)
└── schemes.db                     # SQLite database
```

## 🔍 Sample Queries

```python
# Health schemes
rag.query("health insurance for poor families")

# Education schemes
rag.query("scholarships for girl students")

# Farmer schemes
rag.query("crop insurance and financial support")

# Pension schemes
rag.query("pension for unorganized workers")
```

## 📈 Dataset Stats

- **Total Schemes**: 20
- **Data Sources**: 2 (MyScheme, India.gov.in)
- **Validation**: 100% pass rate
- **Embeddings**: 60 semantic chunks
- **Storage**: JSON + SQLite + ChromaDB

## 🛠️ Troubleshooting

**Issue**: Module not found
```bash
pip3 install --break-system-packages <module-name>
```

**Issue**: Permission denied on run_pipeline.sh
```bash
chmod +x run_pipeline.sh
```

**Issue**: ChromaDB download slow
- First run downloads ~80MB model
- Subsequent runs use cached model

## 📚 Next Steps

1. **Integrate with LLM**: Use with Groq/OpenAI for scheme explanations
2. **Build API**: Create FastAPI endpoints for queries
3. **Add UI**: Build Streamlit interface
4. **Expand Data**: Add more sources and schemes

## 🎯 Use Cases

- ✅ RAG-based chatbot for scheme information
- ✅ Eligibility verification system
- ✅ Scheme recommendation engine
- ✅ Government portal search enhancement
- ✅ Multilingual scheme explainer

---

**Need Help?** Check `DATA_PIPELINE_README.md` for detailed documentation.
