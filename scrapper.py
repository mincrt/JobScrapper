import re
import requests
from bs4 import BeautifulSoup

# LIMIT = 50
# WORD = "python"
# WORD = "matlab"
# print(URL)

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):

    # title = html.find_all("a",{"class": "s-link"}) #.find("a") 
    company = []
    href = []
    location = []
    title = []

    for aa in html.find_all("a",{"class": "s-link"}):
        company.append(aa.string)
        href.append('https://stackoverflow.com/'+aa["href"])

    for bb in html.find_all("div",{"class": "flex--item fc-black-500 fs-body1"}):
        # print('bb : ',bb)
        cc = bb.find("svg",{"class": "iconLocation"})
        if cc is not None:
            location.append(bb.get_text())
        else:
            title.append(bb.get_text())

    # location1, title1 = html.find_all("div",{"class": "flex--item fc-black-500 fs-body1"}, recursive=False)
    # print(location1.get_text(),title1.get_text())
    company = " ".join(company)
    
    # company = company.replace('"',"")
    title = " ".join(title)
    # title = title.replace('"',"")
    # title = re.sub('["]',"",title)
    href =  " ".join(href)
    location =  " ".join(location)
    # print(title)
    return {"title": title, 
            "company": company, 
            "location": location,
            "link": href
            }

def extract_jobs(last_page, url):
    jobs = []    
    for page in range(last_page):
        
        result = requests.get(f"{url}&pg={page+1}")
        print(f"{url}&pg={page+1}...Scraping!!!")
        soup = BeautifulSoup(result.text,"html.parser")
        # results = soup.find_all("a",{"class": "s-link"})
        results = soup.find_all("div",{"class": "flex--item fl1 text mb0"})
        # print(results)
        for a in results:
            job = extract_job(a)
            jobs.append(job)          
    return jobs

def get_jobs(word):
    url = f"https://stackoverflow.com/jobs/companies?q={word}"
    last_page = get_last_page(url)
    # last_page = 1
    jobs = extract_jobs(last_page, url)
    # jobs = extract_jobs(2)
    # print(jobs)
    return jobs
