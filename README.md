# LinkedIn Job Application Bot 🤖

An intelligent automation tool that helps streamline your LinkedIn job application process using Playwright. This bot can automatically fill out job applications, handle multi-step forms, and maintain a log of your applications.

## Features ✨

- **Automated Job Applications**: Automatically fills out job applications using LinkedIn's Easy Apply feature
- **Smart Form Filling**: Intelligently handles various form fields including:
  - Work experience
  - Education details
  - Skills
  - Contact information
  - Years of experience
  - Location preferences
  - Visa/authorization status
- **Application Tracking**: Maintains a detailed Excel log of all applications with:
  - Job ID
  - Title
  - Company
  - Application status
  - Timestamp
- **Error Handling**: Robust error handling and recovery mechanisms
- **Duplicate Prevention**: Prevents duplicate applications to the same job
- **Customizable Profile**: Easy to update your professional information in the code

## Prerequisites 📋

- Python 3.7+
- Playwright
- pandas
- openpyxl

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LinkedIn-Bot.git
cd LinkedIn-Bot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

## Configuration ⚙️

1. Create a `config.py` file in the root directory with your personal information:
```python
# LinkedIn Credentials
LINKEDIN_EMAIL = "your.email@example.com"
LINKEDIN_PASSWORD = "your_password"

# Job Search Settings
LOCATION = "Your Location, Country"  # e.g., "Massachusetts, United States"
KEYWORDS = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "ML Engineer",
    "AI Engineer",
    "Artificial Intelligence Engineer",
    "NLP Engineer",
    "Computer Vision Engineer",
    "Data Analyst",
    "Business Intelligence Analyst",
    "Data Science Intern",
    "Data Engineer",
    "Associate Data Scientist",
    "Associate Software Engineer",
    "Entry Level Software Engineer",
    "Python Developer",
    "Backend Developer",
    "AI Intern",
    "ML Intern",
    "Deep Learning Engineer",
    "Generative AI Engineer",
    "Applied Scientist",
    "ML Research Engineer",
    "Junior Machine Learning Engineer",
    "Junior Data Scientist",
    "Software Engineer - AI/ML",
    "ML Ops Engineer"
]

# Keywords to exclude from job search
EXCLUDE_KEYWORDS = [
    "senior",
    "lead",
    "staff",
    "principal",
    "director",
    "head",
    "manager"
]
```

2. **Personalize Your Profile Information** ⚠️
   
   You MUST update the following information in `apply.py` to match your profile:

   ```python
   # Work Experience
   WORK_EXPERIENCE = {
       "current": {
           "title": "Your Current Title",
           "company": "Your Current Company",
           "start_date": "YYYY-MM",
           "end_date": "Present",
           "description": "Your job description...",
           "location": "City, State"
       },
       "previous": [
           {
               "title": "Previous Title",
               "company": "Previous Company",
               "start_date": "YYYY-MM",
               "end_date": "YYYY-MM",
               "description": "Previous job description...",
               "location": "City, State"
           }
           # Add more previous experiences as needed
       ]
   }

   # Education
   EDUCATION = {
       "current": {
           "degree": "Your Current Degree",
           "school": "Your Current School",
           "start_date": "YYYY-MM",
           "end_date": "YYYY-MM",
           "gpa": "X.X",
           "location": "City, State",
           "coursework": "Your relevant coursework..."
       },
       "previous": {
           "degree": "Previous Degree",
           "school": "Previous School",
           "start_date": "YYYY-MM",
           "end_date": "YYYY-MM",
           "gpa": "X.X",
           "location": "City, State",
           "coursework": "Previous coursework..."
       }
   }

   # Skills
   SKILLS = {
       "programming_languages": ["Your", "Programming", "Languages"],
       "machine_learning": ["Your", "ML", "Skills"],
       "devops": ["Your", "DevOps", "Tools"],
       "cloud_database": ["Your", "Cloud", "Skills"]
   }
   ```

   > ⚠️ **Important**: The bot will use this information to fill out job applications. Make sure all details are accurate and up-to-date.

3. Place your resume in the `resume` directory:
   - Default path: `resume/your_resume.pdf`
   - Update the path in `config.py` if using a different location

> ⚠️ **Important**: The `config.py` file contains sensitive information and is gitignored. Never commit this file to version control.

## Usage 💻

1. Log in to LinkedIn in your browser
2. Navigate to the jobs page
3. Run the bot:
```bash
python apply.py
```

The bot will:
- Process job applications
- Fill out forms automatically
- Log applications to `logs/applied_jobs.xlsx`
- Handle multi-step applications
- Skip already applied jobs

## Project Structure 📁

```
LinkedIn-Bot/
├── apply.py              # Main application logic
├── config.py            # Configuration file (gitignored)
├── resume/              # Resume directory (gitignored)
│   └── your_resume.pdf
├── logs/                # Application logs (gitignored)
│   └── applied_jobs.xlsx
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Features in Detail 🔍

### Smart Form Filling
- Automatically detects and fills required fields
- Handles various input types (text, number, select)
- Smart defaults for common fields
- Intelligent handling of years of experience fields

### Application Tracking
- Maintains detailed logs in Excel format
- Tracks application status
- Prevents duplicate applications
- Timestamps all actions

### Error Handling
- Graceful handling of timeouts
- Recovery from stuck states
- Proper cleanup of failed applications
- Detailed error logging

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer ⚠️

This bot is for educational purposes only. Please use responsibly and in accordance with LinkedIn's terms of service. Excessive automation may lead to account restrictions.

## Support 💬

If you encounter any issues or have questions, please open an issue in the GitHub repository. 