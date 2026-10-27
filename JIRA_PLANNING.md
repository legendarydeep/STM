# Jira Project Planning Guide — Student Task Management System

This document provides a complete, structured blueprint for tracking this project in **Atlassian Jira**. Whether you have access to a Jira Cloud account or need to present project management evidence during your college viva examination, this guide gives you the exact tasks, acceptance criteria, sprints, and workflow.

---

## 1. Project Configuration in Jira

| Parameter | Recommended Setting |
| :--- | :--- |
| **Project Name** | Student Task Management System |
| **Project Key** | `STMS` |
| **Project Template** | **Scrum** (or Kanban for flexible flow) |
| **Project Type** | Team-managed or Company-managed Software Project |
| **Default Workflow** | `To Do` ➔ `In Progress` ➔ `In Review` ➔ `Done` |

---

## 2. Sprint Roadmap & Backlog Breakdown

### **Sprint 1: Architecture & Core CRUD (Duration: 1 Week)**
*Sprint Goal:* Establish database layer, application factory, and basic task creation/viewing.
- **STMS-1**: Project Scaffolding & SQLite Database Initialization
- **STMS-2**: Task Creation Form with Server-side Validation
- **STMS-3**: Task Modification and Status Transition Handlers

### **Sprint 2: UI Experience & Dashboard Analytics (Duration: 1 Week)**
*Sprint Goal:* Implement modern dashboard metrics, responsive CSS design, and multi-criteria filters.
- **STMS-4**: Real-time Dashboard Analytics (Total, Pending, In-Progress, Completed)
- **STMS-5**: Multi-criteria Filter Bar (Status & Priority)
- **STMS-6**: Task Deletion Safeguard with Confirmation Modal

### **Sprint 3: DevOps, Quality Assurance & Containerization (Duration: 1 Week)**
*Sprint Goal:* Ensure 100% test coverage for core paths and containerize the application.
- **STMS-7**: Automated Test Suite using Pytest & Isolated In-Memory/Temp Database
- **STMS-8**: Production-conscious Containerization with Docker & Persistent Volumes

---

## 3. Actionable User Stories & Acceptance Criteria

### **STMS-1: Project Scaffolding & SQLite Database Initialization**
- **Type**: Technical Task
- **Priority**: High
- **Story Points**: 3
- **Description**: Configure Flask application factory (`create_app`), establish database connection lifecycle, and generate `tasks` table with required constraints.
- **Acceptance Criteria**:
  - **Given** an empty or fresh instance directory, **When** the app initializes, **Then** SQLite table `tasks` is created with columns `id`, `title`, `description`, `priority`, `due_date`, `status`, `created_at`.
  - **Given** an ongoing request, **When** database access is needed, **Then** `get_db()` returns a thread-safe connection with `sqlite3.Row` dict mapping.

---

### **STMS-2: Task Creation Form with Server-Side Validation**
- **Type**: User Story
- **Priority**: High
- **Story Points**: 5
- **Description**: As a student, I want to record new assignments and lab deadlines so that I can keep track of upcoming academic responsibilities.
- **Acceptance Criteria (Gherkin format)**:
  - **Scenario 1 (Valid Input)**:
    - *Given* I am on the `/tasks/new` page
    - *When* I fill in a title "OS Lab Sheet 3", priority "High", and submit
    - *Then* the task is stored in SQLite and I am redirected to `/` with a green success message.
  - **Scenario 2 (Invalid / Empty Title)**:
    - *Given* I am on the `/tasks/new` page
    - *When* I leave the title blank or enter whitespace only and submit
    - *Then* the server returns HTTP 400, no database row is inserted, and a danger flash banner displays *"Task title is required."*

---

### **STMS-3: Task Modification and Quick Status Transitions**
- **Type**: User Story
- **Priority**: High
- **Story Points**: 5
- **Description**: As a student, I want to edit task details and update task status (Pending ➔ In Progress ➔ Completed) directly from the dashboard.
- **Acceptance Criteria**:
  - **Given** an existing task in the directory, **When** I change the status dropdown to "In Progress", **Then** the database updates immediately and shows a confirmation toast.
  - **Given** a task needing date/description adjustments, **When** I open `/tasks/<id>/edit` and submit changes, **Then** the record updates without altering the task ID.

---

