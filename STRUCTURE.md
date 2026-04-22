# Project Structure Overview

```
ai-scheme-explainer/
│
├── frontend/                          # React Frontend Application
│   ├── src/
│   │   ├── components/               # Reusable UI Components
│   │   │   ├── Navbar.jsx           # Top navigation bar
│   │   │   ├── Footer.jsx           # Bottom footer
│   │   │   ├── Card.jsx             # Card container component
│   │   │   ├── Button.jsx           # Button component
│   │   │   ├── Input.jsx            # Input field component
│   │   │   └── Skeleton.jsx         # Loading skeleton
│   │   │
│   │   ├── pages/                   # Page Components
│   │   │   ├── Home.jsx             # Landing page with search
│   │   │   ├── Results.jsx          # Scheme explanation results
│   │   │   └── Compare.jsx          # Scheme comparison page
│   │   │
│   │   ├── services/                # API Integration
│   │   │   └── api.js               # API service functions
│   │   │
│   │   ├── App.jsx                  # Main app component with routing
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Global styles
│   │
│   ├── index.html                   # HTML entry point
│   ├── package.json                 # Frontend dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── tailwind.config.js          # Tailwind CSS config
│   ├── postcss.config.js           # PostCSS config
│   └── .env.example                # Environment variables template
│
├── api/                             # Backend API (Vercel Serverless)
│   ├── explain.js                  # Main API endpoint
│   └── package.json                # API dependencies
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD
│
├── vercel.json                     # Vercel deployment config
├── package.json                    # Root package.json
├── .gitignore                      # Git ignore rules
├── README.md                       # Main documentation
└── DEPLOYMENT.md                   # Deployment guide
```

## Key Files Explained

### Frontend

**App.jsx**: Main application component with React Router setup
- Defines routes for Home, Results, and Compare pages
- Includes Navbar and Footer on all pages

**pages/Home.jsx**: Landing page
- Hero section with search input
- Popular schemes grid
- Feature cards

**pages/Results.jsx**: Displays scheme explanation
- Four cards: Summary, Eligibility, Benefits, Process
- Copy-to-clipboard functionality
- Loading states and error handling

**pages/Compare.jsx**: Side-by-side scheme comparison
- Two input fields for scheme names
- Parallel API calls
- Split-view results

**services/api.js**: API integration layer
- Axios-based HTTP client
- Environment-aware API URL

### Backend

**api/explain.js**: Serverless function
- POST endpoint accepting scheme name
- Returns mock AI-generated explanations
- Ready for real AI integration

### Configuration

**vercel.json**: Vercel deployment settings
- API routes configuration
- CORS headers
- Build settings

**tailwind.config.js**: Design system
- Custom color palette
- Theme extensions

## Component Hierarchy

```
App
├── Navbar
├── Routes
│   ├── Home
│   │   ├── Input
│   │   ├── Button
│   │   └── Card (multiple)
│   ├── Results
│   │   ├── Card (multiple)
│   │   ├── Button
│   │   └── Skeleton (loading)
│   └── Compare
│       ├── Input (2x)
│       ├── Button
│       └── Card (multiple)
└── Footer
```

## Data Flow

1. User enters scheme name in Input component
2. Button click triggers navigation to Results page
3. Results page calls `explainScheme()` from api.js
4. API service makes POST request to `/api/explain`
5. Serverless function processes request and returns data
6. Results page displays data in Card components

## Styling System

- **Tailwind CSS**: Utility-first CSS framework
- **Color Palette**:
  - Primary: `#7DD3FC` (sky blue)
  - Accent: `#C7D2FE` (lavender)
  - Muted: `#64748B` (slate gray)
  - Background: `#F8FAFC` (off-white)
- **Typography**: System sans-serif stack
- **Spacing**: Generous padding and margins
- **Effects**: Subtle shadows, smooth transitions

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=https://your-backend-url.vercel.app
```

### Vercel Dashboard
Set `VITE_API_URL` in project settings → Environment Variables
