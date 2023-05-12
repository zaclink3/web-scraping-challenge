from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'

    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    news_title = news_soup.find('div',class_='content_title').text.strip()
    news_paragraph = news_soup.find('div', class_='article_teaser_body').text.strip()

    image_url = 'https://spaceimages-mars.com/'

    browser.visit(image_url)
    browser.find_by_tag('button')[1].click()

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = img_soup.find('img',class_='fancybox-image').get('src')

    img_url = f'https://spaceimages-mars.com/{featured_image_url}'

    facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(facts_url, header=0, index_col=0)[0]
    html_table = tables.to_html(
        classes='table table-striped', border=0).replace('\n', '')

    hemi_url = 'https://marshemispheres.com/'
    response = requests.get(hemi_url)
    hemi_soup = BeautifulSoup(response.text, 'html.parser')

    hemisphere_links = hemi_soup.find_all('div', class_='description')
    data = []

    for link in hemisphere_links:
        title = link.find('h3').text
        hemisphere_url = hemi_url + link.find('a')['href']
        hemisphere_response = requests.get(hemisphere_url)
        hemisphere_soup = BeautifulSoup(hemisphere_response.text, 'html.parser')
        hemi_img_url = hemi_url + hemisphere_soup.find('img', class_='wide-image')['src']
        data.append({'title': title, 'img_url': img_url})


    mars_website_db = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image_url': featured_image_url,
        'html_table': html_table,
        'hemisphere_data': data
    }

    browser.quit()

    return mars_website_db