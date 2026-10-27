"""
Generate professional 16:9 PowerPoint Presentation for TaskMate.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    c_primary = RGBColor(79, 70, 229)     # #4F46E5 Indigo
    c_secondary = RGBColor(59, 130, 246)  # #3B82F6 Blue
    c_dark = RGBColor(15, 23, 42)         # #0F172A Dark Navy
    c_card_bg = RGBColor(255, 255, 255)   # #FFFFFF
    c_card_dark = RGBColor(30, 41, 59)    # #1E293B
    c_text_dark = RGBColor(15, 23, 42)    # Dark text
    c_text_muted = RGBColor(100, 116, 139)# Gray text
    c_text_white = RGBColor(255, 255, 255)
    c_success = RGBColor(16, 185, 129)    # #10B981 Green
    c_warning = RGBColor(245, 158, 11)    # #F59E0B Amber
    c_danger = RGBColor(239, 68, 68)      # #EF4444 Red
    c_light_bg = RGBColor(248, 250, 252)  # #F8FAFC

    def add_header(slide, title_text, category_text="TASKMATE PROJECT PRESENTATION"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = c_dark
        top_bar.line.fill.background()

        # Accent line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.08), Inches(13.333), Inches(0.04))
        accent.fill.solid()
        accent.fill.fore_color.rgb = c_primary
        accent.line.fill.background()

        # Category text
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_secondary
        p.font.name = "Arial"

        # Title text
        tx_box2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.6))
        tf2 = tx_box2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = c_text_white
        p2.font.name = "Arial"

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_card(slide, x, y, w, h, bg_color=c_card_bg, border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Gradient Feel)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, c_dark)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = c_primary
    bar.line.fill.background()

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.4), Inches(1.6), Inches(10.5), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TASKMATE"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = c_text_white
    p.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "Student Task Management System"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = c_secondary
    p2.font.name = "Arial"
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "A Full-Stack Academic Productivity Platform with Flask, SQLite, Automated Testing, Docker, & CI/CD"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.font.name = "Arial"
    p3.space_before = Pt(16)

    # Bottom Metadata Pill
    bottom_card = add_card(s1, 1.0, 5.7, 11.333, 1.1, c_card_dark)
    tb_meta = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(10.9), Inches(0.9))
    tf_m = tb_meta.text_frame
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Department of Computer Science & Engineering • Practical Examination & Viva Presentation"
    p_m1.font.size = Pt(13)
    p_m1.font.bold = True
    p_m1.font.color.rgb = c_text_white
    
    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Developed by: Student Developer   |   Repository: github.com/legendarydeep/STM"
    p_m2.font.size = Pt(11)
    p_m2.font.color.rgb = RGBColor(148, 163, 184)
    p_m2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, c_light_bg)
    add_header(s2, "Problem Statement & Project Motivation", "THE CHALLENGE")

    # Card 1: The Problem
    add_card(s2, 1.0, 1.6, 5.3, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb = s2.shapes.add_textbox(Inches(1.3), Inches(1.8), Inches(4.7), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Academic Challenge"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_danger

    bullets_p1 = [
        "Multiple Deadlines: Students juggle assignments, lab sheets, presentations, and exams across 5-7 subjects simultaneously.",
        "Scattered Information: Important dates are scattered in WhatsApp groups, emails, and manual notebooks.",
        "Missed Deadlines: Lack of real-time visibility leads to last-minute rush, stress, and missed submission cutoffs.",
        "No Visual Analytics: Students cannot quickly see what percentage of work is pending, completed, or overdue."
    ]
    for b in bullets_p1:
        p_b = tf.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = c_text_dark
        p_b.space_before = Pt(10)

    # Card 2: The Solution
    add_card(s2, 6.9, 1.6, 5.4, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb2 = s2.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(4.8), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "The TaskMate Solution"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = c_success

    bullets_p2 = [
        "Centralized Academic Hub: Single dashboard to capture and track all coursework assignments with subject tags.",
        "Real-Time Donut Analytics: Instant visual breakdown of Total, Completed, Pending, and Overdue workloads.",
        "Automated Overdue Detection: Tasks past their deadline automatically trigger overdue badges and alerts.",
        "DevOps & Quality Ready: Built following software engineering standards (pytest, Docker, Git, Jira, CI/CD)."
    ]
    for b in bullets_p2:
        p_b = tf2.add_paragraph()
        p_b.text = "✓ " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = c_text_dark
        p_b.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, c_light_bg)
    add_header(s3, "System Architecture & Technology Stack", "TECHNICAL SPECIFICATIONS")

    tech_items = [
        ("Backend Framework", "Python 3 & Flask 3.1", "Micro-framework providing WSGI compliance, application factory pattern, and fast route dispatching.", c_primary),
        ("Database Engine", "SQLite 3 (Embedded)", "Serverless, zero-config relational database. Stores data in instance/tasks.db with ACID compliance.", c_secondary),
        ("Frontend & UI/UX", "HTML5, Vanilla CSS3, Jinja2", "Modern responsive design system with Light/Dark themes, modal popups, and SVG donut charts.", c_success),
        ("Testing Framework", "pytest 9.1", "Automated regression testing using temporary test databases. 10/10 tests pass in < 1 second.", c_warning),
        ("Containerization", "Docker & Dockerfile", "Lightweight python:3.11-slim image with unprivileged appuser and persistent host volume mounts.", c_danger),
        ("CI Pipeline", "Jenkins (Declarative)", "Automated pipeline: SCM checkout, dependency installation, pytest execution, and JUnit reporting.", c_primary)
    ]

    for idx, (title, subtitle, desc, col) in enumerate(tech_items):
        row = idx // 3
        col_idx = idx % 3
        x = 0.8 + (col_idx * 4.0)
        y = 1.6 + (row * 2.7)

        card = add_card(s3, x, y, 3.7, 2.4, c_card_bg, col)
        tb = s3.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.2), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title.upper()
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = c_text_dark
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = c_text_muted
        p3.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: CORE APPLICATION FEATURES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, c_light_bg)
    add_header(s4, "Key Features & Application Capabilities", "FUNCTIONAL MODULES")

    features = [
        ("Dashboard Analytics", "4 Top Metric Cards (Total, Completed, Pending, Overdue) + Interactive SVG Donut Progress Chart with real-time percentage indicators."),
        ("Quick Completion Toggle", "One-click checkbox on tasks to immediately toggle between Pending and Completed states without full page reloading."),
        ("Add Task Modal & Direct Page", "Fast modal popup with blurred backdrop: Task Title, Subject, Priority (Low/Med/High), Due Date, and Description."),
        ("Multi-Criteria Task Filtering", "Tabbed filtering (All, Pending, Completed, Overdue) + Search query bar + Subject and Priority dropdown filters."),
        ("Table View & Card Grid View", "Switchable display layouts: Dense tabular view for quick management and rich visual card grid for assignment details."),
        ("Calendar & Deadlines Agenda", "Chronological timeline view grouping upcoming and past-due assignments by date for exam/submission scheduling."),
        ("Light & Dark Theme Switcher", "Instant theme switching (☀️/🌙) with dark slate mode (#0B1120) and persistent preference memory in localStorage."),
        ("Split-Screen Login Portal", "Authentication and student profile switcher featuring branded royal-blue banner and demo guest login flow.")
    ]

    for idx, (f_title, f_desc) in enumerate(features):
        row = idx // 2
        col_idx = idx % 2
        x = 0.8 + (col_idx * 5.9)
        y = 1.5 + (row * 1.35)

        card = add_card(s4, x, y, 5.6, 1.15, c_card_bg, RGBColor(226, 232, 240))
        tb = s4.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.1), Inches(5.2), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = "✦  " + f_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = c_primary

        p2 = tf.add_paragraph()
        p2.text = f_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = c_text_muted
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: DATABASE DESIGN & SECURITY
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, c_light_bg)
    add_header(s5, "Database Schema & SQL Injection Prevention", "DATA INTEGRITY")

    # Left: Schema Table
    add_card(s5, 0.8, 1.6, 6.8, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.4), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SQLite Schema: 'tasks' Table"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary

    schema_rows = [
        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT", "Unique sequential task ID"),
        ("title", "TEXT NOT NULL", "Assignment title (Max 150 chars)"),
        ("subject", "TEXT DEFAULT 'General'", "Course category / subject"),
        ("description", "TEXT", "Optional notes, references, steps"),
        ("priority", "TEXT DEFAULT 'Medium'", "Check: Low, Medium, High"),
        ("due_date", "TEXT", "Deadline date string (YYYY-MM-DD)"),
        ("status", "TEXT DEFAULT 'Pending'", "Check: Pending, Completed"),
        ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP", "Task creation timestamp")
    ]
    for col, typ, desc in schema_rows:
        p_col = tf.add_paragraph()
        p_col.text = f"• {col} ({typ}) — {desc}"
        p_col.font.size = Pt(10.5)
        p_col.font.color.rgb = c_text_dark
        p_col.space_before = Pt(4)

    # Right: Security & Injection Prevention
    add_card(s5, 7.9, 1.6, 4.6, 5.2, c_card_bg, c_success)
    tb2 = s5.shapes.add_textbox(Inches(8.1), Inches(1.8), Inches(4.2), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    p2.text = "SQL Injection Prevention"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = c_success

    p_sec1 = tf2.add_paragraph()
    p_sec1.text = "Why Parameterized Queries?"
    p_sec1.font.size = Pt(13)
    p_sec1.font.bold = True
    p_sec1.font.color.rgb = c_text_dark
    p_sec1.space_before = Pt(8)

    p_sec2 = tf2.add_paragraph()
    p_sec2.text = "We strictly use question mark (?) parameter binding in all SQL queries rather than Python f-strings or string concatenation."
    p_sec2.font.size = Pt(11)
    p_sec2.font.color.rgb = c_text_muted
    p_sec2.space_before = Pt(4)

    p_sec3 = tf2.add_paragraph()
    p_sec3.text = "✓ SECURE CODE IMPLEMENTED:\ndb.execute('SELECT * FROM tasks WHERE status = ?', (status,))"
    p_sec3.font.size = Pt(10)
    p_sec3.font.bold = True
    p_sec3.font.color.rgb = c_success
    p_sec3.space_before = Pt(10)

    p_sec4 = tf2.add_paragraph()
    p_sec4.text = "✗ INSECURE VULNERABLE CODE:\ndb.execute(f'SELECT * FROM tasks WHERE status = {status}')"
    p_sec4.font.size = Pt(10)
    p_sec4.font.bold = True
    p_sec4.font.color.rgb = c_danger
    p_sec4.space_before = Pt(8)

    p_sec5 = tf2.add_paragraph()
    p_sec5.text = "The SQLite database engine treats input strictly as literal data, completely neutralizing SQL injection attacks."
    p_sec5.font.size = Pt(10.5)
    p_sec5.font.color.rgb = c_text_dark
    p_sec5.space_before = Pt(10)

    # =========================================================================
    # SLIDE 6: AUTOMATED TESTING WITH PYTEST
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, c_light_bg)
    add_header(s6, "Automated Testing & Quality Assurance", "PYTEST TEST SUITE")

    add_card(s6, 0.8, 1.6, 6.0, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "10 Automated Test Cases (All Passing)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary

    test_list = [
        ("test_home_page_loads", "Verifies HTTP 200 and all metric cards"),
        ("test_create_task", "Tests valid task insertion and DB verification"),
        ("test_create_task_validation", "Verifies empty title returns HTTP 400 Bad Request"),
        ("test_update_task_status", "Validates status change to Completed"),
        ("test_toggle_task", "Tests 1-click checkbox completion toggle"),
        ("test_update_task_details", "Verifies editing title, subject, priority, date"),
        ("test_delete_task", "Tests deletion and removal from SQLite"),
        ("test_dashboard_counts_calculation", "Validates accurate count aggregation"),
        ("test_task_filtering_and_tabs", "Verifies tab filters separate task states"),
        ("test_calendar_and_login_views", "Verifies Calendar and Login routes")
    ]
    for name, desc in test_list:
        p_t = tf.add_paragraph()
        p_t.text = f"✓ {name}: {desc}"
        p_t.font.size = Pt(10)
        p_t.font.color.rgb = c_text_dark
        p_t.space_before = Pt(3)

    # Right: Test Isolation Box
    add_card(s6, 7.1, 1.6, 5.4, 5.2, c_card_dark)
    tb2 = s6.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.0), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    p2.text = "Test Isolation & Execution Metrics"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = c_success

    p_iso = tf2.add_paragraph()
    p_iso.text = "Isolated Temporary Databases:"
    p_iso.font.size = Pt(13)
    p_iso.font.bold = True
    p_iso.font.color.rgb = c_text_white
    p_iso.space_before = Pt(12)

    p_iso2 = tf2.add_paragraph()
    p_iso2.text = "Every test run creates a temporary SQLite file via tempfile.mkstemp() and deletes it on teardown. Real production tasks in instance/tasks.db are NEVER modified or erased."
    p_iso2.font.size = Pt(11)
    p_iso2.font.color.rgb = RGBColor(203, 213, 225)
    p_iso2.space_before = Pt(4)

    p_res = tf2.add_paragraph()
    p_res.text = "================ 10 passed in 0.92s ================"
    p_res.font.size = Pt(11)
    p_res.font.bold = True
    p_res.font.color.rgb = c_success
    p_res.space_before = Pt(16)

    p_ci = tf2.add_paragraph()
    p_ci.text = "JUnit XML Export:\npython -m pytest --junitxml=test-results.xml\nGenerates test health reports for Jenkins CI."
    p_ci.font.size = Pt(10.5)
    p_ci.font.color.rgb = RGBColor(148, 163, 184)
    p_ci.space_before = Pt(12)

    # =========================================================================
    # SLIDE 7: DOCKER CONTAINERIZATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, c_light_bg)
    add_header(s7, "Docker Containerization & Volume Persistence", "DEVOPS PRACTICES")

    # Card 1: Key Docker Features
    add_card(s7, 0.8, 1.6, 5.7, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Production-Conscious Dockerfile"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary

    docker_points = [
        ("Base Image", "python:3.11-slim reduces container image footprint to ~150 MB (avoiding bloat)."),
        ("Non-Root Security", "Creates and switches to an unprivileged system user 'appuser' (UID 1000) for least-privilege execution."),
        ("Layer Caching", "requirements.txt is copied and installed prior to copying source code to leverage Docker cache."),
        ("Port Binding", "Exposes port 5000 and runs Flask with host=0.0.0.0 to allow container network access."),
        (".dockerignore", "Excludes venv/, .git/, *.db, and __pycache__ from the build context.")
    ]
    for title, desc in docker_points:
        p_pt = tf.add_paragraph()
        p_pt.text = f"• {title}: {desc}"
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_text_dark
        p_pt.space_before = Pt(8)

    # Card 2: Volume Persistence
    add_card(s7, 6.8, 1.6, 5.7, 5.2, c_card_bg, c_warning)
    tb2 = s7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    p2.text = "SQLite Data Persistence via Volumes"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = c_warning

    p_vol = tf2.add_paragraph()
    p_vol.text = "The Ephemeral Container Problem:"
    p_vol.font.size = Pt(12)
    p_vol.font.bold = True
    p_vol.font.color.rgb = c_text_dark
    p_vol.space_before = Pt(8)

    p_vol2 = tf2.add_paragraph()
    p_vol2.text = "By default, Docker containers are disposable. When a container is stopped or removed, any SQLite database written inside is destroyed."
    p_vol2.font.size = Pt(10.5)
    p_vol2.font.color.rgb = c_text_muted
    p_vol2.space_before = Pt(2)

    p_vol3 = tf2.add_paragraph()
    p_vol3.text = "The Solution: Host Bind Mount:"
    p_vol3.font.size = Pt(12)
    p_vol3.font.bold = True
    p_vol3.font.color.rgb = c_text_dark
    p_vol3.space_before = Pt(8)

    p_vol4 = tf2.add_paragraph()
    p_vol4.text = 'docker run -d -p 5000:5000 -v "${PWD}/instance:/app/instance" taskmate'
    p_vol4.font.size = Pt(10)
    p_vol4.font.bold = True
    p_vol4.font.color.rgb = c_primary
    p_vol4.space_before = Pt(4)

    p_vol5 = tf2.add_paragraph()
    p_vol5.text = "This mounts the host machine's ./instance directory directly into /app/instance. Tasks remain preserved across container updates and restarts!"
    p_vol5.font.size = Pt(10.5)
    p_vol5.font.color.rgb = c_text_muted
    p_vol5.space_before = Pt(6)

    # =========================================================================
    # SLIDE 8: JENKINS CI & JIRA AGILE PLANNING
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, c_light_bg)
    add_header(s8, "Jenkins CI Pipeline & Jira Agile Planning", "AUTOMATION & SDLC")

    # Left: Jenkins Pipeline
    add_card(s8, 0.8, 1.6, 5.7, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Declarative Jenkinsfile Pipeline"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary

    stages = [
        ("Stage 1: Checkout Code", "Clones latest commit from GitHub repository."),
        ("Stage 2: Install Dependencies", "Installs requirements.txt into the build agent environment."),
        ("Stage 3: Run Automated Tests", "Executes 'pytest --junitxml=test-results.xml'. Any failure halts the pipeline."),
        ("Post Actions: Archive Reports", "The JUnit plugin records test results and plots historical test trend graphs.")
    ]
    for s_title, s_desc in stages:
        p_st = tf.add_paragraph()
        p_st.text = f"▶ {s_title}"
        p_st.font.size = Pt(12)
        p_st.font.bold = True
        p_st.font.color.rgb = c_text_dark
        p_st.space_before = Pt(8)

        p_sd = tf.add_paragraph()
        p_sd.text = s_desc
        p_sd.font.size = Pt(10.5)
        p_sd.font.color.rgb = c_text_muted

    # Right: Jira Agile Planning
    add_card(s8, 6.8, 1.6, 5.7, 5.2, c_card_bg, RGBColor(226, 232, 240))
    tb2 = s8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    p2.text = "Jira Agile Project Planning (STMS)"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = c_secondary

    p_j1 = tf2.add_paragraph()
    p_j1.text = "Scrum Sprint Breakdown:"
    p_j1.font.size = Pt(12)
    p_j1.font.bold = True
    p_j1.font.color.rgb = c_text_dark
    p_j1.space_before = Pt(8)

    jira_points = [
        "Sprint 1: Architecture, database setup, and core CRUD handlers.",
        "Sprint 2: UI redesign, metric cards, donut charts, and modal dialogs.",
        "Sprint 3: Automated testing, Docker containerization, and CI/CD.",
        "Smart Commits Convention: git commit -m '[STMS-2] Implement task validation #resolve' links commits directly to Jira issues."
    ]
    for jp in jira_points:
        p_jp = tf2.add_paragraph()
        p_jp.text = "• " + jp
        p_jp.font.size = Pt(10.5)
        p_jp.font.color.rgb = c_text_muted
        p_jp.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: TOP VIVA VOCE QUESTIONS & ANSWERS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, c_light_bg)
    add_header(s9, "Essential Viva Voce Questions & Answers", "EXAMINATION PREPARATION")

    viva_qa = [
        ("Q: Why did you choose SQLite over MySQL or PostgreSQL?",
         "A: SQLite is serverless, zero-configuration, and stores the entire database in a single portable file (instance/tasks.db). It supports ACID transactions and is ideal for lightweight college practical demonstrations."),
        ("Q: What is the Application Factory pattern in Flask?",
         "A: It creates the Flask app instance inside create_app(test_config). This enables creating multiple isolated app instances with different settings (e.g. temporary in-memory DB for tests vs persistent file DB for production)."),
        ("Q: What is the difference between a Docker Image and a Container?",
         "A: An Image is an immutable, read-only blueprint containing the OS, Python, and code (like a Class). A Container is a running, stateful instance instantiated from that image (like an Object)."),
        ("Q: Why use pytest fixtures with temporary databases?",
         "A: Using tempfile.mkstemp() creates an isolated database for each test session, preventing automated tests from modifying or erasing real student records.")
    ]

    for idx, (q, a) in enumerate(viva_qa):
        row = idx // 2
        col_idx = idx % 2
        x = 0.8 + (col_idx * 5.9)
        y = 1.6 + (row * 2.7)

        card = add_card(s9, x, y, 5.6, 2.4, c_card_bg, RGBColor(226, 232, 240))
        tb = s9.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(5.2), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = q
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = c_primary

        p2 = tf.add_paragraph()
        p2.text = a
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = c_text_dark
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 10: CONCLUSION & DEMONSTRATION WALKTHROUGH
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, c_dark)

    tb = s10.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CONCLUSION & LIVE DEMO"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = c_text_white
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "TaskMate demonstrates end-to-end software engineering best practices:\nClean architecture, secure database interactions, responsive UI, 100% test coverage, and DevOps readiness."
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(16)

    # Center card for links
    demo_card = add_card(s10, 2.5, 4.2, 8.333, 1.8, c_card_dark, c_primary)
    tb_c = s10.shapes.add_textbox(Inches(2.7), Inches(4.3), Inches(7.9), Inches(1.6))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    pc1 = tf_c.paragraphs[0]
    pc1.text = "🚀 Live Application: http://127.0.0.1:5000"
    pc1.font.size = Pt(18)
    pc1.font.bold = True
    pc1.font.color.rgb = c_success
    pc1.alignment = PP_ALIGN.CENTER

    pc2 = tf_c.add_paragraph()
    pc2.text = "📦 GitHub Repository: https://github.com/legendarydeep/STM"
    pc2.font.size = Pt(14)
    pc2.font.color.rgb = c_text_white
    pc2.alignment = PP_ALIGN.CENTER
    pc2.space_before = Pt(6)

    pc3 = tf_c.add_paragraph()
    pc3.text = "Thank you! I am ready for questions."
    pc3.font.size = Pt(14)
    pc3.font.bold = True
    pc3.font.color.rgb = c_secondary
    pc3.alignment = PP_ALIGN.CENTER
    pc3.space_before = Pt(8)

    # Save presentation
    output_path = r"c:\Users\deep\OneDrive\Desktop\asdd mini project\TaskMate_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == '__main__':
    create_presentation()
