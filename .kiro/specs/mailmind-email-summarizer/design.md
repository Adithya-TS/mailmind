# MailMind Design Document

## Overview

MailMind is a Python-based email summarization system that integrates Gmail API and Google's Gemini language models to provide intelligent, prioritized summaries of inbox activity. The system follows a linear pipeline architecture: authenticate → fetch → summarize → send, with each stage handling errors gracefully.

The application is designed as a single-execution script that can be run daily (manually or via cron/scheduler) to deliver email summaries. It uses OAuth 2.0 for secure Gmail access and environment variables for API key management.

## Architecture

### High-Level Architecture

```
┌─────────────┐
│   main.py   │
└──────┬──────┘
       │
       ├──► authenticate_gmail() ──► Gmail OAuth Flow
       │                              ├─ credentials.json (input)
       │                              └─ token.json (output/cache)
       │
       ├──► fetch_emails() ──────────► Gmail API
       │                              └─ Returns: List[EmailMetadata]
       │
       ├──► generate_summary() ──────► Gemini API
       │                              ├─ Input: Email metadata
       │                              └─ Output: Categorized summary
       │
       └──► save_summary() ───────────► File System
                                       └─ Saves summary to summaries/summary_[timestamp].txt
```

### Component Flow

1. **Initialization**: Load environment variables, validate configuration
2. **Authentication**: Establish Gmail API credentials using OAuth
3. **Data Collection**: Fetch latest 20 emails (subject + sender only)
4. **AI Processing**: Send metadata to Gemini for categorization and summarization
5. **Persistence**: Save the formatted summary to a timestamped file
6. **Cleanup**: Log results and exit

## Components and Interfaces

### 1. Authentication Module

**Function**: `authenticate_gmail() -> Resource`

**Purpose**: Handles OAuth 2.0 flow for Gmail API access

**Inputs**:
- `credentials.json` (file): OAuth client credentials from Google Cloud Console
- `token.json` (file, optional): Cached access token

**Outputs**:
- Gmail API service object (Resource)

**Behavior**:
- Check if `token.json` exists and is valid
- If valid token exists, use it
- If no valid token, initiate OAuth flow using `credentials.json`
- Request scopes: `gmail.readonly` and `gmail.send`
- Save new token to `token.json` for future use
- Raise exception if authentication fails

**Error Handling**:
- Missing `credentials.json`: Clear error message with setup instructions
- OAuth failure: Display error and exit
- Invalid token: Automatically refresh or re-authenticate

---

### 2. Email Fetching Module

**Function**: `fetch_emails(service: Resource, max_results: int = 20) -> List[Dict]`

**Purpose**: Retrieves recent email metadata from Gmail inbox

**Inputs**:
- `service`: Authenticated Gmail API service object
- `max_results`: Number of emails to fetch (default: 20)

**Outputs**:
- List of dictionaries containing:
  - `subject`: Email subject line (string)
  - `sender`: Sender email address (string)

**Behavior**:
- Query Gmail API for messages in inbox
- Fetch only message IDs first (for efficiency)
- Retrieve full metadata for each message
- Extract subject from headers
- Extract sender (From field) from headers
- Return list ordered by most recent first
- Handle cases where inbox has fewer than 20 emails

**Error Handling**:
- API request failure: Log error, raise exception
- Missing headers: Use default values ("No Subject", "Unknown Sender")
- Empty inbox: Return empty list

---

### 3. AI Summarization Module

**Function**: `generate_summary(emails: List[Dict], api_key: str) -> str`

**Purpose**: Generates categorized priority summary using Google Gemini

**Inputs**:
- `emails`: List of email metadata dictionaries
- `api_key`: Gemini API key from environment

**Outputs**:
- Formatted summary string with three priority categories

**Behavior**:
- Format email metadata into a structured prompt
- Send prompt to Gemini API (gemini-pro or gemini-2.5-flash)
- Request categorization into High, Medium, Low priority
- Request bullet-point format for each category
- Parse and format the AI response
- Return formatted summary text

**Prompt Structure**:
```
You are an email assistant. Analyze these emails and categorize them by priority:

[Email list with subjects and senders]

Provide a summary with three sections:
- High Priority: [urgent/important emails]
- Medium Priority: [moderate importance]
- Low Priority: [informational/low urgency]

Format each as bullet points.
```

