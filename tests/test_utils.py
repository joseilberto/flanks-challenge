"""Setting up variables and methods to help us perform our tests"""

import codecs
from pathlib import Path

# Here are some variables we need
ATTEMPTS = "3"
ATTEMPT_WAIT = "5"
DB_NAME = "LOCAL_TEST"
DELAY = "1"
INITIAL_URL = "https://localhost/test_url/"
MONGO_HOST = "127.0.0.1"
MONGO_PORT = "27017"
TEST_CRAWLER = "CNMV"

# Sample listing page
sample_listing_path = (
    Path(__file__).resolve().parent / "test_sample_data" / "list_page.html"
)
with codecs.open(sample_listing_path, "r", "utf-8") as sample_file:
    SAMPLE_LISTING = sample_file.read()

# Sample entry page 1
sample_entry_path = (
    Path(__file__).resolve().parent / "test_sample_data" / "entry1.html"
)
with codecs.open(sample_entry_path, "r", "utf-8") as entry_file:
    SAMPLE_ENTRY1 = entry_file.read()

# Sample entry page 2
sample_entry_path = (
    Path(__file__).resolve().parent / "test_sample_data" / "entry2.html"
)
with codecs.open(sample_entry_path, "r", "utf-8") as entry_file:
    SAMPLE_ENTRY2 = entry_file.read()
