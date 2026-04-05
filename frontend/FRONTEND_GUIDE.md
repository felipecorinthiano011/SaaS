# Angular Frontend - ResumeMatcher SaaS

## Overview

A comprehensive Angular-based frontend for the ResumeMatcher SaaS application. Built with Angular standalone components, TailwindCSS, and responsive design.

---

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts           # Authentication service
│   │   │   │   ├── resume-api.service.ts    # Resume analysis API
│   │   │   ├── interceptors/
│   │   │   │   └── auth.interceptor.ts      # JWT token interceptor
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   ├── login.component.ts
│   │   │   │   │   └── login.component.html
│   │   │   │   └── register/
│   │   │   │       ├── register.component.ts
│   │   │   │       └── register.component.html
│   │   │   └── dashboard/
│   │   │       ├── dashboard.component.ts
│   │   │       ├── dashboard.component.html
│   │   │       └── dashboard.component.css
│   │   ├── app.component.ts
│   │   └── app.routes.ts
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── angular.json
├── tailwind.config.js
├── package.json
└── tsconfig.json
```

---

## Features

### 1. Authentication Pages

#### Login Page (`/login`)
- Email and password input
- Form validation
- Error handling
- Link to registration
- Responsive design

#### Register Page (`/register`)
- Full name, email, password input
- Password confirmation validation
- Error handling
- Link to login
- Responsive design

### 2. Dashboard (`/dashboard`)

#### Job Description Input
- Text area for pasting job descriptions
- Minimum length validation
- Real-time input handling

#### Resume Upload
- File upload (PDF/DOCX)
- Automatic text extraction
- Manual text input fallback
- Upload status indication

#### Results Display
- **ATS Score**: Circular progress indicator (0-100)
- **Missing Keywords**: Clickable tags (copy to clipboard)
- **Improvement Suggestions**: Prioritized list (high/medium/low)
- **Optimized Resume**: Preview and download

#### Features
- Tab-based navigation (Input/Results)
- Real-time validation
- Error and success messages
- Loading states
- Responsive layout
- Sticky sidebar on desktop

---

## Core Services

### AuthService

Handles user authentication and session management.

```typescript
// Login
authService.login(email, password)

// Register
authService.register(email, password, name?)

// Logout
authService.logout()

// Check authentication
authService.isAuthenticated()

// Get current user
authService.currentUser$  // Observable
```

### ResumeApiService

Handles resume analysis and API calls.

```typescript
// Upload resume
resumeApiService.uploadResume(file)

// Extract keywords
resumeApiService.extractKeywords(jobDescription)

// Optimize resume
resumeApiService.optimizeResume(jobDescription, resumeText)

// Get analysis
resumeApiService.getAnalysis(id)

// Get all analyses
resumeApiService.getAllAnalyses()
```

### AuthInterceptor

Automatically adds JWT token to API requests.

```typescript
// Automatically adds: Authorization: Bearer <token>
// Handles 401 errors and redirects to login
```

---

## Components

### LoginComponent

**Inputs**: None (form-based)

**Outputs**: 
- Redirects to `/dashboard` on successful login
- Displays error messages on failure

**Features**:
- Email validation
- Password validation
- Loading state
- Error handling

### RegisterComponent

**Inputs**: None (form-based)

**Outputs**:
- Redirects to `/dashboard` on successful registration
- Displays error messages on failure

**Features**:
- Name validation
- Email validation
- Password matching validation
- Loading state
- Error handling

### DashboardComponent

**Inputs**: 
- Job description (textarea)
- Resume file or text (upload or paste)

**Outputs**:
- ATS score
- Missing keywords
- Improvement suggestions
- Optimized resume

**Features**:
- Tab navigation
- Real-time validation
- File upload with progress
- Results display and formatting
- Download functionality
- Responsive design
- Sticky sidebar

---

## Styling

### TailwindCSS

All styling uses TailwindCSS utility classes for:
- Responsive layout
- Color schemes
- Typography
- Spacing
- Shadows
- Animations

### Color Scheme

**Primary**: Blue (`bg-blue-600`)
**Success**: Green (`bg-green-600`)
**Warning**: Yellow (`bg-yellow-600`)
**Error**: Red (`bg-red-600`)
**Neutral**: Gray (`bg-gray-*`)

### Responsive Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

---

## User Flow

```
┌─────────────────────────────────────────────┐
│            Visit /login                      │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
       ▼                       ▼
   [Login]                 [Register]
       │                       │
       └───────────┬───────────┘
                   │
            JWT Token Stored
                   │
                   ▼
         ┌─────────────────────┐
         │  /dashboard         │
         ├─────────────────────┤
         │ 1. Paste Job Desc   │
         │ 2. Upload Resume    │
         │ 3. Click Analyze    │
         │ 4. View Results     │
         │ 5. Download Resume  │
         └─────────────────────┘
                   │
            [Logout] - Redirects to /login
