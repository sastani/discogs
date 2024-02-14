import os
import datetime

def main():
    url_path = 'https://discogs-data-dumps.s3.us-west-2.amazonaws.com/index.html?prefix=data/'
    download_files()


# get in-network files from index file that need to be processed and download them
def download_files():
    reporting_month = get_date()
    checksum_file_name = "discogs_" + reporting_month.strftime('%Y%m') + "01" + "_CHECKSUM.txt"
    f = open(os.getcwd() + "/" + checksum_file_name)
    for line in f:
        line = line.split()
        checksum = line[0]
        resource = line[1]
    #write checksum and resource to dataframe

def get_date():
    curr_date_time = datetime.now()
    return curr_date_time

if __name__ == '__main__':
    main()