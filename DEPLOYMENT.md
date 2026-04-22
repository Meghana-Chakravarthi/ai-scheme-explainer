# Deployment Guide - Step by Step

## Prerequisites
- GitHub account
- Vercel account (free tier works)
- Git installed locally

## Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Scheme Explainer"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/ai-scheme-explainer.git

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy Backend API to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"New Project"**
3. Import your GitHub repository
4. Configure the project:
   - **Project Name**: `scheme-explainer-api`
   - **Framework Preset**: Other
   - **Root Directory**: `.` (leave as root)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
5. Click **"Deploy"**
6. Wait for deployment to complete
7. **Copy the deployment URL** (e.g., `https://scheme-explainer-api.vercel.app`)

## Step 3: Deploy Frontend to Vercel

1. In Vercel dashboard, click **"New Project"** again
2. Import the **same GitHub repository**
3. Configure the project:
   - **Project Name**: `scheme-explainer-frontend`
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: Your backend URL from Step 2 (e.g., `https://scheme-explainer-api.vercel.app`)
5. Click **"Deploy"**
6. Wait for deployment to complete

## Step 4: Test Your Application

1. Open your frontend URL (e.g., `https://scheme-explainer-frontend.vercel.app`)
2. Try searching for a scheme (e.g., "PMAY")
3. Verify the results page loads correctly
4. Test the compare feature

## Step 5: Configure Custom Domain (Optional)

### For Frontend:
1. Go to your frontend project in Vercel
2. Click **Settings** → **Domains**
3. Add your custom domain
4. Follow DNS configuration instructions

### For Backend:
1. Go to your backend project in Vercel
2. Click **Settings** → **Domains**
3. Add API subdomain (e.g., `api.yourdomain.com`)
4. Update frontend environment variable with new API URL

## Troubleshooting

### Frontend can't connect to backend
- Check `VITE_API_URL` environment variable in Vercel
- Ensure backend URL doesn't have trailing slash
- Check browser console for CORS errors

### Build fails
- Check Node.js version (should be 18+)
- Verify all dependencies are in package.json
- Check build logs in Vercel dashboard

### API returns 404
- Verify `/api` folder exists in root
- Check `vercel.json` configuration
- Ensure backend is deployed to root directory

## Automatic Deployments

Once connected to GitHub:
- Every push to `main` branch triggers automatic deployment
- Pull requests create preview deployments
- GitHub Actions runs CI checks before deployment

## Monitoring

- View deployment logs in Vercel dashboard
- Check function logs for API errors
- Monitor performance in Vercel Analytics (free tier available)

## Next Steps

1. Replace mock AI responses with real AI integration
2. Add authentication if needed
3. Set up error tracking (Sentry)
4. Configure analytics
5. Add rate limiting to API
