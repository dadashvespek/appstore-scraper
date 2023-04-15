import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from context_words import context_words
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
def get_text_or_na(element):
    return element.text if element else 'NA'

def get_recommended_app_urls(soup):
    recommended_apps = soup.select('a.Si6A0c.nT2RTe')
    app_names = [app.select_one('span.DdYX5').text for app in recommended_apps]
    app_urls = ['https://play.google.com' + app['href'] for app in recommended_apps]
    return app_names, app_urls

def get_app_urls(keyword, url_template):
    search_url = url_template.format(keyword)
    response = requests.get(search_url,verify=False,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    app_links = soup.select('a.Si6A0c.Gy4nib')
    app_names = [link.find(class_='DdYX5').text for link in app_links]
    app_urls = ['https://play.google.com' + link['href'] for link in app_links]

    return app_names, app_urls

def get_app_data(app_url):
    response = requests.get(app_url,headers=headers,verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    app_name = get_text_or_na(soup.select_one('h1[itemprop="name"] > span'))
    developer_element = soup.select_one('div.tv4jIf > div.Vbfug.auoIOc > a')
    developer = get_text_or_na(developer_element.select_one('span'))

    rating_element = soup.select_one('div.TT9eCd')
    rating = rating_element.text[:-1] if rating_element else 'NA'

    reviews = get_text_or_na(soup.select_one('div.w7Iutd > div.wVqUob > div.g1rdde'))
    installs = get_text_or_na(soup.select_one('div.w7Iutd > div.wVqUob > div.ClM7O'))
    last_updated = get_text_or_na(soup.select_one('div.xg1aie'))
    developer_link = 'https://play.google.com' + developer_element['href'] if developer_element else 'NA'
    
    app_features = soup.select_one('div.tv4jIf > div.ulKokd > div')
    contains_ads = 'Contains ads' in app_features.text if app_features else 'NA'
    in_app_purchases = 'In-app purchases' in app_features.text if app_features else 'NA'

    app_data = {
        'app_name': app_name,
        'developer': developer,
        'rating': rating,
        'reviews': reviews,
        'installs': installs,
        'last_updated': last_updated,
        'developer_link': developer_link,
        'contains_ads': contains_ads,
        'in_app_purchases': in_app_purchases,
        'app_url': app_url
    }
    print(app_data)
    return app_data




def process_app(app_name, app_url, app_data_df, context_words):
    if app_name not in app_data_df['app_name'].values and any(word.lower() in app_name.lower() for word in context_words):
        app_data = get_app_data(app_url)
        new_app_data_df = pd.DataFrame([app_data])
        app_data_df = pd.concat([app_data_df, new_app_data_df], ignore_index=True)
        app_data_df.to_csv('data.csv', index=False)

        # Get recommended apps from the current app page
        recommended_app_names, recommended_app_urls = get_recommended_app_urls(BeautifulSoup(requests.get(app_url).text, 'html.parser'))
        for recommended_app_name, recommended_app_url in zip(recommended_app_names, recommended_app_urls):
            app_data_df = process_app(recommended_app_name, recommended_app_url, app_data_df, context_words)

    return app_data_df


def main(keywords):
    data_file = 'data.csv'

    if os.path.exists(data_file):
        app_data_df = pd.read_csv(data_file)
    else:
        app_data_df = pd.DataFrame(columns=['app_name', 'developer', 'rating', 'reviews', 'installs', 'last_updated', 'developer_link', 'contains_ads', 'in_app_purchases', 'app_url'])

    url_template = 'https://play.google.com/store/search?q={}&c=apps'

    for keyword in keywords:
        app_names, app_urls = get_app_urls(keyword, url_template)

        for app_name, app_url in zip(app_names, app_urls):
            app_data_df = process_app(app_name, app_url, app_data_df, context_words)

        app_data_df.to_csv(data_file, index=False)

    return app_data_df


keywords = ['fitness', 'nutrition']  # Add more keywords if needed
app_data_df = main(keywords)
print(app_data_df)