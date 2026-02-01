 🚀 ORBIT: AI-Powered Recruitment System

**Orbit** (Project Space42) is a secure, AI-driven recruitment platform designed to automate candidate screening. It utilizes Large Language Models (LLMs) to parse resumes, algorithmic logic to score candidates ("Pilots"), and generative AI to create dynamic "Boss Fight" interview scenarios.

## 🛸 Mission Overview

The system is built on a modular architecture separating **Security** (Airlock/Vault), **Intelligence** (Parser/Holodeck), and **Data** (SQLite/Encryption).

### Key Features

* **📄 AI Resume Parsing:** Extracts structured data (Skills, Experience, Projects) from PDFs using Llama 3 (via Groq).
* **🛡️ Active Defense:** `Airlock` module scans uploads for Prompt Injection attacks (e.g., "Ignore previous instructions") before processing.
* **🔐 Military-Grade Encryption:** AES-256 encryption for emails and PBKDF2 hashing for passwords.
* **💯 Anti-Gaming Scoring:** customized algorithm (`scoring.py`) that calculates an "Orbit Score" based on project complexity and fuzzy skill matching.
* **🌌 The Holodeck:** Generates a unique, high-stakes "Satellite Crisis" interview scenario based on the candidate's specific technical weaknesses.

---

## 🛠️ System Architecture

| Module | File | Description |
| --- | --- | --- |
| **The Gatekeeper** | `airlock.py` | Handles file sanitization, UUID renaming, and scans text for adversarial AI attacks. |
| **The Vault** | `vault.py` | Manages AES-256 encryption keys and password hashing. Ensures no PII is stored in plaintext. |
| **The Brain** | `parser_SIB.py` | Connects to Groq API to convert raw PDF text into normalized JSON data. |
| **The Manager** | `parser_DB.py` | Orchestrates the parsing process using threading to handle multiple candidates simultaneously. |
| **The Simulator** | `holodeck.py` | Generates "Boss Fight" scenarios using LLMs based on parsed weakness data. |
| **The Judge** | `scoring.py` | Calculates the candidate's match score (0-100) using logic rules and `thefuzz` library. |
| **Database** | `database.py` | SQLite interface handling Candidate and Application tables. Automatically encrypts data on write. |
| **UI Theme** | `design.py` | Contains the CSS design system (Glassmorphism, Animations, Color Variables) for the frontend. |

---

## ⚙️ Installation & Setup

### 1. Prerequisites

Ensure you have Python 3.9+ installed. Install the required dependencies:

```bash
pip install langchain-groq langchain-core pypdf2 thefuzz cryptography python-dotenv

```

### 2. Environment Variables

This system requires a **Groq API Key** to power the AI modules.

1. Create a file named `.env` in the root directory.
2. Add your API key:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here

```



### 3. Database Initialization

The database will automatically initialize (`orbit.db`) and generate an encryption key (`orbit.key`) the first time you run the application or interaction script.

---

## 🚦 Usage

### Running the Analyzer

The core logic is handled by `parser_DB.py`. To process a candidate, the system flows through:

1. **Upload:** File passes through `airlock.secure_upload()`.
2. **Parse:** `parser_DB.process_candidate()` calls `parser_SIB`.
3. **Score:** Data is sent to `scoring.calculate_orbit_score()`.
4. **Save:** Results are encrypted and stored via `database.py`.

### Troubleshooting Common Issues

**🔴 Error: `CRITICAL ERROR: GROQ_API_KEY not found**`

* **Cause:** The `.env` file is missing or Python cannot see it.
* **Fix:** Ensure `.env` exists and contains `GROQ_API_KEY`. If using VS Code, restart the terminal to reload variables.

**🔴 Match Score is 0%**

Cause:The PDF might be an image/scan (unreadable text) OR the API key is missing (silent fail).
Fix: Use a text-based PDF. Check console logs for connection errors.

**🔴 "System Failure: THREAT DETECTED"**

* **Cause:** The uploaded resume contained phrases like "Ignore previous instructions."
* **Fix:** The `airlock.py` module blocked the file to protect the AI. This is intentional behavior.

---
🔒 Security Protocol

File Storage: Uploaded files are renamed to UUIDs to prevent directory traversal attacks.
* **Encryption:** If `orbit.key` is lost, all encrypted emails in the database become unreadable forever. **Do not lose this key.**
* **Injection:** The system scans for `ignore previous instructions` and `DAN mode` patterns before sending text to the LLM.

---

*System Status: ONLINE* 🟢
*Mission Control: Space42*
