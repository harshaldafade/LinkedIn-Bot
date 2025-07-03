from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS
import time

def debug_linkedin_structure():
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
        
        # Take screenshot
        page.screenshot(path="screenshots/debug_current.png", full_page=True)
        
        # Try to find job cards
        print("🔍 Looking for job cards...")
        
        # Try different selectors
        selectors = [
            "div.job-card-container",
            "li.jobs-search-results__job-card-search--generic-occludable-area",
            "div.base-card",
            "div.job-search-card",
            "div[data-job-id]",
            "li"
        ]
        
        for selector in selectors:
            try:
                cards = page.query_selector_all(selector)
                print(f"✅ Found {len(cards)} elements with selector: {selector}")
                
                if len(cards) > 0:
                    # Inspect the first card
                    first_card = cards[0]
                    print(f"\n📋 First card HTML structure:")
                    print(first_card.inner_html()[:500] + "...")
                    
                    # Try to find title in this card
                    title_selectors = [
                        "a.job-card-list__title",
                        "h3.base-search-card__title a",
                        "a[data-control-name='job_card_click']",
                        "h3 a",
                        "a",
                        "h3",
                        "h2",
                        "h1"
                    ]
                    
                    for title_selector in title_selectors:
                        title_elem = first_card.query_selector(title_selector)
                        if title_elem:
                            title_text = title_elem.inner_text().strip()
                            print(f"✅ Found title with '{title_selector}': '{title_text}'")
                            break
                    else:
                        print(f"❌ No title found with any selector in first card")
                    
                    break
                    
            except Exception as e:
                print(f"❌ Selector {selector} failed: {e}")
        
        # Wait for user to see the page
        print("\n⏳ Waiting 30 seconds for you to inspect the page...")
        time.sleep(30)
        
        browser.close()

if __name__ == "__main__":
    debug_linkedin_structure() 