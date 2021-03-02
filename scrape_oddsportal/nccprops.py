import os
import sys
from pathlib import Path
import platform
from datetime import datetime, date
## this the class definition for all the file locations
## we will store all file locations as class static variables

class fileloc(object):   
    HOME_LOC= Path(__file__).resolve().parent
    DATA_LOC = os.path.join(HOME_LOC, 'ncc-data')   

    OPERATING_SYSTEM = platform.system()
    DOWNLOADS_FOOTYSTATS = 'footystats'
    DOWNLOADS_ODDS_PORTAL = 'oddsportal'
    DOWNLOADS_LEAGUE_STANDING = 'leaguestandings'
    LOG_FORMAT = 'format.log'
    CHROME_DRIVER = 'chromedriver.exe'
    
    ## this is a singleton class
    _instance = None
    def __new__(self):
        if not self._instance:
            self._instance = object.__new__(self)   
            self.initialised = False         
        return self._instance
    
    def __init__(self):
        if not (self.initialised):
            ## create the required directories
                
            if not (os.path.isdir(self.HOME_LOC)):
                print("Error: Home directory dont exists.")
                self.initialised = False
                exit()

            if not (os.path.isdir(self.DATA_LOC)):
                ## create the directory
                os.mkdir(self.DATA_LOC)  

            if not (os.path.isdir(os.path.join(self.DATA_LOC, self.DOWNLOADS_ODDS_PORTAL))):
                ## create the directory
                os.mkdir(os.path.join(self.DATA_LOC, self.DOWNLOADS_ODDS_PORTAL))
            
            self.initialised = True
    
    def get_initialisation_status(self):
        return self.initialised
    
    def get_home_path(self):
        return self.HOME_LOC
        
    def get_data_path(self):
        return self.DATA_LOC 
    
    def get_oddsportal_dir(self):
        return (os.path.join(self.DATA_LOC, self.DOWNLOADS_ODDS_PORTAL))   

    def get_chrome_driver(self):
        return (os.path.join(self.HOME_LOC,self.CHROME_DRIVER))
    
    def get_os(self):
        if (self.OPERATING_SYSTEM == 'Windows'):
            return 'Windows'
        else:
            return self.OPERATING_SYSTEM


##################################################################################################
##################################################################################################
 
CURRENT_YEAR = date.today().year

## for downloading from https://www.football-data.co.uk/ 
 
season_list = ['2015','2016','2017','2018','2019','2020','2021']

fs_country_league_to_div_map = {
    ('ENGLAND','Premier League'):'1',('ENGLAND','Championship'):'2',('ENGLAND','League One'):'3',('ENGLAND','League Two'):'4',('ENGLAND','National League'):'5',
    ('SCOTLAND','Premiership'):'1',('SCOTLAND','Championship'):'2',('SCOTLAND','League One'):'3',('SCOTLAND','League Two'):'4',
    ('GERMANY','Bundesliga'):'1',('GERMANY','2. Bundesliga'):'2',('GERMANY','3. Liga'):'3',('GERMANY','Regionalliga North'):'4',
    ('GERMANY','Regionalliga Nordost'):'4',('GERMANY','Regionalliga West'):'4',('GERMANY','Regionalliga Sudwest'):'4',('GERMANY','Regionalliga Bayern'):'4',
    ('GERMANY','Oberliga Baden-Wurttemberg'):'5',('GERMANY','Oberliga Bayern Nord'):'5',('GERMANY','Oberliga Bayern Sud'):'5',('GERMANY','Oberliga Bremen'):'5',
    ('GERMANY','Oberliga Hamburg'):'5',('GERMANY','Oberliga Hessen'):'5',('GERMANY','Oberliga Mittelrhein'):'5',('GERMANY','Oberliga Niederrhein'):'5',
    ('GERMANY','Oberliga Niedersachsen'):'5',('GERMANY','Oberliga NOFV-Nord'):'5',('GERMANY','Oberliga NOFV- Sud'):'5',
    ('GERMANY','Oberliga Rheinland-Pfalz-Saar'):'5',('GERMANY','Oberliga Schleswig-Holstein'):'5',('GERMANY','Oberliga Westfalen'):'5',
    ('SPAIN','LaLiga'):'1',('SPAIN','LaLiga2'):'2',('SPAIN','Segunda Division B - Group 1'):'3',('SPAIN','Segunda Division B - Group 2'):'3',
    ('SPAIN','Segunda Division B - Group 3'):'3',('SPAIN','Segunda Division B - Group 4'):'3',
    ('ITALY','Serie A'):'1',('ITALY','Serie B'):'2',('ITALY','Serie C - Group A'):'3',('ITALY','Serie C - Group B'):'3',('ITALY','Serie C - Group C'):'3',
    ('FRANCE','Ligue 1'):'1',('FRANCE','Ligue 2'):'2',
    ('NETHERLANDS','Eredivisie'):'1',('NETHERLANDS','Eerste Divisie'):'2',('NETHERLANDS','Tweede Divisie'):'3',('NETHERLANDS','Derde Divisie'):'4',
    ('BELGIUM','Jupiler League'):'1',('GREECE','Super League'):'1',('PORTUGAL','Primeira Liga'):'1',('TURKEY','Super Lig'):'1',
    ('AUSTRIA','Tipico Bundesliga'):'1',('AUSTRIA','2. Liga'):'2',
    ('CZECH REPUBLIC','1. Liga'):'1',('CZECH REPUBLIC','Division 2'):'2',
    ('SWITZERLAND','Super League'):'1',('RUSSIA','Premier League'):'1',('ROMANIA','Liga 1'):'1',
    ('SWEDEN','Allsvenskan'):'1',('SWEDEN','Superettan'):'2',('SWEDEN','Division 1 - Norra'):'3',('SWEDEN','Division 1 - Sodra'):'3',
    ('NORWAY','Eliteserien'):'1',('NORWAY','OBOS-ligaen'):'2',('FINLAND','Veikkausliiga'):'1',('FINLAND','Ykkonen'):'2',
    ('FINLAND','Kakkonen Group A'):'3',('FINLAND','Kakkonen Group B'):'3',('FINLAND','Kakkonen Group C'):'3',
    ('ESTONIA','Meistriliiga'):'1',('ESTONIA','Esiliiga'):'2',('ICELAND','Pepsideild'):'1',('ICELAND','Inkasso-deildin'):'2',
    ('POLAND', 'Ekstraklasa'): '1',('IRELAND', 'Premier Division'): '1',('DENMARK', 'Superliga'): '1',
    ('USA', 'MLS'): '1', ('BRAZIL', 'Serie A'): '1', ('ARGENTINA', 'Superliga'): '1',('ARGENTINA', 'Liga Profesional'): '1',('MEXICO', 'Liga MX'): '1',
    ('JAPAN', 'J1 League'): '1', ('JAPAN', 'J2 League'): '2',
    ('CHINA', 'Super League'): '1',
}

