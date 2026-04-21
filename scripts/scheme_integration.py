"""
Sample integration showing how to use the scheme data with an LLM for RAG-based Q&A
This example uses the RAG pipeline to retrieve relevant schemes and format them for LLM consumption
"""

import json
from rag_pipeline import RAGPipeline

class SchemeExplainer:
    def __init__(self):
        self.rag = RAGPipeline()
        with open('../data/processed/schemes_cleaned.json', 'r') as f:
            self.all_schemes = json.load(f)
    
    def get_scheme_by_name(self, scheme_name):
        """Get full scheme details by name"""
        for scheme in self.all_schemes:
            if scheme['scheme_name'].lower() == scheme_name.lower():
                return scheme
        return None
    
    def search_schemes(self, query, n_results=3):
        """Search for relevant schemes using RAG"""
        results = self.rag.query(query, n_results=n_results)
        
        # Extract unique scheme names from results
        scheme_names = set()
        for metadata in results['metadatas'][0]:
            scheme_names.add(metadata['scheme_name'])
        
        # Get full details for each scheme
        relevant_schemes = []
        for name in scheme_names:
            scheme = self.get_scheme_by_name(name)
            if scheme:
                relevant_schemes.append(scheme)
        
        return relevant_schemes
    
    def format_for_llm(self, schemes):
        """Format scheme data for LLM context"""
        context = "Here are the relevant government schemes:\n\n"
        
        for i, scheme in enumerate(schemes, 1):
            context += f"{i}. {scheme['scheme_name']}\n"
            context += f"   Description: {scheme['description']}\n"
            context += f"   Benefits: {scheme['benefits']}\n"
            context += f"   Eligibility:\n"
            for key, value in scheme['eligibility'].items():
                if value:
                    context += f"      - {key.capitalize()}: {value}\n"
            context += f"   Required Documents: {', '.join(scheme['documents_required'])}\n"
            context += f"   More info: {scheme['source_url']}\n\n"
        
        return context
    
    def check_eligibility(self, scheme_name, user_profile):
        """
        Check if user is eligible for a scheme
        user_profile = {
            'age': 25,
            'gender': 'Female',
            'occupation': 'Student',
            'income': 200000,
            'category': 'General'
        }
        """
        scheme = self.get_scheme_by_name(scheme_name)
        if not scheme:
            return {"eligible": False, "reason": "Scheme not found"}
        
        eligibility = scheme['eligibility']
        reasons = []
        
        # Check age
        if eligibility.get('age'):
            age_str = eligibility['age']
            if '-' in age_str:
                min_age, max_age = map(lambda x: int(x.split()[0]), age_str.split('-'))
                if not (min_age <= user_profile.get('age', 0) <= max_age):
                    reasons.append(f"Age must be between {min_age} and {max_age}")
        
        # Check gender
        if eligibility.get('gender') and eligibility['gender'] != 'All':
            if user_profile.get('gender') != eligibility['gender']:
                reasons.append(f"Only for {eligibility['gender']}")
        
        # Check occupation
        if eligibility.get('occupation'):
            if user_profile.get('occupation', '').lower() not in eligibility['occupation'].lower():
                if eligibility['occupation'] != 'All':
                    reasons.append(f"Only for {eligibility['occupation']}")
        
        if reasons:
            return {"eligible": False, "reasons": reasons}
        else:
            return {"eligible": True, "scheme": scheme}

# Example usage
if __name__ == "__main__":
    explainer = SchemeExplainer()
    
    print("="*80)
    print("EXAMPLE 1: Search for farmer schemes")
    print("="*80)
    
    query = "What schemes are available for farmers?"
    schemes = explainer.search_schemes(query, n_results=3)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(schemes)} relevant schemes:\n")
    
    for scheme in schemes:
        print(f"• {scheme['scheme_name']}")
    
    # Format for LLM
    llm_context = explainer.format_for_llm(schemes)
    print("\n" + "="*80)
    print("LLM CONTEXT (to be sent with user query):")
    print("="*80)
    print(llm_context)
    
    print("\n" + "="*80)
    print("EXAMPLE 2: Check eligibility")
    print("="*80)
    
    user_profile = {
        'age': 25,
        'gender': 'Female',
        'occupation': 'Student',
        'income': 200000,
        'category': 'General'
    }
    
    scheme_name = "AICTE Pragati Scholarship for Girls"
    result = explainer.check_eligibility(scheme_name, user_profile)
    
    print(f"\nUser Profile: {user_profile}")
    print(f"Checking eligibility for: {scheme_name}")
    print(f"Eligible: {result['eligible']}")
    
    if result['eligible']:
        print(f"\n✅ User is eligible for this scheme!")
        print(f"Required documents: {', '.join(result['scheme']['documents_required'])}")
    else:
        print(f"\n❌ User is not eligible")
        print(f"Reasons: {', '.join(result.get('reasons', ['Unknown']))}")
    
    print("\n" + "="*80)
    print("EXAMPLE 3: Integration with LLM (pseudo-code)")
    print("="*80)
    
    print("""
# Pseudo-code for LLM integration:

from groq import Groq
from scheme_integration import SchemeExplainer

client = Groq(api_key="your-api-key")
explainer = SchemeExplainer()

user_query = "I am a farmer looking for financial support schemes"

# 1. Search relevant schemes
schemes = explainer.search_schemes(user_query, n_results=3)

# 2. Format context for LLM
context = explainer.format_for_llm(schemes)

# 3. Send to LLM
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful assistant explaining Indian government schemes. Use this context:\\n\\n{context}"
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
)

print(response.choices[0].message.content)
    """)
