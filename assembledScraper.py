import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import os
import csv

##### THIS CODE GETS THE DETAIL HREF OF EACH INDIVIDUAL CABINET. allDetailsList IS THE STORE OF ALL VARIABLES

page = requests.get('https://www.selectedvendors.com/Goods/categoryGoodsList/53/Cabinets')

hrefs = BeautifulSoup(page.content, 'html.parser')

hrefsList = hrefs.find_all('a')

detailsList = []

allDetailsList = []

imageFileId = []

cabinetImageList = []

cabinetSkuList = []

imageDumpDirectory = 'D:\\'

num = 0

B = True

url = 'https://www.selectedvendors.com/Goods/categoryGoodsList/53/Cabinets'

   ###THIS FUNCTION RETURNS THE NEXT PAGE
def nextPagerMach12():
    global B
    global url
    global hrefsList

    page = requests.get(url)
    nextPage = BeautifulSoup(page.content, 'html.parser')
    nextPage = nextPage.find_all('a')
    hrefsList = nextPage

    for count, value in enumerate(nextPage):
        if 'next' in str(value.attrs):
            url = 'https://www.selectedvendors.com' + value.attrs['href']
            return url

        elif int(len(nextPage)) == count:
            print('ok')
            B = False

   ###THIS FUNCTION FINDS ALL THE DETAIL HREFS
def detailHrefs():
    global detailsList
    detailsList = []

    for link in hrefsList:
        if 'href' in link.attrs:
            if '/G' in str(link.attrs) and 'http' not in str(link.attrs) and 'category' not in str(link.attrs):
                if 'https://www.selectedvendors.com' + str(link.attrs['href']) not in detailsList:
                    detailsList.append('https://www.selectedvendors.com' + str(link.attrs['href']))

   ###THIS GETS ALL THE DETAIL INFORMATION FOR EACH CABINET IN 'detailsList'
def detailInfos():
    global allDetailsList
    allDetailsList = []

    for count, value in enumerate(detailsList):
        detailPage = requests.get(str(detailsList[count]))
        allDetailsList.append(BeautifulSoup(detailPage.content, 'html.parser'))


   ###THIS GETS ALL THE HREFS FOR THE INDIVIDUAL IMAGES ON DETAIL PAGE
def cabinetImageScraper(x):
    cabinetImages = x.find_all('img')
    global cabinetImageList
    cabinetImageList = []

    for count, value in enumerate(cabinetImages):
        if 'bimg' in value.attrs:
            cabinetImageList.append(value.attrs['bimg'])
    return cabinetImageList

    ###THIS FUNCTION GETS THE SKU'S OF EACH CABINET
def cabinetSkuScraper(x):
    global cabinetSkuList
    cabinetSkuList = []

    for count, value in enumerate(x):
        cabinetSkuList.append(value.find('h2').text)
    return cabinetSkuList

   ###THIS FUNCTION SAVES ALL IMAGES OF CABINETS ON DETAIL PAGE TO CHOSEN DIRECTORY
def cabinetImageDownloader(x, y):

    global imageFileId
    imageFileId = []
    y = y.replace('*', '')
    y = y.replace(' ', '')
    y = y.replace('/', '')
    print(str(imageDumpDirectory) + y)
    if os.path.isdir(str(imageDumpDirectory)) == True:
        return
    elif os.path.isdir(str(imageDumpDirectory) + y) == False:
        y = y.replace('*', '')
        y = y.replace(' ', '')
        y = y.replace('/', '')
        os.mkdir(imageDumpDirectory + y)

        os.chdir(imageDumpDirectory + y)

        for count, value in enumerate(x):

            with open(str(count) + '.jpg', 'wb') as f:

                im = requests.get(value)
                f.write(im.content)

   ###THIS FUNCTION CREATES THE CSV FILE
def cabinetCsvMaker():
    rows = []
    for i in range(3):
        fields = ['Sku', 'Description', 'Price', 'Assembled',
                  'Pocket Hole', 'Modification', 'Cut Up To 21',
                  'Hinge Side', 'Blind Side', 'Related Products',
                  'Details',]
        detailHrefs()
        detailInfos()

        # Begin to append to rowToAppend
        for count, value in enumerate(allDetailsList):
            rowToAppend = []
            cleanSku = value.find('h2').text
            # Append sku and Remove \ from sku
            rowToAppend.append(cleanSku.replace('\\', ''))
            p = value.find_all('p')
            for count1, value1 in enumerate(p):
                if 'c22' in str(value1):
                    # Append Description
                    rowToAppend.append(value1.text)
            b = value.find_all('b')
            for count2, value2 in enumerate(b):
                if 'aj' in str(value2):
                    # Append price
                    rowToAppend.append(value2.text)
            # Check whether or not assemble, grab value
            div = value.find_all('div', string=re.compile('Ass'))
            if div:
                rowToAppend.append('Assembled')

            else:
                rowToAppend.append('Null')
            # Check if Pocket Holes, if not then value is Null
            div1 = value.find_all('div', string=re.compile('Pocket'))
            if div1:
                rowToAppend.append('Pocket Hole')

            else:
                rowToAppend.append('Null')
            # Check if Modification possible, if not then value Null
            div2 = value.find_all('div', string=re.compile('Modification'))
            if div2:
                rowToAppend.append('Modification')

            else:
                rowToAppend.append('Null')
            # Check if Cut up to 21", if not then value Null
            div3 = value.find_all('div', string=re.compile('Cut up to 21'))
            if div3:
                rowToAppend.append('Cut up to 21\"')

            else:
                rowToAppend.append('Null')
            # Check if Hinge side, if not then value Null
            div4 = value.find_all('div', string=re.compile('Hing'))
            if div4:
                rowToAppend.append('Hinge side left right')

            else:
                rowToAppend.append('Null')
            # Check if Blind side, if not then value Null
            div5 = value.find_all('div', string=re.compile('Blin'))
            if div5:
                rowToAppend.append('Blind Side')

            else:
                rowToAppend.append('Null')
            # Check if Related products, if not then value Null
            div6 = value.find_all('li', string=re.compile('-'))
            div6String = ''
            for i in div6:
                div6String += i.text + ', '
            if div6:
                rowToAppend.append(div6String)

            else:
                rowToAppend.append('Null')
            #This part gets the other product details at the bottom of the page
            div7 = value.find_all('span')
            if div7:
                for i in div7:
                    if 'data-sheets' in str(i):
                        rowToAppend.append(str(i.text))
            div8 = value.find_all()


            # Append rowToAppend to rows then we create csv later
            rows.append(rowToAppend)



        # Grab the next page
        nextPagerMach12()


    with open('1Test.csv', 'w', encoding="utf-8") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        count = 0
        value = ''
        for count, value in enumerate(rows):
            csvwriter.writerow(rows[count])


cabinetCsvMaker()



   ###THIS BOTTOM PART RUNS THE CODE TO SCRAPE THE IMAGES AND SAVE THEM TO A DIRECTORY
#while True:
 #   for count, value in enumerate(cabinetSkuList):
  #      cabinetImageDownloader(cabinetImageScraper(allDetailsList[count]), cabinetSkuList[count])
#
 #   nextPagerMach12()
  #  detailHrefs()
   # detailInfos()
    #cabinetSkuScraper(allDetailsList)