op_country_league_to_div_map_load = {
    ('AUSTRIA', '2. Liga'): ['austria', '2-liga'], ('CZECH REPUBLIC', '1. Liga'): ['czech-republic', '1-liga'],
    ('CZECH REPUBLIC', 'Division 2'): ['czech-republic', 'division-2'],
    ('ESTONIA', 'Meistriliiga'): ['estonia', 'meistriliiga'], ('ESTONIA', 'Esiliiga'): ['estonia', 'esiliiga'],
    ('FINLAND', 'Ykkonen'): ['finland', 'ykkonen'],
    ('ICELAND', 'Pepsideild'): ('iceland', 'pepsideild'),
    ('ICELAND', 'Inkasso-deildin'): ('iceland', 'inkasso-deildin'),
    ('GERMANY', '3. Liga'): ['germany', '3-liga'], ('GERMANY', 'Regionalliga North'): ('germany', 'regionalliga-north'),
    ('GERMANY', 'Regionalliga Nordost'): ('germany', 'regionalliga-nordost'),
    ('GERMANY', 'Regionalliga West'): ('germany', 'regionalliga-west'),
    ('GERMANY', 'Regionalliga Sudwest'): ('germany', 'regionalliga-sudwest'),
    ('GERMANY', 'Regionalliga Bayern'): ('germany', 'regionalliga-bayern'),
    ('GERMANY', 'Oberliga Baden-Wurttemberg'): ['germany', 'oberliga-baden-wurttemberg'],
    ('GERMANY', 'Oberliga Bayern Nord'): ['germany', 'oberliga-bayern-nord'],
    ('GERMANY', 'Oberliga Bayern Sud'): ['germany', 'oberliga-bayern-sud'],
    ('GERMANY', 'Oberliga Bremen'): ['germany', 'oberliga-bremen'],
    ('GERMANY', 'Oberliga Hamburg'): ['germany', 'oberliga-hamburg'],
    ('GERMANY', 'Oberliga Hessen'): ['germany', 'oberliga-hessen'],
    ('GERMANY', 'Oberliga Mittelrhein'): ['germany', 'oberliga-mittelrhein'],
    ('GERMANY', 'Oberliga Niederrhein'): ['germany', 'oberliga-niederrhein'],
    ('GERMANY', 'Oberliga Niedersachsen'): ['germany', 'oberliga-niedersachsen'],
    ('GERMANY', 'Oberliga NOFV-Nord'): ['germany', 'oberliga-nofv-nord'],
    ('GERMANY', 'Oberliga NOFV- Sud'): ['germany', 'oberliga-nofv-sud'],
    ('GERMANY', 'Oberliga Rheinland-Pfalz-Saar'): ['germany', 'oberliga-rheinland-pfalz-saar'],
    ('GERMANY', 'Oberliga Schleswig-Holstein'): ['germany', 'oberliga-schleswig-holstein'],
    ('GERMANY', 'Oberliga Westfalen'): ['germany', 'oberliga-westfalen'],
    ('NETHERLANDS', 'Eerste Divisie'): ['netherlands', 'eerste-divisie'],
    ('SWEDEN', 'Superettan'): ['sweden', 'superettan'],
    ('SWEDEN', 'Division 1 - Sodra'): ['sweden', 'division-1-sodra'],
    ('SWEDEN', 'Division 1 - Norra'): ['sweden', 'division-1-norra'],
    ('NORWAY', 'OBOS-ligaen'): ['norway', 'obos-ligaen'],
    ('JAPAN', 'J2 League'): ['japan', 'j2-league']
}

