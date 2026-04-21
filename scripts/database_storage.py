import json
import sqlite3
from pathlib import Path

class DatabaseStorage:
    def __init__(self, db_path='../data/schemes.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Main schemes table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheme_name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                benefits TEXT NOT NULL,
                source_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Eligibility table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eligibility (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheme_id INTEGER NOT NULL,
                age TEXT,
                income TEXT,
                gender TEXT,
                category TEXT,
                state TEXT,
                occupation TEXT,
                FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
            )
        ''')
        
        # Documents table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheme_id INTEGER NOT NULL,
                document_name TEXT NOT NULL,
                FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
        print("Database tables created successfully")

    def insert_scheme(self, scheme):
        try:
            # Insert main scheme
            self.cursor.execute('''
                INSERT INTO schemes (scheme_name, description, benefits, source_url)
                VALUES (?, ?, ?, ?)
            ''', (
                scheme['scheme_name'],
                scheme['description'],
                scheme['benefits'],
                scheme['source_url']
            ))
            
            scheme_id = self.cursor.lastrowid
            
            # Insert eligibility
            eligibility = scheme['eligibility']
            self.cursor.execute('''
                INSERT INTO eligibility (scheme_id, age, income, gender, category, state, occupation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                scheme_id,
                eligibility.get('age', ''),
                eligibility.get('income', ''),
                eligibility.get('gender', ''),
                eligibility.get('category', ''),
                eligibility.get('state', ''),
                eligibility.get('occupation', '')
            ))
            
            # Insert documents
            for doc in scheme.get('documents_required', []):
                self.cursor.execute('''
                    INSERT INTO documents (scheme_id, document_name)
                    VALUES (?, ?)
                ''', (scheme_id, doc))
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Scheme already exists: {scheme['scheme_name']}")
            return False
        except Exception as e:
            print(f"Error inserting scheme {scheme.get('scheme_name', 'Unknown')}: {e}")
            return False

    def load_from_json(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            schemes = json.load(f)
        
        success_count = 0
        for scheme in schemes:
            if self.insert_scheme(scheme):
                success_count += 1
        
        print(f"Inserted {success_count}/{len(schemes)} schemes into database")

    def query_schemes(self, filters=None):
        query = '''
            SELECT s.*, e.age, e.income, e.gender, e.category, e.state, e.occupation
            FROM schemes s
            LEFT JOIN eligibility e ON s.id = e.scheme_id
        '''
        
        if filters:
            conditions = []
            params = []
            
            if 'gender' in filters:
                conditions.append("(e.gender = ? OR e.gender = 'All')")
                params.append(filters['gender'])
            
            if 'category' in filters:
                conditions.append("(e.category = ? OR e.category = 'General')")
                params.append(filters['category'])
            
            if 'occupation' in filters:
                conditions.append("e.occupation LIKE ?")
                params.append(f"%{filters['occupation']}%")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        
        return self.cursor.fetchall()

    def get_scheme_details(self, scheme_name):
        self.cursor.execute('''
            SELECT s.*, e.age, e.income, e.gender, e.category, e.state, e.occupation
            FROM schemes s
            LEFT JOIN eligibility e ON s.id = e.scheme_id
            WHERE s.scheme_name = ?
        ''', (scheme_name,))
        
        scheme = self.cursor.fetchone()
        
        if scheme:
            self.cursor.execute('''
                SELECT document_name FROM documents
                WHERE scheme_id = ?
            ''', (scheme[0],))
            
            documents = [row[0] for row in self.cursor.fetchall()]
            
            return {
                'scheme_name': scheme[1],
                'description': scheme[2],
                'benefits': scheme[3],
                'source_url': scheme[4],
                'eligibility': {
                    'age': scheme[6],
                    'income': scheme[7],
                    'gender': scheme[8],
                    'category': scheme[9],
                    'state': scheme[10],
                    'occupation': scheme[11]
                },
                'documents_required': documents
            }
        
        return None

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseStorage()
    
    print("Loading schemes into SQLite database...")
    db.load_from_json('../data/processed/schemes_cleaned.json')
    
    print("\nQuerying schemes for farmers...")
    results = db.query_schemes({'occupation': 'Farmer'})
    print(f"Found {len(results)} schemes for farmers")
    
    print("\nDatabase storage completed!")
    db.close()
