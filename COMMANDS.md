# ⚡ COMMANDS CHEAT SHEET

## 🚀 Quick Commands

### Install & Setup
```bash
# Automated setup (recommended)
./setup.sh

# Manual setup
npm install
cd frontend && npm install && cd ..
```

### Development
```bash
# Start frontend dev server (port 3000)
npm run dev:frontend

# Alternative (from frontend directory)
cd frontend
npm run dev
```

### Build
```bash
# Build frontend for production
npm run build:frontend

# Alternative (from frontend directory)
cd frontend
npm run build
```

### Preview Production Build
```bash
cd frontend
npm run preview
```

---

## 📦 Package Management

### Install Dependencies
```bash
# Install all dependencies
npm run install:all

# Install frontend only
cd frontend && npm install

# Install specific package (frontend)
cd frontend && npm install <package-name>
```

### Update Dependencies
```bash
# Update all packages
cd frontend && npm update

# Check for outdated packages
cd frontend && npm outdated
```

---

## 🔧 Git Commands

### Initial Setup
```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Scheme Explainer"

# Add remote
git remote add origin https://github.com/yourusername/ai-scheme-explainer.git

# Push to GitHub
git push -u origin main
```

### Regular Updates
```bash
# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "Your commit message"

# Push to GitHub
git push
```

### Pull Latest Changes
```bash
# Pull from GitHub
git pull origin main
```

---

## 🌐 Vercel Deployment

### Using Vercel CLI
```bash
# Install Vercel CLI globally
npm i -g vercel

# Login to Vercel
vercel login

# Deploy backend (from root)
vercel --prod

# Deploy frontend (from frontend directory)
cd frontend
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
```

### Using Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository
4. Configure and deploy

---

## 🧪 Testing & Debugging

### Check if Node.js is installed
```bash
node --version
# Should show v18.x.x or higher
```

### Check if npm is installed
```bash
npm --version
# Should show 9.x.x or higher
```

### Test API locally (if you have a local server)
```bash
curl -X POST http://localhost:3001/api/explain \
  -H "Content-Type: application/json" \
  -d '{"schemeName":"PMAY"}'
```

### Check frontend build
```bash
cd frontend
npm run build
# Should create dist/ folder
```

### Clear cache and reinstall
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📁 File Operations

### View project structure
```bash
# List all files
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*'

# Count files
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | wc -l

# List only source files
find frontend/src -type f
```

### Check file sizes
```bash
# Frontend bundle size
cd frontend
npm run build
du -sh dist/
```

---

## 🔍 Troubleshooting Commands

### Port already in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
cd frontend
npm run dev -- --port 3001
```

### Permission denied on setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

### Module not found errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Vercel deployment fails
```bash
# Check Vercel logs
vercel logs

# Redeploy
vercel --prod --force
```

---

## 📊 Useful Checks

### Check installed packages
```bash
cd frontend
npm list --depth=0
```

### Check for security vulnerabilities
```bash
cd frontend
npm audit

# Fix vulnerabilities
npm audit fix
```

### Check bundle size
```bash
cd frontend
npm run build
ls -lh dist/assets/
```

---

## 🎨 Customization Commands

### Change Tailwind config
```bash
# Edit colors
nano frontend/tailwind.config.js

# Rebuild
cd frontend && npm run dev
```

### Add new component
```bash
# Create new component file
touch frontend/src/components/NewComponent.jsx

# Edit the file
nano frontend/src/components/NewComponent.jsx
```

### Add new page
```bash
# Create new page file
touch frontend/src/pages/NewPage.jsx

# Edit App.jsx to add route
nano frontend/src/App.jsx
```

---

## 🔐 Environment Variables

### Create .env file
```bash
# Frontend
echo "VITE_API_URL=http://localhost:3001" > frontend/.env

# Or edit manually
nano frontend/.env
```

### View environment variables (Vercel)
```bash
vercel env ls
```

### Add environment variable (Vercel)
```bash
vercel env add VITE_API_URL production
# Then enter the value when prompted
```

---

## 📝 Documentation Commands

### View README
```bash
cat README.md
# Or
less README.md
```

### View specific documentation
```bash
cat DEPLOYMENT.md
cat STRUCTURE.md
cat UI_DESIGN.md
cat ARCHITECTURE.md
```

### Search in documentation
```bash
grep -r "deployment" *.md
```

---

## 🚨 Emergency Commands

### Complete reset
```bash
# Remove all node_modules
rm -rf node_modules frontend/node_modules api/node_modules

# Remove all lock files
rm -f package-lock.json frontend/package-lock.json api/package-lock.json

# Reinstall everything
./setup.sh
```

### Rollback to previous commit
```bash
# View commit history
git log --oneline

# Rollback to specific commit
git reset --hard <commit-hash>

# Force push (be careful!)
git push --force
```

### Delete Vercel deployment
```bash
# List deployments
vercel ls

# Remove deployment
vercel rm <deployment-name>
```

---

## 📈 Performance Commands

### Analyze bundle
```bash
cd frontend
npm run build
npx vite-bundle-visualizer
```

### Check build time
```bash
cd frontend
time npm run build
```

### Check dev server startup time
```bash
cd frontend
time npm run dev
```

---

## 🎯 Common Workflows

### Daily Development
```bash
# 1. Pull latest changes
git pull

# 2. Install any new dependencies
cd frontend && npm install && cd ..

# 3. Start dev server
npm run dev:frontend

# 4. Make changes...

# 5. Commit and push
git add .
git commit -m "Your changes"
git push
```

### Before Deployment
```bash
# 1. Test build locally
cd frontend && npm run build

# 2. Preview production build
npm run preview

# 3. Commit all changes
git add .
git commit -m "Ready for deployment"

# 4. Push to GitHub
git push

# 5. Vercel auto-deploys
```

### Adding New Feature
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes...

# 3. Test locally
npm run dev:frontend

# 4. Commit changes
git add .
git commit -m "Add new feature"

# 5. Push branch
git push origin feature/new-feature

# 6. Create pull request on GitHub

# 7. Merge and deploy
```

---

## 💡 Pro Tips

```bash
# Use aliases for common commands
alias dev="npm run dev:frontend"
alias build="npm run build:frontend"

# Add to ~/.bashrc or ~/.zshrc
echo 'alias dev="npm run dev:frontend"' >> ~/.bashrc
source ~/.bashrc

# Now just type:
dev
```

---

## 📞 Help Commands

```bash
# npm help
npm help

# Vercel help
vercel help

# Git help
git help

# Node.js version
node --version

# npm version
npm --version
```

---

**Quick Reference:**
- Dev: `npm run dev:frontend`
- Build: `npm run build:frontend`
- Deploy: Push to GitHub (auto-deploys via Vercel)
- Docs: See README.md, DEPLOYMENT.md, etc.
