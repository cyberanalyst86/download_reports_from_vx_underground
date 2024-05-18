import requests
from bs4 import BeautifulSoup
import re
import datetime
import os

def write_pdf_to_directory(response, filename, file_directory):

  isExist = os.path.exists(file_directory + "//" + filename)

  if isExist == False:

    with open(file_directory + "//" + filename, 'wb') as f:
      for chunk in response.iter_content(1024):
        f.write(chunk)

    print(f"Downloaded PDF: {filename}")

  else:

    error = "error"

  return

def create_folder(file_directory):

  isExist = os.path.exists(file_directory)

  if isExist == False:

    os.mkdir(file_directory)

  else:

    error = "error"

def download_pdf(webpage_url, pdf_title_list, file_directory):

  print("download pdf ......")

  pdf_filename_list = []
  pdf_download_url_list = []

  for pdf_title in pdf_title_list:

    pdf_filename_list.append(pdf_title.split(" - ")[1]\
    .replace("\\","").replace("/","").replace(":","")\
    .replace("*","").replace("?","").replace("\"","")\
    .replace("<","").replace(">","").replace("|", "") + ".PDF")

    pdf_title_url = webpage_url + "/" + pdf_title.replace(" ", "%20").replace("&#39;","'")+ "/Paper"

    try:

      response = requests.get(pdf_title_url)

      pdf_download_url = re.findall("href=.*.pdf|href=.*.PDF", response.text)[0].replace("href=\"","")

      print(pdf_download_url.replace("&#39;","'"))

      pdf_download_url_list.append(pdf_download_url.replace("&#39;","'"))

    except IndexError:

      response = requests.get(pdf_title_url.replace("/Paper", ""))

      pdf_download_url = re.findall("href=.*.pdf|href=.*.PDF", response.text)[0].replace("href=\"", "")

      print(pdf_download_url.replace("&#39;","'"))

      pdf_download_url_list.append(pdf_download_url.replace("&#39;","'"))

  print("Total number of PDF = ", len(pdf_download_url_list))

  print("\n")
  print("##############################################################################")
  print("\n")

  print("Saving PDF......")

  for i in range(len(pdf_download_url_list)):

    response = requests.get(pdf_download_url_list[i], stream=True)
    response.raise_for_status()  # Raise an exception for unsuccessful downloads

    filename = pdf_filename_list[i]

    write_pdf_to_directory(response, filename, file_directory)

  return

def get_pdf_title(url):

  print("get pdf title ......")

  pdf_title_list = []

  response = requests.get(url)

  #regex for strings in html containing the pdf titles
  regex_list = re.findall("<p class=\"text-white text-sm truncate\">.*", response.text)

  #parse pdf titles from the strings
  for string in regex_list:

    pdf_title_list.append(string.replace("<p class=\"text-white text-sm truncate\">","").replace("</p>",""))

  return pdf_title_list

def main():

  directory = "C:\\Users\\Public\\download_reports_from_vx_underground\\"
  report_year = "2024"
  file_directory = directory + report_year
  webpage_url = "https://vx-underground.org/APTs/" + str(report_year)

  create_folder(file_directory)

  pdf_title_list = get_pdf_title(webpage_url)

  download_pdf(webpage_url , pdf_title_list, file_directory)

if __name__ == '__main__':
  main()






