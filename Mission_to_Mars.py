#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
from bs4 import BeautifulSoup as bs

data_for_website = {}

# In[2]:


# Setup splinter
def init_chrome_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

# ### NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[3]:

def Mission_to_Mars():
    browser = init_chrome_browser()
    browser.visit('https://mars.nasa.gov/news/')
    title = browser.find_by_css('div.content_title a').text
    paragraph = browser.find_by_css('div.article_teaser_body').text
    data_for_website['news_title'] = title
    data_for_website['news_paragraph'] = paragraph
    return data_for_website


def mars_facts():
    
     # Visit the Mars Facts webpage
    df_mars = pd.read_html('https://space-facts.com/mars/')[0].rename(columns={0: 'Parameters', 1: 'values'})
    df_earth = pd.read_html('https://space-facts.com/earth/')[0].rename(columns={0: 'Parameters', 1: 'values'})
    df_comparison = df_earth.merge(df_mars, on='Parameters', how='left')
    df_comparison_renamed = df_comparison.rename(columns={'Parameters': 'Description', 'values_x': 'Mars', 'values_y': 'Earth'})
    #df.head()
    mars_facts = df_comparison_renamed.to_html(classes='table table-striped', index=False).replace('<tr style="text-align: right;">','<tr>')
    data_for_website['mars_facts'] = mars_facts
    return data_for_website




def featured_image():
    data_for_website['featured_image'] = 'https://spaceimages-mars.com/image/featured/mars2.jpg'
    return data_for_website


def get_hemisphere_data():
    browser = init_chrome_browser()
    base_url = 'https://marshemispheres.com'

    browser.visit(base_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    titles=[]
    img_urls=[]

    for item in items:
        title = item.find('h3').text
        titles.append(title)
        
        url = item.find('a')['href']
        image_url = base_url + "/" + url
        
        browser.visit(image_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_original= soup.find('div',class_='downloads')
        img_url=img_original.find('a')['href']
        image_full_url = base_url + "/" + img_url
        img_data=dict({'title':title, 'img_url':image_full_url})
        img_urls.append(img_data)
    data_for_website['hemi_urls_and_titles'] = img_urls
    return data_for_website
    
