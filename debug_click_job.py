from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS
import time

def debug_click_job():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto("https://www.linkedin.com/login")
        page.fill('input[name="session_key"]', LINKEDIN_EMAIL)
        page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
        page.click('button[type="submit"]')
        
        # Wait for login
        page.wait_for_timeout(8000)
        
        # Go to jobs search
        keyword = KEYWORDS[0]  # Use first keyword
        search_url = (
            f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            f"&location={LOCATION.replace(' ', '%20')}&f_AL=true&f_TPR=r8640&f_WT=2"
        )
        page.goto(search_url)
        page.wait_for_timeout(5000)
        
        # Find job cards
        job_cards = page.query_selector_all("div.job-card-container")
        print(f"✅ Found {len(job_cards)} job cards")
        
        if len(job_cards) > 0:
            # Click on the first job card
            first_card = job_cards[0]
            print("🖱️ Clicking on first job card...")
            
            # Get title before clicking
            title_elem = first_card.query_selector("a")
            title = title_elem.inner_text().strip() if title_elem else "No title"
            if "\n" in title:
                title = title.split("\n")[0].strip()
            print(f"📋 Job title: {title}")
            
            # Click the card
            first_card.click()
            page.wait_for_timeout(3000)
            
            # Check if details pane loaded
            details_pane = page.query_selector("#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details")
            if details_pane:
                print("✅ Job details pane loaded")
                
                # Look for Easy Apply button
                apply_btn = page.query_selector("#jobs-apply-button-id")
                if apply_btn:
                    print("✅ Easy Apply button found!")
                    print(f"Button text: {apply_btn.inner_text()}")
                else:
                    print("❌ Easy Apply button not found")
                    
                    # Check for other apply buttons
                    all_buttons = page.query_selector_all("button")
                    for btn in all_buttons:
                        btn_text = btn.inner_text().strip()
                        if "apply" in btn_text.lower():
                            print(f"Found button with 'apply': '{btn_text}'")
            else:
                print("❌ Job details pane did not load")
        
        # Wait for user to see the page
        print("\n⏳ Waiting 30 seconds for you to inspect the page...")
        time.sleep(30)
        
        browser.close()

if __name__ == "__main__":
    debug_click_job() 