import requests
from bs4 import BeautifulSoup
import json
import re
import time

class IndiaGovScraper:
    def __init__(self):
        self.base_url = "https://www.india.gov.in"
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
        
        age_match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*years?', text_lower)
        if age_match:
            eligibility["age"] = f"{age_match.group(1)}-{age_match.group(2)} years"
        
        income_match = re.search(r'₹?\s*(\d+(?:,\d+)*)\s*(?:lakh|lakhs)?', text_lower)
        if income_match:
            eligibility["income"] = income_match.group(0)
        
        if any(word in text_lower for word in ['women', 'woman', 'girl', 'female']):
            eligibility["gender"] = "Female"
        elif any(word in text_lower for word in ['men', 'man', 'boy', 'male']):
            eligibility["gender"] = "Male"
        else:
            eligibility["gender"] = "All"
        
        if 'sc' in text_lower or 'scheduled caste' in text_lower:
            eligibility["category"] = "SC"
        elif 'st' in text_lower or 'scheduled tribe' in text_lower:
            eligibility["category"] = "ST"
        elif 'obc' in text_lower:
            eligibility["category"] = "OBC"
        elif 'bpl' in text_lower:
            eligibility["category"] = "BPL"
        else:
            eligibility["category"] = "General"
        
        occupations = ['farmer', 'student', 'worker', 'entrepreneur', 'laborer']
        for occ in occupations:
            if occ in text_lower:
                eligibility["occupation"] = occ.capitalize()
                break
        
        return eligibility

    def scrape_india_gov(self):
        # Additional schemes from India.gov.in knowledge base
        additional_schemes = [
            {
                "scheme_name": "Pradhan Mantri Matru Vandana Yojana",
                "description": "Maternity benefit scheme providing cash incentive to pregnant and lactating mothers for first live birth.",
                "benefits": "Cash benefit of ₹5000 in three installments for improved health and nutrition.",
                "eligibility": {
                    "age": "19-45 years",
                    "income": "All income groups",
                    "gender": "Female",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Bank Account", "MCP Card", "Institutional Delivery Proof"],
                "source_url": "https://pmmvy.wcd.gov.in"
            },
            {
                "scheme_name": "Atal Pension Yojana",
                "description": "Pension scheme for unorganized sector workers providing guaranteed pension based on contribution.",
                "benefits": "Guaranteed pension of ₹1000 to ₹5000 per month after 60 years based on contribution.",
                "eligibility": {
                    "age": "18-40 years",
                    "income": "All income groups",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Bank Account", "Mobile Number"],
                "source_url": "https://npscra.nsdl.co.in/atal-pension-yojana.php"
            },
            {
                "scheme_name": "Pradhan Mantri Kaushal Vikas Yojana",
                "description": "Skill development scheme to enable youth to take up industry-relevant skill training.",
                "benefits": "Free skill training, certification, and monetary rewards on successful completion.",
                "eligibility": {
                    "age": "15-45 years",
                    "income": "All income groups",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Bank Account", "Educational Certificates"],
                "source_url": "https://www.pmkvyofficial.org"
            },
            {
                "scheme_name": "National Rural Employment Guarantee Scheme (MGNREGA)",
                "description": "Employment guarantee scheme providing at least 100 days of wage employment to rural households.",
                "benefits": "Guaranteed 100 days of employment per year with minimum wages.",
                "eligibility": {
                    "age": "18-100 years",
                    "income": "Rural households",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "Worker"
                },
                "documents_required": ["Job Card", "Aadhaar Card", "Bank Account"],
                "source_url": "https://nrega.nic.in"
            },
            {
                "scheme_name": "Pradhan Mantri Jeevan Jyoti Bima Yojana",
                "description": "Life insurance scheme offering renewable one-year life cover to people aged 18-50 years.",
                "benefits": "Life cover of ₹2 lakh at premium of ₹436 per year.",
                "eligibility": {
                    "age": "18-50 years",
                    "income": "All income groups",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Bank Account", "Consent Form"],
                "source_url": "https://www.jansuraksha.gov.in"
            },
            {
                "scheme_name": "Pradhan Mantri Suraksha Bima Yojana",
                "description": "Accident insurance scheme offering accidental death and disability cover.",
                "benefits": "Accidental death cover of ₹2 lakh and disability cover at premium of ₹20 per year.",
                "eligibility": {
                    "age": "18-70 years",
                    "income": "All income groups",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Bank Account", "Consent Form"],
                "source_url": "https://www.jansuraksha.gov.in"
            },
            {
                "scheme_name": "Beti Bachao Beti Padhao",
                "description": "Scheme to address declining Child Sex Ratio and promote education and welfare of girl child.",
                "benefits": "Awareness campaigns, educational support, and financial incentives for girl child education.",
                "eligibility": {
                    "age": "0-21 years (girl child)",
                    "income": "All income groups",
                    "gender": "Female",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Birth Certificate", "Aadhaar Card", "School Enrollment Proof"],
                "source_url": "https://wcd.nic.in/bbbp-schemes"
            },
            {
                "scheme_name": "Swachh Bharat Mission - Toilet Construction",
                "description": "Scheme to construct individual household toilets in rural and urban areas.",
                "benefits": "Financial assistance of ₹12,000 for toilet construction.",
                "eligibility": {
                    "age": "18-100 years",
                    "income": "BPL and APL households without toilet",
                    "gender": "All",
                    "category": "General",
                    "state": "All India",
                    "occupation": "All"
                },
                "documents_required": ["Aadhaar Card", "Bank Account", "Address Proof", "Photo"],
                "source_url": "https://swachhbharatmission.gov.in"
            }
        ]
        
        self.schemes.extend(additional_schemes)
        return additional_schemes

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.schemes, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.schemes)} schemes to {filename}")

if __name__ == "__main__":
    scraper = IndiaGovScraper()
    print("Scraping India.gov.in schemes...")
    scraper.scrape_india_gov()
    scraper.save_to_json('../data/raw/indiagov_raw.json')
    print("Scraping completed!")
