from config import COMPANIES
from collectors.greenhouse import fetch_jobs, fetch_job_detail
from database.db import insert_company, insert_job
from html import unescape
from bs4 import BeautifulSoup


for company_slug in COMPANIES:
    print(f"\nProcessing {company_slug}...")
    jobs = fetch_jobs(company_slug)
    print(f"Found {len(jobs)} jobs")

    company_id = insert_company(company_slug, jobs[0].get("company_name") if jobs else company_slug)

    for job in jobs:
        detail = fetch_job_detail(company_slug, job["id"])

        raw_html = detail.get("content", "")
        clean_text = BeautifulSoup(unescape(raw_html), "html.parser").get_text(separator="\n")

        pay_ranges = detail.get("pay_input_ranges", [])
        if pay_ranges:
            pay_min = pay_ranges[0].get("min_cents", 0) / 100
            pay_max = pay_ranges[0].get("max_cents", 0) / 100
            currency = pay_ranges[0].get("currency_type", "N/A")
        else:
            pay_min = pay_max = currency = None

        job_record = {
            "id":               job["id"],
            "company_id":       company_id,
            "title":            detail.get("title"),
            "department":       detail.get("departments", [{}])[0].get("name") if detail.get("departments") else None,
            "location":         detail.get("location", {}).get("name"),
            "requisition_id":   job.get("requisition_id"),
            "first_published":  job.get("first_published"),
            "updated_at":       job.get("updated_at"),
            "url":              job.get("absolute_url"),
            "pay_min":          pay_min,
            "pay_max":          pay_max,
            "currency":         currency,
            "description":      clean_text
        }

        insert_job(job_record)
        print(f"  Saved: {detail.get('title')}")

print("\nDone! Cristhian cara sepia, all jobs saved to database.")

'''
# This is just to test if I had access to the connection

from database.db import get_connection

try:
    conn = get_connection()
    print("Connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
'''