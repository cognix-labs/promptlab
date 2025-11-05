import asyncio
import click
from promptlab.core import PromptLab


@click.group()
def promptlab():
    """PromptLab CLI-Tool für Experiment-Tracking und -Visualisierung"""
    pass


@promptlab.group()
def studio():
    """Studio-bezogene Befehle"""
    pass


@studio.command()
@click.option("-d", "--db", required=True, help="Pfad zur SQLite-Datei")
@click.option(
    "-p", "--port", default=8000, show_default=True, help="Port, auf dem das Studio läuft"
)
def start(db, port):
    """Studio-Server starten"""

    click.echo(f"Starte Studio mit Datenbank: {db}")

    tracer_config = {"type": "local", "db_file": db}
    pl = PromptLab(tracer_config)
    asyncio.run(pl.studio.start_async(port))

    click.echo(f"Läuft auf Port: {port}")


@promptlab.group()
def db():
    """Datenbankverwaltungsbefehle"""
    pass


@db.command()
@click.option("-d", "--db", required=True, help="Pfad zur SQLite-Datei")
def init(db):
    """Datenbank initialisieren"""
    from promptlab.sqlite.database_manager import db_manager

    click.echo(f"Initialisiere Datenbank: {db}")
    db_manager.initialize_database(db)
    click.echo("Datenbank erfolgreich initialisiert!")


@db.command()
@click.option("-d", "--db", required=True, help="Pfad zur SQLite-Datei")
def migrate(db):
    """Datenbankmigrationen ausführen"""
    from promptlab.sqlite.database_manager import db_manager

    click.echo(f"Führe Migrationen für Datenbank aus: {db}")
    db_manager.initialize_database(db)  # This includes running migrations
    click.echo("Migrationen erfolgreich abgeschlossen!")


@db.command()
@click.option("-d", "--db", required=True, help="Pfad zur SQLite-Datei")
@click.option("-m", "--message", required=True, help="Migrationsnachricht")
def revision(db, message):
    """Neue Migrationsrevision erstellen"""
    try:
        from alembic.config import Config
        from alembic import command
        from pathlib import Path

        # Get the alembic.ini from within the package
        package_root = Path(__file__).parent
        alembic_cfg_path = package_root / "alembic.ini"

        if not alembic_cfg_path.exists():
            click.echo("Fehler: Alembic-Konfiguration nicht gefunden", err=True)
            return

        # Configure Alembic
        alembic_cfg = Config(str(alembic_cfg_path))
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db}")

        click.echo(f"Erstelle Migrationsrevision: {message}")
        command.revision(alembic_cfg, message=message, autogenerate=True)
        click.echo("Migrationsrevision erfolgreich erstellt!")

    except ImportError:
        click.echo("Fehler: Alembic nicht installiert", err=True)
    except Exception as e:
        click.echo(f"Fehler beim Erstellen der Migration: {e}", err=True)


if __name__ == "__main__":
    promptlab()
