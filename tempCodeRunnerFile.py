from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS, EXCLUDE_KEYWORDS
from job_scraper import search_jobs
from apply import apply_to_job

def login_to_linkedin(page):
    page.goto("https://www.linkedin.com/login")
    page.fill('input[name="session_key"]', LINKEDIN_EMAIL)
    page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_timeout(3000)
    assert "feed" in page.url
    print("✅ Logged in to LinkedIn.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        login_to_linkedin(page)
        jobs = search_jobs(page, KEYWORDS, LOCATION, max_pages=10, exclude_keywords=EXCLUDE_KEYWORDS)

        print(f"\n🧾 Total Easy Apply Jobs: {len(jobs)}")
        for job in jobs:
            success = apply_to_job(page, job)
            if success:
                print(f"🟢 Applied to: {job['title']}")
            else:
                print(f"🔴 Skipped: {job['title']}")

        browser.close()