**Error Handling**:
- API key missing: Raise configuration error
- API request failure: Log error with details, raise exception
- Invalid response format: Return raw response with warning
- Rate limiting: Display clear error message

---

### 4. Summary Saving Module

**Function**: `save_summary(summary: str, output_dir: str = "summaries") -> str`

**Purpose**: Saves the generated summary to a text file

**Inputs**:
- `summary`: Formatted summary text
- `output_dir`: Directory to save summaries (default: "summaries")

**Outputs**:
- File path of the saved summary

**Behavior**:
- Create output directory if it doesn't exist
- Generate filename with timestamp: "summary_YYYY-MM-DD_HH-MM-SS.txt"
- Write summary to file
- Return full file path

**Error Handling**:
- Directory creation failure: Log error, raise exception
- File write failure: Log error with details, raise exception
- Permission errors: Display clear error message

---

### 5. Main Orchestration

**Function**: `main()`

**Purpose**: Coordinates all modules and handles overall execution flow

**Behavior**:
1. Load environment variables from `.env`
2. Validate GEMINI_API_KEY exists
3. Authenticate with Gmail
4. Fetch emails
5. Generate AI summary
6. Save summary to file
7. Display success message with file path
8. Exit with appropriate status code

**Error Handling**:
- Catch all exceptions at top level
- Log errors with context
- Display user-friendly error messages
- Exit with non-zero status on failure

## Data Models

### EmailMetadata

```python
{
    "subject": str,  # Email subject line
    "sender": str    # Sender email address
}
```

### SummaryReport

```python
{
    "high_priority": List[str],    # High priority email bullets
    "medium_priority": List[str],  # Medium priority email bullets
    "low_priority": List[str]      # Low priority email bullets
}
```

Note: The actual implementation may use a formatted string instead of a structured object, depending on Gemini response format.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, several properties can be consolidated:
- Properties 3.2 and 3.3 both test for three priority categories - can be combined
- Properties 4.1, 4.2, and 4.3 all test email composition - can be combined into comprehensive email format property
- Multiple error handling properties (1.4, 2.4, 3.5, 4.4) follow the same pattern - can be generalized

### Properties

Property 1: Token persistence
*For any* successful OAuth authentication, the system should create a token.json file containing valid authentication credentials
**Validates: Requirements 1.2**

Property 2: Email fetch completeness
*For any* email fetched from the inbox, the result should contain both a subject field and a sender field
**Validates: Requirements 2.2**

Property 3: Email fetch exclusion
*For any* email fetched from the inbox, the result should not contain body content or attachment data
**Validates: Requirements 2.5**

Property 4: Fetch count accuracy
*For any* inbox with at least 20 emails, the fetch operation should return exactly 20 emails
**Validates: Requirements 2.1**

Property 5: Summary metadata completeness
*For any* set of fetched emails, all emails should be included in the data sent to the AI model
**Validates: Requirements 3.1**

Property 6: Summary structure
*For any* AI-generated summary, the output should contain exactly three priority sections: High, Medium, and Low
**Validates: Requirements 3.2, 3.3**

Property 7: Summary item format
*For any* email mentioned in the summary, it should be presented as a bullet point containing both subject and sender information
**Validates: Requirements 3.4**

Property 8: Summary file persistence
*For any* generated summary, the system should save it to a file with a timestamp-based filename in the summaries directory
**Validates: Requirements 4.1, 4.2**

Property 9: Error handling consistency
*For any* API failure (Gmail or Gemini) or file I/O failure, the system should log an error message with details and exit gracefully with a non-zero status code
**Validates: Requirements 1.4, 2.4, 3.5, 4.4, 6.3**

Property 10: Successful execution exit code
*For any* execution that completes all steps without errors, the system should exit with status code 0
**Validates: Requirements 6.2**

Property 11: Progress visibility
*For any* execution, the system should display progress messages for each major step: authentication, fetching, summarizing, and saving
**Validates: Requirements 6.4**

Property 12: API error handling presence
*For any* function that calls external APIs (Gmail or Gemini), the function should include error handling for API failures
**Validates: Requirements 7.5**

## Error Handling

### Authentication Errors
- Missing `credentials.json`: Display setup instructions and exit
- Invalid credentials: Show OAuth error details and exit
- Token refresh failure: Re-initiate OAuth flow
- Network errors: Display connection error and retry guidance

