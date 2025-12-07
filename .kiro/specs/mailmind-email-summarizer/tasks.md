# Implementation Plan

- [x] 1. Set up project structure and dependencies





  - Create main.py file
  - Create requirements.txt with all necessary packages
  - Create .env.example file with GEMINI_KEY template
  - Create summaries directory for output files
  - _Requirements: 5.5, 6.1_

- [x] 2. Implement configuration and environment loading





  - Write function to load environment variables using python-dotenv
  - Implement validation for GEMINI_KEY presence
  - Add error handling for missing .env file
  - Add error handling for missing API key
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 2.1 Write unit tests for configuration loading
  - Test successful .env loading
  - Test missing .env file error
  - Test missing API key error
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 3. Implement Gmail authentication module





  - Write authenticate_gmail() function
  - Implement OAuth flow using credentials.json
  - Implement token caching to token.json
  - Add token reuse logic when valid token exists
  - Add error handling for missing credentials.json
  - Add error handling for authentication failures
  - Request gmail.readonly scope
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ]* 3.1 Write property test for token persistence
  - **Property 1: Token persistence**
  - **Validates: Requirements 1.2**
  - _Requirements: 1.2_

- [ ]* 3.2 Write unit tests for authentication
  - Test token reuse when valid token exists
  - Test OAuth scopes are correctly requested
  - Test error handling for missing credentials
  - _Requirements: 1.3, 1.5, 1.4_

- [x] 4. Implement email fetching module




  - Write fetch_emails() function that takes Gmail service object
  - Implement Gmail API call to fetch 20 most recent emails
  - Extract subject line from email headers
  - Extract sender address from email headers
  - Handle missing headers with default values
  - Ensure only subject and sender are captured (no body/attachments)
  - Handle case where inbox has fewer than 20 emails
  - Add error handling for Gmail API failures
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ]* 4.1 Write property test for email metadata completeness
  - **Property 2: Email fetch completeness**
  - **Validates: Requirements 2.2**
  - _Requirements: 2.2_

- [ ]* 4.2 Write property test for email metadata exclusion
  - **Property 3: Email fetch exclusion**
  - **Validates: Requirements 2.5**
  - _Requirements: 2.5_

- [ ]* 4.3 Write property test for fetch count accuracy
  - **Property 4: Fetch count accuracy**
  - **Validates: Requirements 2.1**
  - _Requirements: 2.1_

- [ ]* 4.4 Write unit tests for email fetching
  - Test handling of missing headers
  - Test inbox with fewer than 20 emails
  - Test error handling for API failures
  - _Requirements: 2.2, 2.3, 2.4_

- [x] 5. Implement AI summarization module





  - Write generate_summary() function that takes email list and API key
  - Format email metadata into structured prompt for Gemini
  - Implement Gemini API call using gemini-pro or gemini-2.5-flash
  - Design prompt to request High/Medium/Low priority categorization
  - Design prompt to request bullet-point format
  - Parse AI response into formatted summary text
  - Add error handling for missing API key
  - Add error handling for Gemini API failures
  - Add error handling for malformed responses
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 5.1 Write property test for summary metadata completeness
  - **Property 5: Summary metadata completeness**
  - **Validates: Requirements 3.1**
  - _Requirements: 3.1_

- [ ]* 5.2 Write property test for summary structure
  - **Property 6: Summary structure**
  - **Validates: Requirements 3.2, 3.3**
  - _Requirements: 3.2, 3.3_

- [ ]* 5.3 Write property test for summary item format
  - **Property 7: Summary item format**
  - **Validates: Requirements 3.4**
  - _Requirements: 3.4_

- [ ]* 5.4 Write unit tests for AI summarization
  - Test prompt formatting with various email counts
  - Test error handling for API failures
  - Test handling of malformed AI responses
  - _Requirements: 3.1, 3.5, 3.5_

- [x] 6. Implement summary saving module





  - Write save_summary() function that takes summary text
  - Create summaries directory if it doesn't exist
  - Generate filename with timestamp: summary_YYYY-MM-DD_HH-MM-SS.txt
  - Write summary to file
  - Return full file path
  - Add error handling for directory creation failures
  - Add error handling for file write failures
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ]* 6.1 Write property test for summary file persistence
  - **Property 8: Summary file persistence**
  - **Validates: Requirements 4.1, 4.2**
  - _Requirements: 4.1, 4.2_

- [ ]* 6.2 Write unit tests for summary saving
  - Test directory creation when it doesn't exist
  - Test filename format with timestamp
  - Test error handling for write failures
  - _Requirements: 4.3, 4.2, 4.4_

- [x] 7. Implement main orchestration function





  - Write main() function to coordinate all modules
  - Load environment variables
  - Validate configuration
  - Call authenticate_gmail()
  - Call fetch_emails()
  - Call generate_summary()
  - Call save_summary()
  - Display progress messages for each step
  - Display success message with file path
  - Implement top-level error handling
  - Exit with status code 0 on success
  - Exit with non-zero status code on errors
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 7.1 Write property test for error handling consistency
  - **Property 9: Error handling consistency**
  - **Validates: Requirements 1.4, 2.4, 3.5, 4.4, 6.3**
  - _Requirements: 1.4, 2.4, 3.5, 4.4, 6.3_

- [ ]* 7.2 Write property test for successful execution exit code
  - **Property 10: Successful execution exit code**
  - **Validates: Requirements 6.2**
  - _Requirements: 6.2_

- [ ]* 7.3 Write property test for progress visibility
  - **Property 11: Progress visibility**
  - **Validates: Requirements 6.4**
  - _Requirements: 6.4_

- [ ]* 7.4 Write property test for API error handling presence
  - **Property 12: API error handling presence**
  - **Validates: Requirements 7.5**
  - _Requirements: 7.5_

- [ ]* 7.5 Write unit tests for main orchestration
  - Test successful end-to-end execution
  - Test error propagation from each module
  - Test progress message display
  - _Requirements: 6.1, 6.3, 6.4_

- [x] 8. Create documentation





  - Write README.md with project overview
  - Document setup instructions for Google Cloud Console
  - Document OAuth credentials.json setup
  - Document Gemini API key setup
  - Document how to run the application
  - Include example summary output
  - Add troubleshooting section
  - _Requirements: 6.1_

- [x] 9. Final checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.
