# Requirements Document

## Introduction

MailMind is an AI-powered email summarization system that connects to a user's Gmail inbox, fetches recent emails, generates an intelligent summary with priority categorization, and saves the summary to a timestamped file. The system aims to reduce email overload by providing concise, actionable summaries of inbox activity.

## Glossary

- **MailMind System**: The complete AI email summarization application
- **Gmail API**: Google's API service for programmatic access to Gmail accounts
- **OAuth Flow**: The authentication process using credentials.json and token.json files
- **Email Metadata**: The subject line and sender information from an email
- **AI Model**: The Google Gemini language model used for generating summaries
- **Priority Category**: Classification of emails as High, Medium, or Low priority
- **Summary Report**: The formatted output containing categorized email summaries

## Requirements

### Requirement 1

**User Story:** As a Gmail user, I want MailMind to authenticate with my Gmail account, so that the system can access my inbox securely.

#### Acceptance Criteria

1. WHEN the MailMind System starts, THE MailMind System SHALL authenticate using OAuth with credentials.json file
2. WHEN OAuth authentication succeeds, THE MailMind System SHALL store the access token in token.json file
3. WHEN token.json exists and contains a valid token, THE MailMind System SHALL reuse the existing token without re-authentication
4. IF authentication fails, THEN THE MailMind System SHALL display a clear error message and terminate gracefully
5. WHEN the user completes OAuth consent, THE MailMind System SHALL obtain read and send permissions for Gmail

### Requirement 2

**User Story:** As a Gmail user, I want MailMind to fetch my recent emails, so that I can get a summary of my latest inbox activity.

#### Acceptance Criteria

1. WHEN the MailMind System fetches emails, THE MailMind System SHALL retrieve exactly 20 most recent emails from the inbox
2. WHEN extracting email data, THE MailMind System SHALL capture the subject line and sender address for each email
3. IF the inbox contains fewer than 20 emails, THEN THE MailMind System SHALL fetch all available emails
4. IF the Gmail API request fails, THEN THE MailMind System SHALL log the error and terminate gracefully
5. WHEN emails are fetched, THE MailMind System SHALL exclude email body content and attachments

### Requirement 3

**User Story:** As a Gmail user, I want MailMind to generate an AI-powered summary of my emails, so that I can quickly understand my inbox priorities.

#### Acceptance Criteria

1. WHEN the MailMind System sends data to the AI Model, THE MailMind System SHALL include all fetched Email Metadata
2. WHEN the AI Model generates output, THE MailMind System SHALL receive a Summary Report with three Priority Categories
3. WHEN formatting the Summary Report, THE MailMind System SHALL organize emails under High, Medium, and Low priority sections
4. WHEN displaying emails in the Summary Report, THE MailMind System SHALL present each email as a bullet point with subject and sender
5. IF the AI Model request fails, THEN THE MailMind System SHALL log the error with details and terminate gracefully

### Requirement 4

**User Story:** As a Gmail user, I want MailMind to save the summary to a file, so that I can review it at my convenience.

#### Acceptance Criteria

1. WHEN the Summary Report is generated, THE MailMind System SHALL save the report to a text file
2. WHEN creating the summary file, THE MailMind System SHALL use a filename with timestamp format: summary_YYYY-MM-DD_HH-MM-SS.txt
3. WHEN saving the summary, THE MailMind System SHALL create a "summaries" directory if it does not exist
4. IF saving the file fails, THEN THE MailMind System SHALL log the error and display a failure message
5. WHEN the file is saved successfully, THE MailMind System SHALL display the full file path in a success message

### Requirement 5

**User Story:** As a developer, I want MailMind to use environment variables for API keys, so that sensitive credentials are not hardcoded.

#### Acceptance Criteria

1. WHEN the MailMind System starts, THE MailMind System SHALL load the GEMINI_API_KEY from a .env file
2. IF the .env file is missing, THEN THE MailMind System SHALL display an error message and terminate
3. IF the GEMINI_API_KEY is not set in the .env file, THEN THE MailMind System SHALL display an error message and terminate
4. WHEN loading environment variables, THE MailMind System SHALL use the python-dotenv library
5. THE MailMind System SHALL provide a .env.example file showing required environment variable format

### Requirement 6

**User Story:** As a user, I want to run MailMind with a single command, so that I can easily execute the daily summary process.

#### Acceptance Criteria

1. WHEN the user executes "python main.py", THE MailMind System SHALL perform all operations from authentication to email delivery
2. WHEN execution completes successfully, THE MailMind System SHALL exit with status code 0
3. IF any error occurs during execution, THEN THE MailMind System SHALL exit with a non-zero status code
4. WHEN the MailMind System runs, THE MailMind System SHALL display progress messages for each major step
5. THE MailMind System SHALL complete all operations without requiring additional user input after OAuth consent

### Requirement 7

**User Story:** As a developer, I want MailMind to have clean, modular code, so that the system is maintainable and extensible.

#### Acceptance Criteria

1. WHEN organizing code, THE MailMind System SHALL separate Gmail authentication into a dedicated function
2. WHEN organizing code, THE MailMind System SHALL separate email fetching into a dedicated function
3. WHEN organizing code, THE MailMind System SHALL separate AI summarization into a dedicated function
4. WHEN organizing code, THE MailMind System SHALL separate summary file saving into a dedicated function
5. WHEN implementing functions, THE MailMind System SHALL include error handling for API failures and file I/O issues
