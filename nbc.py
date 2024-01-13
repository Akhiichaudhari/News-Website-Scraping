import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn import preprocessing
import csv

url = 'https://economictimes.indiatimes.com/'
r = requests.get(url)
htmlcontent = r.content
#print(htmlcontent)

# Parse HTML
soup = BeautifulSoup(htmlcontent, 'html.parser')
sections = soup.find('ul', class_='tabs')
section_list = [] # get all the sections from website
if sections :
    section = sections.find_all('li')
    for item in section:
            section_list.append(item.text)
#print('Section list is ', section_list)
section_list = section_list[1:]
    
print('section list ', section_list)
alt_url = 'https://economictimes.indiatimes.com/industrynews.cms?msid=' #url to alter
url_lists = []
msid = ['13359412','13358259','13358759','13358350','81585238','13357688','13357549','13358050','107115','13356992','13354120','18606290','13357212','78404305','13354103','13353990']
# for loop creates each section link and stored it in alt_url list
for i in msid :
    sections = soup.find('li', {'data-msid' :i})
    section_list.append(sections.get_text())
    alt_url = 'https://economictimes.indiatimes.com/industrynews.cms?msid='
    alt_url += str(i)
    #print(alt_url)
    url_lists.append(alt_url)
#print(url_lists)

# Creating lists for news title and link for news description
title_lists = []
link_lists = []
class_lists = []
for i in range(len(url_lists)) :
    r = requests.get(url_lists[i])
    b = BeautifulSoup(r.content, 'lxml')
    news = b.find_all('h4')
    #print(news)
    for h4_tag in news:
        a_tag = h4_tag.find('a')
        link = a_tag['href']
        text = a_tag.get_text(strip=True)
        title_lists.append(text)
        class_lists.append(section_list[i])
        link_lists.append(link)
        #print('text is :', text)
        #print('link is :', link)
print('---------------')
#print('length of section lists ', len(class_lists))
#print('title_lists ',title_lists)
#print('length of title list is ', len(title_lists))
#print('link_list is ',link_lists)
#print('length of link list is ', len(link_lists))
print('=================================')

news_desc = []
for i in range(len(url_lists)) :
    t = requests.get(url_lists[i])
    #print(t)
    soup = BeautifulSoup(t.text, 'html.parser')
    news = soup.find_all('h4')
    #print('news ', news)
    for h4_tag in news:
        a_tag = h4_tag.find('a')
        link = a_tag['href']
        text = a_tag.get_text(strip=True)
        #print('link ----', link)
        response = requests.get(link)

    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the <div> element with the specified attributes
            div_element = soup.find('div', class_='artText', attrs={'data-brcount': lambda x: x.isdigit() if x else False})

            # Check if the <div> element is found
            if div_element:
                # Extract the text from the <div> element
                div_text = div_element.get_text(strip=True)
                news_desc.append(div_text)
                #print(div_text)
            else:
                # Appending NA for none return type
                news_desc.append('NA')
        else:
            print(f"Failed to fetch the page. Status code: ")

print('length of news desc is ', len(news_desc))
print('length of title', len(title_lists))
print('length of desc ', len(news_desc))
print('length of classes ', len(class_lists))
# Creating dataframe with columns news_title, news_description and class
data= {'Title' : title_lists, 'Desc' : news_desc, 'Section' : class_lists}
df = pd.DataFrame(data)
# print(df.head())
#############################


# Converting column Section with string into numerical value as name class
label_encoder = preprocessing.LabelEncoder()
df['class'] = label_encoder.fit_transform(df['Section'])
print('Final dataset')
print(df)
df.to_csv('Na_data.csv')