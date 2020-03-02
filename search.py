# AIzaSyBco2Cb9AikTpq74k70LyrJNBWDz9fQk9I

# 014265856113199739783:ik1fgtrafyo

from googleapiclient.discovery import build
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from difflib import SequenceMatcher

import requests
import sys

from bs4 import BeautifulSoup

from urllib.request import urlretrieve

my_api_key = "AIzaSyBco2Cb9AikTpq74k70LyrJNBWDz9fQk9I"
my_cse_id = "014265856113199739783:ik1fgtrafyo"


content = """
NBA operates on an online system of accreditation called "Accreditation Workflow Management System (AWMS), which includes institution registration.
"""

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def web_scrape(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser').text
    return soup

def partial_ratio(s1, s2):
  """"Return the ratio of the most similar substring
  as a number between 0 and 100."""

  if len(s1) <= len(s2):
    shorter = s1
    longer = s2
  else:
    shorter = s2
    longer = s1

  m = SequenceMatcher(None, shorter, longer)
  blocks = m.get_matching_blocks()

  scores = []
  matched_blocks = []
  for block in blocks:
    long_start = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
    long_end = long_start + len(shorter)
    long_substr = longer[long_start:long_end]

    m2 = SequenceMatcher(None, shorter, long_substr)
    matched_blocks.append(m2.get_matching_blocks())

    r = m2.ratio()
    scores.append(r)
  
  max_score = max(scores)
  matching_block_of_max = matched_blocks[scores.index(max_score)]

  substrings = []
  for match in matching_block_of_max:
      # print(shorter[match.a:match.a + match.size], end=" =?? ")
      # print(long_substr[match.b:match.b + match.size])
      if(match.size > 10):
        substrings.append([match.a, match.a + match.size])

  return [max_score*100, matching_block_of_max, substrings]


def match_content(Str1, Str2):
    ratio, matched_blocks, substrings = partial_ratio(Str1.lower(), Str2.lower())
    for substring in substrings:
        print(Str1[substring[0]:substring[1]], end="\n\n---------\n")
    print("======================")
    return [ratio, substrings]


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
            # try:
            #     urlretrieve(item['link'], "download.pdf")
            #     scrapped_content = convert_pdf_to_txt("download.pdf");
            #     match_content(content, scrapped_content)

            # except:
            #     print("")
            continue

        scrapped_content = web_scrape(item['link'])
        match_percentage, matched_string = match_content(content, scrapped_content)

        if match_percentage > highest_percentage:
            highest_percentage = match_percentage
        print(matched_string)
        ans += "{}% of content was copied from {}\n <br>".format(match_percentage, item['link'])

    ans += "<br> \nHighest Plagiarism Percentage: {}%".format(highest_percentage)

    if highest_percentage >= 70:
        ans += "<br> \nSorry but your paper is rejected due to high plagiarism. Please try again later."
    else:
        ans += "<br> \nCongratulations your paper has been successfully accepted!"
    return ans


# content = str(input())
print(mainEngine(content))

# scrapped_content = web_scrape("https://en.wikipedia.org/wiki/Michael_Madana_Kama_Rajan")
# match_content(content, scrapped_content)
