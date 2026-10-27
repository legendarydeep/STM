"""
Generate complete, professional PDF Project Report for TaskMate using ReportLab.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Don't draw headers/footers on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header
        self.drawString(54, 755, "TaskMate — Student Task Management System | Project Documentation")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 747, 558, 747)

        # Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Department of Computer Science & Engineering • Practical Examination")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def create_pdf_report():
    pdf_filename = r"c:\Users\deep\OneDrive\Desktop\asdd mini project\TaskMate_Complete_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#4F46E5")
    c_secondary = colors.HexColor("#3B82F6")
    c_dark = colors.HexColor("#0F172A")
    c_muted = colors.HexColor("#64748B")
    c_bg_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_dark,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_primary,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_dark,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # COVER / HEADER TITLE BLOCK
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("TaskMate", title_style))
    story.append(Paragraph("Student Task Management System — Complete Technical Project Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceAfter=15))

    meta_table_data = [
        [Paragraph("<b>Academic Subject:</b>", body_style), Paragraph("Computer Science & Engineering Mini Project", body_style)],
        [Paragraph("<b>Tech Stack:</b>", body_style), Paragraph("Python 3, Flask 3.1, SQLite 3, Jinja2, HTML5/CSS3", body_style)],
        [Paragraph("<b>DevOps Tools:</b>", body_style), Paragraph("Docker, Jenkins CI, pytest 9.1, Git & GitHub, Jira", body_style)],
        [Paragraph("<b>Repository:</b>", body_style), Paragraph("https://github.com/legendarydeep/STM", body_style)],
        [Paragraph("<b>Live Local Endpoint:</b>", body_style), Paragraph("http://127.0.0.1:5000", body_style)],
        [Paragraph("<b>Target Environment:</b>", body_style), Paragraph("Windows 11 / Linux / Containerized Environments", body_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[130, 374])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # 1. ABSTRACT & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Modern undergraduate computer science students are tasked with managing concurrent lab sheets, continuous assessment tests, coding projects, and seminar presentations across multiple courses. Relying on paper notebooks or disparate chat groups leads to missed assignment cutoffs, poor academic prioritization, and cognitive overload.",
        body_style
    ))
    story.append(Paragraph(
        "<b>TaskMate</b> solves this challenge by providing a centralized, responsive web platform tailored for student workflows. It delivers real-time workload analytics (Total, Completed, Pending, and Overdue tasks), subject categorizations, fast modal creation, deadline calendar views, switchable table/card presentations, and light/dark theme switching with zero external database dependencies.",
        body_style
    ))

    # =========================================================================
    # 2. SYSTEM ARCHITECTURE & COMPONENTS
    # =========================================================================
    story.append(Paragraph("2. System Architecture & Tech Stack", h1_style))
    story.append(Paragraph(
        "The project follows the Model-View-Controller (MVC) architectural pattern implemented with a clean Flask Application Factory pattern (<code>create_app</code>):",
        body_style
    ))

    arch_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Functionality & Architectural Role</b>", body_style)],
        [Paragraph("<b>Backend</b>", body_style), Paragraph("Python 3 & Flask 3.1", body_style), Paragraph("Application factory, route dispatching, server-side data validation, and session management.", body_style)],
        [Paragraph("<b>Database</b>", body_style), Paragraph("SQLite 3 (Embedded)", body_style), Paragraph("Single-file relational engine (instance/tasks.db). Thread-safe connections, foreign key support, ACID transactions.", body_style)],
        [Paragraph("<b>Frontend</b>", body_style), Paragraph("HTML5, CSS3, Jinja2", body_style), Paragraph("Light/Dark design system with CSS custom properties, SVG circular donut progress chart, and modal dialogs.", body_style)],
        [Paragraph("<b>Testing</b>", body_style), Paragraph("pytest 9.1", body_style), Paragraph("10 automated unit and integration tests executing against isolated temporary SQLite databases.", body_style)],
        [Paragraph("<b>DevOps</b>", body_style), Paragraph("Docker & Jenkinsfile", body_style), Paragraph("python:3.11-slim container with unprivileged user; declarative CI pipeline generating JUnit XML reports.", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[80, 110, 314])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light])
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. DATABASE SCHEMA & SECURITY
    # =========================================================================
    story.append(Paragraph("3. Database Design & SQL Injection Prevention", h1_style))
    story.append(Paragraph(
        "The application uses an embedded SQLite database with the following table schema definition:",
        body_style
    ))

    db_data = [
        [Paragraph("<b>Column</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Constraints</b>", body_style), Paragraph("<b>Description</b>", body_style)],
        [Paragraph("id", code_style), Paragraph("INTEGER", body_style), Paragraph("PRIMARY KEY AUTOINCREMENT", body_style), Paragraph("Unique integer identifying each task record.", body_style)],
        [Paragraph("title", code_style), Paragraph("TEXT", body_style), Paragraph("NOT NULL, Max 150 chars", body_style), Paragraph("Title / headline of the academic task.", body_style)],
        [Paragraph("subject", code_style), Paragraph("TEXT", body_style), Paragraph("DEFAULT 'General'", body_style), Paragraph("Course name (e.g. Mathematics, Operating Systems).", body_style)],
        [Paragraph("description", code_style), Paragraph("TEXT", body_style), Paragraph("Nullable", body_style), Paragraph("Detailed task notes, links, or instructions.", body_style)],
        [Paragraph("priority", code_style), Paragraph("TEXT", body_style), Paragraph("CHECK: Low, Medium, High", body_style), Paragraph("Priority ranking for task scheduling.", body_style)],
        [Paragraph("due_date", code_style), Paragraph("TEXT", body_style), Paragraph("ISO Format: YYYY-MM-DD", body_style), Paragraph("Submission or exam target deadline.", body_style)],
        [Paragraph("status", code_style), Paragraph("TEXT", body_style), Paragraph("CHECK: Pending, Completed", body_style), Paragraph("Current lifecycle status of the task.", body_style)],
        [Paragraph("created_at", code_style), Paragraph("TIMESTAMP", body_style), Paragraph("DEFAULT CURRENT_TIMESTAMP", body_style), Paragraph("Auto-generated task creation timestamp.", body_style)]
    ]
    t_db = Table(db_data, colWidths=[65, 60, 145, 234])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light])
    ]))
    story.append(t_db)

    story.append(Paragraph("Security Architecture: Preventing SQL Injection", h2_style))
    story.append(Paragraph(
        "All database operations enforce strict <b>parameterized queries</b> using question-mark (<code>?</code>) placeholders. Input strings are passed separately to the SQLite query engine as binary parameters, completely preventing malicious SQL execution via input fields:",
        body_style
    ))
    story.append(Paragraph(
        "<code># SECURE: Parameterized Query<br/>db.execute(\"SELECT * FROM tasks WHERE subject = ? AND status = ?\", (subj, stat))</code>",
        code_style
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. APPLICATION ROUTES SPECIFICATION
    # =========================================================================
    story.append(Paragraph("4. Application Routing & Endpoints", h1_style))
    
    route_data = [
        [Paragraph("<b>Route / Endpoint</b>", body_style), Paragraph("<b>HTTP Method</b>", body_style), Paragraph("<b>Description & Business Logic</b>", body_style)],
        [Paragraph("<code>/</code>", code_style), Paragraph("GET", body_style), Paragraph("Main Dashboard: computes metrics (Total, Completed, Pending, Overdue) and renders recent tasks and deadlines.", body_style)],
        [Paragraph("<code>/tasks</code>", code_style), Paragraph("GET", body_style), Paragraph("My Tasks directory: supports tabbed filters (All, Pending, Completed, Overdue), search query, and table/grid views.", body_style)],
        [Paragraph("<code>/calendar</code>", code_style), Paragraph("GET", body_style), Paragraph("Deadlines view: groups scheduled assignments chronologically by submission date.", body_style)],
        [Paragraph("<code>/tasks/new</code>", code_style), Paragraph("GET / POST", body_style), Paragraph("Task creation endpoint: executes server-side validation and creates a database row.", body_style)],
        [Paragraph("<code>/tasks/&lt;id&gt;/toggle</code>", code_style), Paragraph("POST", body_style), Paragraph("One-click fast toggle: flips task state between 'Completed' and 'Pending'.", body_style)],
        [Paragraph("<code>/tasks/&lt;id&gt;/edit</code>", code_style), Paragraph("GET / POST", body_style), Paragraph("Task modification: updates title, subject, priority, due date, description, and status.", body_style)],
        [Paragraph("<code>/tasks/&lt;id&gt;/delete</code>", code_style), Paragraph("POST", body_style), Paragraph("Deletion: removes task row from database with confirmation safeguard.", body_style)],
        [Paragraph("<code>/login</code> & <code>/logout</code>", code_style), Paragraph("GET / POST", body_style), Paragraph("Split-screen authentication portal with demo sign-in and session clearing.", body_style)],
        [Paragraph("<code>/settings</code>", code_style), Paragraph("GET / POST", body_style), Paragraph("Preferences page: manages student display name and theme mode.", body_style)]
    ]
    t_route = Table(route_data, colWidths=[120, 65, 319])
    t_route.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light])
    ]))
    story.append(t_route)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. AUTOMATED TESTING ANALYSIS
    # =========================================================================
    story.append(Paragraph("5. Automated Testing & Verification Suite", h1_style))
    story.append(Paragraph(
        "Automated regression testing is implemented with <b>pytest</b> in <code>tests/test_app.py</code>. All 10 tests run against an isolated temporary database created via <code>tempfile.mkstemp()</code>, guaranteeing that automated test executions never corrupt or delete production data:",
        body_style
    ))

    test_table_data = [
        [Paragraph("<b>Test Function</b>", body_style), Paragraph("<b>Target Behavior Tested</b>", body_style), Paragraph("<b>Result</b>", body_style)],
        [Paragraph("test_home_page_loads", code_style), Paragraph("Checks HTTP 200 and presence of all 4 metric cards.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_create_task", code_style), Paragraph("Verifies valid task creation and database insertion.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_create_task_validation", code_style), Paragraph("Asserts empty titles return HTTP 400 Bad Request.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_update_task_status", code_style), Paragraph("Tests status transition from Pending to Completed.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_toggle_task", code_style), Paragraph("Tests one-click completion toggle and reverse toggle.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_update_task_details", code_style), Paragraph("Verifies full editing of title, subject, priority, and date.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_delete_task", code_style), Paragraph("Verifies deletion and removal from SQLite database.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_dashboard_counts_calculation", code_style), Paragraph("Validates accurate calculation of Total, Pending, and Overdue.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_task_filtering_and_tabs", code_style), Paragraph("Validates that tab filters isolate Pending from Completed tasks.", body_style), Paragraph("PASSED", body_style)],
        [Paragraph("test_calendar_and_login_views", code_style), Paragraph("Verifies that Calendar and Login endpoints render HTTP 200.", body_style), Paragraph("PASSED", body_style)]
    ]
    t_tests = Table(test_table_data, colWidths=[160, 284, 60])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TEXTCOLOR', (2,1), (2,-1), colors.HexColor("#065F46"))
    ]))
    story.append(t_tests)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 6. DEVOPS: DOCKER & JENKINS CI
    # =========================================================================
    story.append(Paragraph("6. DevOps: Docker Containerization & Jenkins CI", h1_style))
    story.append(Paragraph(
        "<b>A. Docker Containerization:</b> The application is containerized using a slim base image (<code>python:3.11-slim</code>) with an unprivileged system user (<code>appuser</code>, UID 1000). A host bind mount (<code>-v ${PWD}/instance:/app/instance</code>) maps the local database directory to the container, ensuring that SQLite data persists across container restarts and updates.",
        body_style
    ))
    story.append(Paragraph(
        "<b>B. Jenkins Continuous Integration:</b> The declarative <code>Jenkinsfile</code> defines a three-stage automated pipeline: (1) Checkout source code from GitHub, (2) Install Python dependencies from requirements.txt, (3) Execute <code>pytest --junitxml=test-results.xml</code>. The Jenkins JUnit plugin archives the test report to track build health.",
        body_style
    ))
    story.append(Paragraph(
        "<b>C. Jira Agile Planning:</b> Project backlog and sprints are organized under key <b>STMS</b>, covering 8 user stories with Gherkin acceptance criteria (Given/When/Then), story point estimations, and Smart Commits tracking.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 7. VIVA VOCE QUESTIONS & ANSWERS
    # =========================================================================
    story.append(Paragraph("7. Essential Viva Voce Questions & Answers", h1_style))

    viva_list = [
        ("Q1: What is Flask and why is it called a micro-framework?",
         "Flask is a lightweight Python web framework based on Werkzeug WSGI and Jinja2 templating. It is called 'micro' because it provides core routing and templating without enforcing specific database engines or form libraries, leaving architectural choices to the developer."),
        ("Q2: Why did you choose SQLite instead of MySQL or PostgreSQL for this project?",
         "SQLite is serverless, zero-configuration, and stores the entire database in a single portable file (instance/tasks.db). It supports full ACID transactions and eliminated the need to maintain an external database server, making it lightweight and ideal for practical demonstrations."),
        ("Q3: How do you prevent SQL Injection in your database queries?",
         "By strictly using parameterized queries with question-mark (?) placeholders. User inputs are treated as literal values rather than executable SQL statements, completely preventing injection attacks."),
        ("Q4: What is the Application Factory pattern (create_app)?",
         "It is a design pattern where the Flask application instance is created inside a function rather than as a global variable. This enables creating isolated application instances with different configurations (e.g. temporary in-memory database for testing vs file-based database for production)."),
        ("Q5: What is the difference between a Docker image and a Docker container?",
         "A Docker image is a read-only, immutable template containing the OS, libraries, and code (similar to a Class in OOP). A Docker container is a running, stateful instance instantiated from that image (similar to an Object)."),
        ("Q6: Why is a Docker volume essential for SQLite in containerized environments?",
         "Containers are ephemeral; any files written inside a container are deleted when the container is stopped or removed. A Docker Volume or bind mount maps a host directory to /app/instance so database records persist permanently."),
        ("Q7: What does Continuous Integration (CI) mean in this project?",
         "CI is the practice of automatically triggering builds and automated pytest suites whenever code is pushed to GitHub. In our Jenkinsfile, any failing test marks the build as failed, preventing regressions from reaching production."),
        ("Q8: Why did your automated tests use temporary databases instead of tasks.db?",
         "If tests used the live database, running pytest would corrupt or wipe real user tasks. Using Python's tempfile.mkstemp() creates an isolated database for each test session and cleans it up during teardown.")
    ]

    for q, a in viva_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))

    # =========================================================================
    # 8. HOW TO RUN IN EXAM
    # =========================================================================
    story.append(Paragraph("8. Project Demonstration Reference", h1_style))
    story.append(Paragraph(
        "To run the project in VS Code during your examination: (1) Open VS Code terminal (`Ctrl + ~`), (2) Execute <code>python app.py</code>, (3) Open browser at <code>http://127.0.0.1:5000</code>. To run automated tests, execute <code>python -m pytest</code> in the terminal.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Report generated successfully at: {pdf_filename}")

if __name__ == '__main__':
    create_pdf_report()
