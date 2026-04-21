import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os

class RAGPipeline:
    def __init__(self, collection_name="indian_schemes"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="../data/embeddings/chromadb")
        
        # Delete existing collection if exists
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Initialized ChromaDB collection: {collection_name}")

    def chunk_scheme_data(self, scheme):
        chunks = []
        
        # Main description chunk
        main_chunk = f"""
Scheme: {scheme['scheme_name']}
Description: {scheme['description']}
Benefits: {scheme['benefits']}
""".strip()
        chunks.append({
            "text": main_chunk,
            "type": "overview",
            "scheme_name": scheme['scheme_name']
        })
        
        # Eligibility chunk
        eligibility = scheme['eligibility']
        eligibility_text = f"""
Scheme: {scheme['scheme_name']}
Eligibility Criteria:
- Age: {eligibility.get('age', 'Not specified')}
- Income: {eligibility.get('income', 'Not specified')}
- Gender: {eligibility.get('gender', 'All')}
- Category: {eligibility.get('category', 'General')}
- State: {eligibility.get('state', 'All India')}
- Occupation: {eligibility.get('occupation', 'Not specified')}
""".strip()
        chunks.append({
            "text": eligibility_text,
            "type": "eligibility",
            "scheme_name": scheme['scheme_name']
        })
        
        # Documents chunk
        if scheme.get('documents_required'):
            docs_text = f"""
Scheme: {scheme['scheme_name']}
Required Documents:
{chr(10).join(f"- {doc}" for doc in scheme['documents_required'])}
""".strip()
            chunks.append({
                "text": docs_text,
                "type": "documents",
                "scheme_name": scheme['scheme_name']
            })
        
        return chunks

    def generate_embeddings(self, schemes_file):
        with open(schemes_file, 'r', encoding='utf-8') as f:
            schemes = json.load(f)
        
        print(f"Processing {len(schemes)} schemes...")
        
        all_chunks = []
        for scheme in schemes:
            chunks = self.chunk_scheme_data(scheme)
            all_chunks.extend(chunks)
        
        print(f"Generated {len(all_chunks)} chunks")
        
        # Prepare data for ChromaDB
        documents = [chunk['text'] for chunk in all_chunks]
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]
        metadatas = [
            {
                "scheme_name": chunk['scheme_name'],
                "type": chunk['type']
            }
            for chunk in all_chunks
        ]
        
        # Add to ChromaDB in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            
            self.collection.add(
                documents=batch_docs,
                ids=batch_ids,
                metadatas=batch_meta
            )
            print(f"Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        
        print(f"Successfully stored {len(documents)} chunks in ChromaDB")

    def query(self, query_text, n_results=5):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return results

    def test_retrieval(self):
        test_queries = [
            "What schemes are available for farmers?",
            "Health insurance schemes for poor families",
            "Education scholarships for girl students",
            "Pension schemes for workers"
        ]
        
        print("\n=== Testing RAG Retrieval ===\n")
        for query in test_queries:
            print(f"Query: {query}")
            results = self.query(query, n_results=3)
            
            for i, doc in enumerate(results['documents'][0]):
                scheme_name = results['metadatas'][0][i]['scheme_name']
                print(f"\n  Result {i+1}: {scheme_name}")
                print(f"  {doc[:200]}...")
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    rag = RAGPipeline()
    
    schemes_file = '../data/processed/schemes_cleaned.json'
    
    print("Generating embeddings and storing in ChromaDB...")
    rag.generate_embeddings(schemes_file)
    
    print("\nTesting retrieval...")
    rag.test_retrieval()
    
    print("\nRAG pipeline setup complete!")
