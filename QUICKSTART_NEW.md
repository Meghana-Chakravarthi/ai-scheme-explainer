# 🎯 QUICK START GUIDE

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies (2 minutes)
```bash
./setup.sh
```
This will install all required packages for frontend and backend.

### Step 2: Start Development Server (30 seconds)
```bash
npm run dev:frontend
```
The app will start at `http://localhost:3000`

### Step 3: Open Browser
Visit: **http://localhost:3000**

---

## 🌐 Deploy to Production (10 minutes)

### Prerequisites
- GitHub account
- Vercel account (free)

### Deployment Steps

#### 1️⃣ Push to GitHub
```bash
git add .
git commit -m "Complete AI Scheme Explainer"
git push origin main
```

#### 2️⃣ Deploy Backend
1. Go to [vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import your GitHub repository
4. Settings:
   - Project Name: `scheme-explainer-api`
   - Root Directory: `.` (root)
5. Click **"Deploy"**
6. **Copy the URL** (e.g., `https://scheme-explainer-api.vercel.app`)

#### 3️⃣ Deploy Frontend
1. Click **"New Project"** again
2. Import the **same repository**
3. Settings:
   - Project Name: `scheme-explainer-frontend`
   - Framework: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: Your backend URL from step 2
5. Click **"Deploy"**

#### 4️⃣ Done! 🎉
Your app is live at `https://scheme-explainer-frontend.vercel.app`

---

## 📱 Test Your App

### Local Testing
1. Search for "PMAY" or "Ayushman Bharat"
2. View the results page with 4 cards
3. Try the Compare feature
4. Test on mobile (resize browser)

### Production Testing
1. Open your Vercel URL
2. Test all features
3. Check mobile responsiveness
4. Verify API is working

---

## 🎨 What You Built

### Pages
1. **Home** - Search + popular schemes
2. **Results** - Detailed explanation (4 sections)
3. **Compare** - Side-by-side comparison

### Features
- ✅ AI-powered explanations (mock data ready)
- ✅ Responsive design
- ✅ Loading states
- ✅ Error handling
- ✅ Copy-to-clipboard
- ✅ Smooth animations

---

## 🔧 Customize

### Change Colors
Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  primary: '#7DD3FC',  // Change this
  accent: '#C7D2FE',   // Change this
  muted: '#64748B'     // Change this
}
```

### Add Real AI
Edit `api/explain.js` and replace mock data with:
```javascript
// OpenAI example
import OpenAI from 'openai'
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

const completion = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    { role: "system", content: "Explain government schemes" },
    { role: "user", content: `Explain ${schemeName}` }
  ]
})
```

---

## 📚 Documentation

- **README.md** - Full project overview
- **DEPLOYMENT.md** - Detailed deployment guide
- **STRUCTURE.md** - Project architecture
- **UI_DESIGN.md** - Design system
- **SUMMARY.md** - Complete summary

---

## 🆘 Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API not responding
- Check `VITE_API_URL` in frontend/.env
- Verify backend is deployed
- Check Vercel function logs

### Build fails on Vercel
- Verify Node.js version is 18+
- Check build logs in Vercel dashboard
- Ensure all dependencies are in package.json

---

## ✅ Checklist

Before deploying, verify:
- [ ] All dependencies installed (`./setup.sh`)
- [ ] App runs locally (`npm run dev:frontend`)
- [ ] All pages load correctly
- [ ] Search works
- [ ] Compare works
- [ ] Responsive on mobile
- [ ] Code pushed to GitHub
- [ ] Backend deployed to Vercel
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set
- [ ] Production app tested

---

## 🎯 Next Steps

### Immediate
1. Test locally
2. Deploy to Vercel
3. Share your app!

### Short Term
1. Add real AI integration
2. Customize colors/branding
3. Add more schemes

### Long Term
1. User authentication
2. Save favorites
3. Analytics
4. Mobile app

---

## 💡 Tips

- **Development**: Use `npm run dev:frontend` for hot reload
- **Production**: Vercel auto-deploys on git push
- **Environment**: Set variables in Vercel dashboard
- **Logs**: Check Vercel function logs for debugging

---

## 🎉 You're Ready!

Everything is set up and ready to go. Just run:

```bash
./setup.sh
npm run dev:frontend
```

Then visit: **http://localhost:3000**

---

**Need Help?**
- Check DEPLOYMENT.md for detailed instructions
- Review STRUCTURE.md for architecture
- See UI_DESIGN.md for design system

**Happy Coding! 🚀**
