#!/usr/bin/env python3
"""
MailMind Web Application - Flask Frontend

A web-based interface for MailMind email summarization with client-side OAuth.
"""

import os
from datetime import datetime
from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai
from pathlib import Path
import requests as http_requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)  # Enable CORS for API endpoints

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')


def verify_google_token(token: str):
    """Verify Google ID token and return user info."""
    try:
        if not GOOGLE_CLIENT_ID:
            return None
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        
        # Verify issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None
        
        # Extract user info
        user_info = {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "google_id": idinfo.get("sub"),
            "picture": idinfo.get("picture"),
        }
        
        if not user_info["email"] or not user_info["google_id"]:
            return None
        
        return user_info
        
    except Exception as e:
        print(f"Token verification error: {e}")
        return None


def get_credentials_from_session():
    """Get Gmail API credentials from session."""
    if 'access_token' not in session:
        return None
    
    # Create credentials with all required OAuth fields
    credentials = Credentials(
        token=session['access_token'],
        refresh_token=session.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET
    )
    return credentials


def save_user_to_session(user_info, access_token, refresh_token=None):
    """Save user info and access token to session."""
    session['user'] = user_info
    session['access_token'] = access_token
    if refresh_token:
        session['refresh_token'] = refresh_token


def fetch_emails(service, max_results=20):
    """Fetch recent email metadata from Gmail inbox."""
    try:
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return []
        
        emails = []
        for message in messages:
            try:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From']
                ).execute()
                
                headers = msg.get('payload', {}).get('headers', [])
                
                subject = "No Subject"
                sender = "Unknown Sender"
                
                for header in headers:
                    name = header.get('name', '').lower()
                    value = header.get('value', '')
                    
                    if name == 'subject':
                        subject = value if value else "No Subject"
                    elif name == 'from':
                        sender = value if value else "Unknown Sender"
                
                emails.append({
                    'subject': subject,
                    'sender': sender
                })
                
            except Exception as e:
                print(f"Warning: Error processing message: {e}")
                continue
        
        return emails
        
    except HttpError as e:
        raise Exception(f"Gmail API request failed: {e}")


def generate_summary(emails, api_key):
    """Generate AI-powered summary of emails with priority categorization."""
    if not api_key:
        raise Exception("Gemini API key is missing")
    
    if not emails:
        return "No emails to summarize."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        email_list = []
        for i, email in enumerate(emails, 1):
            subject = email.get('subject', 'No Subject')
            sender = email.get('sender', 'Unknown Sender')
            email_list.append(f"{i}. Subject: {subject}\n   From: {sender}")
        
        emails_text = "\n".join(email_list)
        
        prompt = f"""You are an email assistant. Analyze these {len(emails)} emails and categorize them by priority.

Emails to analyze:
{emails_text}

Provide a summary with exactly three sections:
- High Priority: Urgent or important emails requiring immediate attention
- Medium Priority: Emails of moderate importance that should be addressed soon
- Low Priority: Informational emails or low urgency items

Format each email as a bullet point with the subject and sender.
Use this exact format:

High Priority:
• [Subject] - From: [Sender]

Medium Priority:
• [Subject] - From: [Sender]

Low Priority:
• [Subject] - From: [Sender]

If a priority category has no emails, write "None" under that section."""
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            fallback_summary = "Email Summary (AI processing unavailable)\n\n"
            for email in emails:
                fallback_summary += f"• {email.get('subject', 'No Subject')} - From: {email.get('sender', 'Unknown Sender')}\n"
            return fallback_summary
        
        summary_text = response.text.strip()
        
        if "High Priority" not in summary_text or "Medium Priority" not in summary_text or "Low Priority" not in summary_text:
            summary_text = f"[Note: AI response may not be properly formatted]\n\n{summary_text}"
        
        return summary_text
        
    except Exception as e:
        raise Exception(f"Gemini API request failed: {e}")


def save_summary(summary, output_dir="summaries"):
    """Save the generated summary to a timestamped text file."""
    try:
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"summary_{timestamp}.txt"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return file_path
        
    except Exception as e:
        raise Exception(f"Failed to save summary: {e}")


def get_past_summaries():
    """Get list of past summaries."""
    summaries_dir = Path("summaries")
    if not summaries_dir.exists():
        return []
    
    summaries = []
    for file_path in sorted(summaries_dir.glob("summary_*.txt"), reverse=True):
        summaries.append({
            'filename': file_path.name,
            'timestamp': file_path.stem.replace('summary_', ''),
            'path': str(file_path)
        })
    
    return summaries


@app.route('/')
def index():
    """Home page."""
    user = session.get('user')
    is_authenticated = user is not None
    past_summaries = get_past_summaries()
    
    return render_template('index.html', 
                         is_authenticated=is_authenticated,
                         user=user,
                         past_summaries=past_summaries,
                         google_client_id=GOOGLE_CLIENT_ID)


@app.route('/api/auth/google', methods=['POST'])
def auth_google():
    """Verify Google access token and create session."""
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        
        if not access_token:
            return jsonify({'error': 'Missing access token'}), 400
        
        # Verify access token by fetching user info
        try:
            response = http_requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            if response.status_code != 200:
                return jsonify({'error': 'Invalid access token'}), 401
            
            user_data = response.json()
            user_info = {
                'email': user_data.get('email'),
                'name': user_data.get('name'),
                'google_id': user_data.get('id'),
                'picture': user_data.get('picture')
            }
            
        except Exception as e:
            return jsonify({'error': f'Token verification failed: {str(e)}'}), 401
        
        # Save to session
        save_user_to_session(user_info, access_token)
        
        return jsonify({
            'success': True,
            'user': user_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    return redirect(url_for('index'))


@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate email summary."""
    try:
        credentials = get_credentials_from_session()
        
        if not credentials:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Build Gmail service
        service = build('gmail', 'v1', credentials=credentials)
        
        # Fetch emails
        emails = fetch_emails(service)
        
        if not emails:
            return jsonify({'error': 'No emails found in inbox'}), 404
        
        # Generate summary
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        summary = generate_summary(emails, api_key)
        
        # Save summary
        file_path = save_summary(summary)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'file_path': file_path,
            'email_count': len(emails)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/summary/<filename>')
def view_summary(filename):
    """View a past summary."""
    try:
        file_path = Path("summaries") / filename
        
        if not file_path.exists() or not file_path.is_file():
            return render_template('error.html',
                                 error="Summary not found",
                                 message=f"The file {filename} does not exist.")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        timestamp = filename.replace('summary_', '').replace('.txt', '')
        
        return render_template('summary.html',
                             filename=filename,
                             timestamp=timestamp,
                             content=content)
        
    except Exception as e:
        return render_template('error.html',
                             error="Error reading summary",
                             message=str(e))


if __name__ == '__main__':
    # Check for required configuration
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Please create one based on .env.example")
    
    if not GOOGLE_CLIENT_ID:
        print("Warning: GOOGLE_CLIENT_ID not set in .env file")
    
    print("\n" + "="*60)
    print("MailMind Web Application")
    print("="*60)
    print("\nStarting server at: http://localhost:5000")
    print("\nMake sure your .env file has:")
    print("  1. GOOGLE_CLIENT_ID")
    print("  2. GOOGLE_CLIENT_SECRET")
    print("  3. GEMINI_API_KEY")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
