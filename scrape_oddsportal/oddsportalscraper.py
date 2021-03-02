from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
import fnmatch
import pandas as pd
import numpy as npy
import datetime
import time
from ncclogger import formatlogger as log
import random
## this module creates individual team stats file
# custom library
import nccprops
import formatterutil


def scrape_historical_matches_from_op(fl, html_source, file_path, country, league, div, season, count):
    log.debug("Enter")
    match_list = list()
    try:
        soup = bs(html_source, 'lxml')
        tournament_table = soup.find('table', class_='table-main')
        body_ = tournament_table.find('tbody')
        all_matches = body_.find_all('tr')
        match_date = ""
        for _class_ in all_matches:
            if (_class_['class'][0] == 'center'):
                match_date = formatterutil.format_date(_class_.text.split('1X2')[0], 'op')

            if (match_date != ''):
                if ('deactivate' in _class_['class']):
                    odds_count = 0
                    FTHG, FTAG = 0, 0
                    B365H, B365D, B365A = 0, 0, 0
                    FTR = 'NA'
                    for child in _class_.children:
                        if ('table-time' in child['class']):
                            match_time = formatterutil.format_time(child.text.strip(), 'op')
                        elif('table-participant' in child['class']):
                            try:
                                split_team = child.text.split(' - ')
                                HomeTeam = split_team[0].strip()
                                AwayTeam = split_team[1].strip()
                            except:
                                break
                        elif ('odds-nowrp' in child['class']):
                            try:
                                if (odds_count == 0):
                                    odds_count += 1
                                    B365H = round(float(child.text),2)
                                elif (odds_count == 1):
                                    odds_count += 1
                                    B365D = round(float(child.text),2)
                                else:
                                    odds_count += 1
                                    B365A = round(float(child.text),2)
                            except:
                                B365H = 0
                                B365D = 0
                                B365A = 0

                        elif ('table-score' in child['class']):
                            try:
                                split_score = child.text.split(':')
                                FTHG = int(split_score[0])
                                FTAG = int(split_score[1])
                                FTR = 'H' if FTHG > FTAG else ('D' if FTHG == FTAG else 'A')
                            except:
                                break

                    match_dic = {'Country': country, 'League': league, 'Div': div, 'Season': season,
                                   'Date': match_date, 'Time': match_time, 'HomeTeam': HomeTeam,  'AwayTeam': AwayTeam,
                                   'FTHG': FTHG, 'FTAG': FTAG, 'FTR': FTR,
                                   'B365H': B365H, 'B365D': B365D, 'B365A': B365A}


                    match_list.append(match_dic)

        history_matches_df = pd.DataFrame(match_list)
        if (count == 1):
            history_matches_df.to_csv(file_path, mode='w+')
        else:
            history_matches_df.to_csv(file_path, mode='a+', header = False)


    except Exception:
        log.exception("Exception occurred while loading matches from odds portal for country %s and league %s" %(country, league))
        exit()

    log.debug("Exit")

def scrape_latest_matches_from_op(fl, html_source, country, league, season, div):
    log.debug("Enter")
    match_list = list()
    odds_portal_file_path = fl.get_oddsportal_dir()

    try:
        #with open(r'E:\ncc-data\test\Allsvenskan.html') as html_source:
        soup = bs(html_source, 'lxml')

        tournament_table = soup.find('table', class_='table-main')
        body_ = tournament_table.find('tbody')
        all_matches = body_.find_all('tr')

        match_date = ""
        for _class_ in all_matches:
            # print (_class_)
            if (_class_['class'][0] == 'center'):
                match_date = formatterutil.format_date(_class_.text.split('1X2')[0], 'op')

            if (match_date != ''):
                if ('deactivate' in _class_['class']):
                    odds_count = 0
                    FTHG, FTAG = 0, 0
                    B365H, B365D, B365A = 0, 0, 0
                    FTR = 'NA'
                    for child in _class_.children:
                        if ('table-time' in child['class']):
                            match_time = formatterutil.format_time(child.text.strip(), 'op')
                        elif('table-participant' in child['class']):
                            try:
                                split_team = child.text.split(' - ')
                                HomeTeam = split_team[0].strip()
                                AwayTeam = split_team[1].strip()
                            except:
                                break
                        elif ('odds-nowrp' in child['class']):
                            try:
                                if (odds_count == 0):
                                    odds_count += 1
                                    B365H = round(float(child.text),2)
                                elif (odds_count == 1):
                                    odds_count += 1
                                    B365D = round(float(child.text),2)
                                else:
                                    odds_count += 1
                                    B365A = round(float(child.text),2)
                            except:
                                continue

                        elif ('table-score' in child['class']):
                            try:
                                split_score = child.text.split(':')
                                FTHG = int(split_score[0])
                                FTAG = int(split_score[1])
                                FTR = 'H' if FTHG > FTAG else ('D' if FTHG == FTAG else 'A')
                            except:
                                break

                    match_dic = {'Country': country, 'League': league, 'Div': div, 'Season': season,
                                   'Date': match_date, 'Time': match_time, 'HomeTeam': HomeTeam,  'AwayTeam': AwayTeam,
                                   'FTHG': FTHG, 'FTAG': FTAG, 'FTR': FTR,
                                   'B365H': B365H, 'B365D': B365D, 'B365A': B365A}

                    match_list.append(match_dic)

        latest_matches_df = pd.DataFrame(match_list)

        file_path = os.path.join(odds_portal_file_path,country.upper(),str(season),str(div),str(league))
        if not (os.path.isdir(file_path)):
            os.makedirs(file_path)
        latest_matches_df.to_csv(os.path.join(file_path, 'latest.csv'), mode='w+')

    except Exception:
        log.exception("Exception occurred while matches from odds portal")

    log.debug("Exit")

