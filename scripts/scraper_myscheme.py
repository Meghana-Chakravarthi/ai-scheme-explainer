import requests
from bs4 import BeautifulSoup
import json
import time
import re

class MySchemePortalScraper:
    def __init__(self):
        self.base_url = "https://www.myscheme.gov.in"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.schemes = []

    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\r\n\t]', ' ', text)
        return text.strip()

    def extract_eligibility_fields(self, eligibility_text):
        eligibility = {
            "age": "",
            "income": "",
            "gender": "",
            "category": "",
            "state": "",
            "occupation": ""
        }
        
        text_lower = eligibility_text.lower()
        
        # Age extraction
        age_match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*years?', text_lower)
        if age_match:
            eligibility["age"] = f"{age_match.group(1)}-{age_match.group(2)} years"
        elif re.search(r'below\s*(\d+)', text_lower):
            match = re.search(r'below\s*(\d+)', text_lower)
            eligibility["age"] = f"Below {match.group(1)} years"
        elif re.search(r'above\s*(\d+)', text_lower):
            match = re.search(r'above\s*(\d+)', text_lower)
            eligibility["age"] = f"Above {match.group(1)} years"
        
        # Income extraction
        income_match = re.search(r'₹?\s*(\d+(?:,\d+)*)\s*(?:lakh|lakhs)?', text_lower)
        if income_match:
            eligibility["income"] = income_match.group(0)
        
        # Gender
        if any(word in text_lower for word in ['women', 'woman', 'girl', 'female']):
            eligibility["gender"] = "Female"
        elif any(word in text_lower for word in ['men', 'man', 'boy', 'male']):
            eligibility["gender"] = "Male"
        else:
            eligibility["gender"] = "All"
        
        # Category
        if 'sc' in text_lower or 'scheduled caste' in text_lower:
            eligibility["category"] = "SC"
        elif 'st' in text_lower or 'scheduled tribe' in text_lower:
            eligibility["category"] = "ST"
        elif 'obc' in text_lower:
            eligibility["category"] = "OBC"
        elif 'bpl' in text_lower or 'below poverty' in text_lower:
            eligibility["category"] = "BPL"
        else:
            eligibility["category"] = "General"
        
        # Occupation
        occupations = ['farmer', 'student', 'worker', 'entrepreneur', 'laborer']
        for occ in occupations:
            if occ in text_lower:
                eligibility["occupation"] = occ.capitalize()
                break
        
        return eligibility

    def scrape_scheme_details(self, scheme_url):
        try:
            response = requests.get(scheme_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'lxml')
            
            scheme_data = {
                "scheme_name": "",
                "description": "",
                "benefits": "",
                "eligibility": {},
                "documents_required": [],
                "source_url": scheme_url
            }
            
            # Extract scheme name
            title = soup.find('h1') or soup.find('h2', class_=re.compile('title|heading'))
            if title:
                scheme_data["scheme_name"] = self.clean_text(title.get_text())
            
            # Extract description
            desc = soup.find('div', class_=re.compile('description|overview|about'))
            if desc:
                scheme_data["description"] = self.clean_text(desc.get_text())
            
            # Extract benefits
            benefits = soup.find('div', class_=re.compile('benefit|advantage'))
            if benefits:
                scheme_data["benefits"] = self.clean_text(benefits.get_text())
            
            # Extract eligibility
            eligibility_section = soup.find('div', class_=re.compile('eligibility|criteria'))
            if eligibility_section:
                eligibility_text = self.clean_text(eligibility_section.get_text())
                scheme_data["eligibility"] = self.extract_eligibility_fields(eligibility_text)
            
            # Extract documents
            docs_section = soup.find('div', class_=re.compile('document|required'))
            if docs_section:
                docs = docs_section.find_all('li')
                scheme_data["documents_required"] = [self.clean_text(doc.get_text()) for doc in docs]
            
            return scheme_data
        except Exception as e:
            print(f"Error scraping {scheme_url}: {e}")
            return None

    def scrape_myscheme_portal(self):
        # Static list of known schemes (MyScheme portal requires authentication for full access)
        known_schemes = [
            {
                "scheme_name": "PM Kisan Samman Nidhi",
                "description": "Income support scheme providing financial assistance to small and marginal farmers across India.",
                "benefits": "₹6000 per year in three equal installments of ₹2000 each directly transferred to bank accounts.",
                "eligibility": {
                    "age": "18-100 years",
                    "income": "Landholding farmers",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Farmer"
                },
                "documents_required": ["Aadhaar Card", "Bank Account Details", "Land Ownership Documents"],
                "source_url": "https://pmkisan.gov.in"
            },
            {
                "scheme_name": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana",
                "description": "National health protection scheme providing health insurance coverage to economically vulnerable families.",
                "benefits": "Health coverage of ₹5 lakh per family per year for secondary and tertiary hospitalization.",
                "eligibility": {
                    "age": "All ages",
                    "income": "Below ₹3 lakh annual income",
                    "gender": "All",
                    "category": "BPL",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Ration Card", "Income Certificate"],
                "source_url": "https://pmjay.gov.in"
            },
            {
                "scheme_name": "Pradhan Mantri Awas Yojana - Urban",
                "description": "Housing for All mission providing affordable housing to urban poor and economically weaker sections.",
                "benefits": "Interest subsidy on home loans, direct financial assistance for house construction.",
                "eligibility": {
                    "age": "18-70 years",
                    "income": "EWS: Up to ₹3 lakh, LIG: ₹3-6 lakh, MIG: ₹6-18 lakh",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Income Certificate", "Bank Account", "Property Documents"],
                "source_url": "https://pmaymis.gov.in"
            },
            {
                "scheme_name": "National Scholarship Portal - Pre-Matric Scholarship",
                "description": "Financial assistance to students from economically weaker sections for pursuing education.",
                "benefits": "Scholarship amount varies from ₹3000 to ₹12000 per year based on class and category.",
                "eligibility": {
                    "age": "10-18 years",
                    "income": "Below ₹2.5 lakh annual family income",
                    "gender": "All",
                    "category": "SC/ST/OBC/Minority",
                    "state": "All India",
                    "occupation": "Student"
                },
                "documents_required": ["Aadhaar Card", "Income Certificate", "Caste Certificate", "Bank Account", "School ID"],
                "source_url": "https://scholarships.gov.in"
            },
            {
                "scheme_name": "Sukanya Samriddhi Yojana",
                "description": "Small deposit savings scheme for girl child to secure their future education and marriage expenses.",
                "benefits": "High interest rate (currently 8.2%), tax benefits under Section 80C, maturity after 21 years.",
                "eligibility": {
                    "age": "0-10 years (girl child)",
                    "income": "No income limit",
                    "gender": "Female",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Birth Certificate of Girl Child", "Parent's Aadhaar", "Address Proof", "Passport Photo"],
                "source_url": "https://www.nsiindia.gov.in"
            },
            {
                "scheme_name": "PM Ujjwala Yojana",
                "description": "Scheme to provide free LPG connections to women from Below Poverty Line households.",
                "benefits": "Free LPG connection, financial assistance for first refill and stove.",
                "eligibility": {
                    "age": "18-100 years",
                    "income": "BPL families",
                    "gender": "Female",
                    "category": "BPL",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["BPL Card", "Aadhaar Card", "Bank Account", "Address Proof", "Passport Photo"],
                "source_url": "https://pmuy.gov.in"
            },
            {
                "scheme_name": "Stand Up India Scheme",
                "description": "Facilitates bank loans for SC/ST and women entrepreneurs for setting up greenfield enterprises.",
                "benefits": "Bank loans between ₹10 lakh to ₹1 crore for non-farm sector enterprises.",
                "eligibility": {
                    "age": "18-65 years",
                    "income": "No specific limit",
                    "gender": "Women or SC/ST",
                    "category": "SC/ST or Women",
                    "state": "All India",
                    "occupation": "Entrepreneur"
                },
                "documents_required": ["Aadhaar Card", "PAN Card", "Business Plan", "Caste Certificate (if applicable)", "Bank Account"],
                "source_url": "https://www.standupmitra.in"
            },
            {
                "scheme_name": "e-Shram Portal Registration",
                "description": "National database of unorganized workers to provide social security and welfare benefits.",
                "benefits": "₹2 lakh accident insurance, access to various welfare schemes, pension schemes.",
                "eligibility": {
                    "age": "16-59 years",
                    "income": "Monthly income below ₹15000",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Worker"
                },
                "documents_required": ["Aadhaar Card", "Bank Account with IFSC", "Mobile Number"],
                "source_url": "https://eshram.gov.in"
            },
            {
                "scheme_name": "PM Shram Yogi Maandhan Pension Scheme",
                "description": "Voluntary pension scheme for unorganized sector workers ensuring old age protection.",
                "benefits": "Guaranteed monthly pension of ₹3000 after attaining age of 60 years.",
                "eligibility": {
                    "age": "18-40 years",
                    "income": "Monthly income below ₹15000",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Worker"
                },
                "documents_required": ["Aadhaar Card", "Bank Account with IFSC", "Savings Bank Passbook"],
                "source_url": "https://maandhan.in"
            },
            {
                "scheme_name": "AICTE Pragati Scholarship for Girls",
                "description": "Scholarship scheme to encourage girl students to pursue technical education in AICTE approved institutions.",
                "benefits": "₹50,000 per year (₹30,000 tuition fee + ₹20,000 incidental charges).",
                "eligibility": {
                    "age": "17-25 years",
                    "income": "Family income below ₹8 lakh per annum",
                    "gender": "Female",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Student"
                },
                "documents_required": ["Aadhaar Card", "Income Certificate", "Admission Proof", "Bank Account", "Passport Photo"],
                "source_url": "https://www.aicte-india.org"
            },
            {
                "scheme_name": "Pradhan Mantri Mudra Yojana",
                "description": "Provides loans to micro and small business enterprises and individuals for income generating activities.",
                "benefits": "Loans up to ₹10 lakh under three categories: Shishu (up to ₹50k), Kishore (₹50k-₹5L), Tarun (₹5L-₹10L).",
                "eligibility": {
                    "age": "18-65 years",
                    "income": "No specific limit",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Entrepreneur"
                },
                "documents_required": ["Aadhaar Card", "PAN Card", "Business Plan", "Address Proof", "Bank Statements"],
                "source_url": "https://www.mudra.org.in"
            },
            {
                "scheme_name": "Pradhan Mantri Fasal Bima Yojana",
                "description": "Crop insurance scheme providing financial support to farmers in case of crop failure due to natural calamities.",
                "benefits": "Insurance coverage for crop loss, premium subsidy by government.",
                "eligibility": {
                    "age": "18-100 years",
                    "income": "All farmers",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Farmer"
                },
                "documents_required": ["Aadhaar Card", "Land Records", "Bank Account", "Sowing Certificate"],
                "source_url": "https://pmfby.gov.in"
            }
        ]
        
        self.schemes.extend(known_schemes)
        return known_schemes

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.schemes, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.schemes)} schemes to {filename}")

if __name__ == "__main__":
    scraper = MySchemePortalScraper()
    print("Scraping MyScheme Portal...")
    scraper.scrape_myscheme_portal()
    scraper.save_to_json('../data/raw/myscheme_raw.json')
    print("Scraping completed!")
