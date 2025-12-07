# MailMind - Simple Setup (No credentials.json!)

## ✨ This version uses client-side Google Sign-In - much simpler!

### Step 1: Add Your Google Credentials to .env

Open `.env` file and add:

```env
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

**That's it!** No `credentials.json` file needed!

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the App

```bash
python app.py
```

### Step 4: Open Browser

Go to: **http://localhost:5000**

### Step 5: Sign In with Google

Click the "Sign in with Google" button and you're done!

---

## 🔑 How It Works

### Client-Side OAuth Flow:

1. **Frontend**: Google Sign-In button handles OAuth
2. **User**: Signs in with Google in popup/redirect
3. **Frontend**: Receives ID token from Google
4. **Frontend**: Sends ID token to backend `/api/auth/google`
5. **Backend**: Verifies token with Google
6. **Backend**: Creates session for user
7. **Done**: User can now generate summaries!

### No credentials.json Needed!

The OAuth flow happens entirely in the browser using Google's JavaScript SDK. The backend only needs:
- `GOOGLE_CLIENT_ID` - to verify tokens
- `GOOGLE_CLIENT_SECRET` - for Gmail API access

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/google` - Verify Google ID token and create session
  - Body: `{"id_token": "...", "access_token": "..."}`
  - Response: `{"success": true, "user": {...}}`

### Email Summary
- `POST /api/generate` - Generate email summary
  - Requires: Authenticated session
  - Response: `{"success": true, "summary": "...", "email_count": 20}`

### Pages
- `GET /` - Home page
- `GET /logout` - Logout
- `GET /summary/<filename>` - View past summary

---

## 🎯 Quick Test

After starting the server:

1. Open http://localhost:5000
2. Click "Sign in with Google"
3. Grant permissions
4. Click "Generate Summary"
5. See your AI-powered email summary!

---

## 🔒 Security Notes

- ID tokens are verified server-side with Google
- Sessions are encrypted with Flask secret key
- Access tokens stored in session (server-side)
- No credentials stored in browser

---

## ⚙️ Google Cloud Console Setup

Make sure your OAuth client has:

**Application type**: Web application

**Authorized JavaScript origins**:
```
http://localhost:5000
```

**Authorized redirect URIs**:
```
http://localhost:5000
```

(No specific callback URL needed for client-side flow!)

---

## 🐛 Troubleshooting

### "GOOGLE_CLIENT_ID not set"
- Add your Client ID to `.env` file

### Google Sign-In button doesn't appear
- Check browser console for errors
- Verify `GOOGLE_CLIENT_ID` is correct
- Make sure you're accessing via http://localhost:5000 (not 127.0.0.1)

### "Invalid token" error
- Make sure your Client ID matches the one in Google Cloud Console
- Check that the OAuth client is enabled

### "Not authenticated" when generating summary
- Sign in with Google first
- Check that session cookies are enabled

---

## ✅ That's It!

Much simpler than the old flow:
- ❌ No `credentials.json` file
- ❌ No server-side OAuth redirect handling
- ❌ No complex Flow objects
- ✅ Just add Client ID/Secret to `.env`
- ✅ Google Sign-In button handles everything
- ✅ Clean, modern authentication

Enjoy! 🎉
