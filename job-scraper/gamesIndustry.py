#!/usr/bin/env python
# coding: utf-8

# In[16]:


from bs4 import BeautifulSoup
import requests
import csv

#The fucntion deals with appending the row to the CSV
def append_list_as_row(list_of_elem):
    # Open file in append mode
    with open("job-scraper/templates/aswift_prog.csv", 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        write_obj.close()

#List containing all the url's of the different pages
pages = []

#Appends the first page to pages list
pages.append("https://jobs.gamesindustry.biz/jobs/united-kingdom")

#Loops throught the url of the pags and appends them to the pages list
for i in range(1, 45):
        url = "https://jobs.gamesindustry.biz/jobs/united-kingdom?page="+str(i)
        pages.append(url)
    
#Loops through every url in the pages list
for item in pages:
    try:
        page = requests.get(item)
        #Gets the page's HTML
        soup = BeautifulSoup(page.text, 'html.parser')

        #Finds the first job
        firstItem = soup.find(class_="views-row views-row-1 views-row-odd views-row-first")
        #Extracts the title of the first job
        firstTitle = firstItem.find("article").find(class_="node__title").find("a").contents
        #Extracts the location of the first job
        firstLocation = firstItem.find("article").find(class_="location").find("span").text
        firstTitle.append(firstLocation)
        #Adds the title and its location to the CSV as new row
        append_list_as_row(firstTitle)

        #Loops through jobs that occur in an even postion (2n, 4th, 6th, ... jobs on the page)
        for i in range(2, 19, 2):
            try:
                evenItem = soup.find(class_="views-row views-row-"+str(i)+" views-row-even")
                #Extracts the title of the job
                evenTitle = evenItem.find("article").find(class_="node__title").find("a").contents
                #Extracts the title of the location
                evenLocation = evenItem.find("article").find(class_="location").find("span").text
                evenTitle.append(evenLocation)
                #Adds the title and its location to the CSV as new row
                append_list_as_row(evenTitle)
            except Exception:
                continue 
        #Loops through jobs that occur in an odd postion (1st, 3rd, 5th, ... jobs on the page)
        for i in range(3, 20, 2):
            try:
                oddItem = soup.find(class_="views-row views-row-"+str(i)+" views-row-odd")
                #Extracts the title of the job
                oddTitle = oddItem.find("article").find(class_="node__title").find("a").contents
                #Extracts the title of the location
                oddLocation = oddItem.find("article").find(class_="location").find("span").text
                oddTitle.append(oddLocation)
                #Adds the title and its location to the CSV as new row
                append_list_as_row(oddTitle)
            except Exception:
                continue

        lastItem = soup.find(class_="views-row views-row-20 views-row-even views-row-last")
        #Extracts the title of the last job
        lastTitle = lastItem.find("article").find(class_="node__title").find("a").contents
        #Extracts the location of the last job
        lastLocation = lastItem.find("article").find(class_="location").find("span").text
        lastTitle.append(lastLocation)
        #Adds the title and its location to the CSV as new row
        append_list_as_row(lastTitle)
    except Exception:
        continue

# In[ ]:




