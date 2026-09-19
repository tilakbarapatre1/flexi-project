# Employee Leave Automation — Beginner Project

This is a simple beginner-friendly Gradio + SQLite project.

## Run
1. Install Python 3.10+.
2. Open this folder in VS Code / Antigravity.
3. Open Terminal.
4. Run:
   pip install -r requirements.txt
5. Run:
   python app.py
6. Open the local Gradio URL shown in the terminal.

## Demo logins
Manager:
- Email: manager@company.com
- Password: manager123

Employee:
- Email: employee@company.com
- Password: employee123

The database is created automatically as `leave_automation.db`.

## Important
The AI part is implemented as a rule-based "Leave Agent" first, so the project works without an API key. Later, an LLM can be connected to explain recommendations in natural language.
