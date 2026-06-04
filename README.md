# HalalBurg Terminal

A modern, comprehensive financial terminal for Shariah-compliant equity screening, dividend purification, and portfolio Zakat management.

## Features

- **Shariah Screening:** Audit and track Shariah compliance of equities using advanced financial metrics.
- **Dividend Purification:** Calculate and track purification metrics for portfolio dividend income.
- **Portfolio Zakat Manager:** Calculate Nisab thresholds and track Zakat requirements for equity portfolios.
- **Offline AI Analysis:** Run offline financial news summary and sentiment analysis using local LLM engines (Ollama / LM Studio).
- **Macroeconomics & Insights:** Track key macroeconomic indicators using FRED, Finnhub, and FMP data.

## Tech Stack

- **Backend:** Django (Python 3)
- **Data Integration:** Financial Modeling Prep (FMP), Finnhub, FRED, GoldAPI.io
- **Local AI:** Ollama / LM Studio (e.g., Qwen 2.5/3 Coder)
- **Frontend/UI:** Web terminal interfaces (Mock Design references included)

## Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ADM1SH/HalalBerg.git
   cd HalalBerg
   ```

2. **Configure Environment Variables:**
   Create a `.env` file inside the `backend/` directory based on `backend/.env.example`:
   ```bash
   cp backend/.env.example backend/.env
   # Add your production API keys to backend/.env
   ```

3. **Install Dependencies & Run Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

## Development and Mockups
The repository contains design files and reference structures under `/mock design/`.
