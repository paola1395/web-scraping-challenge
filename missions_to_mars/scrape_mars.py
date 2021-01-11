#Dependencies
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
import os
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}

##### NASA MARS NEWS #####

    #URL of page being scraped
    url= "https://mars.nasa.gov/news/"
    browser.visit(url)

    #HTML Object
    html= browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    #Extract/Print title
    latest_news = soup.find_all('div', class_="list_text")
    news = latest_news[0]

    news_title = news.find('div', class_='content_title').text

    #Extract/Print paragraph text
    news_p= news.find('div', class_='article_teaser_body').text

    #Add to mars_data dictionary
    

    ##### JPL MARS SPACE IMAGES #####

    #URL of page
    featured_image_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)

    #HTML Object; Parse HTML with Beautiful Soup
    image_html = browser.html
    soup = bs(image_html, 'html.parser')

    #Extract/Print featured image URL
    featured_img_url= soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    main= "https://www.jpl.nasa.gov"
    featured_image_url= main + featured_img_url

    featured_image_url

    ##### MARS FACTS #####

    #URL of page
    marsfacts_url= 'https://space-facts.com/mars/'

    #Read tables and convert to pandas df
    mars_facts= pd.read_html(marsfacts_url)
    mars_df= mars_facts[0]
    mars_df.columns= ['Description', 'Value']
    mars_df

    #Convert to HTML
    mars_html= mars_df.to_html()
    mars_facts_html= mars_html.replace('\n', '')
    mars_facts_html

    ##### MARS HEMISPHERES #####

    #URL of page
    hemisphere_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    #HTML Object; Parse HTML with Beautiful Soup
    mars_images_html = browser.html
    soup = bs(mars_images_html, 'html.parser')

    #Extract image urls

    items= soup.find_all('div', class_='item')

    #Create empty list to store image urls
    hemisphere_image_urls= []
    main_url= "https://astrogeology.usgs.gov"

    #Loop through items to get each hemisphere url
    for item in items:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        title = item.find('h3').text
        link = item.find('a', class_="itemLink product-item")['href']
        
        #Create HTML Object for individual hemisphere page; Parse HTML with Beautiful Soup
        browser.visit(main_url + link)
        hemisphere_html= browser.html
        soup= bs(hemisphere_html, 'html.parser')
        
        #Extract image source url
        img_url= main_url + soup.find('img', class_='wide-image')['src']
        
        #Create dictionary
        hemisphere_image_urls.append({
            "title": title,
            "img_url": img_url
        })
        
    #Print
    hemisphere_image_urls
