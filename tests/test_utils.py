"""Setting up variables and methods to help us perform our tests"""

import codecs
from pathlib import Path

from src.crawler.pipelines import DataTypes

# Here are some variables we need
ATTEMPTS = "3"
ATTEMPT_WAIT = "0"
DB_NAME = "LOCAL_TEST"
DELAY = "1"
INITIAL_URL = "https://localhost/test_url/"
MONGO_HOST = "127.0.0.1"
MONGO_PORT = "27017"
TEST_CRAWLER = "CNMV"

# Define the results of the first entry page
ENTRY_PAGE1 = DataTypes(
    "SICAV TEST",
    "1",
    "2000-01-01",
    "ES0000000000",
    "Calle TEST, 20",
    1000000.0,
    10000000.0,
    "2023-01-01",
)

sample_test_folder = Path(__file__).resolve().parent / "test_sample_data"
sample_files = {
    "success_list_page": sample_test_folder / "list_page.html",
    "empty_list_page": sample_test_folder / "list_page_empty.html",
    "no_pagination_list_page": (
        sample_test_folder / "list_page_no_pagination.html"
    ),
    "no_current_page_list_page": (
        sample_test_folder / "list_page_no_current_page.html"
    ),
    "no_next_page_list_page": (
        sample_test_folder / "list_page_no_next_page.html"
    ),
    "no_urls_list_list_page": (
        sample_test_folder / "list_page_no_urls_list.html"
    ),
    "empty_urls_list_list_page": (
        sample_test_folder / "list_page_empty_urls_list.html"
    ),
    "success_entry1": sample_test_folder / "entry1.html",
    "success_entry2": sample_test_folder / "entry2.html",
}

SAMPLE_FILES = {}
for file_type, file_path in sample_files.items():
    with codecs.open(file_path, "r", "utf-8") as sample_file:
        SAMPLE_FILES[file_type] = sample_file.read()
