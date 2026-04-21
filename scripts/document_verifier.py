import json
import re
from pathlib import Path

class DocumentVerifier:
    def __init__(self):
        with open('../data/processed/schemes_cleaned.json', 'r') as f:
            self.schemes = json.load(f)
    
    def verify_documents(self, scheme_name, user_documents):
        """
        Check if user has required documents for a scheme
        
        scheme_name: Name of the scheme
        user_documents: List of documents user has
        
        Example:
        user_documents = ['Aadhaar Card', 'Bank Account', 'Income Certificate']
        """
        # Find scheme
        scheme = None
        for s in self.schemes:
            if s['scheme_name'].lower() == scheme_name.lower():
                scheme = s
                break
        
        if not scheme:
            return {"error": "Scheme not found"}
        
        required_docs = scheme['documents_required']
        user_docs_lower = [doc.lower() for doc in user_documents]
        
        # Check which documents are present
        missing_docs = []
        present_docs = []
        
        for req_doc in required_docs:
            found = False
            for user_doc in user_documents:
                if self._match_document(req_doc, user_doc):
                    found = True
                    present_docs.append(req_doc)
                    break
            
            if not found:
                missing_docs.append(req_doc)
        
        return {
            'scheme_name': scheme['scheme_name'],
            'required_documents': required_docs,
            'present_documents': present_docs,
            'missing_documents': missing_docs,
            'verification_status': 'COMPLETE' if len(missing_docs) == 0 else 'INCOMPLETE',
            'completion_percentage': int((len(present_docs) / len(required_docs)) * 100)
        }
    
    def _match_document(self, required, provided):
        """Fuzzy match for document names"""
        req_lower = required.lower()
        prov_lower = provided.lower()
        
        # Exact match
        if req_lower == prov_lower:
            return True
        
        # Partial match
        if req_lower in prov_lower or prov_lower in req_lower:
            return True
        
        # Common variations
        variations = {
            'aadhaar': ['aadhar', 'adhaar', 'adhar', 'uid'],
            'pan': ['pan card', 'permanent account'],
            'bank account': ['bank', 'account', 'passbook'],
            'income certificate': ['income', 'income proof'],
            'caste certificate': ['caste', 'caste proof'],
            'address proof': ['address', 'residence proof'],
            'photo': ['photograph', 'passport photo', 'passport size']
        }
        
        for key, vals in variations.items():
            if key in req_lower:
                for val in vals:
                    if val in prov_lower:
                        return True
        
        return False
    
    def check_eligibility_with_documents(self, scheme_name, user_profile, user_documents):
        """
        Complete check: eligibility + documents
        """
        from eligibility_checker import EligibilityChecker
        
        # Check eligibility
        checker = EligibilityChecker()
        all_results = checker.check_eligibility(user_profile)
        
        # Find this scheme
        scheme_result = None
        for result in all_results:
            if result['scheme']['scheme_name'].lower() == scheme_name.lower():
                scheme_result = result
                break
        
        if not scheme_result:
            return {"error": "Scheme not found"}
        
        # Check documents
        doc_verification = self.verify_documents(scheme_name, user_documents)
        
        return {
            'scheme_name': scheme_name,
            'eligibility_status': 'ELIGIBLE' if scheme_result['match_score'] > 0 else 'NOT ELIGIBLE',
            'eligibility_reasons': scheme_result.get('reasons', []),
            'document_verification': doc_verification,
            'overall_status': 'APPROVED' if (scheme_result['match_score'] > 0 and doc_verification['verification_status'] == 'COMPLETE') else 'PENDING',
            'next_steps': self._get_next_steps(scheme_result['match_score'] > 0, doc_verification)
        }
    
    def _get_next_steps(self, is_eligible, doc_verification):
        """Provide next steps based on status"""
        if not is_eligible:
            return ["You are not eligible for this scheme. Check eligibility criteria."]
        
        if doc_verification['verification_status'] == 'COMPLETE':
            return ["All documents verified. You can proceed with application."]
        
        steps = ["You are eligible but missing documents:"]
        for doc in doc_verification['missing_documents']:
            steps.append(f"  • Obtain {doc}")
        steps.append("Submit application after collecting all documents.")
        
        return steps
    
    def print_verification_result(self, result):
        """Print formatted verification result"""
        print("\n" + "="*80)
        print(f"SCHEME: {result['scheme_name']}")
        print("="*80)
        
        print(f"\n✅ ELIGIBILITY: {result['eligibility_status']}")
        if result.get('eligibility_reasons'):
            print("   Reasons:")
            for reason in result['eligibility_reasons']:
                print(f"   • {reason}")
        
        doc_ver = result['document_verification']
        print(f"\n📄 DOCUMENTS: {doc_ver['verification_status']} ({doc_ver['completion_percentage']}%)")
        
        if doc_ver['present_documents']:
            print("\n   ✅ Present:")
            for doc in doc_ver['present_documents']:
                print(f"      • {doc}")
        
        if doc_ver['missing_documents']:
            print("\n   ❌ Missing:")
            for doc in doc_ver['missing_documents']:
                print(f"      • {doc}")
        
        print(f"\n🎯 OVERALL STATUS: {result['overall_status']}")
        
        print("\n📋 NEXT STEPS:")
        for step in result['next_steps']:
            print(f"   {step}")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    verifier = DocumentVerifier()
    
    # Example 1: Complete documents
    print("\n" + "#"*80)
    print("# EXAMPLE 1: Female Student - AICTE Pragati Scholarship")
    print("#"*80)
    
    user_profile = {
        'age': 20,
        'income': 150000,
        'gender': 'Female',
        'category': 'General',
        'occupation': 'Student'
    }
    
    user_documents = [
        'Aadhaar Card',
        'Income Certificate',
        'Admission Proof',
        'Bank Account',
        'Passport Photo'
    ]
    
    result = verifier.check_eligibility_with_documents(
        'AICTE Pragati Scholarship for Girls',
        user_profile,
        user_documents
    )
    verifier.print_verification_result(result)
    
    # Example 2: Missing documents
    print("\n\n" + "#"*80)
    print("# EXAMPLE 2: Farmer - PM Kisan (Missing Documents)")
    print("#"*80)
    
    user_profile2 = {
        'age': 45,
        'income': 180000,
        'gender': 'Male',
        'category': 'General',
        'occupation': 'Farmer'
    }
    
    user_documents2 = [
        'Aadhaar Card',
        'Bank Account'
        # Missing: Land Ownership Documents
    ]
    
    result2 = verifier.check_eligibility_with_documents(
        'PM Kisan Samman Nidhi',
        user_profile2,
        user_documents2
    )
    verifier.print_verification_result(result2)
    
    # Example 3: Not eligible
    print("\n\n" + "#"*80)
    print("# EXAMPLE 3: Student trying for Farmer scheme")
    print("#"*80)
    
    user_profile3 = {
        'age': 22,
        'income': 150000,
        'gender': 'Male',
        'category': 'General',
        'occupation': 'Student'
    }
    
    user_documents3 = [
        'Aadhaar Card',
        'Bank Account',
        'Land Ownership Documents'
    ]
    
    result3 = verifier.check_eligibility_with_documents(
        'PM Kisan Samman Nidhi',
        user_profile3,
        user_documents3
    )
    verifier.print_verification_result(result3)
