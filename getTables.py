from tracemalloc import start
import requests
from bs4 import BeautifulSoup
import pandas as pd


def getTableFromSection(soup, sectionNumber):
    registerUrl = soup.find('a', {'id': sectionNumber})['href']

    r2 = requests.get('https:' + registerUrl)

    soup = BeautifulSoup(r2.text, 'html.parser')

    tables = soup.find_all('table')

    i = 0
    for table in tables:
        data_frame = pd.read_html(table.prettify(), flavor='bs4')
        data_frame[0].to_csv('output{}_{}.csv'.format(sectionNumber, i), index=False)

        # data_frame.to_csv('output{}.csv'.format(i), index=False)
        i = i + 1

partNum = input('Device: ')
multiSection = input('Do you want to get multiple sections? (y/N): ')

sectionLoopNeeded = multiSection.lower() == 'y'




url = 'https://www.ti.com/document-viewer/{}/datasheet'.format(partNum)

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

if (sectionLoopNeeded):
    print("For multiple section, the lower subsection number entered will be iterated through. Both starting and end section inputs must have the same number of digits")
    startSection = input('Starting Section: ').split('.')
    endSection = input('End Section: ')
    while ('.'.join(startSection) != endSection):
            getTableFromSection(soup, '.'.join(startSection))
            startSection[len(startSection)-1] = str(eval(startSection[len(startSection)-1]) + 1)
else:
    sectionNumber = input('Section Number: ')
    getTableFromSection(soup, sectionNumber)