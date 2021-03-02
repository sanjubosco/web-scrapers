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


def scrape_league_standing_from_fs(fl, html_source, country, league):
    log.debug("Enter")
    league_standing_dir = fl.get_league_standing_dir()

    try:
        league_list = list()

        #with open (r'E:\ncc-data\test\FlashScore_summary.html') as html_source:
        soup = bs(html_source, 'lxml')

        season_element = soup.find('div', class_ =  'teamHeader__text')
        season = season_element.text
        ## format this season
        season = season.replace(" ","").strip()
        div = nccprops.fs_country_league_to_div_map[(country, league)]
        if (nccprops.SEASON_MAP.get(season,-1) == -1):
            ## no need for mapping or this format is not present. for the timebeing let proceed as if this is a good one
            pass
        else:
            season = nccprops.SEASON_MAP[season]

        fs_league_table = soup.find_all('div', class_= 'row___S6WkQ8-')
        log.debug("Scraping standing for Country %s League (formatted) %s Div %s Season %s" %(country, league, div, season))
        for team in fs_league_table:
            try:
                team_stats = list()
                for i, stat in enumerate(team.children):
                    try:
                        ## this is for the scored and conceded goals
                        if (i == 6):
                            goal_stat = stat.text.split(':')
                            team_stats.append(goal_stat[0])
                            team_stats.append(goal_stat[1])
                        elif(i == 0):
                            rank = stat.text.split('.')
                            team_stats.append(rank[0])
                        elif (i == 1):
                            team = stat.text.strip()
                            team_alias = nccprops.get_fs_team_alias(country.upper(), team)
                            team_stats.append(team)
                            team_stats.append(team_alias)
                        else:
                            team_stats.append(stat.text.strip())
                    except Exception:
                        continue

                league_list.append(team_stats)

            except Exception:
                continue

        log.debug("Loading league %s" %league_list)
        league = league.replace('/', '-')
        league_df = pd.DataFrame(league_list, columns=['Rank','Team','Team_Alias', 'MatchesPlayed','Win','Draw','Loss','GoalsScored','GoalsConceded','Points','Form'])
        league_df['Country'] = country
        league_df['League'] = league
        league_df['Div'] = div
        league_df['Season'] = season
        ## note that the PK was created with league originally.
        formatterutil.remove_special_chars_from_df(league_df)
        league_df['PK'] = league_df['Country'].astype(str) + "__" + league_df['Div'].astype(str) + "__" + league_df['Season'].astype(str) + "__" + league_df[
                                       'Team_Alias'].astype(str)
        ## reset the index
        league_df.set_index('PK', drop=True, inplace=True)
        try:
            ## write to file
            league_standing_file = os.path.join(league_standing_dir, country + "_" + league + "_" + season + nccprops.fileloc.LEGUE_STADNING_FILE_EXT + ".csv")
            league_df.to_csv(league_standing_file, mode='w+')

        except Exception:
            log.exception("Exception occurred while writing standings to db")
            exit()

    except Exception:
        log.exception("Exception occurred while scrapping data from flash score")

    log.debug("Exit")

