# Deployment Guide

## Backend Deployment (Render)

1. **Go to [Render](https://render.com)** and sign in with GitHub
2. Click **"New +" → "Web Service"**
3. Connect your GitHub repository: `ASTHA22/Disaster-Intelligence-Mapping-Platform-DIMP`
4. Configure:
   - **Name**: `dimp-backend`
   - **Region**: Singapore (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   - Add `HERE_API_KEY` with your HERE API key
6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Copy the backend URL (e.g., `https://dimp-backend.onrender.com`)

## Frontend Deployment (Vercel)

1. **Go to [Vercel](https://vercel.com)** and sign in with GitHub
2. Click **"Add New" → "Project"**
3. Import your repository: `ASTHA22/Disaster-Intelligence-Mapping-Platform-DIMP`
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. **Environment Variables**:
   - Add `REACT_APP_API_URL` with your Render backend URL (from step 8 above)
6. Click **"Deploy"**
7. Wait for deployment (3-5 minutes)
8. Your app will be live at `https://your-project.vercel.app`

## Update Frontend API URL

After backend is deployed, update the frontend to use the production API:

1. In Vercel dashboard, go to **Settings → Environment Variables**
2. Add: `REACT_APP_API_URL` = `https://dimp-backend.onrender.com` (your Render URL)
3. Redeploy the frontend

## Testing

1. Visit your Vercel URL
2. Check if the map loads
3. Test "Calculate Route" and "Show Coverage" features
4. Verify data is loading from the backend

## Troubleshooting

- **Backend not responding**: Check Render logs for errors
- **Frontend can't connect**: Verify `REACT_APP_API_URL` is set correctly
- **CORS errors**: Backend already has CORS enabled for all origins
- **HERE API errors**: Verify your HERE API key is set in Render environment variables

## Free Tier Limitations

- **Render Free**: Backend sleeps after 15 min of inactivity (first request takes ~30s to wake up)
- **Vercel Free**: Unlimited deployments, 100GB bandwidth/month
