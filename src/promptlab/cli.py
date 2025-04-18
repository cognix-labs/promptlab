import click
import json
from promptlab.core import PromptLab
from promptlab.studio.studio import StudioServer


@click.group()
def cli():
    """PromptTrace CLI tool for experiment tracking and visualization"""
    pass


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to experiment configuration JSON file",
)
@click.option(
    "--tracer",
    "-t",
    type=click.Path(exists=True),
    required=True,
    help="Path to tracer configuration JSON file",
)
def run(config, tracer):
    """Run a PromptTrace experiment using configuration files"""
    try:
        # Load configurations
        with open(config) as f:
            experiment_config = json.load(f)
        with open(tracer) as f:
            tracer_config = json.load(f)

        # Initialize and run
        prompt_trace = PromptLab(tracer_config)
        prompt_trace.run(experiment_config)

        click.echo("Experiment completed successfully")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    "--db-dir",
    "-d",
    type=click.Path(exists=True),
    required=True,
    help="Directory containing trace files and database",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=8000,
    help="Port number for the web server (API will use port+1)",
)
def dashboard(db_dir, port):
    """Start the PromptTrace dashboard web server"""
    try:
        studio_config = {"db_server": db_dir, "port": port}
        studio_config = json.dumps(studio_config)
        server = StudioServer(studio_config)
        server.start()

        click.echo(f"Starting dashboard at http://localhost:{port}")
        click.echo(f"API running at http://localhost:{port + 1}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
