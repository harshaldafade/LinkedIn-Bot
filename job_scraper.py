from playwright.sync_api import Page
import time
import os
from apply import apply_to_job


def search_and_apply_jobs(page: Page, keywords: list, location: str, max_pages: int = 25, exclude_keywords: list = None):
    exclude_keywords = exclude_keywords or []
    os.makedirs("screenshots", exist_ok=True)

    for keyword in keywords:
        print(f"\n🔍 Searching for: {keyword}")
        search_url = (
            f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            f"&location={location.replace(' ', '%20')}&f_AL=true&f_TPR=r86400&f_WT=2"
        )
        page.goto(search_url)
        page.wait_for_timeout(4000)

        for page_num in range(1, max_pages + 1):
            print(f"📄 Parsing page {page_num}...")
            try:
                page.wait_for_selector("li.jobs-search-results__job-card-search--generic-occludable-area", timeout=15000)
                job_cards = page.query_selector_all("li.jobs-search-results__job-card-search--generic-occludable-area")
            except Exception as e:
                print(f"⚠️ Timed out or failed to find job listings on page {page_num}: {e}")
                page.screenshot(path=f"screenshots/{keyword.replace(' ', '_')}_timeout_page_{page_num}.png", full_page=True)
                continue

            if not job_cards:
                print("⚠️ No job cards found on this page.")
                page.screenshot(path=f"screenshots/{keyword.replace(' ', '_')}_no_cards_page_{page_num}.png", full_page=True)

            for idx, card in enumerate(job_cards):
                try:
                    card.scroll_into_view_if_needed()
                    page.wait_for_timeout(1000)

                    # Title
                    title_elem = card.query_selector("a.job-card-list__title--link")
                    title = title_elem.inner_text().strip() if title_elem else None

                    # Company
                    company_elem = card.query_selector("div.artdeco-entity-lockup__subtitle span")
                    company = company_elem.inner_text().strip() if company_elem else None

                    # Location
                    location_elem = card.query_selector("div.artdeco-entity-lockup__caption ul.job-card-container__metadata-wrapper li span")
                    location = location_elem.inner_text().strip() if location_elem else None

                    # Link
                    job_link = title_elem.get_attribute("href") if title_elem else None
                    job_id = card.get_attribute("data-job-id")

                    if not title or not company or not location or not job_link:
                        print("⚠️ Missing one or more essential elements in card.")
                        continue

                    if any(ex_kw.lower() in title.lower() for ex_kw in exclude_keywords):
                        print(f"🚫 Skipping job due to excluded keyword: {title}")
                        continue

                    # Easy Apply: check for 'Easy Apply' text in the footer
                    easy_apply_footer = card.query_selector("ul.job-card-container__footer-wrapper")
                    easy_apply = False
                    if easy_apply_footer:
                        easy_apply = 'Easy Apply' in easy_apply_footer.inner_text()
                    if easy_apply:
                        print(f"✅ Found Easy Apply: {title} at {company}")
                        # Click the job card to load the details pane
                        card.click()
                        page.wait_for_timeout(2000)
                        job = {
                            "title": title,
                            "company": company,
                            "location": location,
                            "link": job_link if job_link.startswith("http") else "https://www.linkedin.com" + job_link,
                            "id": job_id,
                            "card_index": idx
                        }
                        success = apply_to_job(page, job)
                        if success:
                            print(f"🟢 Applied to: {title}")
                        else:
                            print(f"🔴 Skipped: {title}")
                except Exception as e:
                    print(f"⚠️ Error parsing job card: {e}")
                    page.screenshot(path=f"screenshots/{keyword.replace(' ', '_')}_error_card_page_{page_num}.png", full_page=True)
                    continue
            # Pagination
            next_btn = page.query_selector("button.jobs-search-pagination__button--next")
            if next_btn and next_btn.is_enabled():
                next_btn.click()
                time.sleep(4)
            else:
                break
