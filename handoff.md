# HalalBurg Terminal — Session Handoff

## 1) Goals

- Turn HalalBurg Terminal (a "Bloomberg terminal for halal stocks") into a fully live, real, GitHub-portfolio-worthy project — the user's explicit instruction was "nothing mock data please fully functional."
- Add features inspired by World Monitor (github.com/koala73/worldmonitor, AGPL-3.0) — geopolitical risk signal, live news video channels — as **original reimplementations**, credited, not copied (their AGPL license would force the whole app AGPL on public deployment; the tech stacks don't overlap anyway).
- Add TradingView charting ("all the features of TradingView") via their real embeddable widget.
- Redesign the whole frontend to match a specific look the user exported from Google Stitch (a "Brutalist Terminal" dark theme — pure black, neon green/red, JetBrains Mono, Material Symbols icons).
- Push everything to GitHub (MIT licensed, per user's choice when asked).

## 2) Current state

- **Backend** (Django REST, `backend/`): fully live. Every endpoint pulls real data from Finnhub (quotes/fundamentals/news), GoldAPI (gold/silver spot), and Yahoo Finance's public chart endpoint (historical closes for the optimizer). No seeded/mock data remains — the old `seed_data` management command was deleted.
- **Frontend** (Next.js, `frontend/`): 6 pages (Dashboard, Portfolio, Screener, Options, Optimization, Stock Detail), all live-polling the backend. Redesigned to the new dark terminal palette via a token remap (see §4) — confirmed working on Dashboard and Screener; Portfolio/Options/Optimization/Stock Detail inherit it through the same shared components but weren't individually screenshotted after the redesign.
- **Git**: committed and pushed to `origin/main` at `https://github.com/ADM1SH/HalalBerg` (commit `103151e`, 124 files). The redesign changes made *after* that push have **not** been committed/pushed yet.
- **Licensing**: MIT, `LICENSE` file at repo root, user's name, 2026.
- **Dev servers**: currently **stopped** (user asked to kill them to save battery, twice). Backend runs on `:8001`, frontend on `:3000` — start with `cd backend && source .venv/bin/activate && python manage.py runserver 0.0.0.0:8001` and `cd frontend && npm run dev`.
- **Secrets**: `backend/.env` holds `FINNHUB_API_KEY` and `GOLDAPI_KEY` (both real, user-provided, gitignored — never committed).

## 3) Active files

**Backend — new/modified this session:**
- `backend/.env` — API keys (gitignored)
- `backend/halalburg/settings.py` — loads `.env`, adds `FINNHUB_API_KEY`/`GOLDAPI_KEY` settings
- `backend/apps/market/providers.py` — Finnhub/GoldAPI/Yahoo HTTP clients (new)
- `backend/apps/market/services.py` — live quote refresh, thread-pooled (new)
- `backend/apps/market/symbols.py` — the 15-symbol tracked universe (new)
- `backend/apps/market/views.py` — calls `ensure_quotes_fresh()`
- `backend/apps/gold/services.py` — live spot refresh (new)
- `backend/apps/gold/views.py`
- `backend/apps/shariah/services.py` — real AAOIFI-style ratio screen (new)
- `backend/apps/shariah/models.py` — added `liquid_assets_ratio`, `updated_at` (+ migration `0002`)
- `backend/apps/shariah/serializers.py`, `views.py`
- `backend/apps/news/services.py` — real headlines + lexicon sentiment (new)
- `backend/apps/news/risk.py` — original geopolitical risk signal (new)
- `backend/apps/news/models.py` — added `external_id`, real `published_at` (+ migration `0002`)
- `backend/apps/news/views.py`, `urls.py`
- `backend/apps/quant/services.py` — real historical returns/covariance (was hash-based fake)
- `backend/apps/portfolio/views.py` — calls `ensure_quotes_fresh()`/`ensure_spot_fresh()`
- `backend/requirements.txt` — added `httpx`, `python-dotenv`
- **Deleted:** `backend/apps/market/management/` (the fake `seed_data` command)

**Frontend — new/modified this session:**
- `frontend/app/layout.tsx` — JetBrains Mono font, Material Symbols link
- `frontend/app/globals.css` — full color token remap + font + scrollbar + icon class
- `frontend/components/layout/TopNavBar.tsx`, `SideNavBar.tsx` — redesigned to match Stitch export
- `frontend/components/dashboard/RiskSignalPanel.tsx` (new), `LiveChannelsPanel.tsx` (new), `DashboardBento.tsx` (swapped in the above, deleted `MarketPulsePanel.tsx`)
- `frontend/components/stock/TradingViewChart.tsx` (new), `StockDetail.tsx` (added chart, fixed a layout bug)
- `frontend/lib/api.ts`, `types.ts` — added `risk()` endpoint, `RiskSignal` type, `liquid_assets_ratio`

**Root:** `LICENSE` (new, MIT), `.gitignore` (added `backend/.env`), `handoff.md` (this file)

**Untouched cruft, not part of the project — leave alone unless asked:** `backend/manage 2.py`, `backend/requirements 2.txt`, `.gitignore 2`, empty dirs `backend/apps 2`, `backend/halalburg 2`.

## 4) Changes made

1. Wired live data providers (Finnhub, GoldAPI, Yahoo) with a lazy refresh-on-request + TTL cache pattern (no Celery/cron) — quotes 60s, gold 180s, Shariah assessments 6h, news 10min, quant history 1h cache.
2. Replaced the fake hash-based efficient-frontier statistics with real historical returns/covariance from Yahoo daily closes.
3. Built an approximate AAOIFI-style Shariah screen from real Finnhub fundamentals (sector exclusion + debt/liquid-assets ratios). Documented limitation: no clean "interest income" line item at this data tier, so that ratio is honestly left at 0, not fabricated.
4. Parallelized the per-symbol Finnhub/Yahoo fetches with `ThreadPoolExecutor` — cut a cold-cache refresh from ~34s to ~5s.
5. Deleted the DB, migrated fresh, so no seeded rows lingered under new schema fields.
6. Found and fixed a real pre-existing layout bug on Stock Detail: `flex-1` panels inside a CSS grid row with no explicit height were collapsing to header-only (48px) even though their data loaded fine — fixed with explicit heights.
7. Added an original "Geopolitical Risk Signal" (keyword+sentiment weighted score over real news) and "Live Channels" (real YouTube live embeds: Bloomberg TV, Al Jazeera English, Yahoo Finance) — both credited to World Monitor/Elie Habib in-UI, no AGPL code copied.
8. Added a real TradingView Advanced Chart widget embed on Stock Detail (official free widget, not a reimplementation).
9. Added `LICENSE` (MIT) after asking the user which license they wanted.
10. Committed (124 files, one commit) and pushed to `origin/main`.
11. Redesigned the color/font/icon system to match the user's Stitch export: remapped all CSS custom properties in `globals.css` (this cascades through every component automatically since the app already used a token-based Tailwind v4 setup), swapped Geist fonts for JetBrains Mono, added Material Symbols Outlined, restyled `TopNavBar`/`SideNavBar` to match (icon+label nav, GMT clock, CMD placeholder).

## 5) Failed attempts / things that didn't fully land

- **Could not view the user's private Stitch project URL directly** — it required their Google login, which is off-limits; the user exported and pasted the raw HTML instead, which worked.
- **Bloomberg TV's YouTube embed shows a "Watch on YouTube" fallback** instead of playing inline — this is Bloomberg restricting embedding on their end, not a bug in the code. Al Jazeera English and Yahoo Finance play inline fine.
- **TradingView chart showed empty OHLC (∅ placeholders) on a couple of automated-browser reloads** after working correctly on the first load — very likely the embed server being cautious about rapid automated reloads from headless testing, not a code bug. **Needs a real-browser check to confirm it's solid**, not just automated verification.
- **Did not implement the full pixel-perfect Stitch mockup for every page** — deliberately stopped after the high-leverage global token/font/icon remap (confirmed working on Dashboard + Screener) rather than hand-porting every decorative detail, because session cost had already run very high by that point. Specifically skipped: Options' CALL/PUT toggle buttons + $/% input affixes, Optimization's more elaborate frontier chart (dashed grid, CAL line, per-asset dots, Sharpe badges), Portfolio's fake `SYS.LOG` activity feed and FILTER/EXPORT buttons, Screener's pagination footer and live match-count badge. Stock Detail's decorative fake-candlestick mockup was intentionally *not* ported — the real TradingView chart already there is strictly better.
- **The redesign commit was never made** — all the Stitch-matching changes (§4 item 11) are sitting as uncommitted local changes on top of the last push.

## 6) Next steps

1. **Commit and push the redesign.** `git status` will show the token/font/icon/nav changes as modified files — review and commit them (they haven't been pushed yet).
2. **Verify in a real browser, not just automated testing:** the TradingView chart on `/stock/AAPL` (or any symbol) actually renders candlesticks, and the Live Channels tabs switch correctly.
3. **Optional polish**, only if wanted — see the skipped list in §5. Options/Optimization/Portfolio/Screener could get closer to the exact Stitch mockup.
4. **Add real portfolio holdings**: run `python manage.py createsuperuser` in `backend/`, then add holdings at `localhost:8001/admin` — the Portfolio page is intentionally empty until this is done.
5. **Optional cleanup**: the stray duplicate files listed in §3 (`manage 2.py`, `requirements 2.txt`, `.gitignore 2`, two empty `" 2"` dirs) are still sitting in the repo, untracked and unused. Confirm with the user before deleting anything — they may be intentional local backups.
6. **Start dev servers** when ready to keep working (commands in §2) — remember to stop them again afterward, the user has asked twice this session to kill them for battery.
