import time
from playwright.sync_api import Page, TimeoutError
from apply import apply_to_job as robust_apply_to_job

def apply_to_job(page, job, resume_path="resume/Harshal_Dafade_Resume.pdf"):
    return robust_apply_to_job(page, job, resume_path)
