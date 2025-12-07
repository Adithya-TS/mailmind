# MailMind Web Application 🌐

## Modern Client-Side OAuth - No credentials.json Required!

This version uses **Google Sign-In** (client-side OAuth) for a cleaner, simpler authentication flow.

---

## 🚀 Quick Start

### 1. Configure .env

Add your Google OAuth credentials to `.env`:

```env
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install & Run

```bash
pip install -r requirements.txt
python app.py
```

### 3. Open & Sign In

1. Go to http://localhost:5000
2. Click "Sign in with Google"
3. Grant permissions
4. Generate summaries!

---

## ✨ Features

- 🎨 **Beautiful Web UI** - Clean, modern interface
- 🔐 **Google Sign-In** - One-click authentication
- 📊 **AI Summaries** - Priority categorization (High/Medium/Low)
- 📚 **History** - View all past summaries
- 🔒 **Secure** - Token verification server-side
- 📱 **Responsive** - Works on all devices

---

## 📡 API Endpoints

### Authentication

**POST /api/auth/google**
- Verify Google ID token and create session
- Body: `{"id_token": "...", "access_token": "..."}`
- Response: `{"success": true, "user": {...}}`

### Email Summary

**POST /api/generate**
- Generate AI-powered email summary
- Requires: Authenticated session
- Response:
```json
{
  "success": true,
  "summary": "High Priority:\n• Email 1...",
  "file_path": "summaries/summary_2025-12-07_19-30-45.txt",
  "email_count": 20
}
```

### Pages

- `GET /` - Home page
- `GET /logout` - Logout and clear session
- `GET /summary/<filename>` - View specific past summary

---

## 🔧 How It Works

### Authentication Flow:

```
1. User clicks "Sign in with Google" button
   ↓
2. Google Sign-In popup/redirect
   ↓
3. User grants permissions
   ↓
4. Google returns ID token to frontend
   ↓
5. Frontend sends token to /api/auth/google
   ↓
6. Backend verifies token with Google
   ↓
7. Backend creates session
   ↓
8. User is authenticated!
```

### Summary Generation:

```
1. User clicks "Generate Summary"
   ↓
2. Frontend calls POST /api/generate
   ↓
3. Backend fetches 20 recent emails from Gmail
   ↓
4. Backend sends to Gemini AI for categorization
   ↓
5. AI returns prioritized summary
   ↓
6. Backend saves to summaries/ folder
   ↓
7. Frontend displays summary
```

---

## 🎯 Google Cloud Console Setup

### Create OAuth Client:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click "Create Credentials" > "OAuth client ID"
3. Application type: **Web application**
4. Name: "MailMind Web"
5. Authorized JavaScript origins:
   ```
   http://localhost:5000
   ```
6. Authorized redirect URIs:
   ```
   http://localhost:5000
   ```
7. Click "Create"
8. Copy Client ID and Client Secret to `.env`

### Enable APIs:

- Gmail API
- Google+ API (for user info)

---

## 🔒 Security

- **Token Verification**: ID tokens verified server-side with Google
- **Session Management**: Flask sessions with encrypted cookies
- **No Client Secrets**: Client secret never exposed to browser
- **HTTPS Ready**: Easy to deploy with SSL/TLS

---

## 🐛 Troubleshooting

### Google Sign-In button doesn't appear

**Check:**
- Browser console for errors
- `GOOGLE_CLIENT_ID` is set in `.env`
- Accessing via `http://localhost:5000` (not `127.0.0.1`)
- JavaScript origins configured in Google Cloud Console

### "Invalid token" error

**Solutions:**
- Verify Client ID matches Google Cloud Console
- Check OAuth client is enabled
- Ensure APIs are enabled (Gmail, Google+)

### "Not authenticated" when generating summary

**Solutions:**
- Sign in with Google first
- Check browser cookies are enabled
- Verify session is working (check Flask secret key)

### CORS errors

**Solutions:**
- Make sure `flask-cors` is installed
- Check CORS configuration in `app.py`
- Verify request origins

---

## 🚀 Production Deployment

### Environment Variables:

```env
GOOGLE_CLIENT_ID=your_production_client_id
GOOGLE_CLIENT_SECRET=your_production_client_secret
GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=generate_a_strong_random_key
```

### Update OAuth Settings:

Add your production domain to:
- Authorized JavaScript origins: `https://yourdomain.com`
- Authorized redirect URIs: `https://yourdomain.com`

### Use HTTPS:

```bash
# With gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:443 --certfile=cert.pem --keyfile=key.pem app:app
```

### Security Checklist:

- ✅ Use HTTPS
- ✅ Strong Flask secret key
- ✅ Environment variables (not hardcoded)
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Session timeout

---

## 📁 Project Structure

```
mailmind/
├── app.py                      # Flask web application
├── main.py                     # CLI version (still works!)
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Home page with Google Sign-In
│   ├── summary.html           # Summary view
│   └── error.html             # Error page
├── .env                       # Environment variables (you create)
├── requirements.txt           # Python dependencies
├── summaries/                 # Generated summaries
│   └── summary_*.txt
└── README_WEB.md             # This file
```

---

## 💡 Why This Approach?

### Old Way (credentials.json):
- ❌ Download JSON file from Google Cloud
- ❌ Complex server-side OAuth flow
- ❌ Redirect URI configuration
- ❌ Token management complexity
- ❌ Desktop app credentials for web app

### New Way (Client-Side OAuth):
- ✅ Just add Client ID/Secret to `.env`
- ✅ Google Sign-In button handles OAuth
- ✅ Clean, modern authentication
- ✅ Works like Gmail, YouTube, Drive
- ✅ Proper web application credentials

---

## 🎨 Customization

### Change Port:

Edit `app.py`:
```python
app.run(debug=True, port=8080)  # Change to your port
```

Update Google Cloud Console authorized origins:
```
http://localhost:8080
```

### Custom Styling:

Edit `templates/base.html` to customize CSS.

### Add Features:

The API is ready for custom frontends:
- React/Vue/Angular apps
- Mobile apps
- Browser extensions
- Desktop apps

---

## 📞 Support

**Read First:**
- `START_HERE.txt` - Quick visual guide
- `SIMPLE_SETUP.md` - Detailed setup instructions
- This file - Complete documentation

**Common Issues:**
- Check `.env` file has all required variables
- Verify Google Cloud Console configuration
- Check browser console for JavaScript errors
- Ensure cookies are enabled

---

## ✅ Summary

1. Add Client ID and Secret to `.env`
2. Run `python app.py`
3. Open http://localhost:5000
4. Sign in with Google
5. Generate summaries!

**No credentials.json needed!** 🎉

---

Enjoy your modern, clean MailMind web application!
