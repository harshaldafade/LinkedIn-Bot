from playwright.sync_api import Page
import time
import os
from apply import apply_to_job


def scroll_to_load_all_jobs(page: Page):
    """Scroll through the job list to load all jobs on the current page."""
    print("📜 Scrolling to load all jobs...")
    
    # Get initial job count
    initial_jobs = page.query_selector_all("div.job-card-container")
    print(f"📊 Initial job count: {len(initial_jobs)}")
    
    last_job_count = len(initial_jobs)
    scroll_attempts = 0
    max_scroll_attempts = 10
    
    while scroll_attempts < max_scroll_attempts:
        # Scroll to the bottom of the job list
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        
        # Check if new jobs loaded
        current_jobs = page.query_selector_all("div.job-card-container")
        print(f"📊 Current job count: {len(current_jobs)}")
        
        if len(current_jobs) == last_job_count:
            # No new jobs loaded, try scrolling a bit more
            page.evaluate("window.scrollBy(0, 1000)")
            page.wait_for_timeout(1000)
            current_jobs = page.query_selector_all("div.job-card-container")
            
            if len(current_jobs) == last_job_count:
                print(f"✅ All jobs loaded. Total: {len(current_jobs)}")
                break
        
        last_job_count = len(current_jobs)
        scroll_attempts += 1
    
    return page.query_selector_all("div.job-card-container")


