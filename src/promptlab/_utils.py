import json
import os
import re
import threading
from typing import Dict, List, Tuple

import nltk


class Utils:
    _nltk_data_download_lock = threading.Lock()

    @staticmethod
    def sanitize_path(value: str) -> str:
        if any(char in value for char in '<>"|?*'):
            raise ValueError("Invalid characters in file path")

        if not value:
            raise ValueError("File path cannot be empty")

        value = os.path.normpath(value.replace("\t", "\\t"))

        return value

    @staticmethod
    def load_dataset(dataset_path: str) -> List[Dict]:
        dataset_path = Utils.sanitize_path(dataset_path)

        dataset = []
        with open(dataset_path, "r") as file:
            for line in file:
                dataset.append(json.loads(line.strip()))
        return dataset

    @staticmethod
    def split_prompt_template(asset: str) -> Tuple[str, str, List[str]]:
        if asset is None:
            return ("", "", [])

        pattern = r"<<system>>\s*(.*?)\s*<<user>>\s*(.*?)\s*(?=<<|$)"
        matches = re.findall(pattern, asset, re.DOTALL)

        if not matches:
            raise ValueError("No valid prompt format found in template")

        system_prompt = matches[0][0].strip()
        user_prompt = matches[0][1].strip()

        system_prompt_variables = re.findall(r"<(.*?)>", system_prompt)
        user_prompt_variables = re.findall(r"<(.*?)>", user_prompt)
        prompt_template_variables = system_prompt_variables + user_prompt_variables
        prompt_template_variables = list(set(prompt_template_variables))

        return system_prompt, user_prompt, prompt_template_variables

    @staticmethod
    def download_required_nltk_resources():
        """
        Ensure all required NLTK language processing resources are available locally.

        This method checks for the presence of necessary NLTK packages and
        downloads them if they're not already installed. Thread-safe implementation
        prevents multiple concurrent downloads of the same resources.
        """
        required_resources = [
            ("punkt", "tokenizers/punkt.zip"),
            ("punkt_tab", "tokenizers/punkt_tab.zip"),
        ]

        with Utils._nltk_data_download_lock:
            for package_name, resource_path in required_resources:
                try:
                    nltk.data.find(resource_path)
                except LookupError:
                    nltk.download(package_name)
                except Exception as e:
                    print(
                        f"Error checking/downloading NLTK resource {package_name}: {str(e)}"
                    )
