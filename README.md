# Student Task Management System

A complete, beginner-friendly, and lightweight web application built for university computer science practical examinations and project demonstrations.

---

## 📌 Project Overview

The **Student Task Management System** is a full-featured task and academic coursework organizer built with:
- **Backend:** Python 3 & Flask
- **Frontend:** Semantic HTML5, Vanilla CSS3 (modern responsive design system), and Jinja2 templating
- **Database:** SQLite (embedded, persistent, zero-configuration)
- **Testing:** pytest automated regression test suite (with isolated test databases)
- **Containerization:** Docker with non-root security and volume persistence
- **Continuous Integration (CI):** Declarative Jenkinsfile pipeline
- **Version Control:** Git & GitHub integration
- **Project Tracking:** Atlassian Jira user stories and sprint planning

---

## ✨ Features

1. **Dashboard Analytics:** Real-time counters showing Total Tasks, Pending, In Progress, and Completed tasks.
2. **Task Creation Form:** Add tasks with Title, Description, Priority (Low/Medium/High), Due Date, and Initial Status.
3. **Task Directory Listing:** Responsive, tabular/card view of all tasks with priority and status badges.
4. **Quick Status Transition:** Change task status (Pending ➔ In Progress ➔ Completed) directly from the dashboard via inline dropdowns.
5. **Full Task Editing:** Update title, description, priority, due date, and status.
6. **Task Deletion Safeguard:** Safe deletion with a JavaScript confirmation dialog.
7. **Multi-Criteria Filtering:** Filter tasks instantly by status and priority.
8. **Robust Input Validation:** Server-side validation enforcing required fields, length limits, and date formats with color-coded flash alerts.
9. **Data Persistence & Security:** Persistent SQLite storage with parameterized queries (`?`) to prevent SQL injection.

---

## 📁 Project Structure

```
student-task-management/
├── app.py                # Main Flask application and SQLite database handlers
├── requirements.txt      # Python dependencies (Flask, pytest)
├── pytest.ini           # Pytest settings and options
├── Dockerfile            # Container definition with non-root user
├── .dockerignore         # Excluded files during Docker build
├── Jenkinsfile           # Declarative Jenkins CI pipeline
├── .gitignore            # Git exclusion rules
├── README.md             # Project documentation (this file)
├── JIRA_PLANNING.md      # Jira Agile guide, 8 user stories, and acceptance criteria
├── VIVA_PREPARATION.md   # Viva questions, 2-minute oral script, and architecture
├── instance/             # Local database directory (persistent SQLite tasks.db)
│   └── .gitkeep          # Tracks folder in git without committing local database files
├── static/
│   └── css/
│       └── style.css     # Modern, responsive CSS styling
├── templates/
│   ├── base.html         # Master template with navigation, alerts, and footer
│   ├── index.html        # Dashboard, analytics cards, filter toolbar, and task table
│   ├── add_task.html     # Form for creating tasks
│   └── edit_task.html    # Form for editing existing tasks
└── tests/
    └── test_app.py       # 8 automated pytest tests with temporary test db fixtures
```

---

## 🚀 Quickstart Guide (Windows 11)

### 1. Prerequisites Check
Verify that Python and Git are installed by opening **Windows PowerShell**:
```powershell
python --version
git --version
```

### 2. Install Dependencies
Run in the project directory:
```powershell
python -m pip install -r requirements.txt
```

### 3. Run the Flask Web Application
```powershell
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the automated test suite with **pytest**:
```powershell
python -m pytest
```
*Note: Tests run against an isolated temporary database created via `tempfile.mkstemp()`, so running tests will never alter or erase your real student tasks.*

To view detailed test output with test execution timing:
```powershell
python -m pytest -v --durations=0
```

---

## 🐳 Docker Containerization

### Image vs. Container
- **Docker Image:** A read-only template package containing Python, libraries, and code.
- **Docker Container:** A running, isolated instance of the image.

### 1. Build the Docker Image
```bash
docker build -t student-task-manager .
```

### 2. Run the Container with Persistent Storage
We mount the host directory `./instance` into `/app/instance` inside the container so your SQLite database records persist even if the container is stopped or deleted:
```bash
docker run -d -p 5000:5000 -v "${PWD}/instance:/app/instance" --name task-app student-task-manager
```

### 3. Container Management Commands
- **View container logs:**
  ```bash
  docker logs -f task-app
  ```
- **Stop the container:**
  ```bash
  docker stop task-app
  ```
- **Start the container again:**
  ```bash
  docker start task-app
  ```
- **Remove container:**
  ```bash
  docker rm -f task-app
  ```

---

## ⚙️ Jenkins CI Pipeline

The project includes a declarative `Jenkinsfile` that automates testing on every code push.

### What the Pipeline Stages Do:
1. **Checkout Code:** Pulls latest revisions from the Git repository.
2. **Install Dependencies:** Installs packages from `requirements.txt`.
3. **Run Automated Tests:** Executes `pytest --junitxml=test-results.xml`. If any test fails, the build is marked as **FAILED**.
4. **Post-Build Action:** Publishes JUnit test graphs in Jenkins.

### How to Run in Jenkins:
1. Open Jenkins at `http://localhost:8080`.
2. Click **New Item** ➔ Name it `student-task-manager` ➔ Select **Pipeline** ➔ Click **OK**.
3. Under the **Pipeline** configuration section, choose **Pipeline script from SCM**.
4. Set SCM to **Git**, provide your repository URL.
5. In **Script Path**, enter `Jenkinsfile`.
6. Click **Save** and **Build Now**.

---

## 🐙 Git and GitHub Setup Instructions

Follow these exact commands in Windows PowerShell to initialize your Git repository and push your project to GitHub:

### Step 1: Initialize Git and Commit Changes
```powershell
# 1. Initialize local repository
git init

# 2. Check status (verify .gitignore excludes caches and databases)
git status

# 3. Stage all project files
git add .

# 4. Commit files with an informative message
git commit -m "[STMS-1] Initial commit: Student Task Management System with Flask, tests, and Docker"
```

### Step 2: Create a Repository on GitHub
1. Log in to your GitHub account at [github.com](https://github.com).
2. Click the **+** icon in the top right corner and choose **New repository**.
3. Name your repository: `student-task-management`.
4. Choose **Public** (or **Private**).
5. **Do NOT check** "Add a README file", "Add .gitignore", or "Choose a license" (we already created them locally).
6. Click **Create repository**.

### Step 3: Link and Push to GitHub
Copy the commands shown on your new GitHub page and execute them in PowerShell:
```powershell
# Rename default branch to main
git branch -M main

# Add your GitHub remote URL (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/student-task-management.git

# Push your code to GitHub (your browser will prompt you to log in securely)
git push -u origin main
```
*Note: You do not need to generate personal access tokens; the standard Git Credential Manager will open a secure browser login prompt.*

---

## 📋 Viva & Practical Examination Prep

For detailed viva preparation, study [VIVA_PREPARATION.md](file:///c:/Users/deep/OneDrive/Desktop/asdd%20mini%20project/VIVA_PREPARATION.md), which includes:
- System architecture diagram
- Database explanation and SQL injection prevention
- Explanation of Flask routes and application factory
- Git vs. GitHub, Docker image vs. container, Jenkins CI, and Jira
- 25 quick viva questions with concise answers
- A 2-minute oral presentation and demonstration script
