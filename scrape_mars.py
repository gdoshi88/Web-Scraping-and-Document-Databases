from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from pprint import pprint


def scrape():
    executable_path = {
        'executable_path': '/Users/Pariah/Downloads/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=True)

    nasa_mars_title, nasa_mars_paragraph = nasa_mars_news(browser)

    results = {
        'title': nasa_mars_title,
        'paragraph': nasa_mars_paragraph,
        'featured_image': featured_img_url_two(browser),
        'facts': df(),
        'hemispheres': hemisphere_image_urls(browser)
    }

    browser.quit()
    return results


def nasa_mars_news(browser):
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)
    time.sleep(1)

    html_nasa_mars = browser.html
    soup = bs(html_nasa_mars, "html.parser")

    nasa_mars_title = soup.find('div', class_="content_title").get_text()
    nasa_mars_paragraph = soup.find(
        'div', class_="article_teaser_body").get_text()

    return nasa_mars_title, nasa_mars_paragraph


def featured_img_url_two(browser):
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(jpl_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_img_url_raw = soup.find(
        "div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_img_url_raw.split("'")[1]

    # In[260]:

    featured_img_base = "https://www.jpl.nasa.gov"
    featured_img_url_two = featured_img_base + featured_img_url

    return featured_img_url_two


def df():
    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)

    df = tables[0]
    df[['Mars - Earth Comparison', 'Mars']]
    df.set_index('Mars - Earth Comparison', inplace=True)
    df.to_html()
    df.replace('\n', '')

    return df


def hemisphere_image_urls(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')
    hemi_strings = []
    links = hemi_soup.find_all('h3')

    for hemi in links:
        hemi_strings.append(hemi.text)

    hemi_strings

    hemisphere_image_urls = []
    for hemi in hemi_strings:
        hemi_dict = {}
        browser.click_link_by_partial_text(hemi)
        hemi_dict["img_url"] = browser.find_by_text('Sample')['href']
        hemi_dict["title"] = hemi
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

    return hemisphere_image_urls
