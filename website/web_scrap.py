from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def scrap_all():
    url = 'https://tftactics.gg/tierlist/team-comps'

    driver = webdriver.Chrome('.\chromedriver.exe')
    driver.get(url)

    # switch to beautiful soup for data cleaning
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # get team info
    team_portraits = soup.find_all(attrs={"class": "team-portrait"})

    team_tier = []
    team_name = []
    team_ramp = []

    for item in team_portraits:
        team = item.get_text("|").split("|")
        team_tier.append(team[0])
        team_name.append(team[1])
        team_ramp.append(team[2])

    team_id = [i for i in range(len(team_name))]

    # get character and items

    character_wrapper = soup.find_all(attrs={"class": "character-wrapper"})

    char_items = []
    characters = []
    items = []

    for item in character_wrapper:
        parent = item.find_parent("div", class_="team-portrait")
        name = parent.find(attrs={"class": "team-name-elipsis"}).get_text("|").split("|")[0]
        id = team_name.index(name)
        char_item = item.img.get("src").replace("https://rerollcdn.com/", "").replace(".png", "").replace("Skin/4.5/",
                                                                                                          "").split("/")
        char_item[1] = item.img["alt"]
        char_items.append([id, char_item])

    for i in range(len(char_items)):

        if char_items[i][1][0] == "characters":
            characters.append([char_items[i][0], char_items[i][1][1]])
            items.append(["na", "na", "na"])

        if char_items[i][1][0] == "items":
            if char_items[i - 1][1][0] == "characters":
                items[len(items) - 1][-3] = char_items[i][1][1]
            elif char_items[i - 2][1][0] == "characters":
                items[len(items) - 1][-2] = char_items[i][1][1]
            elif char_items[i - 3][1][0] == "characters":
                items[len(items) - 1][-1] = char_items[i][1][1]


    dict_team = {'team_id': team_id, 'team_name': team_name, 'team_tier': team_tier, 'team_ramp': team_ramp}
    df_team = pd.DataFrame(dict_team)

    char_columns = ["team_id", "char_name"]
    df_char = pd.DataFrame(characters, columns=char_columns)
    df_char[['item1', 'item2', 'item3']] = items

    patch = soup.find(attrs={"class": "update-patch"}).get_text()


    ##### section 2: item list web scrapping #######

    url2 = 'https://tftactics.gg/item-builder'

    driver.get(url2)

    # switch to beautiful soup for data cleaning

    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, 'html.parser')

    # get item lists
    base_items = soup2.find_all(attrs={"type": "Base"})
    base = []
    for item in base_items:
        item_name = item.img.get("alt")
        if [item_name, "base"] not in base:
            base.append([item_name, "base"])

    combined_items = soup2.find_all(attrs={"type": "Combined"})
    combined = []
    for item in combined_items:
        item_name = item.img.get("alt")
        if [item_name, "combined"] not in combined:
            combined.append([item_name, "combined"])

    all_items = base + combined

    df_items = pd.DataFrame(all_items, columns=["item_name", "item_type"])

    ###### section 3: item recipe web scrapping #######

    url3 = 'https://tftactics.gg/db/items'

    driver.get(url3)

    html3 = driver.page_source
    soup3 = BeautifulSoup(html3, 'html.parser')

    # get recipe
    rows = soup3.find_all(attrs={"role": "row"})

    recipe_list = {}

    for row in rows:
        items = row.find_all(attrs={"class": "character-icon"})
        if items is not None:
            if len(items) == 3:
                comb = items[0].get("alt")
                recipe_1 = items[1].get("alt")
                recipe_2 = items[2].get("alt")
                recipe_list[comb] = [recipe_1, recipe_2]

    df_recipe = pd.DataFrame.from_dict(recipe_list, orient='index', columns=['recipe_1', 'recipe_2']).rename_axis(
        'item_name').reset_index()

    driver.quit()

    f = open("website/data/patch_update_history.csv", "a")
    f.write(patch + "\n")
    f.close()

    return df_items, df_recipe, df_char, df_team


def db_to_csv(df_items, df_recipe, df_char, df_team):
    base_item_lst = df_items.loc[df_items['item_type'] == "base"]

    def recipe_usage_count(r1, r2, i):
        return int(r1 == i) + int(r2 == i)

    def char_usage_count(i1, i2, i3, i):
        n1 = 0
        n2 = 0
        n3 = 0
        if not i1 == "na":
            n1 = df_recipe.loc[df_recipe["item_name"] == i1, i].tolist()[0]
        if not i2 == "na":
            n2 = df_recipe.loc[df_recipe["item_name"] == i2, i].tolist()[0]
        if not i3 == "na":
            n3 = df_recipe.loc[df_recipe["item_name"] == i3, i].tolist()[0]
        return n1 + n2 + n3

    def team_usage_count(id, i):
        return df_char.loc[df_char["team_id"] == id, i].sum()

    for i in base_item_lst["item_name"].tolist():
        df_recipe[i] = df_recipe.apply(lambda row: recipe_usage_count(row["recipe_1"], row["recipe_2"], i), axis=1)
        df_char[i] = df_char.apply(lambda row: char_usage_count(row["item1"], row["item2"], row["item3"], i), axis=1)
        df_team[i] = df_team.apply(lambda row: team_usage_count(row["team_id"], i), axis=1)

    df_team.to_csv("website\\data\\team_comps")
    df_char.to_csv("website\\data\\team_chars_items")
    df_items.to_csv("website\\data\\item_list")
    df_recipe.to_csv("website\\data\\item_recipe")
