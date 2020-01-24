# AIzaSyBco2Cb9AikTpq74k70LyrJNBWDz9fQk9I

# 014265856113199739783:ik1fgtrafyo

from googleapiclient.discovery import build
import json
from fuzzywuzzy import fuzz
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import requests
import sys

from bs4 import BeautifulSoup

from urllib.request import urlretrieve

my_api_key = "AIzaSyBco2Cb9AikTpq74k70LyrJNBWDz9fQk9I"
my_cse_id = "014265856113199739783:ik1fgtrafyo"


# content = """
# NBA operates on an online system of accreditation called "Accreditation Workflow Management System (AWMS), which includes institution registration.
# """

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def web_scrape(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser').text
    return soup


def match_content(Str1, Str2):
    partial_Ratio = fuzz.partial_ratio(Str1.lower(), Str2.lower())
    # Ratio = fuzz.ratio(Str1.lower(),Str2.lower())

    return partial_Ratio


def check_plagiarism(scrapped, link):
    return match_content(content, scrapped)

    # if(match_percentage > 30):
    #     print("Bro gotcha! {} percent copied from {}. What is this behaviour?".format(match_percentage, link))


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def mainEngine(content):
    result = google_search(content, my_api_key, my_cse_id)
    data = json.loads(json.dumps(result))
    highest_percentage = 0;
    ans = ""
    for item in data['items']:
        if (item['link'].find('.pdf') > 0):
            try:
                urlretrieve(item['link'], "download.pdf")
                scrapped_content = convert_pdf_to_txt("download.pdf");
                match_content(content, scrapped_content)
                # check_plagiarism(scrapped_content, item['link'])
            except:
                print("")
            continue

        scrapped_content = web_scrape(item['link'])
        match_percentage = match_content(content, scrapped_content)

        if match_percentage > highest_percentage:
            highest_percentage = match_percentage
        ans += "{}% of content was copied from {}\n <br>".format(match_percentage, item['link'])

    ans += "<br> \nHighest Plagiarism Percentage: {}%".format(highest_percentage)

    if highest_percentage >= 70:
        ans += "<br> \nSorry but your paper is rejected due to high plagiarism. Please try again later."
    else:
        ans += "<br> \nCongratulations your paper has been successfully accepted!"
    return ans


# content = str(input())
# print(mainEngine(content))

# scrapped_content = web_scrape("https://en.wikipedia.org/wiki/Michael_Madana_Kama_Rajan")
# match_content(content, scrapped_content)