def scrape_fixture_from_fs(fl, html_source, match_date, fixture_file):
    log.debug("Enter")
        
    try:        
        fixture_df = pd.DataFrame(columns = nccprops.Mandatory_Match_Features)
        fixture_list = []
            
        #with open (r'E:\OneDrive\MyCode\ncc\bin\FlashScore.com.html') as html_source:
        soup = bs(html_source,'lxml')

        fs_live_table = soup.find('div',id = 'live-table')

        fs_soccer_matches = fs_live_table.find('div', class_ = 'sportName')
        
        if (fs_soccer_matches['class'][1] == 'soccer'):
            Country = ''
            League = ''
            for child in fs_soccer_matches.children:

                if (child['class'][0] == 'event__header'):
                    Country = child.find('span',class_ = 'event__title--type').text.strip().upper()
                    League = child.find('span',class_ = 'event__title--name').text.strip()
                    
                if (child['class'][0] == 'event__match'):
                    teams = child.find_all('div',class_ = 'event__participant')
                    odds = child.find_all('div',class_ = 'odds__odd') 
                    match_time = child.find('div',class_ = 'event__time')

                    if (match_time is None):
                        ## this match dont have a time. So this is posisbly in progress/completed/postponed etc. skip this match
                        continue
                    else:
                        match_time = formatterutil.format_time(match_time.contents[0].strip(), 'fs')
                    
                    if (len(odds) > 0):
                        if (odds[0].text.strip() not in ('','null','-',None)):
                            try:
                                B365H = float(odds[0].text.strip())
                                B365D = float(odds[1].text.strip())
                                B365A = float(odds[2].text.strip())
                            except:
                                B365H = 0
                                B365D = 0
                                B365A = 0
                        else:
                            B365H = 0
                            B365D = 0
                            B365A = 0
                    else:
                        B365H = 0
                        B365D = 0
                        B365A = 0                        

                    if (len(teams) > 0):
                        HomeTeam = formatterutil.encode_string_to_utf(teams[0].text)
                        AwayTeam = formatterutil.encode_string_to_utf(teams[1].text)
                        HomeTeam_Alias = nccprops.get_fs_team_alias(Country, HomeTeam.strip())
                        AwayTeam_Alias = nccprops.get_fs_team_alias(Country, AwayTeam.strip())

                        ## feature from ncprops.py
                        ## Mandatory_Match_Features = ['Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A']
                        
                        ## now do a mapping for the division
                        try:
                            League = League.replace('/', '-')
                            League = formatterutil.encode_string_to_utf(League)
                            Division = nccprops.fs_country_league_to_div_map[(Country, League)]
                        except Exception:
                            log.debug("Mapping information not found in fs_country_league_to_div_map for league %s from country %s" %(League, Country))
                            Division =  League
                        
                        Season = str(nccprops.get_current_season(Country))

                        fixture_dic = {'Country':Country, 'League':League, 'Div':Division, 'Season':Season, 'Date':match_date, 'Time':match_time, 'HomeTeam':HomeTeam, \
                            'HomeTeam_Alias':HomeTeam_Alias, 'AwayTeam':AwayTeam, 'AwayTeam_Alias':AwayTeam_Alias, 'FTHG':0, 'FTAG':0, 'FTR':'Not Available', 'B365H':B365H,\
                                       'B365D':B365D, 'B365A':B365A, 'FS_League':League}
                        fixture_list.append(fixture_dic)
            
            fixture_df = pd.DataFrame(fixture_list)
            ## normalise and encode to utf
            fixture_df['Country'] = formatterutil.encode_numpy_to_utf(fixture_df['Country'])
            fixture_df['StatSource'] = 'fs_fixture'
            ## now add an extra column
            fixture_df['fixture'] = 1
            
            try:  
            ## write to fixture file 
                if (os.path.isfile(fixture_file)):          
                    fixture_df.to_csv(fixture_file,mode='a', header=False)
                else:
                    fixture_df.to_csv(fixture_file)

            except PermissionError:
                log.warning("PermissionError: Couldnt write to csv file.")
                return                
            except Exception:
                log.warning("Error occurred while writing to fixture csv file.")
                return     

    except Exception:
        log.exception("Exception occurred while scrapping data from flash score")
    
    log.debug("Exit")

