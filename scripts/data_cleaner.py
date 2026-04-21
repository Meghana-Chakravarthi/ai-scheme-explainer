import json
import re
from pathlib import Path

class DataCleaner:
    def __init__(self):
        self.cleaned_schemes = []
        self.seen_schemes = set()

    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\r\n\t]', ' ', text)
        text = re.sub(r'[^\w\s\-.,₹()/:@]', '', text)
        return text.strip()

    def normalize_scheme_name(self, name):
        name = name.lower()
        name = re.sub(r'[^\w\s]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()

    def validate_scheme(self, scheme):
        required_fields = ['scheme_name', 'description', 'benefits', 'eligibility']
        for field in required_fields:
            if field not in scheme or not scheme[field]:
                return False
        
        if not isinstance(scheme['eligibility'], dict):
            return False
        
        if not isinstance(scheme.get('documents_required', []), list):
            return False
        
        return True

    def clean_scheme(self, scheme):
        cleaned = {
            "scheme_name": self.clean_text(scheme.get('scheme_name', '')),
            "description": self.clean_text(scheme.get('description', '')),
            "benefits": self.clean_text(scheme.get('benefits', '')),
            "eligibility": {
                "age": self.clean_text(scheme.get('eligibility', {}).get('age', '')),
                "income": self.clean_text(scheme.get('eligibility', {}).get('income', '')),
                "gender": self.clean_text(scheme.get('eligibility', {}).get('gender', 'All')),
                "category": self.clean_text(scheme.get('eligibility', {}).get('category', 'General')),
                "state": self.clean_text(scheme.get('eligibility', {}).get('state', 'All India')),
                "occupation": self.clean_text(scheme.get('eligibility', {}).get('occupation', ''))
            },
            "documents_required": [self.clean_text(doc) for doc in scheme.get('documents_required', [])],
            "source_url": scheme.get('source_url', '')
        }
        
        return cleaned

    def merge_datasets(self, file_paths):
        all_schemes = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    schemes = json.load(f)
                    all_schemes.extend(schemes)
                    print(f"Loaded {len(schemes)} schemes from {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return all_schemes

    def remove_duplicates(self, schemes):
        unique_schemes = []
        
        for scheme in schemes:
            normalized_name = self.normalize_scheme_name(scheme.get('scheme_name', ''))
            
            if normalized_name not in self.seen_schemes:
                self.seen_schemes.add(normalized_name)
                unique_schemes.append(scheme)
        
        print(f"Removed {len(schemes) - len(unique_schemes)} duplicate schemes")
        return unique_schemes

    def process_all(self, input_files, output_file):
        print("Starting data cleaning process...")
        
        # Merge all datasets
        all_schemes = self.merge_datasets(input_files)
        print(f"Total schemes loaded: {len(all_schemes)}")
        
        # Remove duplicates
        unique_schemes = self.remove_duplicates(all_schemes)
        
        # Clean and validate each scheme
        for scheme in unique_schemes:
            cleaned_scheme = self.clean_scheme(scheme)
            
            if self.validate_scheme(cleaned_scheme):
                self.cleaned_schemes.append(cleaned_scheme)
            else:
                print(f"Skipped invalid scheme: {scheme.get('scheme_name', 'Unknown')}")
        
        # Save cleaned data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.cleaned_schemes, f, indent=2, ensure_ascii=False)
        
        print(f"\nCleaning completed!")
        print(f"Total valid schemes: {len(self.cleaned_schemes)}")
        print(f"Saved to: {output_file}")
        
        return self.cleaned_schemes

if __name__ == "__main__":
    cleaner = DataCleaner()
    
    input_files = [
        '../data/raw/myscheme_raw.json',
        '../data/raw/indiagov_raw.json'
    ]
    
    output_file = '../data/processed/schemes_cleaned.json'
    
    cleaner.process_all(input_files, output_file)
