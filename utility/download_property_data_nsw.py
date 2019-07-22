#!/usr/env/bin python3

"""Main program to download NSW property sales data."""

import os

import download_manager


def get_priperty_data(download_folder: str) -> None:
    """Dowlload data from NSW property site."""
    url = R'https://valuation.property.nsw.gov.au' \
          R'/embed/propertySalesInformation'
    download_url_list = download_manager.get_download_link(url, '.zip')
    if download_url_list:
        for download_url in download_url_list:
            download_path = download_folder + '\\' + \
                str(download_url).split('/')[-1]
            if not os.path.exists(download_path):
                try:
                    download_manager.download_file(download_url, download_path)
                except download_manager.DownloadLinkErr as dwerr:
                    print(F'Download error: "{dwerr}"')
                except FileExistsError as error:
                    print('File already exist :', error)
            else:
                print('file already exist : ', download_path)
    else:
        print('No download link found at given url : ', url)


if __name__ == '__main__':
    FOLDER = R'C:\temp\NSWHoseSaleData\TEST'
    get_priperty_data(FOLDER)
