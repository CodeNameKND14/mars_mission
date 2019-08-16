from bs4 import BeautifulSoup as bs
from splinter import Browser
import time 
import pymongo
import pandas as pd 
import datetime


def init_browser():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

    
def mars_scrape():
    browser =init_browser()
    mars_info_dict = {}
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    new_soup1 = bs(html, 'html.parser')
    
    try:
        slide_item = new_soup1.select_one('ul.item_list li.slide')
        news_title = slide_item.find("div", class_="content_title").get_text()
        print(news_title)
        news_paragraph = slide_item.find("div", class_="article_teaser_body").get_text()
    except AttributeError as Atterror:
        print(Atterror)     
    mars_info_dict['News_Title'] = news_title
    mars_info_dict['News_Body'] = news_paragraph
        
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(3)
    full_image = browser.find_by_id("full_image")
    full_image.click()
    time.sleep(2)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    html2 = browser.html
    new_soup2 = bs(html2, 'html.parser')
    partial_url = new_soup2.select_one('figure.lede a img').get('src')
    featured_image = 'https://www.jpl.nasa.gov' + partial_url
    mars_info_dict['Mars_Featured_Image'] = featured_image
        
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(2)
    html3 = browser.html
    new_soup3= bs(html3, "html.parser")
    mars_weather = new_soup3.find('div', attrs={'class': 'tweet', 'data-name': 'Mars Weather'})
    mars_weather_tweet = mars_weather.find('p', 'tweet-text').get_text()
    mars_info_dict['Mars_Weather_Tweet']= mars_weather_tweet
        
    df = pd.read_html('http://space-facts.com/mars/')[1]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    html_mars_table = df.to_html()
    html_mars_table = html_mars_table.replace('\n', '')
    mars_info_dict["facts"] = html_mars_table
    
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(10)
    html4 = browser.html
    new_soup = bs(html4, 'html.parser')
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item h3')
    x = 1
    for i in range(len(links)):
        browser.find_by_css('a.product-item h3')[i].click()
        sample_element = browser.find_link_by_text('Sample').first
        mars_info_dict['img_url' + str(x)] = sample_element['href']
        mars_info_dict['title'+ str(x)] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(mars_info_dict)
        x+=1
        browser.back()

    browser.quit()
        
    return mars_info_dict
    