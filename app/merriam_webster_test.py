#!/usr/bin/python3
import warnings
import pytest
import logging
from merriam_webster import MerriamWebsterAPI

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
warnings.filterwarnings(
    "ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+"
    )

# Initialize the API client for testing
BASE_PATH = "/Users/rishabh.gupta01/Desktop/Merriam-Webster"
test_client = MerriamWebsterAPI(BASE_PATH)


def test_fetch_definition():
    """Test cases for the MerriamWebsterAPI.fetch_definition method."""
    # Test with a valid word
    assert test_client.fetch_definition("hospital") == (
        "hospital (noun): a charitable institution for the needy, aged, infirm, or young"
    )

    # Test with a nonexistent word
    assert test_client.fetch_definition("nonexistentword") == "Word not found"

    # Test with invalid input (numeric characters)
    with pytest.raises(ValueError, match="The word must contain only alphabetic characters."):
        test_client.fetch_definition("12345")

    # Test with an empty string
    with pytest.raises(ValueError, match="The word must contain only alphabetic characters."):
        test_client.fetch_definition("")

    logging.info("All test cases passed.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(" Testing MerriamWebsterAPI.fetch_definition method")
    pytest.main(["-v", __file__])
    logging.info("Tests completed.")
    logging.shutdown()
    print("Tests completed successfully.")
# Add a blank line here
