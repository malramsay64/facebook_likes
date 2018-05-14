#!/usr/bin/env python3

import os

import altair as alt
import pandas
import requests


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

    # Read in the likes data
    df2 = pandas.read_hdf("likes_data.h5", "Army4")
    # Reduce granularity to each day, taking the maximum likes from that day
    df2 = df2.groupby("page_id").resample("H").max()
    df2 = df2.reset_index(level="time").reset_index(drop=True)
    # Remove entries with no data
    df2.dropna(axis=0, inplace=True)

    # Merge the unit data and the likes data
    plot_df = df2.merge(all_pages, on="page_id")

    chart = alt.Chart(plot_df).mark_line().encode(
        x="time", y=alt.Y("likes", scale=alt.Scale(zero=False)), color="Unit"
    )
    chart.save("all_likes.html")

    chart = alt.Chart(plot_df.query('REG_or_RES == "RESERVE"')).mark_line().encode(
        x="time", y=alt.Y("likes", scale=alt.Scale(zero=False)), color="Unit"
    )
    chart.save("reserve_likes.html")

    chart = alt.Chart(plot_df.query('page_id == "thelancerband"')).mark_line().encode(
        x="time", y=alt.Y("likes", scale=alt.Scale(zero=False)), color="Unit"
    )
    chart.save("lancerband_likes.html")


if __name__ == "__main__":
    default_doc_id = "1WsobPIzZRRGompWYk3dPEzanlicFTwUaqRBIB5iUOVU"
    document_id = os.environ.get("DOCUMENT_ID", default_doc_id)
    main(document_id)
