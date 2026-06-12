import requests
import time

BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

# Reuse the same connection instead of opening a new one every call
session = requests.Session()
session.headers.update({
    "User-Agent": "Data_Science_Project_Crist_hr_ian_V_D"  # identify yourself
})


def fetch_jobs(company_slug: str) -> list:
    url = f"{BASE_URL}/{company_slug}/jobs"
    response = session.get(url)

    if response.status_code == 429:  # rate limited
        print(f"Rate limited on {company_slug}, waiting 60s...")
        time.sleep(60)
        return fetch_jobs(company_slug)  # retry

    if response.status_code != 200:
        print(f"Failed for {company_slug}: {response.status_code}")
        return []

    return response.json().get("jobs", [])


def fetch_job_detail(company_slug: str, job_id: int) -> dict:
    url = f"{BASE_URL}/{company_slug}/jobs/{job_id}"

    time.sleep(0.3)  # small delay between detail calls

    response = session.get(url)

    if response.status_code == 429:
        print(f"  Rate limited on job {job_id}, waiting 60s...")
        time.sleep(60)
        return fetch_job_detail(company_slug, job_id)  # retry

    if response.status_code != 200:
        print(f"  Failed detail for job {job_id}")
        return {}

    return response.json()