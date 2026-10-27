"""
Student Task Management System
A lightweight, beginner-friendly Flask and SQLite web application.
"""

import os
import sqlite3
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    g
)

# Valid choice definitions for robust server-side validation
VALID_PRIORITIES = ['Low', 'Medium', 'High']
VALID_STATUSES = ['Pending', 'In Progress', 'Completed']


def get_db_path(app):
    """Return database file path from app configuration."""
    return app.config.get('DATABASE', os.path.join(app.instance_path, 'tasks.db'))


def get_db(app=None):
    """
    Open a database connection for the current request context.
    Uses sqlite3.Row for dict-like access to columns.
    """
    if 'db' not in g:
        from flask import current_app
        active_app = app or current_app
        db_path = get_db_path(active_app)
        
        # Ensure parent directory exists for SQLite file
        if db_path != ':memory:':
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        # Enable foreign keys support in SQLite
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables if they do not already exist."""
    db_path = get_db_path(app)
    if db_path != ':memory:':
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium',
                due_date TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.close()


def create_app(test_config=None):
    """
    Application factory pattern.
    Allows easy creation of application instances for production and testing.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='student-task-manager-dev-key',
        DATABASE=os.path.join(app.instance_path, 'tasks.db'),
    )

    if test_config is not None:
        app.config.update(test_config)

    # Register teardown function to close db connection
    app.teardown_appcontext(close_db)

    # Initialize the database table
    init_db(app)

    # -------------------------------------------------------------
    # ROUTES
    # -------------------------------------------------------------

    @app.route('/')
    def index():
        """
        Dashboard and Task Listing:
        - Calculates metrics: Total, Pending, In Progress, Completed
        - Supports filtering by status and priority
        """
        db = get_db()

        # 1. Calculate dashboard metrics
        stats_cursor = db.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
            FROM tasks;
        """)
        stats_row = stats_cursor.fetchone()
        stats = {
            'total': stats_row['total'] or 0,
            'pending': stats_row['pending'] or 0,
            'in_progress': stats_row['in_progress'] or 0,
            'completed': stats_row['completed'] or 0
        }

        # 2. Get filters from query parameters
        status_filter = request.args.get('status', '').strip()
        priority_filter = request.args.get('priority', '').strip()

        # 3. Build dynamic filtered query using safe parameterization
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if status_filter in VALID_STATUSES:
            query += " AND status = ?"
            params.append(status_filter)

        if priority_filter in VALID_PRIORITIES:
            query += " AND priority = ?"
            params.append(priority_filter)

        query += " ORDER BY id DESC"

        tasks = db.execute(query, params).fetchall()

        return render_template(
            'index.html',
            tasks=tasks,
            stats=stats,
            selected_status=status_filter,
            selected_priority=priority_filter,
            valid_statuses=VALID_STATUSES,
            valid_priorities=VALID_PRIORITIES
        )

    @app.route('/tasks/new', methods=['GET', 'POST'])
    def add_task():
        """Create a new task with validation."""
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            priority = request.form.get('priority', 'Medium').strip()
            due_date = request.form.get('due_date', '').strip()
            status = request.form.get('status', 'Pending').strip()

            # Server-side validation
            errors = []
            if not title:
                errors.append("Task title is required.")
            elif len(title) > 150:
                errors.append("Task title cannot exceed 150 characters.")

            if priority not in VALID_PRIORITIES:
                errors.append(f"Invalid priority. Choose from: {', '.join(VALID_PRIORITIES)}")

            if status not in VALID_STATUSES:
                errors.append(f"Invalid status. Choose from: {', '.join(VALID_STATUSES)}")

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
                    description=description,
                    priority=priority,
                    due_date=due_date,
                    status=status,
                    valid_statuses=VALID_STATUSES,
                    valid_priorities=VALID_PRIORITIES
                ), 400

            # Safe parameterized insert
            db = get_db()
            db.execute(
                """
                INSERT INTO tasks (title, description, priority, due_date, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, description, priority, due_date if due_date else None, status)
            )
            db.commit()

            flash(f"Task '{title}' created successfully!", 'success')
            return redirect(url_for('index'))

        return render_template(
            'add_task.html',
            valid_statuses=VALID_STATUSES,
            valid_priorities=VALID_PRIORITIES
        )

    @app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    def edit_task(task_id):
        """Edit an existing task."""
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

        if task is None:
            flash(f"Task #{task_id} not found.", 'danger')
            return redirect(url_for('index'))

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
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
                errors.append(f"Invalid priority. Choose from: {', '.join(VALID_PRIORITIES)}")

            if status not in VALID_STATUSES:
                errors.append(f"Invalid status. Choose from: {', '.join(VALID_STATUSES)}")

            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    errors.append("Due date must be in YYYY-MM-DD format.")

            if errors:
                for err in errors:
                    flash(err, 'danger')
                return render_template(
                    'edit_task.html',
                    task=task,
                    valid_statuses=VALID_STATUSES,
                    valid_priorities=VALID_PRIORITIES
                ), 400

            db.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, priority = ?, due_date = ?, status = ?
                WHERE id = ?
                """,
                (title, description, priority, due_date if due_date else None, status, task_id)
            )
            db.commit()

            flash(f"Task #{task_id} updated successfully!", 'success')
            return redirect(url_for('index'))

        return render_template(
            'edit_task.html',
            task=task,
            valid_statuses=VALID_STATUSES,
            valid_priorities=VALID_PRIORITIES
        )

    @app.route('/tasks/<int:task_id>/status', methods=['POST'])
    def update_status(task_id):
        """Quick status change directly from task list."""
        new_status = request.form.get('status', '').strip()
        if new_status not in VALID_STATUSES:
            flash("Invalid status update requested.", 'danger')
            return redirect(url_for('index'))

        db = get_db()
        task = db.execute("SELECT title FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            flash(f"Task #{task_id} not found.", 'danger')
            return redirect(url_for('index'))

        db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        db.commit()

        flash(f"Status for '{task['title']}' changed to {new_status}.", 'success')
        return redirect(url_for('index'))

    @app.route('/tasks/<int:task_id>/delete', methods=['POST'])
    def delete_task(task_id):
        """Delete a task by ID."""
        db = get_db()
        task = db.execute("SELECT title FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            flash(f"Task #{task_id} not found.", 'danger')
            return redirect(url_for('index'))

        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()

        flash(f"Task '{task['title']}' was deleted.", 'info')
        return redirect(url_for('index'))

    return app


# Main entry point for local execution
if __name__ == '__main__':
    app = create_app()
    # Host 0.0.0.0 enables access from local network and inside Docker containers
    app.run(host='0.0.0.0', port=5000, debug=True)