```

---

## Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Angular CLI 17+

### Installation

```bash
cd frontend

# Install dependencies
npm install

# Install TailwindCSS (if not already done)
npm install -D tailwindcss postcss autoprefixer

# Configure TailwindCSS
npx tailwindcss init -p
```

### Configuration

Update `tailwind.config.js`:
```javascript
export default {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Update `src/styles.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Development Server

```bash
# Start development server
ng serve

# Or with npm
npm start

# Application runs on http://localhost:4200
```

### Build for Production

```bash
# Build for production
ng build --configuration production

# Output in dist/ directory
```

---

## API Integration

### Backend Endpoints

**Authentication**:
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

**Resume Analysis**:
- `POST /resume/upload` - Upload and extract resume text
- `POST /job/analyze` - Analyze job description against resume
- `GET /analysis/{id}` - Get analysis results
- `GET /analysis` - Get all user analyses

### AI Service Endpoints

**Keywords**:
- `POST /api/v1/keywords/extract` - Extract keywords from job description

---

## Environment Configuration

### Environment Files

**Development** (`environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080',
  aiServiceUrl: 'http://localhost:8000'
};
```

**Production** (`environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.resumematcher.com',
  aiServiceUrl: 'https://ai.resumematcher.com'
};
```

---

## Error Handling

### HTTP Errors

**401 Unauthorized**:
- Logged out and redirected to `/login`

**400 Bad Request**:
- Displayed in error message
- Form validation shown

**500 Server Error**:
- User-friendly error message displayed
- Error details logged to console

### Form Validation

**Email**: Required + valid format  
**Password**: Required + min 6 characters  
**Name**: Required  
**Confirm Password**: Must match password  
**Job Description**: Required + min 50 characters  
**Resume**: Required + min 50 characters

---

## Performance Optimizations

1. **Lazy Loading**: Components loaded on demand
2. **Change Detection**: OnPush strategy for components
3. **Tree Shaking**: Unused code removed in production build
4. **CSS**: TailwindCSS purged to only used classes
5. **Images**: Optimized and cached
6. **Bundle**: Minified and gzipped

---

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile: iOS Safari 12+, Chrome Android

---

## Testing

### Unit Tests

```bash
# Run unit tests
ng test

# Run with coverage
ng test --code-coverage
```

### E2E Tests

```bash
# Run E2E tests
ng e2e
```

---

## Accessibility

- ARIA labels on form inputs
- Semantic HTML
- Keyboard navigation support
- Color contrast compliance (WCAG AA)
- Screen reader friendly

---

## Security

1. **JWT Authentication**: Secure token-based auth
2. **HTTPS**: Only in production
3. **CORS**: Configured on backend
4. **CSP**: Content Security Policy headers
5. **Input Validation**: Frontend + backend validation
6. **XSS Protection**: Angular's built-in sanitization
7. **CSRF**: Protected with tokens

---

## Deployment

### To Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### To Docker

```bash
# Build image
docker build -t resumematcher-frontend -f docker/frontend.Dockerfile .

# Run container
docker run -p 4200:80 resumematcher-frontend
```

### To AWS S3

```bash
# Build for production
ng build --configuration production

# Sync to S3
aws s3 sync dist/frontend s3://your-bucket-name

# Invalidate CloudFront (if using CDN)
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

---

## Development Guidelines

### Code Style

- Use TypeScript strict mode
- Follow Angular style guide
- Use meaningful variable names
- Add comments for complex logic
- Use reactive patterns (Observables)

### Component Design

- Keep components focused and reusable
- Use dependency injection
- Use @Input/@Output for communication
- Unsubscribe from observables (OnDestroy)
- Use trackBy in *ngFor

### Template Best Practices

- Use structural directives correctly
- Bind to component properties
- Use two-way binding sparingly
- Use safe navigation operator (?.)
- Use async pipe for observables

---

## Troubleshooting

### Common Issues

**Port 4200 already in use**:
```bash
ng serve --port 4300
```

**Dependencies not installing**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Build fails**:
```bash
ng build --configuration production --verbose
```

**CORS errors**:
- Check backend CORS configuration
- Verify API URLs in environment files

---

## Future Enhancements

- [ ] Dark mode support
- [ ] Multi-language support (i18n)
- [ ] File drag-and-drop upload
- [ ] Resume history/versioning
- [ ] Comparison view (before/after)
- [ ] Social sharing
- [ ] PDF generation
- [ ] Offline support (PWA)
- [ ] Advanced analytics
- [ ] AI-powered suggestions

---

## Resources

- [Angular Documentation](https://angular.io/docs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [RxJS Documentation](https://rxjs.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

---

**Status**: Production Ready  
**Version**: 1.0  
**Last Updated**: April 5, 2026

