from playwright.sync_api import sync_playwright
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LOCATION, KEYWORDS
import time

def debug_pagination():
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
        
        print("🔍 Looking for pagination buttons...")
        
        # Look for the specific pagination structure
        pagination_ul = page.query_selector("ul.jobs-search-pagination__pages")
        if pagination_ul:
            print("✅ Found pagination UL")
            print(f"   HTML: {pagination_ul.inner_html()}")
            
            # Look for next button in the pagination
            next_buttons = pagination_ul.query_selector_all("button")
            for i, btn in enumerate(next_buttons):
                try:
                    btn_text = btn.inner_text().strip()
                    btn_class = btn.get_attribute("class")
                    print(f"   Button {i}: '{btn_text}' (class: {btn_class})")
                    
                    # Check if it's the next button
                    if "next" in btn_class.lower() or "next" in btn_text.lower():
                        print(f"   ✅ This looks like the next button!")
                        print(f"   Enabled: {btn.is_enabled()}")
                        print(f"   Visible: {btn.is_visible()}")
                except Exception as e:
                    print(f"   Error with button {i}: {e}")
        else:
            print("❌ Pagination UL not found")
        
        # Try the correct selector
        correct_next_btn = page.query_selector("button.jobs-search-pagination__button--next")
        if correct_next_btn:
            print(f"✅ Found correct next button: {correct_next_btn.inner_text()}")
            print(f"   Enabled: {correct_next_btn.is_enabled()}")
        else:
            print("❌ Correct next button not found")
        
        print("\n⏳ Waiting 10 seconds for you to inspect...")
        time.sleep(10)
        
        browser.close()

if __name__ == "__main__":
    debug_pagination() 