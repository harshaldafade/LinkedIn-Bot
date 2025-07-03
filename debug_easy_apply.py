from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS
import time

def debug_easy_apply():
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
        
        for idx, card in enumerate(job_cards[:5]):  # Check first 5 cards
            print(f"\n📋 Job Card {idx}:")
            
            # Get title
            title_elem = card.query_selector("a")
            title = title_elem.inner_text().strip() if title_elem else "No title"
            if "with verification" in title:
                title = title.split("with verification")[0].strip()
            print(f"   Title: {title}")
            
            # Check for Easy Apply in footer
            footer = card.query_selector("div.job-search-card__footer")
            if footer:
                footer_text = footer.inner_text()
                print(f"   Footer text: '{footer_text}'")
                has_easy_apply = 'Easy Apply' in footer_text
                print(f"   Has Easy Apply: {has_easy_apply}")
            else:
                print(f"   No footer found")
            
            # Check for Easy Apply button
            easy_apply_btn = card.query_selector("button.jobs-apply-button")
            if easy_apply_btn:
                print(f"   Easy Apply button found: {easy_apply_btn.inner_text()}")
            else:
                print(f"   No Easy Apply button")
            
            # Check for any button with "Apply" text
            all_buttons = card.query_selector_all("button")
            for btn in all_buttons:
                btn_text = btn.inner_text().strip()
                if "apply" in btn_text.lower():
                    print(f"   Found button with 'apply': '{btn_text}'")
            
            # Check for any text containing "Easy Apply"
            card_text = card.inner_text()
            if "Easy Apply" in card_text:
                print(f"   'Easy Apply' found in card text")
            else:
                print(f"   'Easy Apply' NOT found in card text")
        
        # Wait for user to see the page
        print("\n⏳ Waiting 30 seconds for you to inspect the page...")
        time.sleep(30)
        
        browser.close()

if __name__ == "__main__":
    debug_easy_apply() 