def load_latest_matches_from_op(fl):
    log.debug("Enter")
    chrome_path = fl.get_chrome_driver()
    driver = webdriver.Chrome(chrome_path)
    base_url = 'https://www.oddsportal.com/soccer/'
    driver.implicitly_wait(60)

    try:

        for key, div in nccprops.fs_country_league_to_div_map.items():
            if (nccprops.op_country_league_to_div_map_load.get(key, -1) == -1):
                continue
            retry = 0
            while (retry in (0,1)):
                try:
                    op_country, op_league = nccprops.op_country_league_to_div_map[key]
                    log.info('Loading [%s] [%s] -- Retry == %s' % (op_country,op_league, retry))
                    url_to_load = base_url + op_country + "/" + op_league + "/" + 'results/'
                    random1 = random.randint(10, 21)
                    random2 = random.randint(10, 21)
                    random3 = random.randint(random1, random2 + 5) if random2 >= random1 else random.randint(random2, random1 + 5)
                    driver.get(url_to_load)
                    time.sleep(random1)
                    html_source = driver.page_source
                    season = nccprops.get_current_season(key[0])
                    scrape_latest_matches_from_op(fl, html_source, key[0], key[1].replace('/', '-'), season, div)
                    time.sleep(random3)
                    retry = 2

                except Exception:
                    if (retry == 0):
                        retry = 1
                    else:
                        retry = 2
                    continue
    except Exception:
        log.exception("Exception occurred while loading flashscore page")
        driver.close()

    log.debug("Exit")

def load_historical_matches_from_op(fl):
    log.debug("Enter")
    odds_portal_file_path = fl.get_oddsportal_dir()
    chrome_path = fl.get_chrome_driver()
    driver = webdriver.Chrome(chrome_path)
    base_url = 'https://www.oddsportal.com/soccer/'
    driver.implicitly_wait(60)
    season_list = nccprops.season_list
    try:
        for key, div in nccprops.fs_country_league_to_div_map.items():
            if (nccprops.op_country_league_to_div_map_load.get(key, -1) == -1):
                continue
            retry = 0
            country = key[0].upper()
            league = key[1].replace('/', '-')
            op_country, op_league = nccprops.op_country_league_to_div_map[key]
            url_to_load = base_url + op_country + "/" + op_league + "/" + 'results/'
            ## these random sleep time is to slow things down and introduce random behavior during scraping process
            random1 = random.randint(11, 19)
            random2 = random.randint(7, 17)
            random3 = random.randint(random1, random2 + 5) if random2 >= random1 else random.randint(random2, random1 + 5)
            driver.get(url_to_load)
            seasons = driver.find_elements_by_class_name('main-filter')[1]
            ## findout what date format we have
            st_date = str(season_list[0])
            slash_date = str(int(st_date) - 1) + "/" + st_date
            try:
                date_format = 'NA'
                if (seasons.find_element_by_link_text(slash_date)):
                    date_format = 'slash'
                else:
                    date_format = 'NA'
            except:
                try:
                    if (seasons.find_element_by_link_text(st_date)):
                        date_format = 'st'
                    else:
                        date_format = 'NA'
                except:
                    log.error('Failed identifying date format for [%s] [%s]' % (op_country, op_league))
                    continue
            log.info('Loading [%s] [%s] Date Format is [%s] -- Retry == %s' % (op_country, op_league, date_format, retry))
            for season in season_list:
                file_path = os.path.join(odds_portal_file_path,country,str(season),str(div),league)
                if (date_format == 'slash'):
                    page_season = str(int(season) - 1) + "/" + season
                elif (date_format == 'st'):
                    page_season = str(season)
                elif (date_format == 'NA'):
                    log.error('Invalid date format for [%s] [%s]' % (op_country, op_league))
                    break
                try:
                    seasons = driver.find_elements_by_class_name('main-filter')[1]
                    time.sleep(random.randint(7,11))
                    season_link = seasons.find_element_by_link_text(page_season)
                    season_link.click()

                except:
                    continue

                ## create directories if required
                if not (os.path.isdir(file_path)):
                    os.makedirs(file_path)
                file_path = os.path.join(file_path,'history.csv')
                if (os.path.isfile(file_path)):
                    ## remove the file so that we can start all over
                    os.remove(file_path)

                count = 1
                while count < 20:
                    log.info("-->Scraping Season [%s] Page [%s]" % (season, count))
                    time.sleep(random.randint(13,23))
                    html_source = driver.page_source
                    scrape_historical_matches_from_op(fl, html_source, file_path, country, league, div, season, count)
                    count += 1
                    try:
                        pages = driver.find_element_by_id('pagination')
                        time.sleep(random.randint(5,10))
                        page = pages.find_element_by_link_text(str(count))
                        time.sleep(random.randint(5,9))
                        page.click()
                        time.sleep(7)
                    except Exception:
                        break
                time.sleep(random3)

        driver.close()
        exit()
    except Exception:
        log.exception("Exception occurred while loading flashscore page")
        driver.close()
    log.debug("Exit")

def main():

    ## initialise fileloc object
    fl = nccprops.fileloc()

    ################################################################
    #load_historical_matches_from_op(fl)
    ################################################################
    load_latest_matches_from_op(fl)
   
## call main
if __name__ == "__main__":
    main()



