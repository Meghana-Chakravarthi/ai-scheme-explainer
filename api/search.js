import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const schemesPath = path.join(__dirname, 'schemes_cleaned.json');
let schemes = [];

try {
  const data = fs.readFileSync(schemesPath, 'utf8');
  schemes = JSON.parse(data);
} catch (error) {
  console.error('Error loading schemes:', error);
}

export default async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { query, category } = req.query;

  let results = schemes;

  // Filter by category if provided
  if (category && category !== 'all') {
    results = results.filter(scheme => 
      scheme.eligibility?.occupation?.toLowerCase() === category.toLowerCase()
    );
  }

  // Filter by search query if provided
  if (query) {
    const searchTerm = query.toLowerCase();
    results = results.filter(scheme =>
      scheme.scheme_name.toLowerCase().includes(searchTerm) ||
      scheme.description.toLowerCase().includes(searchTerm)
    );
  }

  res.status(200).json({
    schemes: results.map(s => ({
      name: s.scheme_name,
      description: s.description,
      target: s.eligibility?.occupation || 'general'
    })),
    total: results.length
  });
};
