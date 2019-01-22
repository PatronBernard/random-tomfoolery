#!/usr/bin/env python
import requests, os, re, datetime, time 
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
#Get the PDF from the website. As the filename changes each week, we need to fetch it through the anchor tag
request = requests.get('https://www.uantwerpen.be/nl/campusleven/eten/weekmenu/')
soup = BeautifulSoup(request.content,'lxml')
links = soup.findAll('a')
for link in links:
    link
    if link.text == 'Ontdek het weekmenu komida@3Eiken restaurant (pdf)':
        url = 'https://www.uantwerpen.be'+link.get('href')
#Download the pdf
request_pdf = requests.get(url)
pdf_file_path = os.path.expanduser('~/Downloads/weekmenu.pdf')
pdf_file = open(pdf_file_path,'wb')
pdf_file.write(request_pdf.content)
pdf_file.close()
#Parse the pdf file to get all menu entries
pdf_file = open(pdf_file_path,'rb')
pdf = PdfFileReader(pdf_file)
text = pdf.getPage(0).extractText().encode('utf-8')
matches = re.finditer(r'\n\n',  text)
menu_item_start = 0
menu_items = [] 
for m in matches:
    menu_item_end = m.start(0)
    menu_item_str=text[menu_item_start:menu_item_end]
    menu_items.append(menu_item_str.replace('\n', ''))
    menu_item_start = menu_item_end
#Set up the notification command
options = '--expire-time=3000 '
basecmd = 'notify-send '
cmd = basecmd + options + '"'
#Send the notifications
dag = datetime.datetime.today().weekday()
os.system(cmd + 'Menu voor vandaag: "')
time.sleep(3)
os.system(cmd + menu_items[dag]+'"')
time.sleep(3)
os.system(cmd + menu_items[dag+2] + '"')
time.sleep(3)
os.system(cmd + menu_items[dag+4] + '"')
#os.system(cmd + 'Dagelijks: "')
#os.system(cmd + menu_items[13]+'"')
#os.system(cmd + menu_items[15]+'"')
#os.system(cmd + menu_items[17]+'"')
