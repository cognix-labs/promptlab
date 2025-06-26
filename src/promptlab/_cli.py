import asyncio
import click
from promptlab.core import PromptLab


@click.group()
def promptlab():
    """PromptLab CLI tool for experiment tracking and visualization"""
    pass


@promptlab.group()
def studio():
    """Studio related commands"""
    pass


@studio.command()
@click.option("-d", "--db", required=True, help="Path to the SQLite file")
@click.option(
    "-p", "--port", default=8000, show_default=True, help="Port to run the Studio on"
)
def start(db, port):
    """Start the studio server"""

    click.echo(f"Starting studio with database: {db}")

    tracer_config = {"type": "local", "db_file": db}
    pl = PromptLab(tracer_config)
    asyncio.run(pl.studio.start_async(port))

    click.echo(f"Running on port: {port}")


if __name__ == "__main__":
    promptlab()
