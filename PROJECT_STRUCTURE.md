# MailMind Project Structure

## 📁 Files Overview

### Core Application Files
- **`app.py`** - Web application with Flask (Google Sign-In OAuth)
- **`main.py`** - CLI version (original command-line tool)
- **`requirements.txt`** - Python dependencies

### Configuration
- **`.env`** - Your environment variables (add your credentials here!)
- **`.env.example`** - Template for environment variables

### Documentation
- **`START_HERE.txt`** - Quick start guide (read this first!)
- **`SIMPLE_SETUP.md`** - Detailed setup instructions
- **`README_WEB.md`** - Complete web app documentation
- **`README.md`** - Original CLI documentation

### Templates (Web UI)
- **`templates/base.html`** - Base template with styling
- **`templates/index.html`** - Home page with Google Sign-In
- **`templates/summary.html`** - Summary view page
- **`templates/error.html`** - Error page

### Output
- **`summaries/`** - Generated email summaries (auto-created)

### Specs (Development)
- **`.kiro/specs/mailmind-email-summarizer/`** - Feature specifications
  - `requirements.md` - Requirements document
  - `design.md` - Design document
  - `tasks.md` - Implementation tasks

---

## 🎯 Which Files Do You Need?

### To Run Web App:
1. Edit `.env` (add your Google credentials)
2. Run `app.py`
3. That's it!

### To Run CLI Version:
1. Edit `.env` (add your Google credentials)
2. Create `credentials.json` (see README.md)
3. Run `main.py`

---

## 📚 Documentation Priority

1. **START_HERE.txt** - Start here for quick setup
2. **SIMPLE_SETUP.md** - More detailed instructions
3. **README_WEB.md** - Complete web app reference
4. **README.md** - CLI version reference

---

## 🗑️ What Was Removed

These outdated files were deleted:
- ~~`SETUP_GUIDE.md`~~ (referenced old credentials.json approach)
- ~~`QUICK_START.txt`~~ (outdated OAuth flow)
- ~~`WEB_README.md`~~ (duplicate of README_WEB.md)
- ~~`QUICKSTART_WEB.md`~~ (empty file)
- ~~`credentials.json`~~ (not needed with new approach!)

---

## ✅ Clean Structure

```
mailmind/
├── app.py                    # ⭐ Web app (use this!)
├── main.py                   # CLI version
├── .env                      # ⭐ Add your credentials here
├── requirements.txt          # Dependencies
├── START_HERE.txt           # ⭐ Quick start guide
├── SIMPLE_SETUP.md          # Detailed setup
├── README_WEB.md            # Web app docs
├── README.md                # CLI docs
├── templates/               # Web UI templates
│   ├── base.html
│   ├── index.html
│   ├── summary.html
│   └── error.html
└── summaries/               # Output folder
    └── summary_*.txt
```

Simple and clean! 🎉
