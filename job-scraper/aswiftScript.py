from bs4 import BeautifulSoup
import requests
import csv
from multiprocessing import Pool
import time

start_time = time.time()

# List of URLs to parse
pages = []
# Packed Data for Pages HTML
packedData = None
# List of jobs titles
jobslist = []
#List of job links to send requests too
jobLinks = []
#Code languages
languages = []
#Languages Found List
LanguagesFound = []

# Gathers the different pages and puts them in a list
for i in range(1, 10):
    url = "https://aswift.com/job-search/?page_job=" + str(i) + "&industry=video-games-bh-1408958&location=united-kingdom&job_title=&cs_=Search&parent=bh-999833&industry=video-games-bh-1408958&job_title=&parent=bh-999833&industry=video-games-bh-1408958&job_title=&parent=bh-999833&industry=video-games-bh-1408958&job_title=&parent=bh-999833&industry=video-games-bh-1408958&job_title="
    pages.append(url)

#Populates languages list with all languages available on github
file = open(r'programming-languages.txt', 'r')
languages = file.readlines()
for i in range (len(languages)):
    languages[i] = languages[i].rstrip('\n')

#Worker function to send requests to the job pages
def get_data(item):
    pagesHtml = []
    # Parses the html
    page = requests.get(item)
    pagesHtml.append(page.text)

    return pagesHtml

#Worker functino to send requests to each job listing
# Returns the html to parse through
def getJobPageInfo(url):
    jobListingPagesHtml = []
    page = requests.get(url)
    jobListingPagesHtml.append(page.text)
    
    return jobListingPagesHtml

#Master function
def main():

    #Using 4 cores to run the worker function -> get_data
    with Pool(8) as p:
        packedData = p.map(get_data, pages)
    
    #Unpacks data from packedData
    unpackedData =[j for i in packedData for j in i]

    for text in unpackedData:
        soup = BeautifulSoup(text, 'html.parser')

        #Look through job listing classic class on html and find all 'ul' elements
        jobs = soup.find("ul", class_="jobs-listing classic")
        split_details = list(jobs.stripped_strings)

        try:
            #Finds all href's to job listings 
            for ul in soup.find_all('ul', class_='jobs-listing classic'):
                for listItem in ul.find_all('li'):
                    linkToJob = listItem.find('a')
                    jobLinks.append(linkToJob['href'])

        #If type error occurs -> end of links
        except TypeError as endOfLinks:
            break

        # Finds out the number of jobs per page
        jobsXPage = len(split_details)/4
        
        # Keeps track of the amount of jobs added to list Jobs on from page
        jobsCompleted = 0
    
        # Makes sure that once all jobs on that page have been added it stops and 
        while jobsCompleted != jobsXPage:
            for e in split_details:

                # Finds the index of the job
                index = split_details.index(e)

                # Used to make sure the location of the job is appended in the right place
                iteration = -1
                
                # The if statement makes sure to select only the Job title page with 10 Jobs
                if index == 1 or index == 5 or index == 9 or index == 13 or index == 17 or index == 21 or index == 25 or index == 29 or index == 33 or index == 37:
                    jobslist.append([e])
                    iteration += 1
                    jobsCompleted += 1
                
                # The if statement makes sure to select only the Job location page with 10 Jobs
                if index == 3 or index == 7 or index == 11 or index == 15 or index == 19 or index == 23 or index == 27 or index == 31 or index == 35 or index == 39:
                    jobslist[iteration].append(e)

    #Use 4 cores to send requests to each job listing link
    with Pool(8) as p:
        jobListingsPacked = p.map(getJobPageInfo, jobLinks)
    #Unpack data returned from jobListingPacked
    unpackJobListings = [j for i in jobListingsPacked for j in i]

    #Looks through the returned html and parses it
    for i in unpackJobListings:
        soup = BeautifulSoup(i, "html.parser")
        jobsInformation = soup.find(class_ = "rich-editor-text")
        LanguageOnLink = []
        string = ""
        # Searches up each language to check if it occurs in within the html
        for language in languages:
            if language.upper() in jobsInformation.text.strip().split() or language.lower() in jobsInformation.text.strip().split():
                LanguageOnLink.append(language)
        
        #Appends each language found per job listing to a permanent array
        LanguagesFound.append(LanguageOnLink)

    #Appends the languages found to each row of the jobslist 
    for i in range(len(jobslist)):
        jobslist[i].append(LanguagesFound[i])
        print(jobslist[i])

    #Writes returned data to CSV
    csvHeaders = ["Job Title", "Location", "Languages"]
    with open('job-scraper/templates/aswift_prog.csv', 'w') as f: 
        write = csv.writer(f) 
        write.writerow(csvHeaders)
        write.writerows(jobslist)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
