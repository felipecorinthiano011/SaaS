# Frontend (Angular + Tailwind)

## Purpose

UI for authentication, job description input, resume upload, and analysis results.

## Structure

- `src/app/core/` shared services and cross-cutting client logic
- `src/app/features/` feature modules/components by domain
- `src/environments/` environment-based API URLs

## Run locally

```powershell
cd frontend
npm install
npm start
```

## Deploy to Vercel

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist/frontend/browser`