### Gmail API Errors
- Rate limiting: Display clear message about quota limits
- Permission errors: Verify OAuth scopes and re-authenticate
- Network timeouts: Retry with exponential backoff (max 3 attempts)
- Invalid response: Log raw response and exit with error

### Gemini API Errors
- Missing API key: Display configuration error and exit
- Invalid API key: Show authentication error
- Rate limiting: Display quota error with guidance
- Network errors: Retry once, then fail with clear message
- Malformed response: Return raw response with warning

### File I/O Errors
- Directory creation failure: Log error and exit
- File write failure: Display permission or disk space error
- Invalid path: Validate output directory before writing

### General Error Handling Strategy
- All errors should be caught at the appropriate level
- Error messages should be user-friendly and actionable
- Technical details should be logged for debugging
- System should always exit gracefully (no crashes)
- Exit codes: 0 for success, 1 for errors

## Testing Strategy

### Unit Testing

The system will use Python's built-in `unittest` framework for unit testing. Unit tests will focus on:

1. **Configuration Loading**
   - Test `.env` file parsing
   - Test missing API key handling
   - Test invalid configuration detection

2. **Email Metadata Extraction**
   - Test subject line parsing from Gmail API response
   - Test sender extraction from headers
   - Test handling of missing headers (default values)

3. **Summary Formatting**
   - Test parsing of AI response into structured format
   - Test bullet point formatting
   - Test handling of malformed AI responses

4. **Error Handling**
   - Test specific error scenarios (missing files, invalid tokens)
   - Test error message formatting
   - Test exit code behavior

Unit tests will use mocking for external API calls to avoid dependencies on Gmail and Gemini services during testing.

### Property-Based Testing

The system will use **Hypothesis** (Python's property-based testing library) for property-based testing. Each property-based test will:

- Run a minimum of 100 iterations with randomly generated inputs
- Be tagged with a comment referencing the specific correctness property from this design document
- Use the format: `# Feature: mailmind-email-summarizer, Property X: [property text]`

Property-based tests will cover:

1. **Email Metadata Completeness** (Property 2)
   - Generate random email data structures
   - Verify all have subject and sender fields

2. **Email Metadata Exclusion** (Property 3)
   - Generate random email data with various fields
   - Verify body and attachments are excluded

3. **Summary Structure** (Property 6)
   - Generate random email sets
   - Verify AI summary always has three priority sections

4. **Summary Item Format** (Property 7)
   - Generate random summaries
   - Verify each item contains subject and sender

5. **Error Handling Consistency** (Property 9)
   - Simulate various API failures
   - Verify consistent error handling and exit codes

### Integration Testing

Integration tests will verify the complete pipeline with real API calls (in a test environment):

1. End-to-end flow with test Gmail account
2. OAuth flow completion
3. Email fetching and summarization
4. Summary delivery

Integration tests will be run manually or in CI/CD with appropriate test credentials.

### Test Coverage Goals

- Unit test coverage: >80% of code
- All error paths should have explicit tests
- All correctness properties should have corresponding property-based tests
- Integration tests should cover happy path and common error scenarios

## Implementation Notes

### Dependencies

```
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

### Configuration Files

1. **credentials.json**: OAuth client credentials from Google Cloud Console
   - Must be obtained by user from Google Cloud Console
   - Requires Gmail API enabled
   - Needs OAuth consent screen configured

2. **token.json**: Cached OAuth token (auto-generated)
   - Created after first successful authentication
   - Automatically refreshed when expired

3. **.env**: Environment variables
   - `GEMINI_API_KEY`: Google Gemini API key

### Gmail API Setup Requirements

Users must:
1. Create a Google Cloud project
2. Enable Gmail API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download credentials.json
5. Place credentials.json in project directory

### Gemini API Setup

Users must:
1. Visit Google AI Studio (https://aistudio.google.com/app/apikey)
2. Generate API key
3. Add key to .env file

### Execution Flow

```
main()
  ├─ load_dotenv()
  ├─ validate_config()
  ├─ authenticate_gmail() → service
  ├─ fetch_emails(service) → emails
  ├─ generate_summary(emails) → summary
  ├─ save_summary(summary) → file_path
  └─ exit(0)
```

### Future Enhancements

Potential improvements for future versions:
- Scheduling support (cron integration)
- Configurable email count
- Custom priority rules
- Multiple email account support
- Web dashboard for viewing summaries
- Email filtering by sender/subject
- Summary history storage
