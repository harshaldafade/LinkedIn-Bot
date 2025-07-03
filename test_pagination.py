from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS
import time

def test_pagination():
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
            f"&location={LOCATION.replace(' ', '%20')}&f_AL=true&f_TPR=r86400&f_WT=2"
        )
        page.goto(search_url)
        page.wait_for_timeout(5000)
        
        # Test pagination for 3 pages
        for page_num in range(1, 4):
            print(f"\n📄 Testing page {page_num}...")
            
            # Count jobs on current page
            job_cards = page.query_selector_all("div.job-card-container")
            print(f"✅ Found {len(job_cards)} job cards on page {page_num}")
            
            # Show first few job titles
            for i, card in enumerate(job_cards[:3]):
                title_elem = card.query_selector("a")
                title = title_elem.inner_text().strip() if title_elem else "No title"
                if "\n" in title:
                    title = title.split("\n")[0].strip()
                print(f"   Job {i}: {title}")
            
            # Try to go to next page
            if page_num < 3:
                print(f"➡️ Attempting to go to page {page_num + 1}...")
                
                # Look for next button
                next_btn = page.query_selector("button.artdeco-pagination__button--next")
                if next_btn:
                    print(f"✅ Next button found: {next_btn.inner_text()}")
                    if next_btn.is_enabled():
                        print("✅ Next button is enabled, clicking...")
                        next_btn.click()
                        time.sleep(4)
                    else:
                        print("❌ Next button is disabled")
                        break
                else:
                    print("❌ Next button not found")
                    break
        
        print("\n⏳ Waiting 10 seconds for you to inspect...")
        time.sleep(10)
        
        browser.close()

if __name__ == "__main__":
    test_pagination() 