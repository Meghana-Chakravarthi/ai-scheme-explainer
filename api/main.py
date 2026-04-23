from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load schemes
SCHEMES_FILE = os.path.join(os.path.dirname(__file__), 'schemes_cleaned.json')
with open(SCHEMES_FILE, 'r', encoding='utf-8') as f:
    SCHEMES = json.load(f)

# Abbreviation map
ABBREVIATIONS = {
    'pmay': 'Pradhan Mantri Awas Yojana',
    'pm-kisan': 'PM Kisan Samman Nidhi',
    'pmkisan': 'PM Kisan Samman Nidhi',
    'pmjay': 'Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana',
    'ayushman': 'Ayushman Bharat',
    'nsp': 'National Scholarship Portal',
    'ssy': 'Sukanya Samriddhi Yojana',
    'pmuy': 'PM Ujjwala Yojana',
    'sui': 'Stand Up India',
    'pmmy': 'Pradhan Mantri Mudra Yojana',
    'apy': 'Atal Pension Yojana',
    'pmfby': 'PM Fasal Bima Yojana',
    'pmgkay': 'Pradhan Mantri Garib Kalyan Anna Yojana',
    'sbm': 'Swachh Bharat Mission',
    'bbbp': 'Beti Bachao Beti Padhao',
    'naps': 'National Apprenticeship Promotion Scheme',
    'pmsvanidhi': 'PM SVANidhi'
}

def normalize_name(name: str) -> str:
    return name.lower().strip().replace('-', '').replace(' ', '')

def find_scheme(query: str):
    query_norm = normalize_name(query)
    
    # Check abbreviations first
    if query_norm in ABBREVIATIONS:
        query = ABBREVIATIONS[query_norm]
        query_norm = normalize_name(query)
    
    # Find matching scheme
    for scheme in SCHEMES:
        scheme_norm = normalize_name(scheme['scheme_name'])
        if query_norm in scheme_norm or scheme_norm in query_norm:
            return scheme
    return None

def format_eligibility(elig):
    if isinstance(elig, str):
        return elig
    parts = []
    if elig.get('age'): parts.append(f"Age: {elig['age']}")
    if elig.get('income'): parts.append(f"Income: {elig['income']}")
    if elig.get('gender'): parts.append(f"Gender: {elig['gender']}")
    if elig.get('category'): parts.append(f"Category: {elig['category']}")
    if elig.get('occupation'): parts.append(f"Occupation: {elig['occupation']}")
    if elig.get('state'): parts.append(f"State: {elig['state']}")
    return '. '.join(parts) + '.'

def generate_explanation(scheme, simplify=False, language='en'):
    summary = scheme['description']
    eligibility = format_eligibility(scheme['eligibility'])
    benefits = scheme['benefits']
    docs = ', '.join(scheme.get('documents_required', []))
    url = scheme.get('source_url', 'government portal')
    
    if simplify:
        summary = summary.split('.')[0] + '.'
        eligibility = eligibility.split('.')[0] + '.'
        benefits = benefits.split('.')[0] + '.'
    
    process = f"Visit {url}. Required documents: {docs}. Apply online or at Common Service Center."
    
    result = {
        'summary': summary,
        'eligibility': eligibility,
        'benefits': benefits,
        'process': process,
        'scheme_name': scheme['scheme_name'],
        'source_url': scheme.get('source_url', '')
    }
    
    return result

# Models
class ExplainRequest(BaseModel):
    scheme_name: str
    simplification_level: Optional[str] = 'standard'
    language: Optional[str] = 'en'

class EligibilityRequest(BaseModel):
    age: int
    income: int
    gender: str
    category: str
    state: str
    occupation: str

class CompareRequest(BaseModel):
    scheme1: str
    scheme2: str

# Endpoints
@app.get("/api/schemes")
def get_all_schemes():
    return {
        'schemes': [
            {
                'name': s['scheme_name'],
                'description': s['description'][:100] + '...',
                'target': s['eligibility'].get('occupation', 'general') if isinstance(s['eligibility'], dict) else 'general'
            }
            for s in SCHEMES
        ],
        'total': len(SCHEMES)
    }

@app.get("/api/scheme/{name}")
def get_scheme(name: str):
    scheme = find_scheme(name)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@app.post("/api/explain")
def explain_scheme(req: ExplainRequest):
    scheme = find_scheme(req.scheme_name)
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme '{req.scheme_name}' not found")
    
    simplify = req.simplification_level == 'simple'
    return generate_explanation(scheme, simplify, req.language)

@app.post("/api/check-eligibility")
def check_eligibility(req: EligibilityRequest):
    eligible = []
    not_eligible = []
    
    for scheme in SCHEMES:
        elig = scheme['eligibility']
        if not isinstance(elig, dict):
            continue
        
        is_eligible = True
        reasons = []
        
        # Check age
        if elig.get('age'):
            age_str = str(elig['age']).lower()
            if 'all' not in age_str and '-' in age_str:
                try:
                    # Remove text like "years", "(girl child)", etc
                    age_range = age_str.split('(')[0].replace('years', '').replace('year', '').strip()
                    min_age, max_age = map(int, age_range.split('-'))
                    if not (min_age <= req.age <= max_age):
                        is_eligible = False
                        reasons.append(f"Age must be {elig['age']}")
                except (ValueError, IndexError):
                    pass  # Skip if age format is invalid
        
        # Check income
        if elig.get('income') and 'Below' in str(elig['income']):
            try:
                max_income = int(''.join(filter(str.isdigit, elig['income'])))
                if req.income > max_income:
                    is_eligible = False
                    reasons.append(f"Income must be below ₹{max_income}")
            except:
                pass
        
        # Check occupation
        if elig.get('occupation') and elig['occupation'] != 'All':
            if req.occupation.lower() not in elig['occupation'].lower():
                is_eligible = False
                reasons.append(f"Must be {elig['occupation']}")
        
        # Check state
        if elig.get('state') and elig['state'] != 'All India':
            if req.state not in elig['state']:
                is_eligible = False
                reasons.append(f"Only for {elig['state']}")
        
        scheme_info = {
            'name': scheme['scheme_name'],
            'description': scheme['description'],
            'benefits': scheme['benefits'],
            'documents': scheme.get('documents_required', []),
            'reasons': reasons
        }
        
        if is_eligible:
            eligible.append(scheme_info)
        else:
            not_eligible.append(scheme_info)
    
    return {
        'eligible': eligible,
        'not_eligible': not_eligible,
        'total_eligible': len(eligible)
    }

@app.post("/api/compare")
def compare_schemes(req: CompareRequest):
    scheme1 = find_scheme(req.scheme1)
    scheme2 = find_scheme(req.scheme2)
    
    if not scheme1:
        raise HTTPException(status_code=404, detail=f"Scheme '{req.scheme1}' not found")
    if not scheme2:
        raise HTTPException(status_code=404, detail=f"Scheme '{req.scheme2}' not found")
    
    return {
        'scheme1': {
            'name': scheme1['scheme_name'],
            'description': scheme1['description'],
            'eligibility': format_eligibility(scheme1['eligibility']),
            'benefits': scheme1['benefits'],
            'documents': scheme1.get('documents_required', []),
            'url': scheme1.get('source_url', '')
        },
        'scheme2': {
            'name': scheme2['scheme_name'],
            'description': scheme2['description'],
            'eligibility': format_eligibility(scheme2['eligibility']),
            'benefits': scheme2['benefits'],
            'documents': scheme2.get('documents_required', []),
            'url': scheme2.get('source_url', '')
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
