#!/usr/bin/env python3
"""
Database migration utility script for OAuth SaaS Backend.

This script provides convenient commands for managing database migrations.
"""

import sys
import subprocess
from pathlib import Path


def run_command(command: str) -> int:
    """Run a shell command and return the exit code."""
    print(f"Running: {command}")
    return subprocess.run(command.split(), cwd=Path(__file__).parent).returncode


def create_migration(message: str) -> int:
    """Create a new migration with autogenerate."""
    return run_command(f'alembic revision --autogenerate -m "{message}"')


def upgrade_database(revision: str = "head") -> int:
    """Upgrade database to a specific revision (default: head)."""
    return run_command(f"alembic upgrade {revision}")


def downgrade_database(revision: str) -> int:
    """Downgrade database to a specific revision."""
    return run_command(f"alembic downgrade {revision}")


def show_current() -> int:
    """Show current migration revision."""
    return run_command("alembic current")


def show_history() -> int:
    """Show migration history."""
    return run_command("alembic history --verbose")


def check_migrations() -> int:
    """Check for pending migrations."""
    return run_command("alembic check")


def show_help():
    """Show help message."""
    help_text = """
Database Migration Utility

Usage: python migrate.py <command> [arguments]

Commands:
    create <message>        Create a new migration with the given message
    upgrade [revision]      Upgrade to head (or specific revision)
    downgrade <revision>    Downgrade to specific revision
    current                 Show current migration revision
    history                 Show migration history
    check                   Check for pending migrations
    help                    Show this help message

Examples:
    python migrate.py create "add user profile fields"
    python migrate.py upgrade
    python migrate.py upgrade +1
    python migrate.py downgrade -1
    python migrate.py current
    python migrate.py history
    python migrate.py check
"""
    print(help_text)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return 1

    command = sys.argv[1].lower()

    try:
        if command == "create":
            if len(sys.argv) < 3:
                print("Error: Migration message required")
                print("Usage: python migrate.py create <message>")
                return 1
            message = " ".join(sys.argv[2:])
            return create_migration(message)

        elif command == "upgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            return upgrade_database(revision)

        elif command == "downgrade":
            if len(sys.argv) < 3:
                print("Error: Revision required for downgrade")
                print("Usage: python migrate.py downgrade <revision>")
                return 1
            revision = sys.argv[2]
            return downgrade_database(revision)

        elif command == "current":
            return show_current()

        elif command == "history":
            return show_history()

        elif command == "check":
            return check_migrations()

        elif command in ["help", "-h", "--help"]:
            show_help()
            return 0

        else:
            print(f"Error: Unknown command '{command}'")
            show_help()
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
