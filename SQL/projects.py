# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: Qin_LilyHeAsamiko
"""
import sqlite3
import requests
from lxml import etree
import re
from io import StringIO
import numpy as np
import csv
import time
import pandas as pd

def get_film_list(file):
    with open(file,'r', encoding='utf-8') as f:
        contents = f.readlines()
    filmList = {}
    filmList[contents[0].replace('\n','')] = contents[1].replace('\n',' ')
    for ci in range(2,len(contents)-1):
        if contents[ci] == '\n':
            if ci ==  len(contents)-2:
                filmList[contents[ci+1].replace('\n','')] = ' '
            else:
                filmList[contents[ci+1].replace('\n','')] = contents[ci+2].replace('\n',' ')
    return filmList

def get_SSIF_data(url = "https://mubi.com/en/hk/films",filmName='monkey-man'):
    '''
    example:    
    <div class="css-121byfp ekc9mtp7"><div class="css-3xflg8 ekc9mtp8"><div class="css-phe038 egp731j0"><span class="css-c0j9gy egp731j1">Directed by</span> <span class="css-o3x71s egp731j2"><span class="css-in3yi3 e1glieyg0"><a class="css-rv1qtj e1y82vqv0" color="#FFFFFF" itemscope="" itemprop="director" itemtype="http://schema.org/Person" href="/en/cast/dev-patel"><meta itemprop="url" content="https://mubi.com/cast/dev-patel"><span itemprop="name">Dev Patel</span></a> </span></span></div><div class="css-1ktktz5 ekc9mtp11">United States, Canada, <span itemprop="dateCreated">2024</span></div><div class="css-138ayl4 ekc9mtp12">Action, Thriller</div><ul class="css-130ofai e1z00vji1"><ul class="css-91d7h3 e1z00vji2"><div class="css-1sylyko e1z00vji3"><div class="css-1tzeee1 e1z00vji0"><svg viewBox="0 0 17 16" width="18px" class="css-13o7eu2 e101vm530"><path d="M8.2 0a8.1 8.1 0 018.22 8c0 4.42-3.68 8-8.21 8A8.1 8.1 0 010 8c0-4.42 3.67-8 8.2-8zm.27 3.52a.74.74 0 10-1.47 0v4.92c0 .2.08.38.21.52l3.52 3.51a.74.74 0 001.04-1.04l-3.3-3.3V3.52z" fill="#FFFFFF" fill-rule="evenodd"></path></svg></div></div><div class="css-1tzeee1 e1z00vji0"><time datetime="PT113M" itemprop="duration">113</time></div></ul></ul></div><div class="css-30qmm7 ekc9mtp13"><section class="css-dq39gh ekc9mtp15"><div class="css-1pvjnn3 e1beraew0 appear-enter-done"><h2 class="css-pjo7jy ekc9mtp16">Synopsis</h2><div itemprop="description" class="css-dykg55 ekc9mtp17"><p>A young man ekes out a meager living in an underground fight club where, night after night, wearing a gorilla mask, he’s beaten bloody by more popular fighters for cash. After years of suppressed rage, he discovers a way to infiltrate the enclave of the city’s sinister elite.</p></div></div></section><section class="css-dq39gh ekc9mtp15"><div class="css-1px1d67 e1z0oclo0"><span>This film is not currently playing on MUBI, but many other great films are. See what’s <a class="css-vjbv9p e1z0oclo1" href="/en/hk/showing">now showing &gt;</a></span></div></section></div></div>    #__next > div.css-8utsz3.ehgydxz0 > div > ul > li:nth-child(1) > div > div > div.css-1towox2.efr5iit1 > div.css-zipjdp.efr5iit5 > a
    director: /html/body/div[1]/div[3]/div[2]/div[1]/div[5]/div/div[2]/section/div[2]/div/div/div[3]/div[1]/div[1]/span[2]/span/a/span
    //*[@id="FilmDetailsAboutFilm"]/div[3]/div[1]/div[1]/span[2]/span/a/span
    Info: /html/body/div[1]/div[3]/div[2]/div[1]/div[5]/div/div[2]/section/div[2]/div/div/div[3]/div[1]/div[2]
    //*[@id="FilmDetailsAboutFilm"]/div[3]/div[1]/div[2]    
    Genre: /html/body/div[1]/div[3]/div[2]/div[1]/div[5]/div/div[2]/section/div[2]/div/div/div[3]/div[1]/div[3]
    //*[@id="FilmDetailsAboutFilm"]/div[3]/div[1]/div[3]
    Length:/html/body/div[1]/div[3]/div[2]/div[1]/div[5]/div/div[2]/section/div[2]/div/div/div[3]/div[1]/ul/ul/div[2]/time
    //*[@id="FilmDetailsAboutFilm"]/div[3]/div[1]/ul/ul/div[2]/time
    
    Introduction:
        "film":{"films":{"402098":{"id":402098,"slug":"monkey-man","title":"Monkey Man","title_locale":"en-US","original_title":"Monkey Man","year":2024,"duration":113,"
    Info and ratings:
        "average_colour_hex":"662926","trailer_url":"https://trailers.mubicdn.net/402098/t-monkey-man_en_us_4012.9889999999996_1920_1080_1706332147.mp4","trailer_id":101166,"popularity":23,"web_url":"https://mubi.com/films/monkey-man","genres":["Action","Thriller"],"average_rating":3.3,"average_rating_out_of_ten":6.5,"number_of_ratings":260,"mubi_release":false
        "trailer_url":"https://trailers.mubicdn.net/402098/t-monkey-man_en_us_4012.9889999999996_1920_1080_1706332147.mp4","trailer_id":101166,"popularity":23,"web_url":"https://mubi.com/films/monkey-man","genres":["Action","Thriller"],"average_rating":3.3,"average_rating_out_of_ten":6.5,"number_of_ratings":260,"mubi_release":false,"should_use_safe_still":false,"still_url":"https://images.mubicdn.net/images/film/402098/cache-957302-1712303932/image-w1280.jpg","title_upcase":"MONKEY MAN","critic_review_rating":3.789473684210526,"content_rating":{"label":"not_rated","rating_code":"NOT RATED","description":"This film has not yet been rated, and may contain adult material.","icon_url":null,"label_hex_color":"e05d04"},"short_synopsis":"A young man ekes out a meager living in an underground fight club where, night after night, wearing a gorilla mask, he’s beaten bloody by more popular fighters for cash. After years of suppressed rage, he discovers a way to infiltrate the enclave of the city’s sinister elite."
    Staff:
        "cast":
        [{"id":15335,"name":"Dev Patel","name_upcase":"DEV PATEL","slug":"dev-patel","credits":"Director, Screenplay, Cast, Producer","image_url":"https://assets.mubicdn.net/images/cast_member/15335/image-w240.jpg?1482223649"},
        {"id":22222,"name":"Sharlto Copley","name_upcase":"SHARLTO COPLEY","slug":"sharlto-copley","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/22222/image-w240.jpg?1478101707"},
        {"id":624733,"name":"Sobhita Dhulipala","name_upcase":"SOBHITA DHULIPALA","slug":"sobhita-dhulipala","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/624733/image-w240.jpg?1576200544"},
        {"id":152702,"name":"Vipin Sharma","name_upcase":"VIPIN SHARMA","slug":"vipin-sharma","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/152702/image-w240.jpg?1524916771"},
        {"id":459343,"name":"Paul Angunawela","name_upcase":"PAUL ANGUNAWELA","slug":"paul-angunawela","credits":"Screenplay","image_url":"https://assets.mubicdn.net/images/cast_member/459343/image-w240.jpg?1712203988"},
        {"id":33420,"name":"John Collee","name_upcase":"JOHN COLLEE","slug":"john-collee","credits":"Screenplay","image_url":"https://assets.mubicdn.net/images/cast_member/33420/image-w240.jpg?1463180470"},
        {"id":57943,"name":"Sharone Meir","name_upcase":"SHARONE MEIR","slug":"sharone-meir","credits":"Cinematography","image_url":"https://assets.mubicdn.net/images/cast_member/57943/image-w240.jpg?1518123131"},
        {"id":210548,"name":"Jed Kurzel","name_upcase":"JED KURZEL","slug":"jed-kurzel","credits":"Music","image_url":"https://assets.mubicdn.net/images/cast_member/210548/image-w240.jpg?1504755721"},
        {"id":101535,"name":"Dávid Jancsó","name_upcase":"DÁVID JANCSÓ","slug":"david-jancso","credits":"Editing","image_url":"https://assets.mubicdn.net/images/cast_member/101535/image-w240.jpg?1490580305"},
        {"id":1056310,"name":"Jomon Thomas","name_upcase":"JOMON THOMAS","slug":"jomon-thomas-1","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/1056310/image-w240.jpg?1712204045"},
        {"id":494758,"name":"Jordan Peele","name_upcase":"JORDAN PEELE","slug":"jordan-peele","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/494758/image-w240.jpg?1613675653"},
        {"id":676060,"name":"Win Rosenfeld","name_upcase":"WIN ROSENFELD","slug":"win-rosenfeld","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/676060/image-w240.jpg?1659681656"},
        {"id":629991,"name":"Ian Cooper","name_upcase":"IAN COOPER","slug":"ian-cooper","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/629991/image-w240.jpg?1613686647"},
        {"id":27820,"name":"Basil Iwanyk","name_upcase":"BASIL IWANYK","slug":"basil-iwanyk","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/27820/image-w240.jpg?1463176518"},
        {"id":197634,"name":"Erica Lee","name_upcase":"ERICA LEE","slug":"erica-lee","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/197634/image-w240.jpg?1489998903"},
        {"id":39450,"name":"Christine Haebler","name_upcase":"CHRISTINE HAEBLER","slug":"christine-haebler","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/39450/image-w240.jpg?1559939794"},
        {"id":614899,"name":"Anjay Nagpal","name_upcase":"ANJAY NAGPAL","slug":"anjay-nagpal","credits":"Producer","image_url":"https://assets.mubicdn.net/images/cast_member/614899/image-w240.jpg?1610680905"},
        {"id":534542,"name":"Jonathan Fuhrman","name_upcase":"JONATHAN FUHRMAN","slug":"jonathan-fuhrman","credits":"Executive Producer","image_url":"https://assets.mubicdn.net/images/cast_member/534542/image-w240.jpg?1602307346"},
        {"id":1145902,"name":"Natalya Pavchinskya","name_upcase":"NATALYA PAVCHINSKYA","slug":"natalya-pavchinskya","credits":"Executive Producer","image_url":"https://assets.mubicdn.net/images/cast_member/1145902/image-w240.jpg?1712204052"},{"id":149831,"name":"Aaron L. Gilbert","name_upcase":"AARON L. GILBERT","slug":"aaron-l-gilbert","credits":"Executive Producer","image_url":"https://assets.mubicdn.net/images/cast_member/149831/image-w240.jpg?1530432797"},{"id":446206,"name":"Andria Spring","name_upcase":"ANDRIA SPRING","slug":"andria-spring","credits":"Executive Producer","image_url":"https://assets.mubicdn.net/images/cast_member/446206/image-w240.jpg?1712203753"},{"id":1145903,"name":"Alison-Jane Roney","name_upcase":"ALISON-JANE RONEY","slug":"alison-jane-roney","credits":"Executive Producer","image_url":"https://assets.mubicdn.net/images/cast_member/1145903/image-w240.jpg?1712203900"},{"id":612330,"name":"Steven Thibault","name_upcase":"STEVEN THIBAULT","slug":"steven-thibault","credits":"Executive Producer","image_url":"https://assets.mubicdn.net/images/cast_member/612330/image-w240.jpg?1614736532"},{"id":306862,"name":"Pitobash","name_upcase":"PITOBASH","slug":"pitobash","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/306862/image-w240.jpg?1629857973"},{"id":282916,"name":"Sikander Kher","name_upcase":"SIKANDER KHER","slug":"sikander-kher","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/282916/image-w240.jpg?1712202758"},{"id":282854,"name":"Ashwini Khalsekar","name_upcase":"ASHWINI KHALSEKAR","slug":"ashwini-khalsekar","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/282854/image-w240.jpg?1712202746"},{"id":1021118,"name":"Adithi Kalkunte","name_upcase":"ADITHI KALKUNTE","slug":"adithi-kalkunte","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/1021118/image-w240.jpg?1712204002"},
        {"id":295710,"name":"Makarand Deshpande","name_upcase":"MAKARAND DESHPANDE","slug":"makarand-deshpande","credits":"Cast","image_url":"https://assets.mubicdn.net/images/cast_member/295710/image-w240.jpg?1545816205"}],
       "industry_events":[{"name":"SXSW Film Festival","slug":"sxsw","year":2024,"entries":["2024"],"logo_url":"https://images.mubicdn.net/images/industry_event/10/cache-222798-1494527060/logo-small_black.png","logo_url_white":"https://images.mubicdn.net/images/industry_event/10/cache-222798-1494527060/logo-large_white.png","event_type":"generic"},{"name":"Shanghai International Film Festival","slug":"shanghai","year":2024,"entries":["2024"],"logo_url":"https://images.mubicdn.net/images/industry_event/184/cache-225362-1495547218/logo-small_black.png","logo_url_white":"https://images.mubicdn.net/images/industry_event/184/cache-225362-1495547218/logo-large_white.png","event_type":"generic"},{"name":"New Horizons International Film Festival","slug":"new-horizons","year":2024,"entries":["2024"],"logo_url":"https://images.mubicdn.net/images/industry_event/372/cache-979240-1719495432/logo-small_black.png","logo_url_white":"https://images.mubicdn.net/images/industry_event/372/cache-979240-1719495432/logo-large_white.png","event_type":"generic"}],"notebook_posts":[],"directors":[{"name":"Dev Patel","name_upcase":"DEV PATEL","slug":"dev-patel"}],"historic_countries":["United States","Canada"],"optimised_trailers":[{"url":"https://trailers.mubicdn.net/402098/optimised/240p-t-monkey-man_en_us_4012.9889999999996_1920_1080_1706332147.mp4","profile":"240p"},{"url":"https://trailers.mubicdn.net/402098/optimised/720p-t-monkey-man_en_us_4012.9889999999996_1920_1080_1706332147.mp4","profile":"720p"},{"url":"https://trailers.mubicdn.net/402098/optimised/1080p-t-monkey-man_en_us_4012.9889999999996_1920_1080_1706332147.mp4","profile":"1080p"}],"mubi_go_highlighted":false,"cast_members_count":29,"industry_events_count":3,"comments_count":45,"episode":null,"portrait_image":null,"consumable":null,"press_quote":null,"star_rating":null,"award":null,"content_warnings":[]
    length:
        {"pageProps":{"initFilm":{"id":402098,"slug":"monkey-man","title":"Monkey Man","title_locale":"en-US","original_title":"Monkey Man","year":2024,"duration":113,
        
    <div class="css-1j6p37b errpx8q7"><div class="css-bzntbt errpx8q9"><div class="css-zm3qx2 e1a6v7fs0"><div class="css-1thr8qj e1a6v7fs1"><svg viewBox="0 0 22 20" fill="#FFFFFF" width="20px" class="css-13o7eu2 e101vm530"><path d="M21.15 7.6a.64.64 0 0 0-.6-.45l-7.05-.14L11.2.43a.63.63 0 0 0-1.2 0L7.67 7l-7.05.14a.63.63 0 0 0-.59.44c-.08.26 0 .54.22.7l5.62 4.22-2.04 6.67a.64.64 0 0 0 .97.71l5.79-3.99 5.8 3.99a.64.64 0 0 0 .73-.01c.22-.16.3-.44.23-.7l-2.04-6.67 5.62-4.21c.21-.17.3-.45.22-.7"></path></svg> <div class="css-1g9erbj e1a6v7fs2">6.5</div><div class="css-3x4005 e1a6v7fs3">/10</div></div><div class="css-1kagd7v e1a6v7fs4">260<!-- --> <!-- -->Ratings</div></div></div></div>
    score: /html/body/div[1]/div[3]/div[2]/div[1]/div[3]/div[3]/div/div[2]/div/div/div[1]/div[1]
    //*[@id="__next"]/div[3]/div[2]/div[1]/div[3]/div[3]/div/div[2]/div/div/div[1]/div[1]
    rating: /html/body/div[1]/div[3]/div[2]/div[1]/div[3]/div[3]/div/div[2]/div/div/div[2]
    //*[@id="__next"]/div[3]/div[2]/div[1]/div[3]/div[3]/div/div[2]/div/div/div[2]
    '''
    #filmName = filmName.encode('utf-8').decode('latin-1')
    filmName = filmName.replace('é','e').replace('ô','o').replace('á','a').replace('ó','o').replace('í','i').replace('ñ','n').replace('ç','c').replace('ú','u')
    URL = '/'.join([url,filmName])
    print(URL)
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Accept': 'text/plain',
    'Connection': 'keep-alive',
    'Origin': URL,
    'Referer': URL+'/',
    # More headers like User-Agent, etc.
    }
    try:
        response = requests.get(url=URL,headers=headers)
        print(response.status_code)
        if response.status_code >=200 and response.status_code < 300:   
            print(response.text) # 打印请求成功的网页源码，和在网页右键查看源代码的内容一样的
            #soup = BeautifulSoup(response.text, 'html.parser')
            #print(soup)
            #print(soup.find_all(attribute = {'meta property'}))
        #    parr = re.compile(r'<span class="title b_t">.*?(.*?)</span>')
        #    poem = re.findall(parr,response.text)  
            film_id = re.findall(r'"film":{"films":.*?{"id":.*?(.*?),"slug":',response.text,re.DOTALL)[0]
            film_name = re.findall(r'"film":{"films":.*?{"id":.*?,"title":.*?(.*?),"title_locale":',response.text,re.DOTALL)[0]
            film_genre = re.findall(r'"film":{"films":.*?{"id":.*?,"genres":(.*?),"average_rating":',response.text,re.DOTALL)[0]
            film_duration = re.findall(r'"film":{"films":.*?{"id":.*?,"duration":(.*?),"stills":',response.text,re.DOTALL)[0]
            film_year = re.findall(r'"film":{"films":.*?{"id":.*?,"year":(.*?),"duration":',response.text,re.DOTALL)[0]
            film_cast = {}
            film_cast_id = re.findall(r'{"id":(\d*?),"name":',response.text,re.DOTALL)
            film_cast_name = re.findall(r'"cast":.*?,"name":.*?"([A-Z][a-z]+[\w\s]*)+","name_upcase":',response.text,re.DOTALL)[0]
            #film_cast_name = re.findall(r',"name":"(.*?)","name_upcase":',response.text,re.DOTALL)
            film_cast_position = re.findall(r'"credits":(.*?),"image_url":',response.text,re.DOTALL)
            film_intro_url = URL
            if len(film_cast_id) == len(film_cast_name) == len(film_cast_position):
                film_cast_zip = zip(film_cast_id,film_cast_name,film_cast_position)
                for item in enumerate(zip(film_cast_id,film_cast_name,film_cast_position)):
                        film_cast[str(item[0])]={"id":item[1][0],"name":item[1][1],"position":item[1][2]}
                print(film_cast_id,film_cast_name,film_cast_position)
            else:
                print(len(film_cast_id),len(film_cast_name),len(film_cast_position))
                film_cast = [film_cast_id,film_cast_name,film_cast_position]
            film_historic_countries = re.findall(r',"historic_countries":(.*?),"optimised_trailers":',response.text,re.DOTALL)[0]
            film_scores = re.findall(r'"average_rating_out_of_ten":(.*?),"number_of_ratings":',response.text,re.DOTALL)[0]
            film_ratings = re.findall(r'"number_of_ratings":(.*?),"mubi_release":false',response.text,re.DOTALL)[0]
            film_short_synopsis = re.findall(r'"short_synopsis":(.*?),"short_synopsis_html"',response.text,re.DOTALL)[0]
            film_trailor_url = re.findall(r'"trailer_url":(.*?),"trailer_id"',response.text,re.DOTALL)[0]
        #    html = etree.HTML(response.text)       
        #    print(html.xpath('//*[@id="__next"]/div[6]/div/ul/li[1]/div/div/div[2]/div[2]/a'))#//*[@id="__next"]/div[4]/div/ul/li/div/div/div[2]/div[2]/a        
            return [film_id,film_name,film_genre,film_duration,film_year,film_historic_countries,film_scores,film_ratings,film_cast,film_short_synopsis,film_trailor_url,film_intro_url]
        else:
            print('URL:',URL)
            time.sleep(1)
            get_SSIF_data(url = url,filmName=filmName)
            time.sleep(1)
            return ('DecodeError!'*11).split('!')[:-1]+[URL]
    except Exception as e:
        print("Process failed: ", e)
        return ('DecodeError!'*11).split('!')[:-1]+[URL]
#def get_SSIF_awards(url = "https://www.imdb.com/event/ev0000605",year = "2024",surfix = "1/?ref_=ev_eh"):
def get_SSIF_awards(url = "https://www.siff.com/english/content?aid=101240622235844574349209197613061422"):
    '''
    example:    
    <div class="event-widgets__award-name">Golden Goblet</div>
    <div class="event-widgets__award-name">Golden Goblet</div>
    #center-3-react > div > div > div:nth-child(1) > div
    //*[@id="center-3-react"]/div/div/div[1]/div
    /html/body/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div/div[1]/div
    '''
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Accept': 'text/plain',
    'Connection': 'keep-alive',
    'Origin': url,
    'Referer': url+'/',
    # More headers like User-Agent, etc.
    }     
    response=requests.get(url=url,headers=headers) 
#    html0 = etree.parse(response.text,parser = etree.HTMLParser(encoding='gbk',recover=True))
#    html = etree.parse(StringIO(response0.text))
    html = etree.HTML(response.text)
    #print(html0.xpath('//body/table/tbody/tr[954]/td[2]/text()'))
    names0 = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/*//p/span/strong')
    names1 = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/*//p/strong')
    details = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/p/span')
    awards = {}
    if len(names0)+len(names1) >= len(details):
        names = names0+names1
        nc = names.copy()
        dc = details.copy()
        try:
            for itemi in range(len(nc)-1):
                if nc[itemi].text is None or nc[itemi].text == '\xa0':
                    nc.remove(nc[itemi])
                if '\xa0' in nc[itemi].text and '\xa0' in nc[itemi+1].text:
                    nc[itemi].text = nc[itemi].text.replace('\xa0',' ') + nc[itemi+1].text.replace('\xa0',' ')
                    nc.remove(nc[itemi+1])
            for itemj in range(len(dc)):
                if dc[itemj].text is None:
                    dc.remove(dc[itemj])
                elif '\xa0' in dc[itemj].text:
                    dc[itemj].text = dc[itemj].text.replace('\xa0',' ')
                dc[itemj] = dc[itemj].text
            for itemij in range(len(nc)):
                if '\xa0' in nc[itemij].text:
                    nc.remove(nc[itemij])
                nc[itemij] = nc[itemij].text
            if "Bakur Bakuradze for SNOWFLAKES IN MY YARD (Georgia/Russia)" not in dc[2]:
                dc.insert(2,"Bakur Bakuradze for SNOWFLAKES IN MY YARD (Georgia/Russia)")        
            if "HUANG Xiaoming in DON'T WORRY, BE HAPPY (China) directed by WEI Shujun" not in dc[3]:    
                dc.insert(3,"HUANG Xiaoming in DON'T WORRY, BE HAPPY (China) directed by WEI Shujun")
        except:
            print(itemi,itemj)
        for i in enumerate(dc):
            if nc[i[0]] is not None and dc[i[0]] is not None:
                awards[str(nc[i[0]])] = dc[i[0]]
    return awards

def get_SSIF_awards_by_re(url = "https://www.siff.com/english/content?aid=101240622235844574349209197613061422"):
    '''
    example:    
    <div class="event-widgets__award-name">Golden Goblet</div>
    <div class="event-widgets__award-name">Golden Goblet</div>
    #center-3-react > div > div > div:nth-child(1) > div
    //*[@id="center-3-react"]/div/div/div[1]/div
    /html/body/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div/div[1]/div
    '''
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Accept': 'text/plain',
    'Connection': 'keep-alive',
    'Origin': url,
    'Referer': url+'/',
    # More headers like User-Agent, etc.
    }     
    response=requests.get(url=url,headers=headers) 
#    html0 = etree.parse(response.text,parser = etree.HTMLParser(encoding='gbk',recover=True))
#    html = etree.parse(StringIO(response0.text))
    html = etree.HTML(response.text)
    #print(html0.xpath('//body/table/tbody/tr[954]/td[2]/text()'))
    names0 = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/*//p/span/strong')
    names1 = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/*//p/strong')
    details = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/p/span')
    awards = {}
    Awards = {}
    if len(names0)+len(names1) >= len(details):
        names = names0+names1
        nc = names.copy()
        dc = details.copy()
        try:
            for itemi in range(len(nc)-1):
                if nc[itemi].text is None or nc[itemi].text == '\xa0':
                    nc.remove(nc[itemi])
                if '\xa0' in nc[itemi].text and '\xa0' in nc[itemi+1].text:
                    nc[itemi].text = nc[itemi].text.replace('\xa0',' ') + nc[itemi+1].text.replace('\xa0',' ')
                    nc.remove(nc[itemi+1])
        except:
            print(itemi)
        try:
            for itemj in range(len(dc)):
                dc[itemj] = dc[itemj].text
        except:
            print(itemj)
        try:
            for itemj in range(len(dc)):
                if dc[itemj] is None:
                    dc.remove(dc[itemj])
                if '\xa0' in dc[itemj]:
                    dc[itemj] = dc[itemj].replace('\xa0',' ')                
        except:
            print(itemj)
        try:
            for itemij in range(len(nc)):
                nc[itemij] = nc[itemij].text
        except:
            print(itemij)
        try:
            for itemij in range(len(nc)):
                if '\xa0' in nc[itemij]:
                    nc.remove(nc[itemij])                
            if "Bakur Bakuradze for SNOWFLAKES IN MY YARD (Georgia/Russia)" not in dc[2]:
                dc.insert(2,"Bakur Bakuradze for SNOWFLAKES IN MY YARD (Georgia/Russia)")        
            if "HUANG Xiaoming in DON'T WORRY, BE HAPPY (China) directed by WEI Shujun" not in dc[3]:    
                dc.insert(3,"HUANG Xiaoming in DON'T WORRY, BE HAPPY (China) directed by WEI Shujun")
        except:
            print(itemij)
        for i in enumerate(dc):
            if nc[i[0]] is not None and dc[i[0]] is not None:
                awards[str(nc[i[0]])] = dc[i[0]]
                Awards[str(nc[i[0]])] = {}
                #Awards[str(nc[i[0]])]['winner_name'] = re.findall(r'('+'([A-Z]*?[a-z]*?+[\w\s]*)+?'+')'+'for*?in*?',dc[i[0]],re.DOTALL)
                #print(re.findall(r'(.*?)'+' in.*?',dc[i[0]],re.DOTALL))
                if re.findall(r'(.*?)'+' in.*?',dc[i[0]],re.DOTALL) or re.findall(r'(.*\s)'+'for?',dc[i[0]],re.DOTALL) and re.findall('(.*?) directed by',dc[i[0]],re.DOTALL):
                    Awards[str(nc[i[0]])]['actor/actress_name'] = re.findall(r'(.*\s)'+'in?',dc[i[0]],re.DOTALL) or re.findall(r'(.*\s)'+'for?',dc[i[0]],re.DOTALL)
                    Awards[str(nc[i[0]])]['winner_film'] = list(set(re.findall('(.*?) directed by',dc[i[0]],re.DOTALL)[0].split(' ')) - set(re.findall(r'[(]'+'.*'+'[)]',dc[i[0]],re.DOTALL))-set(Awards[str(nc[i[0]])]['actor/actress_name'][0].split(' '))-set(['in'])-set(['for']))                
                elif re.findall('(.*?) directed by',dc[i[0]],re.DOTALL):
                    Awards[str(nc[i[0]])]['actor/actress_name'] = ''
                    Awards[str(nc[i[0]])]['winner_film'] = list(set(re.findall('(.*?) directed by',dc[i[0]],re.DOTALL)[0].split(' ')) - set(re.findall(r'[(]'+'.*'+'[)]',dc[i[0]],re.DOTALL)))
                elif re.findall(r'(.*?)'+' in.*?',dc[i[0]],re.DOTALL) or re.findall(r'(.*\s)'+'for?',dc[i[0]],re.DOTALL):
                    Awards[str(nc[i[0]])]['actor/actress_name'] = re.findall(r'(.*?)'+' in.*?',dc[i[0]],re.DOTALL) or re.findall(r'(.*\s)'+'for?',dc[i[0]],re.DOTALL)
                    Awards[str(nc[i[0]])]['winner_film'] = list(set(re.findall(r'(.*?)[(]'+'.*'+'[)]',dc[i[0]],re.DOTALL))-set(Awards[str(nc[i[0]])]['actor/actress_name'])-set(['in'])-set(['for']))
                if re.findall(r'[(]'+'.*'+'[)]',dc[i[0]],re.DOTALL):
                    Awards[str(nc[i[0]])]['winner_country'] = re.findall(r'[(]'+'.*'+'[)]',dc[i[0]],re.DOTALL)
                else:
                    Awards[str(nc[i[0]])]['winner_country'] = ''
                if re.findall(r'directed by (.*?)',dc[i[0]],re.DOTALL):
                    Awards[str(nc[i[0]])]['director']=re.findall(r'directed by (.*)?',dc[i[0]],re.DOTALL)
                else:
                    Awards[str(nc[i[0]])]['director'] = ''
    return awards,Awards

def get_SSIF_awards(url = "https://www.siff.com/english/content?aid=101240622235844574349209197613061422"):
    '''
    example:    
    <div class="event-widgets__award-name">Golden Goblet</div>
    <div class="event-widgets__award-name">Golden Goblet</div>
    #center-3-react > div > div > div:nth-child(1) > div
    //*[@id="center-3-react"]/div/div/div[1]/div
    /html/body/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div/div[1]/div
    '''
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Accept': 'text/plain',
    'Connection': 'keep-alive',
    'Origin': url,
    'Referer': url+'/',
    # More headers like User-Agent, etc.
    }     
    response=requests.get(url=url,headers=headers) 
#    html0 = etree.parse(response.text,parser = etree.HTMLParser(encoding='gbk',recover=True))
#    html = etree.parse(StringIO(response0.text))
    html = etree.HTML(response.text)
    #print(html0.xpath('//body/table/tbody/tr[954]/td[2]/text()'))
    names0 = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/*//p/span/strong')
    names1 = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/*//p/strong')
    details = html.xpath('//body/div[@class="content"]/div[@class="box"]/div[@class="article"]/div[@class="wrapper"]/div[@class="main_text"]/section/p/span')
    awards = {}
    if len(names0)+len(names1) >= len(details):
        names = names0+names1
        nc = names.copy()
        dc = details.copy()
        try:
            for itemi in range(len(nc)-1):
                if nc[itemi].text is None or nc[itemi].text == '\xa0':
                    nc.remove(nc[itemi])
                if '\xa0' in nc[itemi].text and '\xa0' in nc[itemi+1].text:
                    nc[itemi].text = nc[itemi].text.replace('\xa0',' ') + nc[itemi+1].text.replace('\xa0',' ')
                    nc.remove(nc[itemi+1])
            for itemj in range(len(dc)):
                if dc[itemj].text is None:
                    dc.remove(dc[itemj])
                elif '\xa0' in dc[itemj].text:
                    dc[itemj].text = dc[itemj].text.replace('\xa0',' ')
                dc[itemj] = dc[itemj].text
            for itemij in range(len(nc)):
                if '\xa0' in nc[itemij].text:
                    nc.remove(nc[itemij])
                nc[itemij] = nc[itemij].text
            if "Bakur Bakuradze for SNOWFLAKES IN MY YARD (Georgia/Russia)" not in dc[2]:
                dc.insert(2,"Bakur Bakuradze for SNOWFLAKES IN MY YARD (Georgia/Russia)")        
            if "HUANG Xiaoming in DON'T WORRY, BE HAPPY (China) directed by WEI Shujun" not in dc[3]:    
                dc.insert(3,"HUANG Xiaoming in DON'T WORRY, BE HAPPY (China) directed by WEI Shujun")
        except:
            ...
        print(itemi,itemj)
        for i in enumerate(dc):
            if nc[i[0]] is not None and dc[i[0]] is not None:
                awards[str(nc[i[0]])] = dc[i[0]]
    return awards

def readData(files):
    Data = []
    for file in files:
        #tempData = []
        with open(file,'r',encoding = 'utf-8',newline = '') as f:
            contents = pd.read_csv(f)#csv.reader(f) #csv.DictReader(f)
#            for lines in contents:
#                tempData.append(contents)
            Data.append(contents)
    return Data

#in case
Data = readData(["E:\SQL\project\data.csv","E:\SQL\project\data1.csv"])
cData = Data[0]
Index2drop = []
for i in range(len(cData)):    
    print(cData.iloc[i]['film_id'])
    print(cData.iloc[i]['film_id'] == 'DecodeError')
    if cData.iloc[i]['film_id'] == 'DecodeError': 
        if Data[1].iloc[i]['film_id'] != 'DecodeError': 
            cData.loc[i] = Data[1].iloc[i]
        else:
            Index2drop.append(i)
cData.drop(Index2drop,axis  = 0,inplace =True)
cData.to_csv('e:/sql/project/PData.csv',sep = ',')
'''
i = 0    
N = len(cData)        
while i < len(Data[0]):
    if i == N -1 :
        break
    if cData.iloc[i]['film_id'] == 'DecodeError': 
        cData.drop([i],inplace=True)
        N = len(cData)    
        cData = cData
    else:
        i += 1
'''    
    
def connectDB():    
    try:
        # connect to database
        db = sqlite3.connect(r"E:\SQL\project\SIFF.db")
        cursor = db.cursor()
    
    except Exception as e:
        print("Connection failed: ", e)
    return db,cursor

def createTables(cursor):
    print(cursor.execute('''CREATE TABLE IF NOT EXISTS "2024_SIFF" ("film_name" TEXT NOT NULL,"director_name" TEXT,PRIMARY KEY("film_name"));''').fetchall())
    print(cursor.execute('''CREATE TABLE IF NOT EXISTS "awards" ("award_name" TEXT NOT NULL,"actor/actress_name" TEXT,"film_name" TEXT NOT NULL,"director_name" TEXT,PRIMARY KEY("award_name"));''').fetchall())
    print(cursor.execute('''CREATE TABLE IF NOT EXISTS "movies" ("id" INTEGER NOT NULL,"name" TEXT NOT NULL, "film_genre" TEXT, "film_duration" INTEGER, "film_year" INTEGER, "film_historic_coutries" TEXT, "film_scores" INTEGER,"film_ratings" INTEGER, "film_short_synopsis" TEXT,"film_trailor_url" TEXT,"film_intro_url" TEXT);''').fetchall()) #,PRIMARY KEY("name"),FOREIGN KEY("award_name") REFERENCES "awards"("name"),FOREIGN KEY("film_name") REFERENCES "2024_SIFF"("film_name"))
    print(cursor.execute('''CREATE TABLE IF NOT EXISTS "cast_info" ("id" TEXT NOT NULL,"name" TEXT,"position" TEXT);''').fetchall())
    return cursor

def insertIntoTables(cursor):
    try:
        print(cursor.execute('''INSERT INTO "2024_SIFF" ("film_name","director_name") VALUES ('Starfall','Zhang Dalei');''').fetchall())        
    except Exception as e:
        print(e)
    try:
        print(cursor.execute('''INSERT INTO "awards" ("award_name","actor/actress_name","film_name","director_name" ) VALUES ('Best Feature Film', NULL,'The DIVORCE', 'Daniyar Salamat');''').fetchall())
    except Exception as e:
        print(e)
    try:
        print(cursor.execute('''INSERT INTO "movies" ("id","name","film_genre","film_duration","film_year","film_historic_coutries","film_scores","film_ratings","film_short_synopsis","film_trailor_url","film_intro_url") VALUES (416428,"A Corner in the City","Drama",113,1983,"China",NULL,NULL,"",NULL,'https://mubi.com/en/hk/films/a-corner-in-the-city');''').fetchall())
    except Exception as e:
        print(e)
    try:
        print(cursor.execute('''INSERT INTO "cast_info" ("id","name","position") VALUES ('221540','W',"Director");''').fetchall())
    except Exception as e:
        print(e)
    return cursor

def insertIntoTablesfromDF(cursor,siffList,awardList,filmList,filmDF):#cursor,fL,Awards,filmData,cData
    for i in range(len(siffList)):
        try:
            print(cursor.execute(f'''INSERT INTO "2024_SIFF" ("film_name","director_name") VALUES ({list(siffList.keys())[i]},{list(siffList.values())[i]});''').fetchall())
        except Exception as e:
            print('siff: ',e)
    for j in range(len(awardList)):
        try:
            print(cursor.execute(f'''INSERT INTO "awards" ("award_name","actor/actress_name","film_name","director_name" ) VALUES ({list(awardList.keys())[j]}, {list(awardList.values())[j]['actor/actress_name']},{list(awardList.values())[j]['winner_film']}, {list(awardList.values())[i]['director']});''').fetchall())
        except Exception as e:
            print('award: ',e)
    for k in range(len(filmList)):
        try:
            print(cursor.execute(f'''INSERT INTO "movies" ("id","name","film_genre","film_duration","film_year","film_historic_coutries","film_scores","film_ratings","film_short_synopsis","film_trailor_url","film_intro_url") VALUES ({filmList[k]['film_id']},{filmList[k]['film_name']},{filmList[k]['film_genre']},{filmList[k]['film_duration']},{filmList[k]['film_year']},{filmList[k]['film_historic_countries']},{filmList[k]['film_scores']},{filmList[k]['film_ratings']},{filmList[k]['film_short_synopsis']},{filmList[k]['film_trailor_url']},{filmList[k]['film_intro_url']});''').fetchall())
        except Exception as e:
            print('movies: ', e)
        tempData = filmList[k]['film_cast']
        print(tempData)
        if type(filmList[k]['film_cast']) == dict:
            for ki in enumerate(tempData):
                try:
                    print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({tempData[ki[0]]['id']},{tempData[ki[0]]['name']},{tempData[ki[0]]['position']});''').fetchall())
                except Exception as e:
                    print('cast_info: ',e)
        if type(filmList[k]['film_cast']) == list:
#            if min(len(tempData[0]),len(tempData[1]),len(tempData[2])) >2:
#                for ki in range(min(len(tempData[0]),len(tempData[1]),len(tempData[2]))):
#                    try:
#                        print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({tempData[0][ki]},{tempData[1][ki]},{tempData[2][ki]});''').fetchall())        
#                    except Exception as e:
#                        print('cast_info: ',e)
#            elif min(len(tempData[0]),len(tempData[1]),len(tempData[2])) ==2:
#                for ki in range(min(len(tempData[0]),len(tempData[1]),len(tempData[2]))):
 #                   try:
 #                       print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({tempData[0][0]},{tempData[1]},{tempData[2][0]});''').fetchall())        
 #                   except Exception as e:
  #                      print('cast_info: ',e)
#            else:
            try:
                    #print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({list(tempData[0])[0]},{list(tempData[1])[0]},{list(tempData[2])[0]});''').fetchall())        
#                    if len(tempData[0]) == 1:
#                        print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({tempData[0]},{tempData[1][0]},{tempData[2][0]});''').fetchall())
#                    elif len(tempData[1]) == 1:
#                       print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({tempData[0][0]},{tempData[1]},{tempData[2][0]});''').fetchall())
#                    elif len(tempData[2]) == 1:
                    print(cursor.execute(f'''INSERT INTO "cast_info" ("id","name","position") VALUES ({tempData[0][0]},{tempData[1]},{tempData[2][0]});''').fetchall())
            except Exception as e:
                    print('cast_info: ',e)
    return cursor

def createIndexes(cursor):
    print(cursor.execute('''CREATE INDEX IF NOT EXISTS "award_name_search" ON "movies" ("name");''').fetchall())
    print(cursor.execute('''CREATE INDEX IF NOT EXISTS "film_info_search" ON "movies" ("name");''').fetchall())
    print(cursor.execute('''CREATE INDEX IF NOT EXISTS "film_name_search" ON "awards" ("award_name");''').fetchall())
    return cursor
    
def TableSearchbyIndexes(cursor):
    print(cursor.execute('''SELECT award_name FROM "awards" WHERE "film_name" == 'The DIVORCE';''').fetchall())
    print(cursor.execute('''SELECT * FROM "movies" WHERE "name" = "A Corner in the City";''').fetchall())
    print(cursor.execute('''SELECT film_name FROM "awards" WHERE "award_name" = "Best Feature Film";''').fetchall())
    return cursor    
    
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)

def main():
    awards_general, awards_dict = get_SSIF_awards_by_re(url = "https://www.siff.com/english/content?aid=101240622235844574349209197613061422")
    fL = get_film_list(r"E:\SQL\project\siff.txt")
    #savepath = r'E:/SQL/project/data.csv'
    testpath = r'E:/SQL/project/data1.csv'
    savepath = testpath
    with open(savepath,'w',newline = '',encoding='utf_8_sig') as f:
        columns = ['film_id','film_name','film_genre','film_duration','film_year','film_historic_countries','film_scores','film_ratings','film_cast_info','film_short_synopsis','film_trailor_url','film_intro_url']
        writer = csv.DictWriter(f,fieldnames = columns)
        writer.writeheader()
        filmData = {}
        for fmi in enumerate(fL):
            fmName = fmi[1].lower().replace("’",'-').replace("'",'-').replace(" ",'-').replace(".",'-').replace(',','-').replace(':','-').replace('!','-').replace('?','-').replace('...','-').replace('......','-').replace('--','-')#.replace("/",'-').replace("\",'-').replace('\\','-').replace('//','-')
            if fmName[-1] == '-':
                fmName = fmName[:-1]
            #film_id,film_name,film_genre,film_duration,film_historic_countries,film_scores,film_ratings,
            #film_cast,film_short_synopsis,film_trailor_url]
            TEMP= get_SSIF_data(url = 'https://mubi.com/en/hk/films',filmName=fmName)            
            filmData[fmi[0]] = {}
            if TEMP is None:
                TEMP = ('Error!'*12).split('!')[:-1]
            if len(TEMP) == 12:
                filmData[fmi[0]]['film_id'] = TEMP[0]
                filmData[fmi[0]]['film_name'] = TEMP[1]
                filmData[fmi[0]]['film_genre'] = TEMP[2]
                filmData[fmi[0]]['film_duration'] = TEMP[3]
                filmData[fmi[0]]['film_year'] = TEMP[4]
                filmData[fmi[0]]['film_historic_countries'] = TEMP[5]
                filmData[fmi[0]]['film_scores'] = TEMP[6]
                filmData[fmi[0]]['film_ratings'] = TEMP[7]
                filmData[fmi[0]]['film_cast'] = TEMP[8]
                filmData[fmi[0]]['film_short_synopsis'] = TEMP[9]
                filmData[fmi[0]]['film_trailor_url'] = TEMP[10]
                filmData[fmi[0]]['film_intro_url'] = TEMP[11]
                data_dict ={'film_id':TEMP[0],'film_name':TEMP[1],'film_genre':TEMP[2],'film_duration':TEMP[3],'film_year':TEMP[4],'film_historic_countries':TEMP[5],'film_scores':TEMP[6],'film_ratings':TEMP[7],'film_cast_info':TEMP[8],'film_short_synopsis':TEMP[9],'film_trailor_url':TEMP[10],'film_intro_url':TEMP[11]}  
                print(fmi,' writing...')
                writer.writerow(data_dict)
            else:                
                print('Error! Failed to get the data!')

    db,cursor = connectDB()
    cursor = createTables(cursor)
    cursor = insertIntoTables(cursor)
    print(cursor.execute('''PRAGMA table_info(awards);''').fetchall())
    '''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'print_number', 'INTEGER', 0, None, 0), (2, 'english_title', 'TEXT', 0, None, 0), (3, 'japanese_title', 'TEXT', 0, None, 0), (4, 'artist', 'TEXT', 0, None, 0), (5, 'average_color', 'TEXT', 0, None, 0), (6, 'brightness', 'NUMERIC', 0, None, 0), (7, 'contrast', 'NUMERIC', 0, None, 0), (8, 'entropy', 'NUMERIC', 0, None, 0)]'''
    cursor = createIndexes(cursor)
    cursor = TableSearchbyIndexes(cursor)
    cursor = insertIntoTablesfromDF(cursor,fL,awards_dict,filmData,cData)
    cursor = TableSearchbyIndexes(cursor)
    print(cursor.execute('''select * from "2024_SIFF";''').fetchall())
    print(cursor.execute('''select * from "awards";''').fetchall())
    print(cursor.execute('''select * from "movies";''').fetchall()) #,PRIMARY KEY("name"),FOREIGN KEY("award_name") REFERENCES "awards"("name"),FOREIGN KEY("film_name") REFERENCES "2024_SIFF"("film_name"))
    print(cursor.execute('''select * from "cast_info";''').fetchall())



    #In schema.sql, write a SQL query to create and insert into tables.
    text1 = 'CREATE TABLE "2024_SIFF" ("film_name" TEXT NOT NULL, "director_name" TEXT,PRIMARY KEY("film_name"));\n'
    text2 = '-- Represent awards of the 2024_SIFF /n' + '''CREATE TABLE "awards" ("award_name" TEXT NOT NULL,"actor/actress_name" TEXT,"film_name" TEXT NOT NULL, "director_name" TEXT,PRIMARY KEY("award_name"));\n'''
    text3 = '-- Represent info of movies\n'+'CREATE TABLE "movies" ("id" INTEGER NOT NULL,"name" TEXT NOT NULL,"film_genre" TEXT,"film_duration" INTEGER,"film_year" INTEGER,"film_historic_coutries" TEXT,"film_scores“ INTEGER,"film_ratings" INTEGER,"film_short_synopsis" TEXT, "film_trailor_url" TEXT, "film_intro_url" TEXT,PRIMARY KEY("name"),FOREIGN KEY("award_name") REFERENCES "awards"("name"),FOREIGN KEY("film_name") REFERENCES "2024_SIFF"("name"));\n'
    text4 = '-- Represent cast of movies\n'+'CREATE TABLE "cast_info" ("id" TEXT NOT NULL,"name" TEXT,"position" TEXT);\n'
    text5 = '-- Create indexes to speed common searches\n'+'CREATE INDEX "award_name_search" ON "movies" ("name");\n'+'CREATE INDEX "film_info_search" ON "movies" ("name");\n'+'CREATE INDEX "film_name_search" ON "awards" ("award_name");'
    
    asw(r'E:\SQL\project\schema.sql',text1+text2+text3+text4+text5)

    #In queries.sql, write a SQL query to search info in the tables. The query should:        
    text11 = '-- Find all award_name given movie name\n'+'SELECT award_name FROM "awards" WHERE "film_name" == "The DIVORCE";\n'
    text12 = '-- Find all film_info ON given movie name\n'+'\n'+'SELECT * FROM "movies" WHERE "name" = "A Corner in the City";\n'   
    text13 = '-- Find all film_name given award_name\n'+'SELECT film_name FROM "awards" WHERE "award_name" = "Best Feature Film";\n'
    text14 = '-- Add a new entry\n'+ 'INSERT INTO "2024_SIFF" ("film_name","director_name")\n' + 'VALUES ("Starfall","Zhang Dalei");\n'
    text15 = '-- Add a new award\n'+'INSERT INTO "awards" ("award_name","actor/actress_name","film_name","director_name")n'+'VALUES ("Best Feature Film", NULL,"The DIVORCE", "Daniyar Salamat);\n'+'\n'
    text16 = '-- Add a new movie\n'+'INSERT INTO "movies" ("id","name","film_genre","film_duration","film_year","film_historic_coutries","film_scores","film_ratings","film_short_synopsis","film_trailor_url","film_intro_url")\n'+'VALUES (416428,"A Corner in the City","Drama",113,1983,"China",NULL,NULL,"",NULL,"https://mubi.com/en/hk/films/a-corner-in-the-city"});\n'
    text17 = '-- Add a new cast_info\n'+'INSERT INTO "cast_info" ("id","name","position")\n'+'VALUES (“221540”,“W”,"Director");\n'
    asw(r'E:\SQL\project\queries.sql',text11+text12+text13+text14+text15+text16+text17)
    
