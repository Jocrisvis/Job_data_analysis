# Greenhouse Job Board ETL

A Python ETL pipeline that pulls job postings from the [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html) and stores them in a PostgreSQL database.

## What it does

- Fetches job listings for a list of companies via the Greenhouse public API
- Cleans HTML descriptions
- Upserts records into PostgreSQL — no duplicates, always fresh data

## Project structure

```
├── main.py                 # Entry point
├── config.py               # Companies list and DB config (reads from .env)
├── collectors/
│   └── greenhouse.py       # API calls
├── database/
│   └── db.py               # DB insert/upsert logic
├── .env                   
└── .gitignore
```

## Scheduling

Use Windows Task Scheduler (or cron on Mac/Linux) to run `main.py` automatically on a schedule. The upsert logic ensures re-runs never create duplicates.

## Notes

The main objective is to create a summary of the main tasks in a job, highlight potential skills, salary and to create a job website. 

- Uses the Greenhouse public Job Board API — no API key required
- Deduplication is handled via `ON CONFLICT (id) DO UPDATE` in PostgreSQL
- Credentials are managed via `.env` and never hardcoded
