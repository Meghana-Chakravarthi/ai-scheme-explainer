import re
import json

class SchemeDocumentParser:
    def __init__(self):
        pass
    
    def parse_scheme_document(self, document_text):
        """
        Parse a scheme document and extract eligibility criteria
        document_text: Full text of the scheme document
        """
        criteria = {
            'scheme_name': '',
            'description': '',
            'benefits': '',
            'eligibility': {
                'age': '',
                'income': '',
                'gender': '',
                'category': '',
                'occupation': ''
            },
            'documents_required': []
        }
        
        text_lower = document_text.lower()
        
        # Extract scheme name (usually in first few lines or title)
        lines = document_text.split('\n')
        for line in lines[:10]:
            if len(line.strip()) > 10 and len(line.strip()) < 100:
                if any(word in line.lower() for word in ['scheme', 'yojana', 'loan', 'program']):
                    criteria['scheme_name'] = line.strip()
                    break
        
        # Extract age criteria
        age_patterns = [
            r'age.*?(\d+)\s*(?:to|-|and)\s*(\d+)',
            r'between\s*(\d+)\s*(?:to|-|and)\s*(\d+)\s*years',
            r'(\d+)\s*to\s*(\d+)\s*years',
            r'above\s*(\d+)\s*years',
            r'below\s*(\d+)\s*years'
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if 'above' in pattern:
                    criteria['eligibility']['age'] = f"Above {match.group(1)} years"
                elif 'below' in pattern:
                    criteria['eligibility']['age'] = f"Below {match.group(1)} years"
                else:
                    criteria['eligibility']['age'] = f"{match.group(1)}-{match.group(2)} years"
                break
        
        # Extract income criteria
        income_patterns = [
            r'income.*?(?:below|up to|maximum|not exceeding).*?₹?\s*(\d+(?:,\d+)*)\s*(lakh|lakhs)?',
            r'annual income.*?₹?\s*(\d+(?:,\d+)*)\s*(lakh|lakhs)?',
            r'family income.*?₹?\s*(\d+(?:,\d+)*)\s*(lakh|lakhs)?'
        ]
        
        for pattern in income_patterns:
            match = re.search(pattern, text_lower)
            if match:
                amount = match.group(1).replace(',', '')
                unit = match.group(2) if len(match.groups()) > 1 and match.group(2) else ''
                criteria['eligibility']['income'] = f"Below ₹{amount} {unit}".strip()
                break
        
        # Extract gender
        if any(word in text_lower for word in ['women', 'woman', 'female', 'girl', 'mahila']):
            criteria['eligibility']['gender'] = 'Female'
        elif any(word in text_lower for word in ['men', 'man', 'male', 'boy']):
            criteria['eligibility']['gender'] = 'Male'
        else:
            criteria['eligibility']['gender'] = 'All'
        
        # Extract category
        if 'sc' in text_lower or 'scheduled caste' in text_lower:
            criteria['eligibility']['category'] = 'SC'
        elif 'st' in text_lower or 'scheduled tribe' in text_lower:
            criteria['eligibility']['category'] = 'ST'
        elif 'obc' in text_lower:
            criteria['eligibility']['category'] = 'OBC'
        elif 'bpl' in text_lower or 'below poverty' in text_lower:
            criteria['eligibility']['category'] = 'BPL'
        else:
            criteria['eligibility']['category'] = 'General'
        
        # Extract occupation
        occupations = ['farmer', 'student', 'worker', 'entrepreneur', 'business', 'self-employed']
        for occ in occupations:
            if occ in text_lower:
                criteria['eligibility']['occupation'] = occ.capitalize()
                break
        
        # Extract documents
        doc_section = re.search(r'(documents? required|required documents?|documents? needed)(.*?)(?:\n\n|\Z)', text_lower, re.DOTALL)
        if doc_section:
            doc_text = doc_section.group(2)
            common_docs = [
                'aadhaar card', 'pan card', 'bank account', 'income certificate',
                'caste certificate', 'address proof', 'photo', 'passport',
                'land documents', 'business proof', 'age proof'
            ]
            for doc in common_docs:
                if doc in doc_text:
                    criteria['documents_required'].append(doc.title())
        
        return criteria
    
    def check_eligibility_from_document(self, document_text, user_profile):
        """
        Parse document and check user eligibility
        """
        # Parse the document
        scheme_criteria = self.parse_scheme_document(document_text)
        
        # Check eligibility
        is_eligible = True
        reasons = []
        
        # Check age
        if scheme_criteria['eligibility']['age']:
            age_str = scheme_criteria['eligibility']['age'].lower()
            user_age = user_profile.get('age', 0)
            
            if 'below' in age_str:
                max_age = int(re.search(r'\d+', age_str).group())
                if user_age >= max_age:
                    is_eligible = False
                    reasons.append(f"Age must be below {max_age}")
            elif 'above' in age_str:
                min_age = int(re.search(r'\d+', age_str).group())
                if user_age < min_age:
                    is_eligible = False
                    reasons.append(f"Age must be above {min_age}")
            elif '-' in age_str:
                ages = re.findall(r'\d+', age_str)
                if len(ages) >= 2:
                    min_age, max_age = int(ages[0]), int(ages[1])
                    if not (min_age <= user_age <= max_age):
                        is_eligible = False
                        reasons.append(f"Age must be between {min_age}-{max_age}")
        
        # Check gender
        if scheme_criteria['eligibility']['gender'] != 'All':
            if user_profile.get('gender', '').lower() != scheme_criteria['eligibility']['gender'].lower():
                is_eligible = False
                reasons.append(f"Only for {scheme_criteria['eligibility']['gender']}")
        
        # Check category
        if scheme_criteria['eligibility']['category'] not in ['General', 'All']:
            if user_profile.get('category', 'General') != scheme_criteria['eligibility']['category']:
                is_eligible = False
                reasons.append(f"Only for {scheme_criteria['eligibility']['category']} category")
        
        # Check occupation
        if scheme_criteria['eligibility']['occupation']:
            user_occ = user_profile.get('occupation', '').lower()
            scheme_occ = scheme_criteria['eligibility']['occupation'].lower()
            if user_occ not in scheme_occ and scheme_occ not in user_occ:
                is_eligible = False
                reasons.append(f"Only for {scheme_criteria['eligibility']['occupation']}")
        
        return {
            'scheme_criteria': scheme_criteria,
            'eligibility_status': 'ELIGIBLE' if is_eligible else 'NOT ELIGIBLE',
            'reasons': reasons,
            'user_profile': user_profile
        }
    
    def print_result(self, result):
        """Print formatted result"""
        print("\n" + "="*80)
        print("SCHEME DOCUMENT ANALYSIS")
        print("="*80)
        
        criteria = result['scheme_criteria']
        print(f"\n📋 SCHEME: {criteria['scheme_name'] or 'Unnamed Scheme'}")
        
        print("\n✅ ELIGIBILITY CRITERIA EXTRACTED:")
        for key, value in criteria['eligibility'].items():
            if value:
                print(f"   • {key.capitalize()}: {value}")
        
        if criteria['documents_required']:
            print("\n📄 DOCUMENTS REQUIRED:")
            for doc in criteria['documents_required']:
                print(f"   • {doc}")
        
        print("\n" + "="*80)
        print("YOUR PROFILE")
        print("="*80)
        for key, value in result['user_profile'].items():
            print(f"   • {key.capitalize()}: {value}")
        
        print("\n" + "="*80)
        print(f"🎯 ELIGIBILITY: {result['eligibility_status']}")
        print("="*80)
        
        if result['reasons']:
            print("\n❌ REASONS:")
            for reason in result['reasons']:
                print(f"   • {reason}")
        else:
            print("\n✅ You meet all eligibility criteria!")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    parser = SchemeDocumentParser()
    
    # Example 1: Sample loan scheme document
    print("\n" + "#"*80)
    print("# EXAMPLE: Education Loan Scheme Document")
    print("#"*80)
    
    sample_document = """
    EDUCATION LOAN SCHEME FOR STUDENTS
    
    This scheme provides financial assistance to students pursuing higher education
    in recognized institutions across India.
    
    ELIGIBILITY CRITERIA:
    - Age: Between 18 to 35 years
    - Annual family income should not exceed ₹8 lakh
    - Must be enrolled in a recognized educational institution
    - Open to all categories (General, SC, ST, OBC)
    
    BENEFITS:
    - Loan amount up to ₹10 lakh for studies in India
    - Interest subsidy for economically weaker sections
    - Flexible repayment options
    
    DOCUMENTS REQUIRED:
    - Aadhaar Card
    - Income Certificate
    - Admission Proof
    - Bank Account Details
    - PAN Card
    - Address Proof
    
    APPLICATION PROCESS:
    Visit the nearest bank branch or apply online through the official portal.
    """
    
    # User 1: Eligible student
    user1 = {
        'age': 22,
        'income': 500000,
        'gender': 'Male',
        'category': 'General',
        'occupation': 'Student'
    }
    
    print("\n--- USER 1: Eligible Student ---")
    result1 = parser.check_eligibility_from_document(sample_document, user1)
    parser.print_result(result1)
    
    # User 2: Not eligible (too old)
    user2 = {
        'age': 40,
        'income': 600000,
        'gender': 'Female',
        'category': 'General',
        'occupation': 'Student'
    }
    
    print("\n\n--- USER 2: Not Eligible (Age) ---")
    result2 = parser.check_eligibility_from_document(sample_document, user2)
    parser.print_result(result2)
