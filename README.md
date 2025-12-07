# MailMind - AI-Powered Email Summarization System

MailMind is a Python-based email summarization tool that connects to your Gmail inbox, fetches recent emails, and generates an intelligent summary with priority categorization using Google's Gemini AI. The system helps you quickly understand your inbox priorities without reading every email.

## Features

- 🔐 **Secure Gmail Authentication**: OAuth 2.0 authentication with token caching
- 📧 **Smart Email Fetching**: Retrieves the 20 most recent emails (subject and sender only)
- 🤖 **AI-Powered Summarization**: Uses Google Gemini to categorize emails by priority
- 📊 **Priority Categorization**: Automatically sorts emails into High, Medium, and Low priority
- 💾 **Timestamped Summaries**: Saves summaries to organized text files
- ⚡ **Single Command Execution**: Run everything with `python main.py`

## Prerequisites

- Python 3.7 or higher
- A Google account with Gmail
- Google Cloud Console account (free)
- Google Gemini API key (free tier available)

## Installation

1. **Clone or download this repository**

2. **Install required dependencies**

```bash
pip install -r requirements.txt
```

The required packages are:
- `google-auth-oauthlib` - Gmail OAuth authentication
- `google-auth-httplib2` - HTTP library for Google APIs
- `google-api-python-client` - Gmail API client
- `google-generativeai` - Gemini AI SDK
- `python-dotenv` - Environment variable management

## Setup Instructions

### Step 1: Set Up Google Cloud Console and Gmail API

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project**
   - Click "Select a project" at the top
   - Click "New Project"
   - Enter a project name (e.g., "MailMind")
   - Click "Create"

3. **Enable Gmail API**
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click on "Gmail API"
   - Click "Enable"

4. **Configure OAuth Consent Screen**
   - Go to "APIs & Services" > "OAuth consent screen"
   - Select "External" user type
   - Click "Create"
   - Fill in required fields:
     - App name: "MailMind"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" section (click "Save and Continue")
   - Add your email as a test user
   - Click "Save and Continue"

5. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Desktop app" as application type
   - Name it "MailMind Desktop Client"
   - Click "Create"
   - Click "Download JSON" on the popup
   - Save the downloaded file as `credentials.json` in your project directory

### Step 2: Set Up Gemini API Key

1. **Get Your Gemini API Key**
   - Visit: https://aistudio.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Select a Google Cloud project (or create a new one)
   - Copy the generated API key

2. **Create .env File**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` in a text editor
   - Replace `your_gemini_api_key_here` with your actual API key:
     ```
     GEMINI_API_KEY=AIzaSyD...your_actual_key_here
     ```

### Step 3: Verify Setup

Your project directory should now contain:
- `main.py` - The main application script
- `requirements.txt` - Python dependencies
- `credentials.json` - Gmail OAuth credentials (from Google Cloud Console)
- `.env` - Environment variables with your Gemini API key

## Usage

### Running MailMind

Simply run the main script:

```bash
python main.py
```

### First Run

On your first run:
1. The script will open your web browser for Gmail authentication
2. Sign in with your Google account
3. Click "Allow" to grant MailMind access to read your Gmail
4. The browser will show "The authentication flow has completed"
5. Return to your terminal - the script will continue automatically
6. A `token.json` file will be created to cache your credentials

### Subsequent Runs

On subsequent runs:
- The script will use the cached `token.json` file
- No browser authentication needed (unless token expires)
- The entire process completes in seconds

### What Happens

1. **Authentication**: Connects to Gmail using OAuth
2. **Fetching**: Retrieves the 20 most recent emails from your inbox
3. **Summarization**: Sends email metadata to Gemini AI for analysis
4. **Categorization**: AI categorizes emails by priority (High/Medium/Low)
5. **Saving**: Saves the summary to `summaries/summary_YYYY-MM-DD_HH-MM-SS.txt`
6. **Display**: Shows the summary in your terminal

## Example Output

```
✓ Configuration loaded successfully.

Authenticating with Gmail...
✓ Gmail authentication successful.

Fetching emails from inbox...
Found 20 email(s). Extracting metadata...
✓ Successfully extracted metadata from 20 email(s).
✓ Fetched 20 email(s).

Generating AI-powered summary...
Sending emails to Gemini AI for summarization...
✓ AI summary generated successfully.
✓ Summary generated successfully.

Saving summary to file...
✓ Summary saved successfully.

============================================================
EMAIL SUMMARY
============================================================
High Priority:
• Project Deadline Reminder - From: boss@company.com
• Urgent: Server Down Alert - From: alerts@monitoring.com
• Meeting Request: Q4 Planning - From: manager@company.com

Medium Priority:
• Weekly Team Update - From: team@company.com
• Invoice #12345 - From: billing@vendor.com
• Newsletter: Industry Trends - From: newsletter@industry.com

Low Priority:
• LinkedIn Connection Request - From: linkedin@notifications.com
• Promotional: 50% Off Sale - From: marketing@store.com
• Social Media Digest - From: digest@social.com
============================================================

