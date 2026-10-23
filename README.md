# 💸 Expense Tracker

A Python expense tracking application with a **command-line version** and a **web version (Streamlit)**. Data is stored in a local **SQLite** database.

## Features
- Add, view, and delete expenses
- Category-wise and month-wise spending reports
- Input validation (bad amounts, dates, or IDs never crash the app)
- Logging of actions and errors to `expense_tracker.log`
- Web dashboard with charts, deployable free on Streamlit Community Cloud

## Demo
- Live app: _add your Streamlit link here_
- Demo video: _add your video link here_

## Project Structure
```
expense-tracker/
├── main.py            # CLI interface (menu, input, output)
├── streamlit_app.py   # Web interface
├── database.py        # All SQLite queries
├── services.py        # Input validation and formatting
├── logger.py          # Logging configuration
├── requirements.txt
└── README.md
```

## Architecture
```
 main.py (CLI) ─┐
                ├─> services.py  (validate input)
 streamlit_app ─┤
                └─> database.py ──> expenses.db (SQLite)
 (all modules) ─────────────────> logger.py ──> expense_tracker.log
```
The UI files only take input and show output. Validation lives in `services.py` and every SQL query lives in `database.py`, so both interfaces share the same logic.

## Database Schema
Table: `expenses`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key, auto-increment |
| amount | REAL | Required, must be greater than 0 |
| category | TEXT | Required (e.g. Food, Travel) |
| description | TEXT | Optional |
| date | TEXT | `YYYY-MM-DD`, required |

## Error Handling
- Invalid amount, category, or date -> user is asked again with a clear message
- Database failures -> caught as `DatabaseError`, logged, friendly message shown
- Unexpected errors -> full traceback written to the log, app keeps running

## Setup
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```
Run the CLI version (no installs needed):
```bash
python main.py
```
Run the web version:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy (free)
1. Push the project to GitHub
2. Go to https://share.streamlit.io and sign in with GitHub
3. Click **Create app**, choose your repo, set main file to `streamlit_app.py`, then **Deploy**

Note: on Streamlit Cloud the SQLite file can reset when the app restarts, which is fine for a demo.

## What I Learned
- Splitting code into modules
- Working with SQLite from Python
- Exception handling and input validation
- Logging with the `logging` module
- Git, GitHub, and deploying with Streamlit

## Future Improvements
- Monthly budget limits and alerts
- Export to CSV
- Edit existing expenses
