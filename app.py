"""
TaskMate — Student Task Management System
A modern, responsive Flask & SQLite web application with Light/Dark themes,
real-time dashboard analytics, subject tracking, and complete task workflows.
"""

import os
import sqlite3
from datetime import datetime, date
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g
)

# Valid choice definitions
VALID_PRIORITIES = ['Low', 'Medium', 'High']
VALID_STATUSES = ['Pending', 'In Progress', 'Completed']
DEFAULT_SUBJECTS = [
    'Mathematics',
    'Web Development',
    'Computer Science',
    'Database Systems',
    'Operating Systems',
    'English',
    'General'
]


def get_db_path(app):
    """Return database file path from app configuration."""
    return app.config.get('DATABASE', os.path.join(app.instance_path, 'tasks.db'))


def get_db(app=None):
    """
    Open a database connection for the current request context.
    Uses sqlite3.Row for dictionary-like column access.
    """
    if 'db' not in g:
        from flask import current_app
        active_app = app or current_app
        db_path = get_db_path(active_app)

        if db_path != ':memory:':
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables and migrate schema if needed."""
    db_path = get_db_path(app)
    if db_path != ':memory:':
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT DEFAULT 'General',
                description TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium',
                due_date TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Migration check: add 'subject' column if upgrading an existing db
        cursor = conn.execute("PRAGMA table_info(tasks);")
        columns = [row[1] for row in cursor.fetchall()]
        if 'subject' not in columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN subject TEXT DEFAULT 'General';")

        # Seed sample tasks if DB is completely empty and NOT in TESTING mode
        if not app.config.get('TESTING', False):
            count_cursor = conn.execute("SELECT COUNT(*) FROM tasks;")
            if count_cursor.fetchone()[0] == 0:
                today_str = date.today().strftime('%Y-%m-%d')
                conn.executemany("""
                    INSERT INTO tasks (title, subject, description, priority, due_date, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, [
                    ('Math Assignment', 'Mathematics', 'Calculus problem set chapters 3 and 4.', 'Medium', today_str, 'Completed'),
                    ('Web Development Project', 'Web Development', 'Build the complete frontend and backend for the student task management system.', 'High', today_str, 'Pending'),
                    ('Data Structures Notes', 'Computer Science', 'Review binary search trees and heap implementations.', 'Medium', '2026-11-15', 'Pending'),
                    ('Database Lab Report', 'Database Systems', 'Write SQL queries for normalization and indexing benchmarks.', 'High', '2026-10-01', 'Pending'),
                    ('English Presentation', 'English', 'Prepare 10 slides on technical communication and modern engineering.', 'Low', '2026-11-20', 'Pending')
                ])

    conn.close()


