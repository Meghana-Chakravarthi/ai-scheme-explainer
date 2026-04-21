import json
import re

class EligibilityChecker:
    def __init__(self):
        with open('../data/processed/schemes_cleaned.json', 'r') as f:
            self.schemes = json.load(f)
    
    def check_eligibility(self, user_profile):
        """
        user_profile = {
            'age': 25,
            'income': 200000,
            'gender': 'Female',  # Male/Female/Other
            'category': 'General',  # General/SC/ST/OBC/BPL
            'state': 'Karnataka',
            'occupation': 'Student'  # Farmer/Student/Worker/Entrepreneur/etc
        }
        """
        eligible_schemes = []
        
        for scheme in self.schemes:
            eligibility = scheme['eligibility']
            reasons = []
            is_eligible = True
            
            # Check age
            if eligibility.get('age'):
                age_str = eligibility['age'].lower()
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
            if eligibility.get('gender') and eligibility['gender'] != 'All':
                if user_profile.get('gender', '').lower() != eligibility['gender'].lower():
                    is_eligible = False
                    reasons.append(f"Only for {eligibility['gender']}")
            
            # Check category
            if eligibility.get('category') and eligibility['category'] not in ['General', 'All']:
                user_category = user_profile.get('category', 'General')
                if user_category != eligibility['category'] and eligibility['category'] != 'General':
                    # BPL schemes are strict
                    if eligibility['category'] == 'BPL' and user_category != 'BPL':
                        is_eligible = False
                        reasons.append(f"Only for {eligibility['category']} category")
            
            # Check occupation
            if eligibility.get('occupation') and eligibility['occupation'] not in ['All', '']:
                user_occupation = user_profile.get('occupation', '').lower()
                scheme_occupation = eligibility['occupation'].lower()
                if user_occupation not in scheme_occupation and scheme_occupation not in user_occupation:
                    is_eligible = False
                    reasons.append(f"Only for {eligibility['occupation']}")
            
            # Check income (basic check)
            if eligibility.get('income'):
                income_str = eligibility['income'].lower()
                user_income = user_profile.get('income', 0)
                
                if 'below' in income_str or 'up to' in income_str:
                    income_match = re.search(r'₹?\s*(\d+(?:,\d+)*)', income_str)
                    if income_match:
                        max_income = int(income_match.group(1).replace(',', ''))
                        if 'lakh' in income_str:
                            max_income *= 100000
                        if user_income > max_income:
                            is_eligible = False
                            reasons.append(f"Income must be below ₹{max_income}")
            
            if is_eligible:
                eligible_schemes.append({
                    'scheme': scheme,
                    'match_score': 100
                })
            else:
                eligible_schemes.append({
                    'scheme': scheme,
                    'match_score': 0,
                    'reasons': reasons
                })
        
        # Sort by eligibility
        eligible_schemes.sort(key=lambda x: x['match_score'], reverse=True)
        
        return eligible_schemes
    
    def get_eligible_schemes(self, user_profile):
        """Return only eligible schemes"""
        all_results = self.check_eligibility(user_profile)
        return [r for r in all_results if r['match_score'] > 0]
    
    def print_results(self, user_profile):
        """Print formatted results"""
        print("\n" + "="*80)
        print("USER PROFILE")
        print("="*80)
        for key, value in user_profile.items():
            print(f"  {key.capitalize()}: {value}")
        
        results = self.check_eligibility(user_profile)
        eligible = [r for r in results if r['match_score'] > 0]
        
        print("\n" + "="*80)
        print(f"✅ ELIGIBLE SCHEMES: {len(eligible)}/{len(results)}")
        print("="*80)
        
        for i, result in enumerate(eligible, 1):
            scheme = result['scheme']
            print(f"\n{i}. {scheme['scheme_name']}")
            print(f"   📋 {scheme['description']}")
            print(f"   💰 {scheme['benefits']}")
            print(f"   📄 Documents: {', '.join(scheme['documents_required'][:3])}")
            print(f"   🔗 {scheme['source_url']}")
        
        # Show ineligible schemes
        ineligible = [r for r in results if r['match_score'] == 0]
        if ineligible:
            print("\n" + "="*80)
            print(f"❌ NOT ELIGIBLE: {len(ineligible)} schemes")
            print("="*80)
            for result in ineligible[:5]:
                scheme = result['scheme']
                print(f"\n• {scheme['scheme_name']}")
                print(f"  Reasons: {', '.join(result['reasons'])}")

if __name__ == "__main__":
    checker = EligibilityChecker()
    
    # Example 1: Female student
    print("\n" + "#"*80)
    print("# EXAMPLE 1: Female Student")
    print("#"*80)
    
    user1 = {
        'age': 20,
        'income': 150000,
        'gender': 'Female',
        'category': 'General',
        'state': 'Karnataka',
        'occupation': 'Student'
    }
    checker.print_results(user1)
    
    # Example 2: Farmer
    print("\n\n" + "#"*80)
    print("# EXAMPLE 2: Farmer")
    print("#"*80)
    
    user2 = {
        'age': 45,
        'income': 180000,
        'gender': 'Male',
        'category': 'General',
        'state': 'Punjab',
        'occupation': 'Farmer'
    }
    checker.print_results(user2)
    
    # Example 3: BPL Woman
    print("\n\n" + "#"*80)
    print("# EXAMPLE 3: BPL Woman")
    print("#"*80)
    
    user3 = {
        'age': 30,
        'income': 100000,
        'gender': 'Female',
        'category': 'BPL',
        'state': 'Bihar',
        'occupation': 'Worker'
    }
    checker.print_results(user3)
