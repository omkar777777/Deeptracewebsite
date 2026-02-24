# DeepTrace - Vercel Deployment Guide

## Overview
This project is configured for deployment on Vercel with:
- **Frontend**: React + Vite (static site)
- **Backend**: Flask Python (serverless functions)

## Pre-Deployment Checklist

### 1. Environment Variables
Create environment variables in your Vercel project dashboard:

**Frontend Environment Variables:**
- `VITE_API_URL`: The backend API URL (e.g., `https://your-project.vercel.app/api`)

**Backend Environment Variables:**
- `FLASK_DEBUG`: Set to `False` (recommended for production)
- `PORT`: Automatically set by Vercel (default: 5000)

### 2. Local Testing

Before deploying, test locally:

```bash
# Install dependencies
cd deeptrace-frontend
npm install
cd ../deeptrace-backend
pip install -r requirements.txt

# Run frontend (dev mode)
cd deeptrace-frontend
npm run dev

# Run backend (in another terminal)
cd deeptrace-backend
python app.py
```

Then set the API URL in your browser:
- Create `.env.local` in `deeptrace-frontend/`:
  ```
  VITE_API_URL=http://localhost:5000/api
  ```

## Deployment Steps

### 1. Connect to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

### 2. Configure Environment Variables in Vercel Dashboard

After your first deployment:
1. Go to your project on [Vercel Dashboard](https://vercel.com/dashboard)
2. Navigate to **Settings → Environment Variables**
3. Add the environment variables listed above

### 3. Set Production URL

Once deployed, update the environment variable:
- `VITE_API_URL`: `https://<your-vercel-project>.vercel.app/api`

## Project Structure

```
/
├── deeptrace-frontend/       # React + Vite frontend
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── deeptrace-backend/        # Flask backend
│   ├── app.py               # Main Flask app
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   ├── stego/
│   ├── steganalysis/
│   ├── crypto/
│   ├── watermark/
│   └── utils/
│
├── api/
│   └── index.py            # Vercel serverless entry point
│
├── vercel.json             # Vercel configuration
├── .vercelignore           # Files to ignore during deployment
└── README.md
```

## Key Configuration Files

### `vercel.json`
Defines the build and routing configuration for Vercel:
- Builds the frontend with Vite
- Runs Python backend as serverless functions
- Routes `/api/*` requests to the backend
- Routes all other requests to the frontend

### `.vercelignore`
Specifies files and directories to exclude from deployment:
- Node modules and Python cache
- Development files and logs
- Debug files
- Git configuration

### Environment Variables
- `deeptrace-frontend/.env.example`: Frontend configuration template
- `deeptrace-backend/.env.example`: Backend configuration template

## Troubleshooting

### Issue: "Module not found" error
- Ensure all dependencies in `deeptrace-backend/requirements.txt` are listed
- Check that relative imports are correct in the backend

### Issue: CORS errors
- CORS is already enabled in `app.py` with Flask-CORS
- Verify the `VITE_API_URL` environment variable matches your deployment URL

### Issue: File upload limits
- Vercel has a 50MB payload limit for serverless functions
- The backend limits file uploads to 20MB for security

### Issue: Backend timeouts
- Vercel serverless functions have a maximum execution time
- Complex operations may need optimization or a separate backend deployment

## Production Optimization

### Frontend
- Vite automatically optimizes the build with code splitting
- Consider adding image optimization tools
- Enable gzip compression (Vercel does this automatically)

### Backend
- For heavy computational tasks, consider:
  - Increasing function timeout (Vercel Pro plan)
  - Using a separate backend deployment (e.g., Railway, Heroku)
- Monitor function logs in Vercel dashboard

## Alternative: Separate Backend Deployment

If the Python backend needs more resources:

1. Deploy backend separately to:
   - [Railway.app](https://railway.app)
   - [Render.com](https://render.com)
   - [PythonAnywhere](https://www.pythonanywhere.com)

2. Update `VITE_API_URL` to the external backend URL

## Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Support](https://vercel.com/docs/serverless-functions/python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vite Documentation](https://vitejs.dev/)

## Support

For issues or questions:
1. Check Vercel logs: `vercel logs`
2. Review browser console for frontend errors
3. Check the Vercel dashboard for deployment status
