# trial-task
  ----------

## Task description
   ----------

The job is to crawl job posts from https://www.mycareersfuture.sg/ and to parse the salary, date posted and closed, and skills requirements posted.

To create a website that allows one to select from popular skills from a wide diversity of job types and to visualise two week trending data on the skills. 

Should be able to click through to get a description of the job as crawled, or link directly to the job page in the website.

## Project Structure
   ---------
This project can be divide into crawler and web part.

> crawler 
>> mcfCrawler.py # crawl/parse/save/collect jobs data


>> chromedriver_win.exe # webdriver used in selenium (windows version)

>> chromedriver_mac # chromedriver mac version

>> chromedriver_linux # chromedriver linux version

>> jobs_folder # saving all crawled data in this folder

>>> Jobs0to30.json # at first we named json files with Jobs[start_page]to[end_page].json

>>> Jobs40to40.json # then changed to name with Jobs[datetime].json

>>>Jobs2019-04-03-03-42.json # to avoid same filename problem

> web

>> allJobs.json # collected all data from jobs_folder

>> index.html # HTML file of website

>> index.js # javascript file of website

>> index.css # CSS file of website

## Operating Instructions
   ------------

### mcfCrawler.py
<br>

Our crawler enviornment is Python + Selenium + Chromedriver_v2.46

If you don't install Selenium, you can run

> pip install selenium

Also, please check your version of Chrome

Chromedriver version 2.46 supports `Chrome v71-73`

As for code running, if your operating system is windows, run

> python mcfCrawler.python win

for mac, run 

> python mcfCrawler.python mac

for linux(default), run

> python mcfCrawler.python linux

Furthermore, user can set page range you want to crawl in command. Command example is like

> python mcfCrawler.python your_OS start_page end_page

For example, you can run command like

> python mcfCrawler.python win 10 20

In this code, we start crawling jobs information from website https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=0. 

So this program will crawl jobs information from https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=10. to https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=20.

No page range in command is ok. Default page range is from page 0 to page 10.
### index.html
<br>
User can check many skills at same time. 

Jobs table below shows jobs that need all skills you have checked. 

Click job title of each job can link to its originally page.

##### P.S. More details of this project is in each file's comment.