def create_app(test_config=None):
    """Application factory for TaskMate."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='taskmate-student-secret-key-2026',
        DATABASE=os.path.join(app.instance_path, 'tasks.db'),
    )

    if test_config is not None:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)
    init_db(app)

    # Context processor to inject common variables into all templates
    @app.context_processor
    def inject_global_data():
        current_user = session.get('user', 'Student')
        current_theme = session.get('theme', 'light')
        today_formatted = datetime.now().strftime("%A, %d %B %Y")
        return {
            'current_user': current_user,
            'current_theme': current_theme,
            'today_formatted': today_formatted,
            'valid_statuses': VALID_STATUSES,
            'valid_priorities': VALID_PRIORITIES,
            'default_subjects': DEFAULT_SUBJECTS
        }

    # -------------------------------------------------------------
    # HELPER FUNCTIONS
    # -------------------------------------------------------------
    def get_task_metrics(db):
        """Calculate total, completed, pending, overdue counts and percentages."""
        today_iso = date.today().strftime('%Y-%m-%d')
        query = """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN status != 'Completed' AND (due_date IS NULL OR due_date = '' OR due_date >= ?) THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status != 'Completed' AND due_date IS NOT NULL AND due_date != '' AND due_date < ? THEN 1 ELSE 0 END) AS overdue
            FROM tasks;
        """
        row = db.execute(query, (today_iso, today_iso)).fetchone()
        total = row['total'] or 0
        completed = row['completed'] or 0
        pending = row['pending'] or 0
        overdue = row['overdue'] or 0

        # Percentages for donut chart
        completed_pct = round((completed / total) * 100) if total > 0 else 0
        pending_pct = round((pending / total) * 100) if total > 0 else 0
        overdue_pct = round((overdue / total) * 100) if total > 0 else 0

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completed_pct': completed_pct,
            'pending_pct': pending_pct,
            'overdue_pct': overdue_pct
        }

    # -------------------------------------------------------------
    # ROUTES
    # -------------------------------------------------------------

    @app.route('/')
    def index():
        """
        Dashboard View (Panel 1 & 3):
        - 4 top metric cards: Total, Completed, Pending, Overdue
        - Donut chart representation of task progress
        - Recent Tasks with quick check completion
        - Upcoming deadlines list
        """
        db = get_db()
        stats = get_task_metrics(db)

        # Recent tasks (last 6 items)
        recent_tasks = db.execute("""
            SELECT * FROM tasks
            ORDER BY id DESC
            LIMIT 6
        """).fetchall()

        # Upcoming deadlines (pending tasks with due dates)
        today_iso = date.today().strftime('%Y-%m-%d')
        upcoming_tasks = db.execute("""
            SELECT * FROM tasks
            WHERE status != 'Completed' AND due_date IS NOT NULL AND due_date != ''
            ORDER BY due_date ASC
            LIMIT 5
        """).fetchall()

        return render_template(
            'index.html',
            stats=stats,
            recent_tasks=recent_tasks,
            upcoming_tasks=upcoming_tasks,
            today_iso=today_iso
        )

    @app.route('/tasks')
    def tasks_view():
        """
        My Tasks View (Panel 4 & 7):
        - Filter tabs: All, Pending, Completed, Overdue
        - Subject and Priority filters
        - Live search query
        - Grid card view and table view modes
        """
        db = get_db()
        today_iso = date.today().strftime('%Y-%m-%d')

        tab = request.args.get('tab', 'All').strip()
        search_query = request.args.get('q', '').strip()
        priority_filter = request.args.get('priority', '').strip()
        subject_filter = request.args.get('subject', '').strip()
        view_mode = request.args.get('view', 'table').strip()

        # Build query
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if tab == 'Pending':
            query += " AND status = 'Pending'"
        elif tab == 'Completed':
            query += " AND status = 'Completed'"
        elif tab == 'Overdue':
            query += " AND status != 'Completed' AND due_date IS NOT NULL AND due_date != '' AND due_date < ?"
            params.append(today_iso)

        if search_query:
            query += " AND (title LIKE ? OR description LIKE ? OR subject LIKE ?)"
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard])

        if priority_filter in VALID_PRIORITIES:
            query += " AND priority = ?"
            params.append(priority_filter)

        if subject_filter:
            query += " AND subject = ?"
            params.append(subject_filter)

        query += " ORDER BY id DESC"
        tasks = db.execute(query, params).fetchall()

        # Available subjects in DB
        subject_rows = db.execute("SELECT DISTINCT subject FROM tasks WHERE subject IS NOT NULL AND subject != ''").fetchall()
        existing_subjects = sorted(list(set([r['subject'] for r in subject_rows] + DEFAULT_SUBJECTS)))

        stats = get_task_metrics(db)

        return render_template(
            'tasks.html',
            tasks=tasks,
            stats=stats,
            current_tab=tab,
            search_query=search_query,
            priority_filter=priority_filter,
            subject_filter=subject_filter,
            view_mode=view_mode,
            subjects=existing_subjects,
            today_iso=today_iso
        )

    @app.route('/completed')
    def completed_view():
        """Quick shortcut to Completed Tasks tab."""
        return redirect(url_for('tasks_view', tab='Completed'))

    @app.route('/calendar')
    def calendar_view():
        """
        Calendar / Deadlines Agenda View:
        Displays tasks grouped by due date.
        """
        db = get_db()
        tasks = db.execute("""
            SELECT * FROM tasks
            WHERE due_date IS NOT NULL AND due_date != ''
            ORDER BY due_date ASC, priority DESC
        """).fetchall()

        # Group tasks by due date
        grouped = {}
        for task in tasks:
            d = task['due_date']
            if d not in grouped:
                grouped[d] = []
            grouped[d].append(task)

        today_iso = date.today().strftime('%Y-%m-%d')
        return render_template('calendar.html', grouped_tasks=grouped, today_iso=today_iso)

    @app.route('/settings', methods=['GET', 'POST'])
    def settings_view():
        """Settings View: student profile, theme, and data reset."""
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_profile':
                user_name = request.form.get('user_name', 'Student').strip() or 'Student'
                session['user'] = user_name
                flash(f"Profile updated! Welcome, {user_name}.", 'success')
            elif action == 'toggle_theme':
                new_theme = request.form.get('theme', 'light')
                session['theme'] = new_theme
                flash(f"Theme switched to {new_theme.capitalize()} mode.", 'info')
            elif action == 'clear_data':
                db = get_db()
                db.execute("DELETE FROM tasks")
                db.commit()
                flash("All tasks have been cleared.", 'danger')
            return redirect(url_for('settings_view'))

        return render_template('settings.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login_view():
        """
        Login Screen (Panel 6):
        Split layout with left branding banner and right sign-in form.
        """
        if request.method == 'POST':
            email_or_user = request.form.get('username', '').strip()
            if email_or_user:
                session['user'] = email_or_user.split('@')[0].capitalize()
            else:
                session['user'] = 'Student'
            flash(f"Welcome back, {session['user']}!", 'success')
            return redirect(url_for('index'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        """Log out and reset session user."""
        session.pop('user', None)
        flash("You have been signed out.", 'info')
        return redirect(url_for('login_view'))

    @app.route('/tasks/new', methods=['GET', 'POST'])
    def add_task():
        """Create a new task with validation (supports modal or direct page)."""
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            subject = request.form.get('subject', 'General').strip() or 'General'
            description = request.form.get('description', '').strip()
            priority = request.form.get('priority', 'Medium').strip()
            due_date = request.form.get('due_date', '').strip()
            status = request.form.get('status', 'Pending').strip()

            errors = []
            if not title:
                errors.append("Task title is required.")
            elif len(title) > 150:
                errors.append("Task title cannot exceed 150 characters.")

            if priority not in VALID_PRIORITIES:
                errors.append(f"Invalid priority: {priority}")

            if status not in VALID_STATUSES:
                errors.append(f"Invalid status: {status}")

            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    errors.append("Due date must be in YYYY-MM-DD format.")

            if errors:
                for err in errors:
                    flash(err, 'danger')
                return render_template(
                    'add_task.html',
                    title=title,
                    subject=subject,
                    description=description,
                    priority=priority,
                    due_date=due_date,
                    status=status
                ), 400

            db = get_db()
            db.execute("""
                INSERT INTO tasks (title, subject, description, priority, due_date, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, subject, description, priority, due_date if due_date else None, status))
            db.commit()

            flash(f"Task '{title}' created successfully!", 'success')
            return redirect(request.referrer or url_for('index'))

        return render_template('add_task.html')

    @app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
    def toggle_task(task_id):
        """Toggle a task between Completed and Pending via one click checkbox."""
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            flash("Task not found.", 'danger')
            return redirect(url_for('index'))

        new_status = 'Pending' if task['status'] == 'Completed' else 'Completed'
        db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        db.commit()

        if new_status == 'Completed':
            flash(f"🎉 Task '{task['title']}' marked as Completed!", 'success')
        else:
            flash(f"Task '{task['title']}' moved back to Pending.", 'info')

        return redirect(request.referrer or url_for('index'))

    @app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    def edit_task(task_id):
        """Edit an existing task."""
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

        if task is None:
            flash(f"Task #{task_id} not found.", 'danger')
            return redirect(url_for('tasks_view'))

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            subject = request.form.get('subject', 'General').strip() or 'General'
            description = request.form.get('description', '').strip()
            priority = request.form.get('priority', 'Medium').strip()
            due_date = request.form.get('due_date', '').strip()
            status = request.form.get('status', 'Pending').strip()

            errors = []
            if not title:
                errors.append("Task title is required.")
            elif len(title) > 150:
                errors.append("Task title cannot exceed 150 characters.")

            if priority not in VALID_PRIORITIES:
                errors.append(f"Invalid priority: {priority}")

            if status not in VALID_STATUSES:
                errors.append(f"Invalid status: {status}")

            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    errors.append("Due date must be in YYYY-MM-DD format.")

            if errors:
                for err in errors:
                    flash(err, 'danger')
                return render_template('edit_task.html', task=task), 400

            db.execute("""
                UPDATE tasks
                SET title = ?, subject = ?, description = ?, priority = ?, due_date = ?, status = ?
                WHERE id = ?
            """, (title, subject, description, priority, due_date if due_date else None, status, task_id))
            db.commit()

            flash(f"Task #{task_id} updated successfully!", 'success')
            return redirect(url_for('tasks_view'))

        return render_template('edit_task.html', task=task)

    @app.route('/tasks/<int:task_id>/status', methods=['POST'])
    def update_status(task_id):
        """Quick status change directly from dropdown."""
        new_status = request.form.get('status', '').strip()
        if new_status not in VALID_STATUSES:
            flash("Invalid status requested.", 'danger')
            return redirect(request.referrer or url_for('index'))

        db = get_db()
        task = db.execute("SELECT title FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            flash("Task not found.", 'danger')
            return redirect(request.referrer or url_for('index'))

        db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        db.commit()

        flash(f"Status for '{task['title']}' changed to {new_status}.", 'success')
        return redirect(request.referrer or url_for('index'))

    @app.route('/tasks/<int:task_id>/delete', methods=['POST'])
    def delete_task(task_id):
        """Delete task with confirmation."""
        db = get_db()
        task = db.execute("SELECT title FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            flash("Task not found.", 'danger')
            return redirect(request.referrer or url_for('index'))

        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()

        flash(f"Task '{task['title']}' was deleted.", 'info')
        return redirect(request.referrer or url_for('index'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
