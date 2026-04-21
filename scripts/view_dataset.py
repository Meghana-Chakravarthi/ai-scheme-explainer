import json
import sys

def display_scheme(scheme, index):
    print(f"\n{'='*80}")
    print(f"SCHEME #{index + 1}: {scheme['scheme_name']}")
    print(f"{'='*80}")
    print(f"\n📋 DESCRIPTION:")
    print(f"   {scheme['description']}")
    print(f"\n💰 BENEFITS:")
    print(f"   {scheme['benefits']}")
    print(f"\n✅ ELIGIBILITY:")
    for key, value in scheme['eligibility'].items():
        if value:
            print(f"   • {key.capitalize()}: {value}")
    print(f"\n📄 REQUIRED DOCUMENTS:")
    for doc in scheme['documents_required']:
        print(f"   • {doc}")
    print(f"\n🔗 SOURCE: {scheme['source_url']}")

def main():
    try:
        with open('../data/processed/schemes_cleaned.json', 'r', encoding='utf-8') as f:
            schemes = json.load(f)
        
        print(f"\n{'#'*80}")
        print(f"# INDIAN GOVERNMENT SCHEMES DATASET")
        print(f"# Total Schemes: {len(schemes)}")
        print(f"{'#'*80}")
        
        if len(sys.argv) > 1:
            # Display specific scheme by index
            try:
                index = int(sys.argv[1]) - 1
                if 0 <= index < len(schemes):
                    display_scheme(schemes[index], index)
                else:
                    print(f"Error: Scheme index must be between 1 and {len(schemes)}")
            except ValueError:
                print("Error: Please provide a valid scheme number")
        else:
            # Display all schemes
            for i, scheme in enumerate(schemes):
                display_scheme(scheme, i)
        
        print(f"\n{'='*80}\n")
        print(f"💡 TIP: Run 'python3 view_dataset.py <number>' to view a specific scheme")
        print(f"   Example: python3 view_dataset.py 1\n")
        
    except FileNotFoundError:
        print("Error: Dataset not found. Please run the pipeline first.")
        print("Run: bash run_pipeline.sh")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
