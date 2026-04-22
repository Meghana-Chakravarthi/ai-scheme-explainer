# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                     http://localhost:3000                    │
│                  (or Vercel Frontend URL)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    REACT FRONTEND                            │
│                  (Vite + Tailwind CSS)                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     Home     │  │   Results    │  │   Compare    │     │
│  │     Page     │  │     Page     │  │     Page     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              UI Components Layer                      │  │
│  │  Navbar | Footer | Card | Button | Input | Skeleton  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Service (Axios)                      │  │
│  │         explainScheme(schemeName)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ POST /api/explain
                         │ { schemeName: "..." }
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  VERCEL SERVERLESS API                       │
│                    (Node.js Backend)                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              /api/explain.js                          │  │
│  │                                                        │  │
│  │  1. Receive scheme name                               │  │
│  │  2. Process request                                   │  │
│  │  3. Generate/fetch explanation                        │  │
│  │  4. Return JSON response                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Response:                                                   │
│  {                                                           │
│    summary: "...",                                           │
│    eligibility: "...",                                       │
│    benefits: "...",                                          │
│    process: "..."                                            │
│  }                                                           │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Action → Component → API Service → Backend → Response → UI Update

Example: Search for "PMAY"

1. User types "PMAY" in Input component
2. User clicks Search button
3. Navigate to Results page
4. Results page calls explainScheme("PMAY")
5. API service makes POST to /api/explain
6. Backend processes request
7. Backend returns explanation data
8. Results page displays 4 cards with data
```

## Component Hierarchy

```
App
├── Navbar
│   ├── Logo (FileText icon)
│   ├── Navigation Links
│   └── User Avatar
│
├── Router
│   │
│   ├── Home Page
│   │   ├── Hero Section
│   │   │   ├── Badge (Sparkles icon)
│   │   │   ├── Heading
│   │   │   ├── Subtext
│   │   │   └── Search Box
│   │   │       ├── Input
│   │   │       └── Button
│   │   │
│   │   ├── Popular Schemes Grid
│   │   │   └── Card (x4)
│   │   │
│   │   └── Features Grid
│   │       └── Card (x3)
│   │
│   ├── Results Page
│   │   ├── Header
│   │   │   ├── Scheme Name
│   │   │   └── Subtitle
│   │   │
│   │   ├── Explanation Grid
│   │   │   ├── Summary Card
│   │   │   ├── Eligibility Card
│   │   │   ├── Benefits Card
│   │   │   └── Process Card
│   │   │
│   │   └── Actions
│   │       └── Button (Explain Simpler)
│   │
│   └── Compare Page
│       ├── Header
│       ├── Input Section
│       │   ├── Input (Scheme 1)
│       │   ├── Input (Scheme 2)
│       │   └── Button (Compare)
│       │
│       └── Comparison Grid
│           ├── Scheme 1 Column
│           │   └── Card (x4)
│           └── Scheme 2 Column
│               └── Card (x4)
│
└── Footer
    ├── Copyright
    └── Links
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND STACK                        │
├─────────────────────────────────────────────────────────┤
│  React 18.2.0          │  UI Framework                  │
│  Vite 5.1.4            │  Build Tool                    │
│  Tailwind CSS 3.4.1    │  Styling                       │
│  React Router 6.22.0   │  Routing                       │
│  Lucide React 0.344.0  │  Icons                         │
│  Axios 1.6.7           │  HTTP Client                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    BACKEND STACK                         │
├─────────────────────────────────────────────────────────┤
│  Node.js 18+           │  Runtime                       │
│  Vercel Functions      │  Serverless                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    DEVOPS STACK                          │
├─────────────────────────────────────────────────────────┤
│  GitHub Actions        │  CI/CD                         │
│  Vercel                │  Hosting & Deployment          │
│  Git                   │  Version Control               │
└─────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      GITHUB REPO                         │
│              ai-scheme-explainer                         │
└────────────┬────────────────────────┬───────────────────┘
             │                        │
             │ Push to main           │ Push to main
             │                        │
