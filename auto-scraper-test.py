import requests
from bs4 import BeautifulSoup

URL = "https://www.investopedia.com/terms/c"

def scrapeUrlDescription(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find("meta", itemprop="description")
    print(description["content"])

def main():
    print("hello world")
    page = requests.get(URL)

    #print(page.text)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="dictionary-top300-list__list-content_1-0")

    #print(results.prettify())

    job_elements = results.find_all("a", class_="dictionary-top300-list__list mntl-text-link")
    print(job_elements)

    phrase_urls = []

    for job_element in job_elements: 
        print(job_element, end = "\n"*2)
        link = job_element["href"]
        title = job_element.find("span",class_="link__wrapper")
        print(title.text)
        phrase_urls.append((title.text,link))

    #print(urls)

    for phrase_url in phrase_urls: 
        scrapeUrlDescription(phrase_url[1])

if __name__ == "__main__":
    main()


#todo
#get the title and save that to as the key 
#pass this to a database for elasticsearch 