def load_fixture_from_fs(fl, forecast_days):
    log.debug("Enter")     
    chrome_path = fl.get_chrome_driver()
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://www.flashscore.com/')
    random1 = random.randint(1,21)
    random2 = random.randint(1,11)
    random3 = random.randint(random1,random2+5) if random2 >= random1 else random.randint(random2,random1+5)
    fixture_file = os.path.join(fl.get_data_path(),fl.get_fixture_file())
    
    try:

        tabs = WebDriverWait(driver, 60).until(lambda d: d.find_elements_by_class_name('tabs__text'))
        for tab in tabs:
            if (tab.text == 'Odds'):
                link = tab

        link.click()        
        time.sleep(random1)
        calendar_nav = driver.find_elements_by_class_name('calendar__direction')
        today = datetime.date.today()
        ##we will get the data for the next 7 days
        if (os.path.isfile(fixture_file)):
            os.remove(fixture_file)

        for day in range(forecast_days):
            for nav in calendar_nav:
                class_values = nav.get_attribute('class').split(' ')
                if (class_values[1].strip() == 'calendar__direction--tomorrow'):
                    nav.click()
                    time.sleep(random2)
                    tabs = WebDriverWait(driver, 53).until(lambda d: d.find_element_by_class_name('event__header'))
                    time.sleep(random3)
                    html_source = driver.page_source
                    match_date = today + datetime.timedelta(days=day)               
                    scrape_fixture_from_fs(fl, html_source, match_date,fixture_file)
            
    except Exception:
        log.exception("Exception occurred while loading flashscore page")
        driver.close()
        exit()

    driver.close()
    log.debug("Exit")

def load_league_standing_from_fs(fl, number_of_seasons):
    log.debug("Enter")
    chrome_path = fl.get_chrome_driver()
    driver = webdriver.Chrome(chrome_path)
    driver.implicitly_wait(120)

    fs_country_leagues = nccprops.fs_country_league_to_div_map.keys()
    count = 0
    try:
        for country, league in fs_country_leagues:
            random1 = random.randint(1, 21)
            random2 = random.randint(1, 11)
            random3 = random.randint(random1, random2 + 5) if random2 >= random1 else random.randint(random2, random1 + 5)

            time.sleep(random1)
            league = league.replace('/', '-')

            ## create the fs url
            fs_league = league.replace('.', '-')
            fs_league = fs_league.replace(' -', '-').replace('- ', '-')
            fs_league = fs_league.replace(' ', '-').lower()
            fs_country = country.strip().replace(' ', '-')
            country_league_url = 'https://www.flashscore.com/football/' + fs_country.lower() + "/" + fs_league + "/"
            driver.get(country_league_url)
            seasons_count = 0
            archive_clicked = False
            log.debug("Loading standing for Country %s League %s - URL %s" % (country, league,country_league_url))
            for i in range(number_of_seasons*2):

                if (seasons_count > number_of_seasons):
                    break

                if not archive_clicked:
                    archive_clicked = True
                    time.sleep(random.randint(1, 5))
                    archive = driver.find_element_by_id('li4')
                    archive.click()
                    seasons = driver.find_elements_by_class_name('leagueTable__seasonName')
                    time.sleep(random2)

                try:
                    if i == 0:
                        seasons[i].click()
                        seasons_count += 1
                        archive_clicked = False
                    else:
                        parent_element = seasons[i].find_element_by_xpath('..')
                        parent_name = parent_element.get_attribute('class').split(' ')
                        if (parent_name[0] == 'leagueTable__season'):
                            ## incrementing by one since there are two elements by same class and we want every second one
                            seasons[i].click()
                            seasons_count += 1
                            archive_clicked = False
                        else:
                            continue

                except Exception:
                    break

                time.sleep(random3)
                html_source = driver.page_source
                #print (html_source)
                scrape_league_standing_from_fs(fl, html_source,country, league)

    except Exception:
        log.exception("Exception occurred. Exiting...")
        driver.close()
        exit()
    driver.close()

    log.debug("Exit")


def main():

    ## initialise fileloc object
    fl = nccprops.fileloc()
    number_of_seasons = 7
    ################################################################
    #load_league_standing_from_fs(fl, number_of_seasons)
    ################################################################

    forecast_days = 7
    load_fixture_from_fs(fl, forecast_days)
   
## call main
if __name__ == "__main__":
    main()



