import json

class SchemeValidator:
    def __init__(self):
        self.validation_errors = []
        self.validation_warnings = []

    def validate_required_fields(self, scheme):
        required_fields = ['scheme_name', 'description', 'benefits', 'eligibility', 'documents_required', 'source_url']
        
        for field in required_fields:
            if field not in scheme:
                self.validation_errors.append(f"Missing field '{field}' in scheme: {scheme.get('scheme_name', 'Unknown')}")
                return False
            
            if field == 'eligibility':
                if not isinstance(scheme[field], dict):
                    self.validation_errors.append(f"Field 'eligibility' must be a dict in scheme: {scheme['scheme_name']}")
                    return False
            elif field == 'documents_required':
                if not isinstance(scheme[field], list):
                    self.validation_errors.append(f"Field 'documents_required' must be a list in scheme: {scheme['scheme_name']}")
                    return False
            else:
                if not scheme[field] or not str(scheme[field]).strip():
                    self.validation_errors.append(f"Field '{field}' is empty in scheme: {scheme.get('scheme_name', 'Unknown')}")
                    return False
        
        return True

    def validate_eligibility_structure(self, scheme):
        required_eligibility_fields = ['age', 'income', 'gender', 'category', 'state', 'occupation']
        eligibility = scheme.get('eligibility', {})
        
        for field in required_eligibility_fields:
            if field not in eligibility:
                self.validation_warnings.append(f"Missing eligibility field '{field}' in scheme: {scheme['scheme_name']}")
        
        return True

    def validate_text_quality(self, scheme):
        # Check minimum text length
        if len(scheme.get('description', '')) < 20:
            self.validation_warnings.append(f"Description too short in scheme: {scheme['scheme_name']}")
        
        if len(scheme.get('benefits', '')) < 10:
            self.validation_warnings.append(f"Benefits description too short in scheme: {scheme['scheme_name']}")
        
        # Check for placeholder text
        placeholder_patterns = ['lorem ipsum', 'placeholder', 'xxx', 'tbd', 'to be determined']
        for field in ['description', 'benefits']:
            text = scheme.get(field, '').lower()
            for pattern in placeholder_patterns:
                if pattern in text:
                    self.validation_errors.append(f"Placeholder text found in '{field}' of scheme: {scheme['scheme_name']}")
        
        return True

    def validate_documents(self, scheme):
        docs = scheme.get('documents_required', [])
        
        if len(docs) == 0:
            self.validation_warnings.append(f"No documents listed for scheme: {scheme['scheme_name']}")
        
        for doc in docs:
            if not doc or not doc.strip():
                self.validation_errors.append(f"Empty document entry in scheme: {scheme['scheme_name']}")
        
        return True

    def validate_all(self, schemes_file):
        with open(schemes_file, 'r', encoding='utf-8') as f:
            schemes = json.load(f)
        
        print(f"Validating {len(schemes)} schemes...\n")
        
        valid_count = 0
        for scheme in schemes:
            is_valid = True
            
            if not self.validate_required_fields(scheme):
                is_valid = False
            else:
                self.validate_eligibility_structure(scheme)
                self.validate_text_quality(scheme)
                self.validate_documents(scheme)
            
            if is_valid:
                valid_count += 1
        
        # Print results
        print("="*60)
        print("VALIDATION REPORT")
        print("="*60)
        print(f"Total schemes: {len(schemes)}")
        print(f"Valid schemes: {valid_count}")
        print(f"Invalid schemes: {len(schemes) - valid_count}")
        print(f"\nErrors: {len(self.validation_errors)}")
        print(f"Warnings: {len(self.validation_warnings)}")
        
        if self.validation_errors:
            print("\n--- ERRORS ---")
            for error in self.validation_errors[:10]:
                print(f"  ❌ {error}")
            if len(self.validation_errors) > 10:
                print(f"  ... and {len(self.validation_errors) - 10} more errors")
        
        if self.validation_warnings:
            print("\n--- WARNINGS ---")
            for warning in self.validation_warnings[:10]:
                print(f"  ⚠️  {warning}")
            if len(self.validation_warnings) > 10:
                print(f"  ... and {len(self.validation_warnings) - 10} more warnings")
        
        print("\n" + "="*60)
        
        if len(self.validation_errors) == 0:
            print("✅ All schemes passed validation!")
        else:
            print("❌ Some schemes have validation errors")
        
        return len(self.validation_errors) == 0

if __name__ == "__main__":
    validator = SchemeValidator()
    schemes_file = '../data/processed/schemes_cleaned.json'
    validator.validate_all(schemes_file)
