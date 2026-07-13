# HalalBurg Terminal

A Bloomberg-style terminal for screening and tracking Shariah-compliant stocks — live market data, an AAOIFI-style halal screen, portfolio optimization, gold/silver spot prices, a geopolitical risk signal, and TradingView charting.

No mock data: every number comes from a live provider at request time (with short-lived caching).

## Stack

- **Backend**: Django + Django REST Framework, `cvxpy`/`numpy`/`pandas`/`scipy` for portfolio optimization
- **Frontend**: Next.js 16 (React 19), Tailwind CSS 4
- **Data sources**: [Finnhub](https://finnhub.io) (quotes, fundamentals, news), [GoldAPI](https://www.goldapi.io) (gold/silver spot), Yahoo Finance public chart endpoint (historical closes), TradingView (embedded chart widget)

## Features

- Live-polling dashboard with a geopolitical risk signal and live news channels
- Shariah screener using real Finnhub fundamentals (sector exclusion + debt/liquid-assets ratios)
- Portfolio view with efficient-frontier optimization from real historical returns/covariance
- Options and gold/silver spot pages
- Per-stock detail page with a live TradingView chart

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

Create `backend/.env` with your own API keys:

```
FINNHUB_API_KEY=your_key_here
GOLDAPI_KEY=your_key_here
```

Get a free key at [finnhub.io](https://finnhub.io) and [goldapi.io](https://www.goldapi.io).

### Frontend

```bash
cd frontend
npm install
```

### Run both

```bash
./start.sh
```

Backend: `http://localhost:8001` · Frontend: `http://localhost:3000`

To use the Portfolio page, add holdings via the Django admin:

```bash
cd backend && python manage.py createsuperuser
```

then visit `http://localhost:8001/admin`.

## Credit

The geopolitical risk signal and live news channels are original implementations inspired by [World Monitor](https://github.com/koala73/worldmonitor) (AGPL-3.0) — no code from that project is used.

## License

MIT — see [LICENSE](LICENSE).
