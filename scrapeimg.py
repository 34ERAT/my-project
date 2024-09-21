import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, select
from save_load_json import save_json,load_json


# Set up the web driver (make sure to download the appropriate driver for your browser)

def scrape_images(driver:webdriver.Chrome,query, num_images,country):
    # Create a Google Images search URL
    query=f"{query} {country}"
    search_url = f"https://www.google.com/search?q={query.replace(' ','+')}+-video+-youtube+-map+-log+-stock&tbm=isch"
    # open the google images search page
    driver.get(search_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#rso > div > div > div.wH6SXe.u32vCb > div > div")))
    # for _ in range(num_images // 50):
    driver.execute_script("window.scrollBy(0,10000)")
    time.sleep(5)
    # Scroll back to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)
    # Scroll back to the top of the page
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    imgs=[]
    selected=0
    index=0
    print(search_url)
    while selected <= num_images :
        driver.find_element(By.XPATH,f'//*[@id="rso"]/div/div/div[1]/div/div/div[{index+1}]/div[2]/h3/a').click()
        time.sleep(6)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]')))
            urls = driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a')
            time.sleep(6)
            urls = driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a')
            try:
                img_src = urls.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]').get_attribute("src")
                tmb_src= urls.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[2]').get_attribute("src")
                data = {
                    "query": query.replace(country,'').strip(),
                    "preview_url":tmb_src,
                    "image_url":img_src,
                    } 
                imgs.append(data)
                selected=selected+1
                index=index+1
            except:
                print("missing an img tag skipping image")
                index=index+1
        except:
            print("missing the the required atag ::: seams its not and image")
            index=index+1

    return imgs

def start(query_file,output_file,country):
    driver = webdriver.Chrome()
    querys =load_json(query_file)
    for i,query in enumerate(querys): 
        if query["visited"]:
            continue
        print(f" on query number ::: {i} /{len(querys)} images needed {query['count']+3}")
        data=load_json(output_file)
        data= data+scrape_images(driver=driver,query=query["search_term"],num_images=query["count"]+3,country=country)
        query["visited"]=True
        save_json(query_file,querys)
        save_json(output_file,data)
    driver.quit()


def Main():
    if len(sys.argv) < 2:
        print("# Usage scrapeimage  [query_file] [output_file] [coutry]")
        # options="""
        # ####\t options \t ####\n
        #    -v  # exclude videos\n
        #    -y  # exclude youtube videos\n
        #    -m  # exclude map images\n
        #    -l  # exclude images with logos\n
        #    -s  # exclude stock images\n
        # """
        # print(options)
        return

    # search_url = f"https://www.google.com/search?q={query.replace(' ','+')}+-video+-youtube+-map+-logo+-stock&tbm=isch"
    query_file = sys.argv[1].strip()
    output_file = sys.argv[2].strip()
    cntry = sys.argv[3].strip()
    start(query_file=query_file,output_file=output_file,country=cntry)

Main()