op_country_league_to_div_map = {
    ('AUSTRIA','2. Liga'):['austria','2-liga'],('CZECH REPUBLIC','1. Liga'):['czech-republic','1-liga'],
    ('CZECH REPUBLIC','Division 2'):['czech-republic','division-2'],
    ('ESTONIA','Meistriliiga'):['estonia','meistriliiga'],('ESTONIA','Esiliiga'):['estonia','esiliiga'],
    ('FINLAND','Ykkonen'):['finland','ykkonen'],
    ('ICELAND','Pepsideild'):('iceland','pepsideild'),('ICELAND','Inkasso-deildin'):('iceland','inkasso-deildin'),
    ('GERMANY','3. Liga'):['germany','3-liga'],('GERMANY','Regionalliga North'):('germany','regionalliga-north'),
    ('GERMANY','Regionalliga Nordost'):('germany','regionalliga-nordost'),('GERMANY','Regionalliga West'):('germany','regionalliga-west'),
    ('GERMANY','Regionalliga Sudwest'):('germany','regionalliga-sudwest'),('GERMANY','Regionalliga Bayern'):('germany','regionalliga-bayern'),
    ('GERMANY', 'Oberliga Baden-Wurttemberg'): ['germany', 'oberliga-baden-wurttemberg'],('GERMANY', 'Oberliga Bayern Nord'): ['germany', 'oberliga-bayern-nord'],
    ('GERMANY', 'Oberliga Bayern Sud'): ['germany', 'oberliga-bayern-sud'],('GERMANY','Oberliga Bremen'): ['germany', 'oberliga-bremen'],
	('GERMANY', 'Oberliga Hamburg'): ['germany', 'oberliga-hamburg'],('GERMANY', 'Oberliga Hessen'): ['germany', 'oberliga-hessen'],
    ('GERMANY', 'Oberliga Mittelrhein'): ['germany', 'oberliga-mittelrhein'],('GERMANY', 'Oberliga Niederrhein'): ['germany', 'oberliga-niederrhein'],
    ('GERMANY', 'Oberliga Niedersachsen'): ['germany', 'oberliga-niedersachsen'],('GERMANY', 'Oberliga NOFV-Nord'): ['germany', 'oberliga-nofv-nord'],
    ('GERMANY', 'Oberliga NOFV- Sud'): ['germany', 'oberliga-nofv-sud'],('GERMANY', 'Oberliga Rheinland-Pfalz-Saar'): ['germany', 'oberliga-rheinland-pfalz-saar'],
	('GERMANY', 'Oberliga Schleswig-Holstein'): ['germany', 'oberliga-schleswig-holstein'],('GERMANY', 'Oberliga Westfalen'): ['germany', 'oberliga-westfalen'],
    ('NETHERLANDS','Eerste Divisie'):['netherlands','eerste-divisie'],
    ('SWEDEN','Superettan'):['sweden','superettan'],('SWEDEN','Division 1 - Sodra'):['sweden','division-1-sodra'],
    ('SWEDEN','Division 1 - Norra'):['sweden','division-1-norra'],
    ('NORWAY','OBOS-ligaen'):['norway','obos-ligaen'],
    ('JAPAN', 'J2 League'):['japan', 'j2-league']
}

current_season_map = {
    'ENGLAND':'2021',
    'SCOTLAND':'2021',
    'GERMANY':'2021',
    'SPAIN':'2021',
    'ITALY':'2021',
    'FRANCE':'2021',
    'NETHERLANDS':'2021',
    'SWEDEN':'2020',
    'NORWAY':'2020',
    'FINLAND':'2020',
    'ESTONIA':'2020',
    'JAPAN':'2020'

}

Mandatory_Match_Features = ['Country', 'League', 'Div', 'Season', 'Date', 'Time', 'HomeTeam', 'HomeTeam_Alias', 'AwayTeam', 'AwayTeam_Alias','FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A','StatSource','FS_League']
MATCH_KEY_FEATURES = ['Country', 'League', 'Season', 'HomeTeam_Alias', 'AwayTeam_Alias','Date']

SEASON_MAP = {'2012/2013':'2013','2013/2014':'2014','2014/2015':'2015','2015/2016':'2016','2016/2017':'2017','2017/2018':'2018',
              '2018/2019':'2019','2019/2020':'2020','2020/2021':'2021','2021/2022':'2022',
              '2012-2013':'2013','2013-2014':'2014','2014-2015':'2015','2015-2016':'2016','2016-2017':'2017','2017-2018':'2018',
              '2018-2019':'2019','2019-2020':'2020','2020-2021':'2021','2021-2022':'2022',
              ## added spacially for covid situation
                '2019-2021':'2020', '2019/2021':'2020'
              }

def get_current_season(country):
    country = country.upper()
    try:
        season = current_season_map[country]
        return season        
    except Exception:
        return CURRENT_YEAR