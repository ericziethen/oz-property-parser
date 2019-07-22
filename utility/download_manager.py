#!/usr/env/bin python3

"""Download manager which provides methods to download data."""

from typing import List

import requests
import bs4


class DownloadLinkErr(Exception):
    """Generic Exception to inform the User that download link error."""


def get_download_link(url: str, extn: str) -> List[str]:
    """Get list of all download links from given url and with given extn."""
    res = requests.get(url)
    # Handle redirecting if site is redirected due to an error accessing site
    temp_download_link_list = []
    if res.ok:
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        for tag in soup.find_all('a'):
            download_url = tag.get('href')
            if extn in download_url:
                temp_download_link_list.append(download_url)
    return temp_download_link_list


def download_file(url: str, file_path: str) -> None:
    """Download file from given link to the given file path."""
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise DownloadLinkErr(F'An Http Error occurred: "{errh}"')
    except requests.exceptions.ConnectionError as errc:
        raise DownloadLinkErr(F'An Error Connecting to the'
                              F'API occurred: "{errc}"')
    except requests.exceptions.Timeout as errt:
        raise DownloadLinkErr(F'A Timeout Error occurred: "{errt}"')
    except requests.exceptions.RequestException as err:
        raise DownloadLinkErr(F'An Unknown Error occurred: "{err}"')
    with open(file_path, 'xb') as file_pointer:
        file_pointer.write(res.content)


if __name__ == '__main__':
    URL_TEST = R'http://www.valuergeneral.nsw.gov.au/__psi/weekly/20190701.zip'
    FILE = R'C:\temp\NSWHoseSaleData\201907011.zip'
    try:
        download_file(URL_TEST, FILE)
    except DownloadLinkErr as dwerr:
        print(F'Download error: "{dwerr}"')
