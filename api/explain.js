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

function findScheme(schemeName) {
  const searchTerm = schemeName.toLowerCase().trim();
  return schemes.find(scheme => 
    scheme.scheme_name.toLowerCase().includes(searchTerm) ||
    scheme.scheme_name.toLowerCase().replace(/\s+/g, '').includes(searchTerm.replace(/\s+/g, ''))
  );
}

function formatEligibility(eligibility) {
  if (typeof eligibility === 'string') return eligibility;
  if (typeof eligibility === 'object') {
    const parts = [];
    if (eligibility.age) parts.push(`Age: ${eligibility.age}`);
    if (eligibility.income) parts.push(`Income: ${eligibility.income}`);
    if (eligibility.gender) parts.push(`Gender: ${eligibility.gender}`);
    if (eligibility.category) parts.push(`Category: ${eligibility.category}`);
    if (eligibility.occupation) parts.push(`Occupation: ${eligibility.occupation}`);
    if (eligibility.state) parts.push(`State: ${eligibility.state}`);
    return parts.join('. ') + '.';
  }
  return 'Eligibility criteria not specified';
}

export default async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { schemeName, simplify } = req.body;

  if (!schemeName) {
    res.status(400).json({ error: 'Scheme name is required' });
    return;
  }

  const scheme = findScheme(schemeName);

  if (scheme) {
    let summary = scheme.description || 'No description available';
    let eligibility = formatEligibility(scheme.eligibility);
    let benefits = scheme.benefits || 'Benefits information not available';
    let process = `To apply for ${scheme.scheme_name}: Visit the official portal at ${scheme.source_url || 'the government website'}. Required documents: ${scheme.documents_required?.join(', ') || 'Check official website'}. Submit your application online or at the nearest Common Service Center.`;

    // Simplify if requested
    if (simplify) {
      summary = summary.split('.')[0] + '.';
      eligibility = eligibility.split('.').slice(0, 2).join('. ') + '.';
      benefits = benefits.split('.')[0] + '.';
      process = process.split('.').slice(0, 2).join('. ') + '.';
    }

    res.status(200).json({
      summary,
      eligibility,
      benefits,
      process,
      scheme_name: scheme.scheme_name,
      source_url: scheme.source_url
    });
  } else {
    res.status(404).json({
      error: 'Scheme not found',
      summary: `${schemeName} scheme not found in our database.`,
      eligibility: 'Please check the scheme name and try again.',
      benefits: 'Visit the official government portal for details.',
      process: 'Search for the correct scheme name or browse all schemes.'
    });
  }
};
