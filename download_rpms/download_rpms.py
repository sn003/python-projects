"""This script requires bs4 and html5lib module"""
import glob
import sys
import os
import re
import requests 
from bs4 import BeautifulSoup 
import time
import concurrent.futures
  
t1 = time.perf_counter()
destination = "/root/downloaded_rpms"
rpms_file = "/root/rpms_list.txt"

try:
    os.rmdir(destination)
except OSError:
    pass


def get_required_rpms_list(pkg_list_file):
    rpmlist = []
    with open(pkg_list_file, "r") as fp:
        rpmlist = fp.readlines()
    return rpmlist
  
def get_rpm_links(rpm_url): 
    r = requests.get(rpm_url) 
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html5lib') 
      
    # find all links on web-page 
    links = soup.findAll('a') 

    rpm_list = get_required_rpms_list(sys.argv[2])
    # filter the link ending with .rpm
    rpm_links = []
    for rpm_name in rpm_list:
        pattern = r'^%s-' % rpm_name.strip("\n")
        for link in links: 
            #if (link['href'].startswith(rpm_name.strip("\n") + "-") 
            try:
                match = re.search(pattern, link['href'])
            except Exception:
                match = rpm_name.strip("\n") in link['href']
            if match and link['href'].endswith('rpm'):
                rpm_links.append(rpm_url + link['href'])
                break
    return rpm_links 
  
  
def download_rpm_series(link): 

    # obtain filename by splitting url and getting  
    # last string 
    file_name = os.path.join(destination, link.split('/')[-1])
  
    # create response object 
    r = requests.get(link, stream = True) 
         
    # download started 
    with open(file_name, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk) 
          
    print(f"{file_name} downloaded!")
  

def download_rpms(rpm_links):
    if not os.path.exists(destination):
        os.mkdir(destination)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_rpm_series, rpm_links)

    print("All rpms downloaded!: downloaded_rpms_count=%d" % len(rpm_links))
    return len(rpm_links)


def create_file():
    with open(rpms_file, "w") as fp:
        for each_rpm in os.listdir(destination):
            fp.write(each_rpm + "\n")
        
def main():
    try:
        # getting all rpm links 
        rpm_links = get_rpm_links(sys.argv[1]) 
        print("configured rpms in file. Count= %d" % len(rpm_links))
        downloaded_count = download_rpms(rpm_links) 
        file_count = len(get_required_rpms_list(sys.argv[2]))
        print("No of rpms configured in file configured_count=%d" % file_count)
        create_file()
        t2 = time.perf_counter()
        print(f"Total time taken {round(t2 - t1)} secs..")
    
        if downloaded_count > file_count:
            raise ValueError("More rpms downloaded than configured ones. Script Logic error. FIX IT.")
        elif downloaded_count == file_count:
            print("Voila!! All configured rpms are downloaded. You rock!!")
        else:
            raise ValueError("Less rpms downloaded than configured ones. Need attention!!")

    except Exception as exp:
        import traceback
        print(traceback.format_exc())
        print("Exception raised: %s" % str(exp))
        sys.exit(1)

if __name__ == "__main__": 

    if(len(sys.argv) != 3):
        print("Usage: python3 download_os_rpms.py <artifactory_url> <path_to_package_list>")
        sys.exit(1)
    main()