def search_and_apply_jobs(page: Page, keywords: list, location: str, max_pages: int = 25, exclude_keywords: list = None):
    exclude_keywords = exclude_keywords or []
    os.makedirs("screenshots", exist_ok=True)

    for keyword in keywords:
        print(f"\n🔍 Searching for: {keyword}")
        print(f"📍 Location: {location}")
        
        try:
            search_url = (
                f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
                f"&location={location.replace(' ', '%20')}&f_AL=true&f_TPR=r86400"
            )
            print(f"🔗 URL: {search_url}")
            page.goto(search_url)
            page.wait_for_timeout(4000)
        except Exception as e:
            print(f"❌ Error navigating to search page: {e}")
            continue

        total_jobs_processed = 0
        
        for page_num in range(1, max_pages + 1):
            print(f"📄 Parsing page {page_num}...")
            
            try:
                # Use the working selector we found
                page.wait_for_selector("div.job-card-container", timeout=15000)
                
                # Scroll to load all jobs on this page
                job_cards = scroll_to_load_all_jobs(page)
                print(f"✅ Found {len(job_cards)} job cards after scrolling")
                    
            except Exception as e:
                print(f"⚠️ Timed out or failed to find job listings on page {page_num}: {e}")
                page.screenshot(path=f"screenshots/{keyword.replace(' ', '_')}_timeout_page_{page_num}.png", full_page=True)
                continue

            jobs_processed = 0
            processed_job_ids = set()  # Track processed jobs to avoid duplicates
            
            for idx, card in enumerate(job_cards):
                try:
                    # Check if page is still valid
                    if page.is_closed():
                        print("❌ Page was closed, stopping job processing")
                        return
                    
                    # Get job ID to avoid duplicates
                    job_id = card.get_attribute("data-job-id")
                    if job_id in processed_job_ids:
                        print(f"🔄 Skipping duplicate job ID: {job_id}")
                        continue
                    
                    card.scroll_into_view_if_needed()
                    page.wait_for_timeout(1000)

                    # Title - use the working selector from debug
                    title_elem = card.query_selector("a")
                    title = title_elem.inner_text().strip() if title_elem else None
                    
                    # Clean up title (remove "with verification" and duplicates)
                    if title:
                        if "with verification" in title:
                            title = title.split("with verification")[0].strip()
                        # Remove duplicate titles (split by newline and take first)
                        if "\n" in title:
                            title = title.split("\n")[0].strip()

                    # Company - try multiple selectors
                    company_selectors = [
                        "div.artdeco-entity-lockup__subtitle span",
                        "span.job-search-card__company-name",
                        "h4.base-search-card__subtitle a"
                    ]
                    
                    company_elem = None
                    for selector in company_selectors:
                        company_elem = card.query_selector(selector)
                        if company_elem:
                            break
                    
                    company = company_elem.inner_text().strip() if company_elem else None

                    # Location - try multiple selectors
                    location_selectors = [
                        "div.artdeco-entity-lockup__caption span",
                        "span.job-search-card__location",
                        "span[aria-label*='location']"
                    ]
                    
                    location_elem = None
                    for selector in location_selectors:
                        location_elem = card.query_selector(selector)
                        if location_elem:
                            break
                    
                    job_location = location_elem.inner_text().strip() if location_elem else None

                    # Link
                    job_link = title_elem.get_attribute("href") if title_elem else None

                    print(f"📋 Job {idx}: Title='{title}', Company='{company}', Location='{job_location}'")

                    if not title or not company or not job_location or not job_link:
                        print("⚠️ Missing one or more essential elements in card.")
                        continue

                    # Filter by location - only apply to jobs in Massachusetts or remote
                    if job_location and not any(loc in job_location.lower() for loc in ["massachusetts", "ma"]):
                        print(f"🚫 Skipping job due to location: {job_location}")
                        continue

                    if any(ex_kw.lower() in title.lower() for ex_kw in exclude_keywords):
                        print(f"🚫 Skipping job due to excluded keyword: {title}")
                        continue

                    # Click on the job card to load details and check for Easy Apply
                    print(f"🖱️ Clicking on job card: {title}")
                    card.click()
                    page.wait_for_timeout(2000)
                    
                    # Check for Easy Apply button in the details pane
                    easy_apply = False
                    apply_btn = page.query_selector("#jobs-apply-button-id")
                    if apply_btn:
                        easy_apply = True
                        print(f"✅ Easy Apply button found for: {title}")
                    
                    if easy_apply:
                        print(f"✅ Found Easy Apply: {title} at {company}")
                        job = {
                            "title": title,
                            "company": company,
                            "location": job_location,
                            "link": job_link if job_link.startswith("http") else "https://www.linkedin.com" + job_link,
                            "id": job_id,
                            "card_index": idx
                        }
                        try:
                            success = apply_to_job(page, job)
                            if success:
                                print(f"🟢 Applied to: {title}")
                                jobs_processed += 1
                                total_jobs_processed += 1
                            else:
                                print(f"🔴 Skipped: {title}")
                        except Exception as e:
                            print(f"❌ Error during application: {e}")
                            # Try to close any open dialogs
                            try:
                                close_btn = page.query_selector("button[aria-label='Dismiss']") or page.query_selector("button[aria-label='Close']")
                                if close_btn:
                                    close_btn.click()
                                    page.wait_for_timeout(1000)
                            except:
                                pass
                    else:
                        print(f"❌ No Easy Apply found for: {title}")
                    
                    # Mark this job as processed
                    processed_job_ids.add(job_id)
                        
                except Exception as e:
                    print(f"⚠️ Error parsing job card: {e}")
                    continue
            
            print(f"📊 Page {page_num}: Processed {jobs_processed} jobs")
            
            # Pagination - try to go to next page using the correct selector
            try:
                if page.is_closed():
                    print("❌ Page was closed, stopping pagination")
                    return
                
                # Wait a bit before checking for next button
                page.wait_for_timeout(2000)
                    
                # Use the correct LinkedIn pagination selector
                next_btn = page.query_selector("button.jobs-search-pagination__button--next")
                if next_btn and next_btn.is_enabled():
                    print(f"➡️ Moving to page {page_num + 1}...")
                    next_btn.click()
                    time.sleep(4)
                else:
                    print(f"🏁 No more pages available for '{keyword}' (reached page {page_num})")
                    break
            except Exception as e:
                print(f"⚠️ Error navigating to next page: {e}")
                break
        
        print(f"🎯 Total jobs processed for '{keyword}': {total_jobs_processed}")
