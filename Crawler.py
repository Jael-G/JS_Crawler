from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint
import requests as r
from tqdm import tqdm
from art import *
from os import system
import csv
from collections import Counter

java_dict={}
headers_dictionary={}

try:
    with open('repetitions.csv','r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            headers_dictionary[row[0]]=row[3]
except:
    pass

def GetMetrics(url, l):
    global java_dict
    sites_link=[]
    header_list={}
    response={}
    writer.writerow({'Site' : url+' : '+str(len(l))+' Files'})

    for site in tqdm(l):
        if site in java_dict:
            java_dict[site].append(url)
        else:
            java_dict[site]=[url]

        header_list={}

        if site[0:2]=='ht':
            try:
                response=r.get(site, timeout=2).headers
                for key,value in response.items():
                    if key in ['Expires','Last-Modified', 'Cache-Control']:
                        header_list[key]=value
            except:
                pass

        elif site[0:2]=='//':
            try:
                response=r.get('http:'+site, timeout=2).headers
                for key,value in response.items():
                    if key in ['Expires','Last-Modified', 'Cache-Control']:
                        header_list[key]=value

            except:
                pass
        elif site[0:2]!='//' and site[0]=='/':
            try:
                response=r.get('http://'+url+site, timeout=2).headers
                for key,value in response.items():
                    if key in ['Expires','Last-Modified', 'Cache-Control']:
                        header_list[key]=value
            except:
                pass

        if site not in headers_dictionary.keys():
            headers_dictionary[site]=header_list
        writer.writerow({'Site':'' ,'Javascript Files' : site, 'Headers':header_list})




opts = Options()
opts.binary_location = 'INSER PATH FOR CHROMIUM chrome.exe'
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=opts)


amout_of_js_files={}
#opts = Options()
#opts.set_headless()
#assert opts.headless


system('cls')
print(text2art('WEB CRAWLER'), end="\t\tBy Jael Gonzalez\n")
print("***WARNINGS***\n[*]Some Headers from the Javascript files are not loaded because of the request timeoout\nThis can be manually change in the program but it's not recommended\n[*]The headless-driver option has been commented out because it produces many errors\n")
print('*********************************************************************************************')

entire_scripts=[]

with open('INSERT WEBSITE LIST PATH', mode='r') as f:
    content=f.read().splitlines()

with open('NAME FILE FOR OUTPUT OF DATA', mode='w', newline='') as f:
    fieldnames=['Site', 'Javascript Files', 'Headers']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    number_of_url=1
    for url in content:
        print(f'[{number_of_url}/100] '+url, end='')
        counter=0
        try:
            driver.get('http://'+url+'/')


        except:
            print('conecction to ' + url+ ' failed')
            pass


        soup = BeautifulSoup(driver.page_source, "html.parser")

        l = [i.get('src') for i in soup.find_all('script') if i.get('src')]
        entire_scripts.extend(l)

        print(f': {len(l)} files')
        GetMetrics(url, l)
        number_of_url+=1
dictionary={}

driver.quit()
print('\n\WRITING FILES...\n\n')
try:
    with open('repetitions.csv','r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            correct_value=row[1]
            bad_characters=["{","}","[","]","'","'"]
            for character in bad_characters:
                correct_value=correct_value.replace(character,'')
            correct_value=correct_value.split(',')
            dictionary[row[0]]=correct_value
except:
    pass

for key in java_dict.keys():
    if key in dictionary.keys():
        dictionary[key].extend(java_dict[key])
    else:
        dictionary[key]=java_dict[key]

with open('repetitions.csv','w',newline='') as file:
    new_fieldnames=['Javascript Files','Sites', 'Repetitions', 'Headers']
    writer=csv.DictWriter(file, fieldnames=new_fieldnames)
    writer.writeheader()
    for key,value in dictionary.items():
        writer.writerow({'Javascript Files' : key, 'Sites' : set(value), 'Repetitions' : len(set(value)), 'Headers':headers_dictionary[key]})
