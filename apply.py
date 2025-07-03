from playwright.sync_api import Page, TimeoutError
import time
from pathlib import Path
from openpyxl.utils.exceptions import InvalidFileException
from pandas.errors import EmptyDataError
import pandas as pd
from datetime import datetime
import os
import re

EXCEL_LOG_PATH = 'logs/applied_jobs.xlsx'

# Work experience and education data
WORK_EXPERIENCE = {
    "current": {
        "title": "Data Analyst/Engineer",
        "company": "UMass Lowell (Office of Graduate and Professional Studies)",
        "start_date": "2024-01",
        "end_date": "Present",
        "description": "Built and scaled production-grade ETL pipelines in Python and SQL to clean, merge, and transform high-volume admissions data from Salesforce, CSV, and API sources, improving pipeline throughput by 1.3x while maintaining data integrity across 25k+ records/month. Enhanced downstream workflow stability by 30% by resolving data anomalies. Developed, evaluated, and deployed machine learning models (logistic regression, decision trees, random forest classifiers) to predict applicant conversion and enrollment, increasing campaign precision by 25%. Automated model selection and tuning workflows using GridSearchCV and cross-validation, and delivered Power BI dashboards for real-time insights into admissions trends, pipeline conversion, and model KPIs; reduced manual reporting time by 60%.",
        "location": "Lowell, MA"
    },
    "previous": [
        {
            "title": "Web Maintenance Specialist",
            "company": "UMass Lowell (Lowell Center for Space Science and Technology)",
            "start_date": "2023-12",
            "end_date": "2025-05",
            "description": "Rebuilt institutional websites using Tridion CMS with responsive design patterns and modular components, improving page load speed by 20%. Enhancing scalability and cross-device compatibility, while boosting website traffic by over 42%. Automated site content deployment workflows using Python and Bash scripts, reducing release time by 35% and eliminating reliance on manual FTP transfers through streamlined CI processes. Implemented structured metadata, schema.org tags, and WCAG 2.1 compliance, improving SEO performance and accessibility.",
            "location": "Lowell, MA"
        },
        {
            "title": "Robotic Process Automation Intern",
            "company": "All India Council for Technical Education",
            "start_date": "2022-03",
            "end_date": "2022-05",
            "description": "Built scalable Blue Prism bots automating approval workflows, reducing operational delay by 45% across document lifecycles. Refactored legacy automation scripts into reusable logic blocks and object layers, shortening development cycles by 30%. Performed exception handling, logging, and audit trail generation to ensure fault-tolerant automation and compliance.",
            "location": "Pune, Maharashtra"
        }
    ]
}

EDUCATION = {
    "current": {
        "degree": "MS Computer Science",
        "school": "University of Massachusetts",
        "start_date": "2023-09",
        "end_date": "2025-05",
        "gpa": "3.7",
        "location": "Lowell, MA",
        "coursework": "Algorithms, Operating Systems, Internet of Things, Human Robot Interaction, Human Computer Interaction, ML/DL security and privacy, Natural Language Processing, Internet & Web Systems, Reinforcement Learning, Data Science"
    },
    "previous": {
        "degree": "B.E. Computer Engineering",
        "school": "Pune University",
        "start_date": "2019-09",
        "end_date": "2023-05",
        "gpa": "3.6",
        "location": "Pune, India",
        "coursework": "Data Structures and Algorithms, Machine Learning, Deep Learning, Artificial Intelligence, Computer Vision, Cloud computing, Blockchain, Data Science and Big Data Analytics, Business Intelligence"
    }
}

SKILLS = {
    "programming_languages": ["Python", "C++", "Java", "JavaScript", "TypeScript", "Solidity", "SQL", "Bash", "C#", "Ruby", "PHP"],
    "machine_learning": ["TensorFlow", "PyTorch", "Scikit-learn", "NumPy", "Keras", "Hugging Face Transformers", "RAG", "Generative AI", "LangChain", "Pydantic", "Reinforcement Learning", "OpenAI Gym", "Sentence-Transformers", "OpenCV", "CNNs", "Vision Transformers"],
    "devops": ["Git", "Docker", "Kubernetes", "Jenkins", "VS Code", "Postman", "SaaS Tools", "Jupyter Notebook"],
    "cloud_database": ["AWS (EC2, S3, Lambda)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Salesforce", "PostgreSQL", "MySQL", "MongoDB", "SQLite", "AstraDB (Cassandra)"]
}