✓ Summary saved to: summaries/summary_2025-12-07_14-30-45.txt
```

## File Structure

```
mailmind/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── credentials.json        # Gmail OAuth credentials (you create this)
├── token.json             # Cached OAuth token (auto-generated)
├── .env                   # Environment variables (you create this)
├── .env.example           # Environment template
├── README.md              # This file
└── summaries/             # Output directory (auto-created)
    ├── summary_2025-12-07_14-30-45.txt
    └── summary_2025-12-07_18-45-00.txt
```

## Troubleshooting

### Error: "credentials.json file not found"

**Problem**: The Gmail OAuth credentials file is missing.

**Solution**:
1. Follow Step 1 of the setup instructions above
2. Download the OAuth credentials from Google Cloud Console
3. Save the file as `credentials.json` in your project directory
4. Ensure the filename is exactly `credentials.json` (not `credentials (1).json`)

### Error: ".env file not found"

**Problem**: The environment configuration file is missing.

**Solution**:
1. Copy the example file: `cp .env.example .env`
2. Edit `.env` and add your Gemini API key
3. Ensure the file is named `.env` (with the dot at the beginning)

### Error: "GEMINI_API_KEY is not set"

**Problem**: The Gemini API key is missing from your `.env` file.

**Solution**:
1. Get an API key from https://aistudio.google.com/app/apikey
2. Open `.env` in a text editor
3. Add the line: `GEMINI_API_KEY=your_actual_key_here`
4. Save the file

### Error: "Authentication failed" or OAuth Issues

**Problem**: Gmail authentication is not working.

**Solution**:
1. Delete `token.json` if it exists
2. Ensure `credentials.json` is valid and in the correct location
3. Check that Gmail API is enabled in Google Cloud Console
4. Verify you added yourself as a test user in OAuth consent screen
5. Try running the script again

### Error: "Gmail API request failed" or "Quota exceeded"

**Problem**: Gmail API quota limits reached.

**Solution**:
1. Wait a few minutes and try again
2. Check your quota at: https://console.cloud.google.com/apis/api/gmail.googleapis.com/quotas
3. The free tier allows 1 billion quota units per day (more than enough for normal use)

### Error: "Gemini API authentication failed"

**Problem**: Invalid or expired Gemini API key.

**Solution**:
1. Verify your API key at: https://aistudio.google.com/app/apikey
2. Generate a new API key if needed
3. Update the `GEMINI_API_KEY` in your `.env` file
4. Ensure there are no extra spaces or quotes around the key

### Error: "Gemini API quota exceeded"

**Problem**: You've exceeded the free tier limits for Gemini API.

**Solution**:
1. Check your usage at: https://aistudio.google.com/app/apikey
2. Wait for the quota to reset (usually daily)
3. Consider upgrading to a paid plan if you need higher limits

### Warning: "AI response does not contain expected priority sections"

**Problem**: Gemini AI returned an unexpected format.

**Solution**:
- This is usually harmless - the summary will still be saved
- The AI occasionally formats responses differently
- The summary will include a note about the formatting issue
- Try running again if the output is unusable

### No Emails Found

**Problem**: The script reports "No emails found in inbox."

**Solution**:
1. Check that you have emails in your Gmail inbox
2. Verify you're authenticating with the correct Google account
3. Check that the emails are in the INBOX label (not archived or in other folders)

### Permission Errors When Saving Files

**Problem**: Cannot create `summaries` directory or write files.

**Solution**:
1. Check that you have write permissions in the project directory
2. On Linux/Mac, try: `chmod +w .`
3. On Windows, check folder permissions in Properties
4. Try running from a different directory where you have write access

### Script Hangs During OAuth

**Problem**: Browser opens but script doesn't continue.

**Solution**:
1. Complete the OAuth flow in the browser
2. Look for "The authentication flow has completed" message
3. Close the browser tab and return to terminal
4. If still stuck, press Ctrl+C and try again
5. Delete `token.json` and retry

## Privacy and Security

- **Email Privacy**: MailMind only reads email subject lines and sender addresses - never the email body or attachments
- **Local Storage**: OAuth tokens are stored locally in `token.json`
- **API Keys**: Keep your `.env` file secure and never commit it to version control
- **Read-Only Access**: MailMind only requests read-only Gmail permissions
- **No Data Sharing**: Your email data is sent only to Google's Gemini API for summarization

## Limitations

- Fetches only the 20 most recent emails per run
- Requires internet connection for Gmail and Gemini API access
- Subject to Gmail API and Gemini API rate limits
- AI categorization accuracy depends on email content and Gemini model performance

## Future Enhancements

Potential improvements for future versions:
- Configurable email count
- Email filtering by sender, date, or labels
- Scheduled automatic runs (cron/task scheduler)
- Multiple email account support
- Web dashboard for viewing summaries
- Custom priority rules
- Email summary history and trends

## License

This project is provided as-is for personal and educational use.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your setup follows all steps in the Setup Instructions
3. Check that all dependencies are installed correctly
4. Ensure your API keys and credentials are valid

## Credits

Built with:
- [Gmail API](https://developers.google.com/gmail/api) - Email access
- [Google Gemini](https://ai.google.dev/) - AI summarization
- [Python](https://www.python.org/) - Core language
