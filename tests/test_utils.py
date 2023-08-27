"""Setting up variables and methods to help us perform our tests"""

import codecs
from pathlib import Path

# Here are some variables we need
ATTEMPTS = "3"
ATTEMPT_WAIT = "0"
DB_NAME = "LOCAL_TEST"
DELAY = "1"
INITIAL_URL = "https://localhost/test_url/"
MONGO_HOST = "127.0.0.1"
MONGO_PORT = "27017"
TEST_CRAWLER = "CNMV"

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
    "success_entry1": sample_test_folder / "entry1.html",
    "success_entry2": sample_test_folder / "entry2.html",
}

SAMPLE_FILES = {}
for file_type, file_path in sample_files.items():
    with codecs.open(file_path, "r", "utf-8") as sample_file:
        SAMPLE_FILES[file_type] = sample_file.read()