┌────────────▼──────────┐  ┌─────────▼──────────────────┐
│   VERCEL PROJECT 1    │  │   VERCEL PROJECT 2         │
│   (Backend API)       │  │   (Frontend)               │
│                       │  │                            │
│  Root: .              │  │  Root: frontend            │
│  Auto-detect: API     │  │  Framework: Vite           │
│                       │  │  Build: npm run build      │
│  URL:                 │  │  Output: dist              │
│  scheme-api.vercel.app│  │                            │
└───────────────────────┘  │  Env: VITE_API_URL         │
                           │                            │
                           │  URL:                      │
                           │  scheme-app.vercel.app     │
                           └────────────────────────────┘
```

## Request/Response Flow

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Enter "PMAY"
     │
┌────▼─────────────────────────────────────────────────┐
│  Home Page                                           │
│  - Input: "PMAY"                                     │
│  - Click Search                                      │
└────┬─────────────────────────────────────────────────┘
     │
     │ 2. Navigate to /results
     │
┌────▼─────────────────────────────────────────────────┐
│  Results Page                                        │
│  - useEffect triggers                                │
│  - Call explainScheme("PMAY")                        │
└────┬─────────────────────────────────────────────────┘
     │
     │ 3. POST /api/explain
     │    { schemeName: "PMAY" }
     │
┌────▼─────────────────────────────────────────────────┐
│  API Service (api.js)                                │
│  - axios.post(API_URL + '/api/explain', data)       │
└────┬─────────────────────────────────────────────────┘
     │
     │ 4. HTTP Request
     │
┌────▼─────────────────────────────────────────────────┐
│  Vercel Serverless Function                          │
│  /api/explain.js                                     │
│  - Validate input                                    │
│  - Generate/fetch explanation                        │
│  - Return JSON                                       │
└────┬─────────────────────────────────────────────────┘
     │
     │ 5. Response
     │    {
     │      summary: "...",
     │      eligibility: "...",
     │      benefits: "...",
     │      process: "..."
     │    }
     │
┌────▼─────────────────────────────────────────────────┐
│  Results Page                                        │
│  - setData(response)                                 │
│  - Render 4 cards                                    │
│  - Show copy buttons                                 │
└──────────────────────────────────────────────────────┘
```

## File Organization

```
Frontend Files:
├── Entry Point: index.html → main.jsx → App.jsx
├── Routing: App.jsx (React Router)
├── Pages: Home.jsx, Results.jsx, Compare.jsx
├── Components: Navbar, Footer, Card, Button, Input, Skeleton
├── Services: api.js (Axios wrapper)
└── Styles: index.css (Tailwind)

Backend Files:
└── API: api/explain.js (Serverless function)

Config Files:
├── Frontend: vite.config.js, tailwind.config.js, postcss.config.js
├── Backend: vercel.json
├── CI/CD: .github/workflows/ci.yml
└── Package: package.json (root + frontend + api)
```

## State Management

```
No global state management needed (simple app)

Local State (useState):
- Home: schemeName (search input)
- Results: data, loading, error
- Compare: scheme1, scheme2, data1, data2, loading

Navigation State (React Router):
- location.state.schemeName (passed between pages)
```

## API Contract

```
Endpoint: POST /api/explain

Request:
{
  "schemeName": string (required)
}

Response (Success - 200):
{
  "summary": string,
  "eligibility": string,
  "benefits": string,
  "process": string
}

Response (Error - 400):
{
  "error": string
}

Response (Error - 405):
{
  "error": "Method not allowed"
}
```

## Environment Variables

```
Frontend (.env):
VITE_API_URL=https://your-backend.vercel.app

Backend (Vercel Dashboard):
(None required for mock data)
(Add OPENAI_API_KEY for real AI)
```

---

**This architecture is:**
- ✅ Scalable (serverless)
- ✅ Fast (Vite + CDN)
- ✅ Maintainable (modular)
- ✅ Production-ready
