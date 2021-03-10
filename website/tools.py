
from bs4 import BeautifulSoup
from selenium import webdriver


def build_team_view(id, df_team, df_char):
    idn = int(id)

    name = df_team.loc[idn, 'team_name']
    df = df_char.loc[df_char['team_id'] == idn, 'team_id':'item3']

    def blank(val):
        if val == "na":
            return 'color: lightgrey'
        else:
            return 'color: black'

    html = df.rename(columns = {"char_name": "Character","item1": "Combined item 1","item2": "Combined item 2", "item3": "Combined item 3"}).style.applymap(blank).hide_columns(['team_id']).hide_index().render()
    return name, html


def team_len(df_team):
    return df_team.shape[0]


def get_patch():
    url = 'https://tftactics.gg/tierlist/team-comps'

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    patch = soup.find(attrs={"class": "update-patch"}).get_text()

    f = open("website/data/patch_check_history.csv", "a")
    f.write(patch + "\n")
    f.close()

    driver.quit()
    return patch


def pretty_html(df):
    new_df = df.rename(columns={"team_id": "Team ID", "team_name": "Team Name", "team_tier": "Tier", "team_ramp": "Ramp up"})

    def color_map(val):
        if "/" in str(val) and (len(val) == 3) and (val[0] == val[-1]) and (val[-1] != "0"):
            color = 'lightblue'
        elif "/" in str(val) and (len(val) == 3) and (val[0] < val[-1]) and (val[-1] != "0"):
            color = 'lightpink'
        elif "/" in str(val) and (len(val) == 3) and (val[0] > val[-1]) and (val[-1] != "0"):
            color = 'moccasin'
        else:
            color = 'white'
        return 'background-color: %s' % color

    html = new_df.style.applymap(color_map).hide_index().render()
    return html
