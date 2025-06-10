from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS
import time

SEARCH_KEYWORD = KEYWORDS[0]  # Use the first keyword for demo
SEARCH_URL = (
    f"https://www.linkedin.com/jobs/search/?keywords={SEARCH_KEYWORD.replace(' ', '%20')}"
    f"&location={LOCATION.replace(' ', '%20')}&f_AL=true&f_TPR=r86400&f_WT=2"
)


def login_to_linkedin(page):
    page.goto("https://www.linkedin.com/login")
    page.fill('input[name="session_key"]', LINKEDIN_EMAIL)
    page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
    page.click('button[type="submit"]')
    
    # Wait for either successful login or security check
    try:
        # Wait for either the feed/jobs page (successful login) or security check
        page.wait_for_selector('div[role="dialog"]:has-text("security check")', timeout=5000)
        print("⚠️ Security check detected. Please complete the puzzle manually.")
        
        # Wait for the user to complete the security check
        while True:
            try:
                # Check if we're on the feed or jobs page (indicating successful login)
                if "feed" in page.url or "jobs" in page.url:
                    print("✅ Security check completed successfully.")
                    break
                # Check if the security check dialog is still present
                if page.query_selector('div[role="dialog"]:has-text("security check")'):
                    time.sleep(1)  # Wait a bit before checking again
                    continue
                # If neither condition is met, we might be on a different page
                break
            except Exception:
                time.sleep(1)
                continue
        
        # Final verification of successful login
        if "feed" in page.url or "jobs" in page.url:
            print("✅ Logged in to LinkedIn.")
        else:
            print("❌ Login failed after security check.")
            raise Exception("Login failed after security check")
            
    except Exception as e:
        # If no security check dialog appears, verify we're logged in
        if "feed" in page.url or "jobs" in page.url:
            print("✅ Logged in to LinkedIn.")
        else:
            print(f"❌ Login failed: {e}")
            raise Exception(f"Login failed: {e}")
    
    # Wait a bit after login to ensure everything is loaded
    page.wait_for_timeout(3000)


def save_jobs_page_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        login_to_linkedin(page)
        page.goto(SEARCH_URL)
        page.wait_for_timeout(5000)
        html = page.content()
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ Saved jobs page HTML to page_source.html")
        browser.close()


if __name__ == "__main__":
    save_jobs_page_html() 