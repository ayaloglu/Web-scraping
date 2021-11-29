# Dependencies
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd



def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #find the latest news title from the webpage

    last_news_title = soup.findAll('div',class_ = 'content_title')
    #last_news_title[0].text

    #find the latest news contents from the webpage
    last_news_content = soup.findAll('div',class_ = 'article_teaser_body')
    #last_news_content[0].text

    # page for image scraping

    url_2 = 'https://spaceimages-mars.com'
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the featured image link
    a = soup.findAll('a', class_= "showimg fancybox-thumbs")
    #a[0]['href']

    # write the complete url for the featured image
    featured_image_url = url_2 +"/"+ a[0]["href"]
    #featured_image_url

    # page for getting info about mars 
    url_3 = 'https://galaxyfacts-mars.com'

    tables = pd.read_html(url_3)
    #tables[0]
    table_1 = tables[0]

    w =table_1.drop(columns= [2])


    x = tables[1]

    table = w.append(x).reset_index(drop=True)


    # generate html table from the dataframe

    html_table = table.to_html(index=False, classes="table", header=False)
    

    # clean up the table by stripping unwanted n's
    html_table = html_table.replace('\n', '')

    # obtain high res images for each Mars' hemisphere

    url_4 = 'https://marshemispheres.com/'

    browser.visit(url_4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # write a for loop to click and go on the pages for each image and retrieve the image url and the title.

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_links = soup.findAll('h3')
    hemisphere_image_urls =[]
    for link in image_links:
        
        print(link.text)
        try:
            browser.links.find_by_partial_text(link.text).click()
            
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')

            b = soup.findAll('img', class_= "wide-image")
            image_1_url = b[0]['src']

            image_1_link = url_4 + image_1_url

            c = soup.findAll('h2', class_= "title")
            title_hemisphere = c[0].text
            title_hemisphere = title_hemisphere.replace(" Enhanced", "")
            title_hemisphere

            hemisphere_image_urls.append({"title" :title_hemisphere,
                                "img_url" : image_1_link})

        

            browser.links.find_by_partial_text('Back').click()
        except: 
            
            pass
        
        



    browser.quit()

    mars_information={ 
        "Latest_news_Title": last_news_title[0].text,
        "Latest_news_content": last_news_content[0].text,
        "Featured_Mars_Image": featured_image_url,
        "Information_about_Mars" : html_table,
        "High_Res_images_of_Mars_hemispheres" : hemisphere_image_urls
    }

    return  mars_information
