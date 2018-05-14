#!/usr/bin/env python3

import logging
import os

import humanfriendly
import pandas
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)


def main(document_id):
    fb_pages_spreadsheet = f"https://docs.google.com/spreadsheets/d/{document_id}/export?format=csv"
    all_pages = pandas.read_csv(fb_pages_spreadsheet)

    # Remove pages without a 'Page ID'
    pages = all_pages["Page ID"].dropna()

    # The page_id column is the primary key linking the input and likes tables
    all_pages.rename(columns={"Page ID": "page_id"}, inplace=True)

    # Replace spaces with underscores in column names
    cols = all_pages.columns
    cols = cols.map(lambda x: x.replace(" ", "_") if isinstance(x, (str, bytes)) else x)
    all_pages.columns = cols

    data = []

    for page in pages:
        try:
            site = requests.get(f"https://facebook.com/pg/{page}/community")
            doc = BeautifulSoup(site.text, "html.parser")
            num_likes = humanfriendly.parse_size(
                doc.find_all(text="Total Likes")[0].parent.previous.replace(",", "")
            )
            data.append(
                {"page_id": page, "likes": num_likes, "time": pandas.Timestamp.now()}
            )
            logger.info("Success on %s with %d likes", page, num_likes)
        except IndexError:
            logger.warning("Errored on %s", page)

    df = pandas.DataFrame.from_records(data)
    # Use datetime stamp as index
    df.set_index("time", inplace=True)
    # Append data to existing dataset
    df.to_hdf("likes_data.h5", "Army4", format="table", append=True)


if __name__ == "__main__":
    default_doc_id = "1WsobPIzZRRGompWYk3dPEzanlicFTwUaqRBIB5iUOVU"
    document_id = os.environ.get("DOCUMENT_ID", default_doc_id)
    main(document_id)
