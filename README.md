# Automated School Schedule Telegram Bot

[![Python](https://shields.io)](https://python.org)
[![Aiogram](https://shields.io)](https://aiogram.dev)
[![Database](https://shields.io)](https://sqlite.org)
[![License: MIT](https://shields.io)](https://opensource.org)

## 📌 Overview & Motivation
In educational institutions with dynamic schedules and multiple shifts, distributing daily timetable updates manually often leads to delays and communication bottlenecks. 

This project is a **production-grade, asynchronous Telegram bot** designed to automate the ingestion, parsing, and personalized delivery of school schedules. Serving **600+ daily active users (DAU)** across 1st and 2nd school shifts, the system eliminates manual intervention by continuously synchronizing with live cloud spreadsheets and delivering timely, segmented notifications.

---

## 🏗️ System Architecture & Data Pipeline
The application follows a modular architecture separating data ingestion, state management, database persistence, and user interaction:

1. **Automated Data-Ingestion Pipeline (`excel.py`):**
   * Polls live **Google Sheets** via HTTP requests (`requests`) every **2 minutes**.
   * Streams and parses dynamic `.xlsx` spreadsheets directly **in memory** using `openpyxl` and `io.BytesIO`, avoiding disk I/O overhead and eliminating the need for manual schedule uploads.
   * Transforms unstructured tabular timetable grids into structured, queryable schedule records by grade and shift.

2. **Relational Storage & Segmentation (`database.py`):**
   * Uses a lightweight relational **SQLite3** database to persist user profiles, shift assignments, and grade segments.
   * Enables targeted data retrieval and segmented broadcast delivery.

3. **Asynchronous Interaction & State Management (`handlers.py`, `states.py`, `keyboards.py`):**
   * Built on `aiogram 3` (`asyncio`) for non-blocking concurrent request handling.
   * Implements a **Finite State Machine (FSM)** to guide users through structured onboarding (selecting school shift and class/grade) and profile updates.

4. **Fault-Tolerant Scheduled Broadcasting (`main.py`):**
   * Integrates **APScheduler** for automated cron-based daily schedule dispatches.
   * Implements rate-limiting and robust exception handling (specifically managing `TelegramForbiddenError` for blocked users and `TelegramRetryAfter` for API flood limits) to ensure uninterrupted delivery at scale.

---

## 🛠️ Tech Stack
* **Core Language:** Python 3.10+ (`asyncio`, `io.BytesIO`)
* **Bot Framework:** Aiogram 3.x (FSM, Routers, Inline/Reply Keyboards)
* **Data Ingestion & Parsing:** Requests, OpenPyXL, Google Sheets REST/Export API
* **Database:** SQLite3
* **Task Scheduling:** APScheduler (Cron triggers)

---

## 📂 Repository Structure
```text
schoolbot/
├── main.py             # Entry point, bot initialization, and APScheduler cron setup
├── handlers.py         # Asynchronous message and callback query handlers
├── states.py           # Finite State Machine (FSM) definitions for user onboarding
├── keyboards.py        # Dynamic inline and reply keyboard builders
├── database.py         # SQLite3 connection management and CRUD operations
├── excel.py            # In-memory Google Sheets fetching and OpenPyXL parsing logic
└── requirements.txt    # Python dependencies
```

---

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com
cd schoolbot
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file (or configure environment variables directly) with your Telegram Bot Token and target Google Sheets URL:
```env
BOT_TOKEN=your_telegram_bot_token_here
SHEET_URL=your_google_sheets_export_url_here
```

### 4. Run the application
```bash
python main.py
```

---

## 📊 Production Impact & Key Metrics
* **Active User Base:** 600+ Daily Active Users (DAU) across two school shifts.
* **Data Latency:** ≤ 2 minutes from spreadsheet edit to bot availability via automated in-memory syncing.
* **Reliability:** Automated exception handling and API rate-limit compliance prevent broadcast crashes during peak morning traffic.

---

## 🔮 Future Improvements
* **Database Migration:** Migrate from SQLite3 to **PostgreSQL** with connection pooling (`asyncpg`) to support higher write concurrency.
* **Analytics & Telemetry:** Add structured logging and usage analytics (e.g., peak query times, most requested grade schedules) to optimize caching intervals.
* **Containerization:** Add a `Dockerfile` and `docker-compose.yml` for reproducible cloud deployment.
