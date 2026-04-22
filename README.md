# AI Scheme Explainer

A modern, production-ready web application that provides AI-powered explanations of government schemes with an elegant, minimalistic UI.

## Features

- **Modern SaaS UI**: Clean, airy design with soft color palette
- **AI-Powered Explanations**: Instant scheme summaries, eligibility, benefits, and application process
- **Scheme Comparison**: Side-by-side comparison of two schemes
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Production Ready**: Complete CI/CD pipeline with Vercel deployment

## Tech Stack

### Frontend
- React 18 + Vite
- Tailwind CSS
- React Router
- Lucide Icons
- Axios

### Backend
- Vercel Serverless Functions
- Node.js

## Project Structure

```
ai-scheme-explainer/
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── main.jsx      # Entry point
│   ├── package.json
│   └── vite.config.js
├── api/                  # Vercel serverless functions
│   └── explain.js        # Main API endpoint
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD
├── vercel.json           # Vercel configuration
└── package.json          # Root package.json
```

## Local Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-scheme-explainer.git
cd ai-scheme-explainer
```

2. **Install dependencies**
```bash
npm run install:all
```

3. **Start frontend development server**
```bash
npm run dev:frontend
```

The app will be available at `http://localhost:3000`

### Environment Variables

Create `frontend/.env` file:
```
VITE_API_URL=http://localhost:3001
```

For production, set this to your Vercel backend URL.

## Deployment to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Deploy Frontend**
   - Project Name: `scheme-explainer-frontend`
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Add Environment Variable:
     - `VITE_API_URL`: (will be set after backend deployment)

4. **Deploy Backend**
   - Create another project for the API
   - Project Name: `scheme-explainer-api`
   - Root Directory: `.` (root)
   - Vercel will automatically detect serverless functions in `/api`

5. **Update Frontend Environment**
   - Copy your backend URL (e.g., `https://scheme-explainer-api.vercel.app`)
   - Go to frontend project settings → Environment Variables
   - Update `VITE_API_URL` with backend URL
   - Redeploy frontend

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy Backend**
```bash
vercel --prod
```

3. **Deploy Frontend**
```bash
cd frontend
vercel --prod
```

4. **Set Environment Variables**
```bash
vercel env add VITE_API_URL production
```

## CI/CD Pipeline

GitHub Actions automatically:
- Installs dependencies
- Builds the frontend
- Runs checks on every push to `main`

Vercel automatically deploys on every push to the connected branch.

## API Endpoints

### POST /api/explain
Explains a government scheme

**Request:**
```json
{
  "schemeName": "Pradhan Mantri Awas Yojana"
}
```

**Response:**
```json
{
  "summary": "...",
  "eligibility": "...",
  "benefits": "...",
  "process": "..."
}
```

## Customization

### Colors
Edit `frontend/tailwind.config.js`:
```js
colors: {
  primary: '#7DD3FC',
  accent: '#C7D2FE',
  muted: '#64748B'
}
```

### Mock Data
Replace mock responses in `api/explain.js` with actual AI integration (OpenAI, Anthropic, etc.)

## Production Checklist

- [ ] Update API endpoint with real AI integration
- [ ] Add rate limiting to API
- [ ] Set up error tracking (Sentry)
- [ ] Add analytics (Google Analytics, Plausible)
- [ ] Configure custom domain in Vercel
- [ ] Enable HTTPS (automatic with Vercel)
- [ ] Add SEO meta tags
- [ ] Test on multiple devices

## License

MIT

## Support

For issues or questions, please open a GitHub issue.
