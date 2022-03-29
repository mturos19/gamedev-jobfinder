from unicodedata import normalize
from csv import writer as csv_writer

import requests
from bs4 import BeautifulSoup


def read_langs_file():
    """Read the list of programming languages from its file."""
    with open("programming-languages.txt", "r") as file:
        langs = file.readlines()
    # Not sure why this part is necessary
    # Copied from some other code
    for i in range(len(langs)):
        langs[i] = langs[i].rstrip("\n")
    return langs


def scrape():
    """Get job data from https://www.opmjobs.com/jobs/ jobs board.

    Since that jobs board uses AJAX, the AJAX endpoint /jm-ajax/get_listings
    is the actual source of the data.
    The endpoint provides the data as HTML inside JSON.
    This function grabs the HTML from the JSON and then scrapes
    that HTML using BeautifulSoup.
    """
    BASE_URL = "https://opmjobs.com/jm-ajax/get_listings"
    PER_PAGE = 50
    langs = read_langs_file()

    job_data = []
    # Starting page number
    page = 1
    page_empty = False

    while not page_empty:
        response = requests.get(
            BASE_URL
            + "?page={0}&per_page={1}".format(page, PER_PAGE)
            )
        # the HTML response is under "html" in the json object
        html = response.json()["html"]
        soup = BeautifulSoup(html, "html.parser")

        # If there are no jobs on this page, this page is considered
        # "empty" and no further pages are checked
        if not soup.find_all("div", class_="job-item"):
            page_empty = True

        # each job listing is inside a div with the class
        # `job-item`
        # each of those has job-position and job-location class
        # divs inside of it
        for job_div in soup.find_all("div", class_="job-item"):
            title: str = job_div.find("h3", class_="job-title").text
            location: str = job_div.find("div", class_="job-location") \
                .find("strong").text
            # breakpoint()
            # infer the languages from the job description
            # If any of the words in the job description is in the langs
            # list, then assume that it is a language relevant to the
            # job and record it
            # follow a link to find the job description page
            job_desc_link = job_div.find("a")["href"]
            job_desc_html = requests.get(job_desc_link).text
            # then use beautifulsoup to parse the text out of the html
            job_desc_soup = BeautifulSoup(job_desc_html, "html.parser")
            job_desc_text = job_desc_soup.find(
                "div",
                class_="job_description"
                ).text.replace("\n", "")
            languages: list = [lang for lang in langs
                               if normalize("NFC", lang)
                               in
                               normalize("NFC", job_desc_text).split(" ")]
            # Only add a scraped listing to the output list if it isn't a
            # duplicate of a listing already scraped.
            # For some reason, the AJAX endpoint gives a lot of duplicates.
            # This is the best workaround I could find.
            if (title, location, languages) not in job_data:
                job_data.append((title, location, languages))
        # Look at the next page in the next iteration
        page += 1
    return job_data


def scrape_all():
    """Scrape all the websites in the system."""
    job_data = scrape()
    with open(
            "ASWIFT-UK-industry=videogames-category=programming.csv",
            "a"
    ) as csv_file:
        writer = csv_writer(csv_file)
        writer.writerows(job_data)


if __name__ == "__main__":
    scrape_all()
