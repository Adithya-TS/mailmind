You are an expert software engineer. 
Your task is to generate a complete, production-quality Python project based on the specification below. 
Follow each section carefully. 
Use hidden deliberate reasoning internally before producing your final answer. 
Do NOT include your chain of thought — only final results.

────────────────────────────────────────
PROJECT SPECIFICATION
────────────────────────────────────────

Project Name:
MailMind – AI Email Summarizer

One-Line Goal:
“I hate reading long emails, so I built MailMind — an AI bot that reads my Gmail inbox and sends me a daily summary.”

Core Features:
1. Connect to Gmail using Gmail API via OAuth (credentials.json + token.json).
2. Fetch the latest 20 emails: subject + sender only.
3. Send the email metadata to an AI model and generate:
   - A concise daily summary
   - Categorized priorities: High, Medium, Low
   - Bullet points under each category
4. Email the generated summary back to the user’s Gmail.
5. Use `.env` file for GEMINI_KEY.
6. Code should run with a single command:
   python main.py

────────────────────────────────────────
TECHNICAL REQUIREMENTS
────────────────────────────────────────

Language:
Python 3.10+

Libraries:
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- geminikey
- python-dotenv
- base Python libraries

Architecture Criteria:
- Clean, readable code
- Separate logical units (fetching, summarizing, sending)
- Error handling for Gmail API and AI API
- Comments for clarity

────────────────────────────────────────
DELIVERABLES
────────────────────────────────────────

Generate the following in the final output:

1. main.py  
   - Complete working script  
   - Gmail authentication  
   - Email fetching  
   - AI summarization  
   - Email sending  
   - Clear function separation  

2. requirements.txt  
   - Include all needed pip packages  

3. README.md  
   Must include:
   - Project explanation  
   - Setup instructions  
   - How to run  
   - Example summary output  
   - Troubleshooting  

4. Folder structure:
   mailmind/
     ├─ main.py
     ├─ requirements.txt
     ├─ README.md
     ├─ .env.example



────────────────────────────────────────
OUTPUT FORMAT
────────────────────────────────────────

Return your answer IN THIS STRUCTURE ONLY:

1. 📁 Folder Structure  
2. 🧠 main.py  
3. 📄 requirements.txt  
4. 📝 README.md  
5. 🔧 .env.example  
6. 🎤 30-Second Pitch  

Do NOT include explanations, chain of thought, or extra comments outside the generated files.

────────────────────────────────────────

Begin.
