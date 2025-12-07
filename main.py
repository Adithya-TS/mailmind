#!/usr/bin/env python3
"""
MailMind - AI-Powered Email Summarization System

This script connects to Gmail, fetches recent emails, generates an AI summary
with priority categorization, and saves the summary to a timestamped file.
"""

import os
import sys
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """
    Authenticate with Gmail API using OAuth 2.0.
    
    This function handles the OAuth flow using credentials.json and caches
    the access token in token.json for future use. If a valid token exists,
    it will be reused without re-authentication.
    
    Returns:
        Resource: Authenticated Gmail API service object
        
    Raises:
        SystemExit: If credentials.json is missing or authentication fails
    """
    creds = None
    
    # Check if token.json exists with valid credentials
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"Warning: Could not load token.json: {e}")
            creds = None
    
    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Re-authenticating...")
                creds = None
        
        if not creds:
            # Check if credentials.json exists
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json file not found.")
                print("\nTo set up Gmail API access:")
                print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
                print("2. Create a new project or select an existing one")
                print("3. Enable the Gmail API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download the credentials and save as 'credentials.json'")
                sys.exit(1)
            
            try:
                print("Starting OAuth authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("Authentication successful!")
            except Exception as e:
                print(f"Error: Authentication failed: {e}")
                print("\nPlease ensure:")
                print("- credentials.json is valid")
                print("- You have internet connection")
                print("- You completed the OAuth consent in your browser")
                sys.exit(1)
        
        # Save the credentials for the next run
        try:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            print("Token saved to token.json for future use.")
        except Exception as e:
            print(f"Warning: Could not save token.json: {e}")
    
    # Build and return the Gmail API service
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error: Failed to build Gmail service: {e}")
        sys.exit(1)


def fetch_emails(service, max_results=20):
    """
    Fetch recent email metadata from Gmail inbox.
    
    This function retrieves the most recent emails from the inbox and extracts
    only the subject line and sender address. Email body content and attachments
    are explicitly excluded.
    
    Args:
        service: Authenticated Gmail API service object
        max_results: Maximum number of emails to fetch (default: 20)
        
    Returns:
        List[Dict]: List of email metadata dictionaries, each containing:
            - subject (str): Email subject line
            - sender (str): Sender email address
            
    Raises:
        SystemExit: If Gmail API request fails
    """
    try:
        # Fetch message IDs from inbox
        print(f"Fetching up to {max_results} most recent emails...")
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print("No emails found in inbox.")
            return []
        
        print(f"Found {len(messages)} email(s). Extracting metadata...")
        
        # Extract metadata for each message
        emails = []
        for message in messages:
            try:
                # Fetch message metadata (headers only, no body)
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From']
                ).execute()
                
                # Extract headers
                headers = msg.get('payload', {}).get('headers', [])
                
                # Find subject and sender in headers
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
                
            except HttpError as e:
                print(f"Warning: Failed to fetch message {message['id']}: {e}")
                continue
            except Exception as e:
                print(f"Warning: Error processing message {message['id']}: {e}")
                continue
        
        print(f"✓ Successfully extracted metadata from {len(emails)} email(s).")
        return emails
        
    except HttpError as e:
        print(f"Error: Gmail API request failed: {e}")
        print("\nPossible causes:")
        print("- Network connection issues")
        print("- Invalid or expired credentials")
        print("- Gmail API quota exceeded")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error while fetching emails: {e}")
        sys.exit(1)


