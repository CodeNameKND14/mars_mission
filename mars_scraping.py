# Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time 
import pymongo
import pandas as pd 
import datetime

#define  function for exec path for chromedriver.exe
def init_browser():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

#Function to scrape all necessary information from mars related websites  
def mars_scrape():
    browser =init_browser()
    #Create empty dictionay to store all the mars information
    mars_info_dict = {}
    
    # Part  1. NASA Mars News
    # -------------------------------------------
    #Define url and browse the site using chrome. 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    #create soup object and use beautiful soup to parse html.
    new_soup1 = bs(html, 'html.parser')
    
    try:
        # Used the parent element to find the first a tag and save it 
        slide_item = new_soup1.select_one('ul.item_list li.slide')
        news_title = slide_item.find("div", class_="content_title").get_text()
        print(news_title)
        # Use the parent element to find the paragraph text
        news_paragraph = slide_item.find("div", class_="article_teaser_body").get_text()
    
    # If try fails run except function
    except AttributeError as Atterror:
        print(Atterror)
    
    # Store info in dictionary
    mars_info_dict['News_Title'] = news_title
    mars_info_dict['News_Body'] = news_paragraph
    
    
    # Part 2. PL Mars Space Images - Featured Image
    # ---------------------------------------------
    #click on the link for "more info"
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(3)
    full_image = browser.find_by_id("full_image")
    full_image.click()
    time.sleep(2)
    
    # Parse html using bs4 and find the path for the  full size image.
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    html2 = browser.html
    new_soup2 = bs(html2, 'html.parser')
    partial_url = new_soup2.select_one('figure.lede a img').get('src')
    featured_image = 'https://www.jpl.nasa.gov' + partial_url
    
    #Save featured image url to the Mars dictionary.
    mars_info_dict['Mars_Featured_Image'] = featured_image
    
    
    # Part 3 Mars Weather tweet
    ## ------------------------
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(2)
    html3 = browser.html
    
    # Parse html using bs4 and find the path to obtain info from tweet
    new_soup3= bs(html3, "html.parser")
    mars_weather = new_soup3.find('div', attrs={'class': 'tweet', 'data-name': 'Mars Weather'})
    mars_weather_tweet = mars_weather.find('p', 'tweet-text').get_text()
    mars_info_dict['Mars_Weather_Tweet']= mars_weather_tweet
    
    # Create dataframe using pandas
    df = pd.read_html('http://space-facts.com/mars/')[0]
    # Provide appropriate column names for the dataframe.
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    #Add another html version of the Mars facts tables
    html_mars_table = df.to_html()
    html_mars_table = html_mars_table.replace('\n', '')
    mars_info_dict["facts"] = html_mars_table
    
    # # Part 5.### Mars Hemispheres
    #------------------------------- 
    # to obtain high resolution images for each of Mar's hemispheres.
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(5)
    html4 = browser.html
    
    # Parse through html to obtain photos 
    new_soup = bs(html4, 'html.parser')
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item h3')
    x = 1
    for i in range(len(links)):
        browser.find_by_css('a.product-item h3')[i].click()
        sample_element = browser.find_link_by_text('Sample').first
        # put str(x) to account for the number on the url
        mars_info_dict['img_url' + str(x)] = sample_element['href']
        mars_info_dict['title'+ str(x)] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(mars_info_dict)
        x+=1
        browser.back()

    browser.quit()
        
    return mars_info_dict
    