def log_job_to_excel(job_id, title, company, status):
    """Append job entry to Excel log."""
    try:
        df = pd.read_excel(EXCEL_LOG_PATH, engine='openpyxl')
    except (FileNotFoundError, InvalidFileException, EmptyDataError):
        df = pd.DataFrame(columns=['Job ID', 'Title', 'Company', 'Status', 'Applied At'])

    df = df[df['Job ID'] != job_id]  # Remove duplicates
    new_entry = {
        'Job ID': job_id,
        'Title': title,
        'Company': company,
        'Status': status,
        'Applied At': datetime.utcnow().isoformat()
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_excel(EXCEL_LOG_PATH, index=False)

def is_job_logged_in_excel(job_id):
    """Check if a job is already logged in Excel."""
    try:
        df = pd.read_excel(EXCEL_LOG_PATH, engine='openpyxl')
        return job_id in df['Job ID'].values
    except (FileNotFoundError, InvalidFileException, EmptyDataError):
        return False
'''

def fill_work_experience(page, experience_type="current"):
    """Fill work experience fields in the form."""
    try:
        exp = WORK_EXPERIENCE[experience_type]
        
        # Fill title
        title_input = page.query_selector("input[aria-label*='title' i], input[aria-label*='job title' i]")
        if title_input:
            title_input.fill(exp["title"])
            
        # Fill company
        company_input = page.query_selector("input[aria-label*='company' i], input[aria-label*='employer' i]")
        if company_input:
            company_input.fill(exp["company"])
            
        # Fill dates
        start_date_input = page.query_selector("input[aria-label*='start date' i]")
        if start_date_input:
            start_date_input.fill(exp["start_date"])
            
        end_date_input = page.query_selector("input[aria-label*='end date' i]")
        if end_date_input:
            end_date_input.fill(exp["end_date"])
            
        # Fill description
        description_input = page.query_selector("textarea[aria-label*='description' i]")
        if description_input:
            description_input.fill(exp["description"])
            
        # Fill location
        location_input = page.query_selector("input[aria-label*='location' i]")
        if location_input:
            location_input.fill(exp["location"])
            
        return True
    except Exception as e:
        print(f"⚠️ Error filling work experience: {e}")
        return False 
        '''

def fill_education(page, education_type="current"):
    """Fill education fields in the form."""
    try:
        edu = EDUCATION[education_type]
        
        # Fill degree
        degree_input = page.query_selector("input[aria-label*='degree' i], input[aria-label*='major' i]")
        if degree_input:
            degree_input.fill(edu["degree"])
            
        # Fill school
        school_input = page.query_selector("input[aria-label*='school' i], input[aria-label*='university' i]")
        if school_input:
            school_input.fill(edu["school"])
            
        # Fill dates
        start_date_input = page.query_selector("input[aria-label*='start date' i]")
        if start_date_input:
            start_date_input.fill(edu["start_date"])
            
        end_date_input = page.query_selector("input[aria-label*='end date' i]")
        if end_date_input:
            end_date_input.fill(edu["end_date"])
            
        # Fill GPA
        gpa_input = page.query_selector("input[aria-label*='gpa' i]")
        if gpa_input:
            gpa_input.fill(edu["gpa"])
            
        # Fill location
        location_input = page.query_selector("input[aria-label*='location' i]")
        if location_input:
            location_input.fill(edu["location"])
            
        return True
    except Exception as e:
        print(f"⚠️ Error filling education: {e}")
        return False

def fill_skills(page):
    """Fill skills fields in the form."""
    try:
        # Combine all skills into a single string
        all_skills = []
        for category in SKILLS.values():
            all_skills.extend(category)
        skills_text = ", ".join(all_skills)
        
        # Fill skills textarea
        skills_input = page.query_selector("textarea[aria-label*='skills' i], input[aria-label*='skills' i]")
        if skills_input:
            skills_input.fill(skills_text)
            
        return True
    except Exception as e:
        print(f"⚠️ Error filling skills: {e}")
        return False

def apply_to_job(page: Page, job, resume_path: str = "resume/Harshal_Dafade_Resume.pdf") -> bool:
    """Apply to a single job using LinkedIn Easy Apply if possible."""
    job_id = job.get("id")
    title = job.get("title", "")
    company = job.get("company", "")

    if is_job_logged_in_excel(job_id):
        print(f"🟡 Already applied to: {title} at {company}")
        return False

    print(f"\n⚙️ Applying to: {title} at {company}")

    try:
        # Do NOT navigate to job["link"]; assume card was already clicked
        # Wait for job details pane to load
        try:
            page.wait_for_selector("#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details", timeout=10000)
        except Exception as e:
            print(f"⚠️ Job details pane did not load: {e}")
            log_job_to_excel(job_id, title, company, "error - details pane not loaded")
            return False

        # Find the Easy Apply button in the details pane
        apply_btn = page.query_selector("#jobs-apply-button-id")
        if not apply_btn:
            details_pane = page.query_selector("#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details")
            apply_btn = details_pane.query_selector("button.jobs-apply-button") if details_pane else None
        if not apply_btn:
            # Fallback to global selector
            apply_btn = page.query_selector("button.jobs-apply-button")
        if not apply_btn:
            log_job_to_excel(job_id, title, company, "skipped - no apply button")
            print("❌ Easy Apply button not found in details pane.")
            return False
        apply_btn.click()
        page.wait_for_timeout(2000)

        # Upload resume
        resume_input = page.query_selector("input[type='file']")
        if resume_input:
            resume_input.set_input_files(Path(resume_path))
            print("📎 Resume uploaded.")

        # Track attempts to proceed
        max_attempts = 3
        current_attempt = 0
        last_state = None
        review_attempts = 0
        max_review_attempts = 2

        while True:
            # Always scroll the modal to the bottom before clicking buttons
            try:
                page.eval_on_selector('div[role="dialog"]', 'el => el.scrollTo(0, el.scrollHeight)')
                page.wait_for_timeout(500)
            except Exception:
                pass

            # Autofill required input fields with default values
            required_inputs = page.query_selector_all("div[role='dialog'] input[required]")
            for inp in required_inputs:
                input_type = inp.get_attribute("type")
                value = inp.input_value()
                label_el = inp.evaluate_handle("el => el.closest('label') || el.closest('div')")
                label_text = label_el.inner_text().strip().lower() if label_el else ""

                if not value:
                    # Check for years of experience fields
                    is_years_field = (
                        input_type == "number" or 
                        "years of experience" in label_text or 
                        "how many years" in label_text or 
                        "years in" in label_text or 
                        "experience in years" in label_text or
                        re.search(r"(\d+)\+?\s*years?", label_text) or
                        "years" in label_text and any(kw in label_text for kw in ["experience", "work", "industry", "field"])
                    )

                    if is_years_field:
                        # Clear any existing value first
                        inp.fill("")
                        page.wait_for_timeout(100)
                        
                        # For industry-specific experience, use a reasonable default
                        default_value = "3"  # Default value
                        if "software" in label_text or "development" in label_text or "programming" in label_text:
                            default_value = "5"
                        elif "data" in label_text or "analytics" in label_text:
                            default_value = "3"
                        elif "machine learning" in label_text or "ai" in label_text:
                            default_value = "3"
                        
                        # Use JavaScript to set the value directly and ensure it's a whole number
                        page.evaluate(f"""(value) => {{
                            const input = document.querySelector('input[aria-label="{label_el.inner_text()}"]');
                            if (input) {{
                                // Clear any existing value
                                input.value = '';
                                // Set the new value
                                input.value = value;
                                // Ensure it's treated as a number
                                input.type = 'number';
                                // Prevent any text input
                                input.addEventListener('input', function(e) {{
                                    if (!/^\d*$/.test(this.value)) {{
                                        this.value = value;
                                    }}
                                }});
                                // Dispatch events
                                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }}""", default_value)
                        
                        # Verify the value was set correctly and monitor for changes
                        page.wait_for_timeout(100)
                        current_value = inp.input_value()
                        if not current_value.isdigit():
                            # If not correct, try one more time with direct fill
                            inp.fill(default_value)
                            page.wait_for_timeout(100)
                            if not inp.input_value().isdigit():
                                print(f"⚠️ Warning: Could not set numeric value for {label_text}")
                                # One final attempt with type="number" and strict monitoring
                                page.evaluate(f"""(value) => {{
                                    const input = document.querySelector('input[aria-label="{label_el.inner_text()}"]');
                                    if (input) {{
                                        input.type = 'number';
                                        input.value = value;
                                        // Add strict monitoring
                                        const observer = new MutationObserver((mutations) => {{
                                            if (!/^\d*$/.test(input.value)) {{
                                                input.value = value;
                                            }}
                                        }});
                                        observer.observe(input, {{ 
                                            attributes: true, 
                                            childList: true, 
                                            characterData: true 
                                        }});
                                    }}
                                }}""", default_value)
                        
                        # Final verification after a short delay
                        page.wait_for_timeout(500)
                        final_value = inp.input_value()
                        if not final_value.isdigit():
                            print(f"⚠️ Warning: Value changed after setting for {label_text}")
                            # Force the value one last time
                            inp.fill(default_value)
                            page.wait_for_timeout(100)
                            if not inp.input_value().isdigit():
                                print(f"❌ Failed to set numeric value for {label_text}")
                    elif "salary" in label_text:
                        inp.fill("80000")
                    elif "phone" in label_text:
                        inp.fill("9785696638")
                    elif "email" in label_text:
                        inp.fill("harshaldafade2001@gmail.com")
                    elif re.search(r"(authorized|citizen|visa|sponsorship|work in us)", label_text):
                        inp.fill("Yes")
                    else:
                        inp.fill("Yes")  # generic fallback

            # Autofill required select fields with the first non-disabled option
            required_selects = page.query_selector_all("div[role='dialog'] select[required]")
            for sel in required_selects:
                label_el = sel.evaluate_handle("el => el.closest('label') || el.closest('div')")
                label_text = label_el.inner_text().strip().lower() if label_el else ""
    
                options = sel.query_selector_all("option")
                option_values = [(opt.get_attribute("value"), opt.inner_text().strip()) for opt in options if opt.get_attribute("value") and not opt.get_attribute("disabled")]

                selected = False
                for value, text in option_values:
                    # Prioritize United States for country selection
                    if "country" in label_text or "location" in label_text:
                        if "united states" in text.lower():
                            sel.select_option(value)
                            selected = True
                            break
                    elif any(kw in label_text for kw in ["citizen", "authorization", "authorized", "work in the united states"]):
                        if "yes" in text.lower():
                            sel.select_option(value)
                            selected = True
                            break
                    elif any(kw in label_text for kw in ["sponsorship", "require visa"]):
                        if "no" in text.lower():
                            sel.select_option(value)
                            selected = True
                            break
                    elif any(kw in label_text for kw in ["relocate", "move"]):
                        if "yes" in text.lower():
                            sel.select_option(value)
                            selected = True
                            break
                    elif any(kw in label_text for kw in ["experience", "years"]):
                        if "5" in text or "5+" in text or "more than 5" in text:
                            sel.select_option(value)
                            selected = True
                            break
                if not selected:
                    for value, text in option_values:
                        if text.strip() and not re.search(r"select|choose|option", text.lower()):
                            sel.select_option(value)
                            selected = True
                            break

            # Check for work experience fields and fill them
          #  if page.query_selector("input[aria-label*='title' i], input[aria-label*='job title' i]"):
          #      fill_work_experience(page)

            # Check for education fields and fill them
            if page.query_selector("input[aria-label*='degree' i], input[aria-label*='major' i]"):
                fill_education(page)

            # Check for skills fields and fill them
            if page.query_selector("textarea[aria-label*='skills' i], input[aria-label*='skills' i]"):
                fill_skills(page)

            # Autofill email address if required and empty
            email_input = page.query_selector("div[role='dialog'] input[type='email']")
            if email_input and not email_input.input_value():
                email_input.fill("harshaldafade2001@gmail.com")

            # Autofill phone country code if required and empty
            country_code_select = page.query_selector("div[role='dialog'] select[name*='countryCode']")
            if country_code_select:
                country_code_select.select_option("1")  # United States (+1)

            # Autofill phone number if required and empty
            phone_input = page.query_selector("div[role='dialog'] input[type='tel']")
            if phone_input and not phone_input.input_value():
                phone_input.fill("9785696638")

            # Autofill email dropdown if present and not selected
            email_selects = page.query_selector_all("div[role='dialog'] select[required]")
            for sel in email_selects:
                options = sel.query_selector_all("option")
                values = [opt.get_attribute("value") for opt in options]
                if "harshaldafade2001@gmail.com" in values:
                    if sel.input_value() == "Select an option":
                        sel.select_option("harshaldafade2001@gmail.com")

            # Autofill phone country code dropdown if present and not selected
            phone_country_selects = page.query_selector_all("div[role='dialog'] select[required]")
            for sel in phone_country_selects:
                options = sel.query_selector_all("option")
                values = [opt.get_attribute("value") for opt in options]
                if "United States (+1)" in values:
                    if sel.input_value() == "Select an option":
                        sel.select_option("United States (+1)")

            # Try to click 'Submit application' first
            submit_btn = page.query_selector("button[aria-label='Submit application']")
            if not submit_btn:
                submit_btn = page.query_selector("div[role='dialog'] button:has-text('Submit application')")
            if submit_btn:
                submit_btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                submit_btn.click()
                page.wait_for_timeout(2000)
                log_job_to_excel(job_id, title, company, "applied")
                print("✅ Application submitted.")
                
                # Handle the final "Done" button
                try:
                    # Wait for the success dialog
                    page.wait_for_selector("button[aria-label='Done']", timeout=5000)
                    done_btn = page.query_selector("button[aria-label='Done']")
                    if done_btn:
                        done_btn.click()
                        page.wait_for_timeout(1000)
                        print("✅ Clicked Done after submission.")
                except Exception as e:
                    print(f"⚠️ Could not find or click Done button: {e}")
                    # Try alternative selectors for Done button
                    try:
                        done_btn = page.query_selector("button:has-text('Done')") or page.query_selector("button:has-text('Close')")
                        if done_btn:
                            done_btn.click()
                            page.wait_for_timeout(1000)
                            print("✅ Clicked alternative Done/Close button.")
                    except Exception as e2:
                        print(f"⚠️ Could not find alternative Done button: {e2}")
                
                return True

            # Then try 'Review'
            review_btn = page.query_selector("button[aria-label='Review']")
            if not review_btn:
                review_btn = page.query_selector("div[role='dialog'] button:has-text('Review')")
            if review_btn:
                review_btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                review_btn.click()
                page.wait_for_timeout(2000)
                review_attempts += 1
                
                # If we've been in review stage too many times, try to proceed or discard
                if review_attempts >= max_review_attempts:
                    print("⚠️ Stuck in review stage. Attempting to proceed...")
                    # Try to find and click the submit button in review stage
                    review_submit = page.query_selector("button[aria-label='Submit application']") or page.query_selector("div[role='dialog'] button:has-text('Submit application')")
                    if review_submit:
                        review_submit.scroll_into_view_if_needed()
                        page.wait_for_timeout(500)
                        review_submit.click()
                        page.wait_for_timeout(2000)
                        log_job_to_excel(job_id, title, company, "applied")
                        print("✅ Application submitted from review stage.")
                        return True
                    else:
                        print("⚠️ Could not find submit button in review stage. Discarding application...")
                        try:
                            # Try to find and click the close (X) button
                            close_btn = page.query_selector("button[aria-label='Dismiss']") or page.query_selector("button[aria-label='Close']")
                            if close_btn:
                                close_btn.click()
                                page.wait_for_timeout(1000)
                                
                                # Look for and click the 'Discard' button in the confirmation dialog
                                discard_btn = page.query_selector("button:has-text('Discard')")
                                if discard_btn:
                                    discard_btn.click()
                                    page.wait_for_timeout(1000)
                                    log_job_to_excel(job_id, title, company, "discarded - stuck in review")
                                    print("❌ Application discarded due to being stuck in review.")
                                    return False
                        except Exception as e:
                            print(f"⚠️ Error while trying to discard application: {e}")
                            return False
                continue

            # Then try 'Next'
            next_btn = page.query_selector("div[role='dialog'] button:has-text('Next')")
            if next_btn:
                next_btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                next_btn.click()
                page.wait_for_timeout(2000)
                continue

            # Check if we're stuck in the same state
            current_state = page.evaluate("""() => {
                const dialog = document.querySelector('div[role="dialog"]');
                return dialog ? dialog.innerHTML : '';
            }""")
            
            if current_state == last_state:
                current_attempt += 1
                if current_attempt >= max_attempts:
                    print("⚠️ Stuck in the same state after multiple attempts. Discarding application...")
                    try:
                        # Try to find and click the close (X) button
                        close_btn = page.query_selector("button[aria-label='Dismiss']") or page.query_selector("button[aria-label='Close']")
                        if close_btn:
                            close_btn.click()
                            page.wait_for_timeout(1000)
                            
                            # Look for and click the 'Discard' button in the confirmation dialog
                            discard_btn = page.query_selector("button:has-text('Discard')")
                            if discard_btn:
                                discard_btn.click()
                                page.wait_for_timeout(1000)
                                log_job_to_excel(job_id, title, company, "discarded - stuck")
                                print("❌ Application discarded due to being stuck.")
                                return False
                    except Exception as e:
                        print(f"⚠️ Error while trying to discard application: {e}")
                        return False
            else:
                current_attempt = 0
                last_state = current_state

            # If none found, exit
            log_job_to_excel(job_id, title, company, "skipped - multi-step or unsupported")
            print("⚠️ Skipped due to complex form.")
            return False

    except TimeoutError:
        log_job_to_excel(job_id, title, company, "error - timeout")
        print("❌ Timeout or form error.")
        return False
    except Exception as e:
        log_job_to_excel(job_id, title, company, f"error - {str(e)}")
        print(f"❌ Error during apply: {e}")
        return False
