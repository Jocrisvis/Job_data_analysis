import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def insert_company(slug: str, name: str) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO companies (slug, name)
        VALUES (%s, %s)
        ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
    """, (slug, name))

    company_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return company_id


def insert_job(job: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO jobs (
            id, company_id, title, department, location,
            requisition_id, first_published, updated_at,
            url, pay_min, pay_max, currency, description
        ) VALUES (
            %(id)s, %(company_id)s, %(title)s, %(department)s, %(location)s,
            %(requisition_id)s, %(first_published)s, %(updated_at)s,
            %(url)s, %(pay_min)s, %(pay_max)s, %(currency)s, %(description)s
        )
        ON CONFLICT (id) DO UPDATE SET
            title          = EXCLUDED.title,
            department     = EXCLUDED.department,
            location       = EXCLUDED.location,
            updated_at     = EXCLUDED.updated_at,
            url            = EXCLUDED.url,
            pay_min        = EXCLUDED.pay_min,
            pay_max        = EXCLUDED.pay_max,
            currency       = EXCLUDED.currency,
            description    = EXCLUDED.description
    """, job)

    conn.commit()
    cur.close()
    conn.close()