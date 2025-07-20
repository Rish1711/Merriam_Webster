#!/usr/bin/python3
import requests
import os
import argparse
from configparser import ConfigParser
import logging
from logging.handlers import RotatingFileHandler
import warnings
warnings.filterwarnings(
    "ignore", category=UserWarning, module="urllib3"
    )
warnings.filterwarnings(
    "ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+"
    )


class MerriamWebsterAPI:
    def __init__(self, BASE_PATH):
        """
        Initialize the Merriam-Webster API client.
        Args:
            base_path (str): Base path of the project directory.
        """
        self.base_path = BASE_PATH
        self.config_path = f"{self.base_path}/conf/config.ini"
        self.configsecrets_path = f"{self.base_path}/conf/configsecrets.ini"
        self._setup_logging()
        self._load_config()

    def _setup_logging(self):
        """Set up logging for the application."""
        logs_dir = os.path.join(self.base_path, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_file = f"{self.base_path}/logs/merriam_webster.log"
        logging.basicConfig(level=logging.INFO)
        handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
            )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
            )
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

    def _load_config(self):
        """Load configuration from the config file."""
        config = ConfigParser()
        config.read([self.config_path, self.configsecrets_path])

        self.api_key = config.get("merriam-webster", "api_key", fallback=None)
        if not self.api_key:
            logging.error("API key is missing in the configuration file.")
            raise ValueError(
                "API key is missing in the configuration file."
                )
        else:
            logging.debug("API key loaded successfully.")

        self.base_url = config.get(
            "merriam-webster", "base_url", fallback=None
            )
        if not self.base_url:
            logging.error("Base URL is missing in the configuration file.")
            raise ValueError(
                "Base URL is missing in the configuration file."
                )

    def fetch_definition(self, word):
        """
        Fetch the definition of a word from the Merriam-Webster Dictionary API.
        Args:
            word (str): The word to look up.
        Returns:
            str: A formatted string with the word's part of
            speech and first definition,
            or an error message if not found.
        """
        try:
            # Validate the word input
            if not word.isalpha():
                logging.error("Invalid word input: %s", word)
                raise ValueError(
                    "The word must contain only alphabetic characters."
                    )

            # Construct the full API URL
            url = f"{self.base_url}/{word}?key={self.api_key}"
            logging.info(
                f"Fetching definition for word: {word} from URL: {url}"
                )

            # Send GET request to the API
            response = requests.get(url)
            response.raise_for_status()
            logging.info(
                "Received response for word: %s with status code: %d",
                word,
                response.status_code,
                )

            # Parse the JSON response
            data = response.json()
            print(f"Response content: {data}")  # Debugging output

            # If valid response and definitions are found
            # If the response is a list but does not contain valid definitions
            if isinstance(
                data, list) and (
                    not data or isinstance(data[0], str)
                    ):
                logging.warning(f"No definitions found for word: {word}")
                return "Word not found"

            # If valid response and definitions are found
            if isinstance(data, list) and isinstance(data[0], dict):
                fl = data[0].get("fl", "N/A")
                shortdef = data[0].get("shortdef", ["No definition found"])[0]
                return f"{word} ({fl}): {shortdef}"
            else:
                logging.warning(f"No definitions found for word: {word}")
                return "Word not found"
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return "Error fetching definition"


def main():
    """
    Parses command-line arguments and
    prints the definition of the provided word.
    """
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Dictionary CLI Tool")
    parser.add_argument("word", help="Word to look up")
    args = parser.parse_args()

    # Initialize the Merriam-Webster API client
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"Base path: {BASE_PATH}")  # Debugging output
    logging.info(f"Base path: {BASE_PATH}")
    api_client = MerriamWebsterAPI(BASE_PATH)

    # Fetch and print the definition
    print(api_client.fetch_definition(args.word))


# Run main function when script is executed
if __name__ == "__main__":
    main()
