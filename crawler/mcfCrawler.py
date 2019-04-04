'''
    crawl/parse/save/collect jobs information
    Created by Qi on 03/31/19
'''

import os
import sys
import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


'''
    parse function
    crawling and parsing jobs information using selenium
    and saving them in json format
'''


def parse():
    # settings for the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--incognito')

    if sys.argv[1] == "win":
        driver = webdriver.Chrome(
            'chromedriver_win.exe', chrome_options=options)
    elif sys.argv[1] == "mac":
        driver = webdriver.Chrome(
            'chromedriver_mac', chrome_options=options)
    else:
        driver = webdriver.Chrome(
            'chromedriver_linux', chrome_options=options)

    # set range of page we want to crawl
    start_page = 0   # default
    end_page = 10
    if len(sys.argv) == 4:
        start_page = int(sys.argv[2])
        end_page = int(sys.argv[3])

    '''
        example of jobs_json:
        [
            {
                job_title: string ,
                job_url: string ,
                salary_range: [low, high] ,
                date_posted: string ,
                date_closed: string,
                skills: [skill1, skill2, ... , skill20]
            },
            ...
            {
                ...
            }
        ]
    '''
    jobs_json = []
    for page in range(start_page, end_page + 1):
        url = "https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=" \
            + str(page)
        # using chromedriver to connect website
        driver.get(url)
        # because this website is a dynamic website
        # we need to wait a while for website loading
        time.sleep(10)
        # find job links from the start URLs
        # then save those links into a list
        job_links = driver.find_elements_by_xpath(
            '//div[@class="card-list"]//a')
        job_urls = [job_link.get_attribute('href') for job_link in job_links]

        # we click into each url of job to get more details
        for job_url in job_urls:
            print(job_url)
            try:
                # doing the same thing we told above
                driver.get(job_url)
                time.sleep(10)
                # check HTML to find location of thing we wanted
                # and use xpath to find relevant infomation
                job_title = driver.find_element_by_xpath(
                    '//h1[@id="job_title"]').text
                salary_range = [salary.text for salary in
                                driver.find_elements_by_xpath(
                                    '//span[contains(@class, "salary_range")]//span')]
                date_posted = driver.find_element_by_xpath(
                    '//span[@id="last_posted_date"]').text
                date_closed = driver.find_element_by_xpath(
                    '//span[@id="expiry_date"]').text
                skills = [skill.text for skill in
                          driver.find_elements_by_xpath(
                              '//div[@id="skills-needed"]//label')]

                # first save the data in a dictionary
                tmp_dict = {}
                tmp_dict['job_title'] = job_title
                tmp_dict['job_url'] = job_url
                # make some adjustment of data we crawled
                tmp_dict['salary_range'] = salary_range[:-1]
                tmp_dict['date_posted'] = date_posted[7:]
                tmp_dict['date_closed'] = date_closed[11:]
                tmp_dict['skills'] = skills
                print(tmp_dict)
                # then put the dictionary in our final json list
                jobs_json.append(tmp_dict)

            except Exception:
                continue

    # don't forget to close the driver
    driver.close()

    # save our data in json format as easily read by javascript
    # using datetime as filename in order to avoid repeat problem
    json_filepath = './jobs_folder/Jobs' + \
        time.strftime('%Y-%m-%d-%H-%M', time.localtime()) + '.json'
    with open(json_filepath, 'w') as mcfj:
        json.dump(jobs_json, mcfj)


'''
    collect_json function collect all json files
    from ./jobs_folder into one
    and remove repeated jobs we crawled
'''


def collect_json():
    jobs_list = []
    for root, dirs, files in os.walk('./jobs_folder'):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                jobs_json = json.load(f)
            jobs_list += jobs_json

    # remove repeated jobs
    jobs_list = [json.dumps(job) for job in jobs_list]
    jobs_list = list(set(jobs_list))
    jobs_list = [json.loads(job) for job in jobs_list]

    # we add string jobJson() in order to use jsonp
    # to transfer local json file to website
    with open('../web/allJobs.json', 'w') as allJ:
        allJ.write("jobJson(")
        json.dump(jobs_list, allJ)
        allJ.write(")")

if __name__ == "__main__":
    parse()
    collect_json()