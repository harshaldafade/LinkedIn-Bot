from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS, EXCLUDE_KEYWORDS
from job_scraper import search_and_apply_jobs
import time

def login_to_linkedin(page):
    page.goto("https://www.linkedin.com/login")
    page.fill('input[name="session_key"]', LINKEDIN_EMAIL)
    page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
    page.click('button[type="submit"]')
    
    # Wait for either successful login or security check
    try:
        # Wait longer for initial page load
        page.wait_for_timeout(8000)  # Increased initial wait
        
        # Check for various security check indicators
        security_check_selectors = [
            'div[role="dialog"]',  # Any dialog
            'div.challenge-dialog',  # Challenge dialog
            'div[class*="challenge"]',  # Any element with "challenge" in class
            'div[class*="security"]',  # Any element with "security" in class
            'div[class*="verification"]',  # Any element with "verification" in class
            'div[class*="captcha"]',  # Any element with "captcha" in class
            'div[class*="puzzle"]',  # Any element with "puzzle" in class
            'iframe[src*="challenge"]',  # Challenge iframe
            'iframe[src*="security"]',  # Security iframe
            'iframe[src*="captcha"]',  # Captcha iframe
        ]
        
        # Initial check for security check
        security_check_present = False
        for _ in range(3):  # Try multiple times
            for selector in security_check_selectors:
                try:
                    if page.query_selector(selector):
                        security_check_present = True
                        print("⚠️ Security check detected. Please complete the puzzle manually.")
                        break
                except Exception:
                    continue
            if security_check_present:
                break
            page.wait_for_timeout(2000)  # Wait between attempts
        
        # If no security check detected, check if we're already logged in
        if not security_check_present:
            if "feed" in page.url or "jobs" in page.url:
                print("✅ Already logged in to LinkedIn.")
                return
            # Wait a bit more and check again
            page.wait_for_timeout(5000)
            if "feed" in page.url or "jobs" in page.url:
                print("✅ Logged in to LinkedIn.")
                return
        
        # If security check is present, wait for completion
        if security_check_present:
            max_wait_time = 600  # 10 minutes maximum wait
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                try:
                    # Check if we're on the feed or jobs page (indicating successful login)
                    if "feed" in page.url or "jobs" in page.url:
                        print("✅ Security check completed successfully.")
                        return
                    
                    # Check if any security check dialog is still present
                    dialog_still_present = False
                    for selector in security_check_selectors:
                        if page.query_selector(selector):
                            dialog_still_present = True
                            break
                    
                    if not dialog_still_present:
                        # If no dialog is present and we're not on feed/jobs, wait a bit more
                        page.wait_for_timeout(3000)
                        if "feed" in page.url or "jobs" in page.url:
                            print("✅ Security check completed successfully.")
                            return
                    
                    time.sleep(3)  # Wait a bit before checking again
                    
                except Exception:
                    time.sleep(3)
                    continue
            
            # If we've waited the maximum time, check one last time
            if "feed" in page.url or "jobs" in page.url:
                print("✅ Security check completed successfully.")
                return
            else:
                print("❌ Login failed after security check timeout.")
                raise Exception("Login failed after security check timeout")
        
    except Exception as e:
        # If any error occurs, verify we're logged in
        if "feed" in page.url or "jobs" in page.url:
            print("✅ Logged in to LinkedIn.")
            return
        print(f"❌ Login failed: {e}")
        raise Exception(f"Login failed: {e}")
    
    # Wait a bit after login to ensure everything is loaded
    page.wait_for_timeout(3000)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        login_to_linkedin(page)
        search_and_apply_jobs(page, KEYWORDS, LOCATION, max_pages=10, exclude_keywords=EXCLUDE_KEYWORDS)

        browser.close()

if __name__ == "__main__":
    main()
