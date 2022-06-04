import requests
from bs4 import BeautifulSoup
import uuid
import json
from populatesearchindex import upload_files

URL = "https://www.investopedia.com/terms/c"

def scrapeUrlDescription(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find("meta", itemprop="description")
    return description["content"]

def create_document_upload(finance_term_details):
    document_upload = []

    for finance_term in finance_term_details:
        uuid_id = str(uuid.uuid4())
        finance_dict = { 
            "@search.action": "upload",
            'FinanceTermId': uuid_id,
            'FinanceTerm':finance_term[0],
            'Description':finance_term[1],
            'Url':finance_term[2]
        }
        #finance_json = json.dumps(finance_dict)
        document_upload.append(finance_dict)

    return document_upload

def main():
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

    finance_term_details = []

    count = 0 
    for phrase_url in phrase_urls[:10]: 
        description = scrapeUrlDescription(phrase_url[1])
        finance_term_details.append((phrase_url[0],description,phrase_url[1]))
        count = count + 1
        print(count)


    document_upload = create_document_upload(finance_term_details)
    print(document_upload)
    upload_files(document_upload)

    #print(finance_term_details)

if __name__ == "__main__":
    main()


#todo
#get the title and save that to as the key 
#pass this to a database for elasticsearch 

