# 🚀 Quick Reference - Deployed App

## Live URLs

**Frontend**: https://scheme-explainer-frontend.vercel.app
**Backend**: https://scheme-explainer-api.vercel.app

## Quick Actions

### Visit Your App
```
https://scheme-explainer-frontend.vercel.app
```

### Test Backend API
```bash
curl -X POST https://scheme-explainer-api.vercel.app/api/explain.js \
  -H "Content-Type: application/json" \
  -d '{"schemeName":"PMAY"}'
```

### Redeploy
```bash
./deploy.sh
```

### View Logs
- Backend: https://vercel.com/rmr2024s-projects/scheme-explainer-api
- Frontend: https://vercel.com/rmr2024s-projects/scheme-explainer-frontend

## Deployment Status

✅ Backend: Live
✅ Frontend: Live
✅ API: Working
✅ HTTPS: Enabled
✅ Auto-deploy: Enabled

## Environment Variables

**Frontend**:
- VITE_API_URL = https://scheme-explainer-api.vercel.app

## Next Steps

1. Visit the app and test features
2. Share with others
3. Add real AI integration
4. Customize design

---

**Deployed**: April 22, 2026
**Status**: 100% Operational