### **STMS-4: Real-Time Dashboard Metrics**
- **Type**: User Story
- **Priority**: Medium
- **Story Points**: 3
- **Description**: As a student, I want a summary bar showing the counts of Total, Pending, In Progress, and Completed tasks so that I can gauge my workload at a glance.
- **Acceptance Criteria**:
  - **Given** 2 pending tasks, 1 in-progress task, and 1 completed task in the database,
  - **When** the student navigates to the home page `/`,
  - **Then** the dashboard cards display: Total = 4, Pending = 2, In Progress = 1, Completed = 1.

---

### **STMS-5: Multi-Criteria Filter Bar**
- **Type**: User Story
- **Priority**: Medium
- **Story Points**: 3
- **Description**: As a student with numerous tasks, I want to filter tasks by status and priority so that I can isolate urgent or active items.
- **Acceptance Criteria**:
  - **Given** multiple tasks with varied statuses and priorities,
  - **When** I select "Status: In Progress" and "Priority: High",
  - **Then** only tasks matching both criteria are displayed in the table.
  - **When** I click "Clear Filters", the full unfiltered list returns.

---

### **STMS-6: Task Deletion Safeguard**
- **Type**: User Story
- **Priority**: Medium
- **Story Points**: 2
- **Description**: As a student, I want an alert asking for confirmation before deleting a task so that I don't accidentally erase my assignments.
- **Acceptance Criteria**:
  - **Given** a task row in the dashboard,
  - **When** I click the "Delete" button,
  - **Then** a confirmation prompt pops up asking *"Are you sure you want to delete this task?"*.
  - **When** I confirm, the task is removed via HTTP POST and a flash notice is rendered.

---

### **STMS-7: Automated Regression Test Suite with Pytest**
- **Type**: Quality Assurance
- **Priority**: High
- **Story Points**: 5
- **Description**: Build an automated regression test suite ensuring test isolation through temporary SQLite databases.
- **Acceptance Criteria**:
  - Running `python -m pytest` executes at least 8 unit/integration tests.
  - Tests verify: home page load, task creation, input validation, status update, task editing, deletion, dashboard calculations, and filtering.
  - Test suite passes with 0 failures and generates JUnit XML for CI pipelines.

---

### **STMS-8: Containerization with Docker & Data Persistence**
- **Type**: DevOps Task
- **Priority**: High
- **Story Points**: 5
- **Description**: Package the application into a Docker container with non-root security and SQLite volume persistence.
- **Acceptance Criteria**:
  - Docker image builds using a slim Python base (`python:3.11-slim`).
  - Container runs under an unprivileged user (`appuser`).
  - SQLite database directory `/app/instance` is bound to a host directory or named volume so database records persist across container restarts.

---

## 4. Git Branch & Commit Naming Convention

Aligning Git commits and branches to Jira ticket keys allows full traceability from requirement to code.

### **Branch Naming Standard**
```
feature/STMS-<issue_number>-<short-description>
bugfix/STMS-<issue_number>-<short-description>
hotfix/STMS-<issue_number>-<short-description>
```
*Examples:*
- `feature/STMS-2-create-task-form`
- `feature/STMS-4-dashboard-metrics`
- `bugfix/STMS-6-delete-confirmation`

### **Commit Message Standard**
Format: `[<ISSUE_KEY>] <Imperative summary of changes>`
*Examples:*
- `[STMS-1] Initialize SQLite schema and Flask application factory`
- `[STMS-2] Implement task creation route with server-side validation`
- `[STMS-7] Add pytest automated tests with temporary test db fixture`

---

## 5. How to Link Jira to GitHub

If you connect Jira to GitHub (or are asked about it in your viva):
1. **In Jira Cloud**:
   - Go to **Apps** ➔ **Explore more apps** ➔ Search for **GitHub for Jira**.
   - Click **Get it now** and connect your GitHub personal account or organization.
   - Authorize repository access to your `student-task-management` repository.
2. **Using Smart Commits**:
   - When committing code, referencing the issue key automatically links the commit to the Jira issue:
     ```bash
     git commit -m "[STMS-2] Add task validation #comment Completed server validation logic"
     ```
   - You can even transition issues directly:
     ```bash
     git commit -m "[STMS-2] Finalize task creation feature #resolve"
     ```
3. **Manual Entry (If Jira is not connected)**:
   - Create a free Jira Cloud workspace at [atlassian.com/software/jira](https://www.atlassian.com/software/jira).
   - Create a project with key `STMS`.
   - Manually copy the 8 user stories from Section 3 into your backlog.
