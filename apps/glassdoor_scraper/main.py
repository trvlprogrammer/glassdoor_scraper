# Import necessary libraries
# standard libraries
import argparse
import json
import os
import sys
from os.path import exists
from datetime import datetime
from time import time
import csv
# 3rd-party libraries
# custom functions
from apps.glassdoor_scraper.packages.common import requestAndParse
from apps.glassdoor_scraper.packages.page import extract_maximums, extract_listings
from apps.glassdoor_scraper.packages.listing import extract_listing, extract_listing_dict


class glassdoor_scraper():    
    def scrape(self, base_url, target_num):

        maxJobs, maxPages = extract_maximums(base_url)
        if (target_num >= maxJobs):
            print("[ERROR] Target number larger than maximum number of jobs. Exiting program...\n")
            os._exit(0)
        page_index = 1
        total_listingCount = 0

        # initialises prev_url as base_url
        prev_url = base_url

        while total_listingCount <= target_num:
            # clean up buffer
            list_returnedTuple = []

            new_url = self.update_url(prev_url, page_index)
            page_soup,_ = requestAndParse(new_url)
            listings_set, jobCount = extract_listings(page_soup)

            for listing_url in listings_set:
                return_json = extract_listing_dict(listing_url)
                list_returnedTuple.append(return_json)

            # done with page, moving onto next page
            print(list_returnedTuple)
            total_listingCount = total_listingCount + jobCount
            print("[INFO] Finished processing page index {}; Total number of jobs processed: {}".format(page_index, total_listingCount))
            page_index = page_index + 1
            prev_url = new_url

        return list_returnedTuple
   
            # loads user defined parameters
    def load_configs(self, path):
        with open(path) as config_file:
            configurations = json.load(config_file)

        base_url = configurations['base_url']
        target_num = int(configurations["target_num"])
        return base_url, target_num


    # appends list of tuples in specified output csv file
    # a tuple is written as a single row in csv file 
    def fileWriter(self, listOfTuples, output_fileName):
        with open(output_fileName,'a', newline='') as out:
            csv_out=csv.writer(out)
            for row_tuple in listOfTuples:
                try:
                    csv_out.writerow(row_tuple)
                    # can also do csv_out.writerows(data) instead of the for loop
                except Exception as e:
                    print("[WARN] In filewriter: {}".format(e))


    # updates url according to the page_index desired
    def update_url(self, prev_url, page_index):
        if page_index == 1:
            prev_substring = ".htm"
            new_substring = "_IP" + str(page_index) + ".htm"
        else:
            prev_substring = "_IP" + str(page_index - 1) + ".htm"
            new_substring = "_IP" + str(page_index) + ".htm"

        new_url = prev_url.replace(prev_substring, new_substring)
        return new_url

if __name__ == "__main__":
    glassdoor_scraper( 
        configfile=None,
        baseurl="https://www.glassdoor.com/Job/seattle-software-engineer-jobs-SRCH_IL.0,7_IC1150505_KO8,25.htm?clickSource=searchBox",
        targetnum=75
        )