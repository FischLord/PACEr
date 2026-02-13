"""
Einmaliges Migrationsskript: JSON-Daten -> SQLite
Migriert Reports aus PACEr/reports/ und Stats aus stats.json in die Datenbank.
"""
import os
import json
from datetime import datetime, date
from app import create_app
from models import db, Report, UsageStatistic


def migrate_reports(base_path):
    """Migriert JSON-Reports aus dem reports-Verzeichnis in die DB."""
    reports_path = os.path.join(base_path, 'reports')
    if not os.path.exists(reports_path):
        print("Kein reports-Verzeichnis gefunden, ueberspringe...")
        return

    count = 0
    for date_folder in sorted(os.listdir(reports_path)):
        folder_path = os.path.join(reports_path, date_folder)
        if not os.path.isdir(folder_path):
            continue

        # Parse date from folder name (DD.MM.YYYY)
        try:
            report_date = datetime.strptime(date_folder, "%d.%m.%Y")
        except ValueError:
            print(f"  Ueberspringe ungültigen Ordner: {date_folder}")
            continue

        for filename in sorted(os.listdir(folder_path)):
            if not filename.endswith('.json'):
                continue

            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)

                report = Report(
                    name=data.get('Name', ''),
                    vorname=data.get('Vorname', ''),
                    email=data.get('Email', ''),
                    issue=data.get('Issue', ''),
                    created_at=report_date,
                )
                db.session.add(report)
                count += 1
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  Fehler bei {filepath}: {e}")

    db.session.commit()
    print(f"  {count} Reports migriert.")


def migrate_stats(base_path):
    """Migriert stats.json in die DB."""
    stats_path = os.path.join(base_path, 'stats.json')
    if not os.path.exists(stats_path):
        print("Keine stats.json gefunden, ueberspringe...")
        return

    count = 0
    with open(stats_path, 'r') as f:
        data = json.load(f)

    for date_str, usage_count in data.items():
        try:
            stat_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"  Ueberspringe ungueltiges Datum: {date_str}")
            continue

        stat = UsageStatistic(date=stat_date, count=usage_count)
        db.session.add(stat)
        count += 1

    db.session.commit()
    print(f"  {count} Statistik-Eintraege migriert.")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        base_path = os.path.dirname(os.path.abspath(__file__))

        print("Starte Migration...")
        print("\n1. Reports migrieren:")
        migrate_reports(base_path)

        print("\n2. Statistiken migrieren:")
        migrate_stats(base_path)

        print("\nMigration abgeschlossen!")
