import os
from pathlib import Path

from promptlab.enums import TracerType
from promptlab.types import ExperimentConfig, TracerConfig


class ConfigValidator:
    @staticmethod
    def validate_experiment_config(experiment_config: ExperimentConfig):
        # ConfigValidator.validate_prompt_template(experiment_config.prompt_template.name)
        ConfigValidator.validate_dataset(experiment_config.dataset.name)

    @staticmethod
    def validate_db_file_exists(db_file: str) -> None:
        if not isinstance(db_file, str):
            raise ValueError(
                f"Database file path must be a string, got {type(db_file)}"
            )

        try:
            path = Path(db_file)

            # Check if file exists
            if path.exists():
                if not path.is_file():
                    raise ValueError(f"Path exists but is not a file: {db_file}")
                if not os.access(path, os.W_OK):
                    raise ValueError(
                        f"Database file exists but is not writable: {db_file}"
                    )
            else:
                # If file doesn't exist, check if parent directory exists and is writable
                parent_dir = path.parent
                if not parent_dir.exists():
                    raise ValueError(f"Parent directory does not exist: {parent_dir}")
                if not os.access(parent_dir, os.W_OK):
                    raise ValueError(f"Parent directory is not writable: {parent_dir}")

        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Invalid database file path: {str(e)}")

    @staticmethod
    def validate_prompt_template(name: str) -> None:
        if not isinstance(name, str):
            raise ValueError(f"Name must be a string, got {type(name)}")

    @staticmethod
    def validate_dataset(name: str) -> None:
        if not isinstance(name, str):
            raise ValueError(f"Name must be a string, got {type(name)}")
