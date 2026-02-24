# Quick Start: Deploying to Vercel

## 1. Install Vercel CLI
```bash
npm install -g vercel
```

## 2. Login to Vercel
```bash
vercel login
```

## 3. Deploy
From the project root directory:
```bash
vercel
```

## 4. Set Environment Variables
After the first deployment:
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings → Environment Variables**
4. Add this variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-project.vercel.app/api`
   - **Environments**: Select all (Production, Preview, Development)
5. Click **Save**

## 5. Trigger Redeploy
After adding environment variables, redeploy:
```bash
vercel --prod
```

## Local Development

Create `.env.local` in `deeptrace-frontend/`:
```
VITE_API_URL=http://localhost:5000/api
```

Then run:
```bash
# Terminal 1: Backend
cd deeptrace-backend
python app.py

# Terminal 2: Frontend
cd deeptrace-frontend
npm run dev
```

## Files Modified/Created

✅ **Modified:**
- `deeptrace-frontend/src/services/api.js` - Use environment variables
- `deeptrace-frontend/package.json` - Added build script
- `deeptrace-backend/app.py` - Use PORT from environment

✅ **Created:**
- `vercel.json` - Vercel configuration
- `.vercelignore` - Deployment ignore list
- `api/index.py` - Serverless function entry point
- `deeptrace-frontend/.env.example` - Frontend env template
- `deeptrace-backend/.env.example` - Backend env template
- `deeptrace-frontend/.env.local.example` - Local dev template
- `deeptrace-backend/runtime.txt` - Python version (3.11)
- `VERCEL_DEPLOYMENT.md` - Detailed deployment guide

## Next Steps

1. Test locally with the environment variables
2. Push changes to GitHub
3. Connect your GitHub repo to Vercel
4. Set environment variables in Vercel dashboard
5. Deploy and monitor the build logs

Need help? Check `VERCEL_DEPLOYMENT.md` for troubleshooting.