def generate_summary(emails, api_key):
    """
    Generate an AI-powered summary of emails with priority categorization.
    
    This function sends email metadata to Google's Gemini AI model to generate
    a categorized summary with High, Medium, and Low priority sections. Each
    email is presented as a bullet point with subject and sender information.
    
    Args:
        emails: List of email metadata dictionaries containing 'subject' and 'sender'
        api_key: Google Gemini API key
        
    Returns:
        str: Formatted summary text with three priority categories
        
    Raises:
        SystemExit: If API key is missing, API request fails, or response is malformed
    """
    # Validate API key
    if not api_key:
        print("Error: Gemini API key is missing.")
        print("Please ensure GEMINI_API_KEY is set in your .env file.")
        sys.exit(1)
    
    # Handle empty email list
    if not emails:
        return "No emails to summarize."
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Use gemini-2.5-flash model (faster and more cost-effective)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Format email metadata into structured prompt
        email_list = []
        for i, email in enumerate(emails, 1):
            subject = email.get('subject', 'No Subject')
            sender = email.get('sender', 'Unknown Sender')
            email_list.append(f"{i}. Subject: {subject}\n   From: {sender}")
        
        emails_text = "\n".join(email_list)
        
        # Design prompt for priority categorization and bullet-point format
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
        
        print("Sending emails to Gemini AI for summarization...")
        
        # Make API call to Gemini
        response = model.generate_content(prompt)
        
        # Parse AI response
        if not response or not response.text:
            print("Warning: Gemini API returned an empty response.")
            print("Returning raw email list as fallback.")
            # Return a basic formatted summary as fallback
            fallback_summary = "Email Summary (AI processing unavailable)\n\n"
            for email in emails:
                fallback_summary += f"• {email.get('subject', 'No Subject')} - From: {email.get('sender', 'Unknown Sender')}\n"
            return fallback_summary
        
        summary_text = response.text.strip()
        
        # Validate that the response contains the expected priority sections
        if "High Priority" not in summary_text or "Medium Priority" not in summary_text or "Low Priority" not in summary_text:
            print("Warning: AI response does not contain expected priority sections.")
            print("Returning response with warning note.")
            summary_text = f"[Note: AI response may not be properly formatted]\n\n{summary_text}"
        
        print("✓ AI summary generated successfully.")
        return summary_text
        
    except Exception as e:
        # Handle various API errors
        error_message = str(e).lower()
        
        if "api key" in error_message or "authentication" in error_message or "invalid" in error_message:
            print(f"Error: Gemini API authentication failed: {e}")
            print("\nPlease verify:")
            print("- Your API key is correct")
            print("- The API key is active")
            print("- Get a valid key from: https://aistudio.google.com/app/apikey")
        elif "quota" in error_message or "rate limit" in error_message:
            print(f"Error: Gemini API quota exceeded: {e}")
            print("\nYou have exceeded your API quota or rate limit.")
            print("Please wait and try again later, or check your quota at:")
            print("https://aistudio.google.com/app/apikey")
        elif "network" in error_message or "connection" in error_message:
            print(f"Error: Network error while calling Gemini API: {e}")
            print("\nPlease check your internet connection and try again.")
        else:
            print(f"Error: Gemini API request failed: {e}")
            print("\nAn unexpected error occurred while generating the summary.")
        
        sys.exit(1)


def save_summary(summary, output_dir="summaries"):
    """
    Save the generated summary to a timestamped text file.
    
    This function creates the output directory if it doesn't exist, generates
    a filename with the current timestamp, and writes the summary to the file.
    
    Args:
        summary: Formatted summary text to save
        output_dir: Directory to save summaries (default: "summaries")
        
    Returns:
        str: Full file path of the saved summary
        
    Raises:
        SystemExit: If directory creation or file write fails
    """
    from datetime import datetime
    
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            print(f"Creating directory: {output_dir}")
            os.makedirs(output_dir)
            print(f"✓ Directory created: {output_dir}")
        
        # Generate filename with timestamp: summary_YYYY-MM-DD_HH-MM-SS.txt
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"summary_{timestamp}.txt"
        file_path = os.path.join(output_dir, filename)
        
        # Write summary to file
        print(f"Saving summary to: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✓ Summary saved successfully.")
        return file_path
        
    except OSError as e:
        # Handle directory creation failures
        if "mkdir" in str(e).lower() or "directory" in str(e).lower():
            print(f"Error: Failed to create directory '{output_dir}': {e}")
            print("\nPossible causes:")
            print("- Insufficient permissions")
            print("- Invalid directory path")
            print("- Disk space issues")
        else:
            # Handle file write failures
            print(f"Error: Failed to write summary file: {e}")
            print("\nPossible causes:")
            print("- Insufficient permissions")
            print("- Disk space full")
            print("- File system errors")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error while saving summary: {e}")
        sys.exit(1)


def load_configuration():
    """
    Load and validate environment variables from .env file.
    
    Returns:
        dict: Configuration dictionary containing validated environment variables
        
    Raises:
        SystemExit: If .env file is missing or GEMINI_API_KEY is not set
    """
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Error: .env file not found.")
        print("Please create a .env file based on .env.example")
        print("See .env.example for required configuration.")
        sys.exit(1)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Validate GEMINI_API_KEY is present
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY is not set in .env file.")
        print("Please add your Gemini API key to the .env file.")
        print("Get your API key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)
    
    return {
        'gemini_api_key': gemini_api_key
    }


def main():
    """Main orchestration function for MailMind."""
    try:
        # Load and validate configuration
        config = load_configuration()
        print("✓ Configuration loaded successfully.")
        
        # Authenticate with Gmail
        print("\nAuthenticating with Gmail...")
        gmail_service = authenticate_gmail()
        print("✓ Gmail authentication successful.")
        
        # Fetch emails
        print("\nFetching emails from inbox...")
        emails = fetch_emails(gmail_service)
        print(f"✓ Fetched {len(emails)} email(s).")
        
        # Generate AI summary
        if emails:
            print("\nGenerating AI-powered summary...")
            summary = generate_summary(emails, config['gemini_api_key'])
            print("✓ Summary generated successfully.")
            
            # Save summary to file
            print("\nSaving summary to file...")
            file_path = save_summary(summary)
            
            # Display summary and success message
            print("\n" + "="*60)
            print("EMAIL SUMMARY")
            print("="*60)
            print(summary)
            print("="*60)
            print(f"\n✓ Summary saved to: {file_path}")
        else:
            print("\nNo emails to summarize.")
        
        # Exit with success status code
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
