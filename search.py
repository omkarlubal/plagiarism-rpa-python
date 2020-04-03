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


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def web_scrape(link):
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser').text
    except:
        soup = ''
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
      if(match.size > 50):
        substrings.append([match.a, match.a + match.size])

  return [max_score*100, matching_block_of_max, substrings]


links = []
def get_colored_html(pdf_content, cleaned_matches):
    global links
    output = "<br><hr><br>"
    lastIndex = None
    index = 0
    for block in cleaned_matches:
        current_color = colors[index % (len(colors) - 1)]
        links.append(block[2])
        output += "<span style='background-color:"+current_color+"'>"+pdf_content[block[0]:block[1]] + "</span> <sup style='background-color: #0008; padding: 5px; color: #fff;'>" + str(len(links) - 1) + "</sup>"
        index = index + 1
        lastIndex = block[1]
        
    lastItem = cleaned_matches[len(cleaned_matches) - 1][1]
    output += pdf_content[lastItem:None] + "<br>"

    return output


def match_content(Str1, Str2, link):
    ratio, matched_blocks, substrings = partial_ratio(Str1.lower(), Str2.lower())
    for substring in substrings:
        substring.append(link)
        
    return [ratio, substrings]


    # if(match_percentage > 30):
    #     print("Bro gotcha! {} percent copied from {}. What is this behaviour?".format(match_percentage, link))



def cleaninfy_output(matchingStrings):
  outputBlocks = [];
  for match in matchingStrings:
    for block in match: 
      outputBlocks.append(block)

  outputBlocks.sort(key= lambda x: [x[0], x[0] - x[1]])

  # safeZone = []
  # outputBlocks = [[0, 14], [0, 200], [10, 200], [130, 245]]

  safe_zone=[]
  safe_zone.append(outputBlocks[0])

  for i in range(1 , len(outputBlocks)):
    if outputBlocks[i][0] >= safe_zone[-1][0] and outputBlocks[i][1] <= safe_zone[-1][1]:
      continue
    else:
      safe_zone.append(outputBlocks[i])

  # 3) correct overlapping indexes such that they dont touch each other
  for i in range(1,len(safe_zone)):
    if safe_zone[i][0] <= safe_zone[i-1][1]:
      safe_zone[i][0] = safe_zone[i-1][1]+1 

  return safe_zone
    

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

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def mainEngine(content):
    global links
    result = google_search(content, my_api_key, my_cse_id)
    data = json.loads(json.dumps(result))
    highest_percentage = 0;
    ans = ""
    index = 0
    all_matched_strings = []

    for item in data['items']:
        if (item['link'].find('.pdf') > 0):
            continue

        scrapped_content = web_scrape(item['link'])
        match_percentage, matched_string = match_content(content, scrapped_content, item['link'])
        if match_percentage > highest_percentage:
            highest_percentage = match_percentage

        if(len(matched_string) > 0):
            all_matched_strings.append(matched_string)
        # ans += get_colored_html(content, matched_string, item['link'], index)
        # ans += "<br>{0}% of content was copied from <a href='{1}'>{1}</a>\n <br>".format(match_percentage, item['link'])
        index += 1


    ans += """
    <style>
    body{padding: 100px}
    </style>
    """
    cleaned_matches = cleaninfy_output(all_matched_strings)
    colored_html = get_colored_html(content, cleaned_matches)        
    ans += colored_html

    ans += "<br><hr>"
    for i in range(len(links)):
        ans += ("<br><i>" + str(i) +"</i>: <a href='"+ links[i]+"'>" + links[i] + "</a>")
    ans += "<br><br><hr>"

    ans += "<br><br> \nHighest Plagiarism Percentage: {}%".format(highest_percentage)

    if highest_percentage >= 70:
        ans += "<br> \nSorry but your paper is rejected due to high plagiarism. Please try again later."
    else:
        ans += "<br> \nCongratulations your paper has been accepted!"
    # print(cleaninfy_output(all_matched_strings))
    return ans


# content = str(input())

content = """
Node.js® is a JavaScript runtime built on Chrome's V8 JavaScript engine. 
As an asynchronous event-driven JavaScript runtime, Node.js is designed to build scalable network applications. In the following "hello world" example, many connections can be handled concurrently. Upon each connection, the callback is fired, but if there is no work to be done, Node.js will sleep.
"""

colors = ['#9de5fc', '#d1fc9d', '#fcfc9d', '#fcb39d', '#a29dfc', '#e79dfc', '#a89dfc', '#49e65e', '#49c1e6', '#fff242']

htmlFile = open("out.html", "w");
htmlFile.write(mainEngine(content))
htmlFile.close()
# scrapped_content = web_scrape("https://en.wikipedia.org/wiki/Michael_Madana_Kama_Rajan")
# match_content(content, scrapped_content)
