'''
    @date: 2019-03-31
    @author: Qi Sun  
    @desc: Crawl/parse/save/collect jobs information
    @func: parse(), collect_json()
'''

import os
import sys
import time
import json

from selenium import webdriver


def parse():
    '''
        Crawling and parsing jobs information using selenium
        and saving them in json format

        Structure of our json files:
        [   
            {
                version: your OS + crawler version
                date_obtained: [date_posted1, date_posted2, ...]
            },
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

        @param: None
        @return: None
    '''

    # define constant indices first
    sleep_time = 10
    # indice of input arguments
    os_id = 1
    start_page_id = 2
    end_page_id = 3
    # indice of job dictionary
    job_title_str = 'job_title'
    job_url_str = 'job_url'
    salary_range_str = 'salary_range'
    date_posted_str = 'date_posted'
    date_closed_str = 'date_closed'
    skills_str = 'skills'

    # settings for the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--incognito')

    # input arguments needs to be vetted to ensure escapes are properly
    # checked and sanitized to prevent a hacker 
    # from maliciously executing arbitrary code within string arguments
    if len(sys.argv) == 4:
        # different system has different webdriver
        if sys.argv[os_id] == "win":
            driver = webdriver.Chrome(
                'chromedriver_win.exe', chrome_options=options)
        elif sys.argv[os_id] == "mac":
            driver = webdriver.Chrome(
                'chromedriver_mac', chrome_options=options)
        elif sys.argv[os_id] == "linux":
            driver = webdriver.Chrome(
                'chromedriver_linux', chrome_options=options)
        # check whether OS is collect entered
        else:
            print("OS input error")
            raise Exception
        # check whether page range input are digits
        # if not, raise exception
        start_page_str = sys.argv[start_page_id]
        end_page_str = sys.argv[end_page_id]
        if start_page_str.isdigit() == False or \
            end_page_str.isdigit() == False:
            print("Page range input error")
            raise Exception
        start_page = int(sys.argv[start_page_id])
        end_page = int(sys.argv[end_page_id])

    else:
        print("Please input 4 arguments")
        raise Exception

    jobs_json = []
    date_obtained = []
    for page in range(start_page, end_page + 1):
        url = "https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=" \
            + str(page)
        # using chromedriver to connect website
        driver.get(url)
        # because this website is a dynamic website
        # we need to wait a while for website loading
        time.sleep(sleep_time)
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
                time.sleep(sleep_time)
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
            except Exception:
                continue

            else:
                # first save the data in a dictionary
                tmp_dict = {}
                tmp_dict[job_title_str] = job_title
                tmp_dict[job_url_str] = job_url
                # make some adjustment of data we crawled
                tmp_dict[salary_range_str] = salary_range[:-1]
                tmp_dict[date_posted_str] = date_posted[7:]
                tmp_dict[date_closed_str] = date_closed[11:]
                tmp_dict[skills_str] = skills
                
                # then put the dictionary in our final json list
                jobs_json.append(tmp_dict)
                date_obtained.append(date_posted[7:])

    # don't forget to close the driver
    driver.close()

    # save our data in json format as easily read by javascript
    # add a self-describing header structure in json payload
    # which describes the version of the crawler and date obtained
    date_obtained = list(set(date_obtained))
    version = sys.argv[os_id] + " 3.0"
    header = [{'version': version, 'date_obtained': date_obtained}]
    jobs_json = header + jobs_json
    
    # using datetime as filename in order to avoid repeat problem
    json_filepath = './jobs_folder/Jobs' + \
        time.strftime('%Y-%m-%d-%H-%M', time.localtime()) + '.json'
    with open(json_filepath, 'w') as mcfj:
        json.dump(jobs_json, mcfj)


def collect_json():
    '''
        Collecting all json files from ./jobs_folder into one
        and remove repeated jobs we crawled
        
        Structure of our final json payload:
        jobJson([   
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
                ])

        @param: None
        @return: None
    '''

    jobs_list = []
    for root, dirs, files in os.walk('./jobs_folder'):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                jobs_json = json.load(f)[1:]  # remove header
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