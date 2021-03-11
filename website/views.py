from flask import Blueprint, render_template, request, redirect, url_for
from website.recom import *
from website.tools import *
from website.web_scrap import *

views = Blueprint('views', __name__)


@views.context_processor
def base_set():
    df_team = pd.read_csv("website\\data\\team_comps")
    team_n = team_len(df_team)
    return dict(team_n=team_n)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/standard')
def standard():
    df_team = pd.read_csv("website\\data\\team_comps")
    df_items = pd.read_csv("website\\data\\item_list")
    data = recommendation([],df_team,df_items)
    html = pretty_html(data)
    return render_template("standard.html", tables=html)


@views.route('/custom')
def custom():
    return render_template("custom.html")


@views.route('/custom/select_items', methods=['GET', 'POST'])
def select_items():
    if request.method == 'POST':
        user_input = []
        for key, val in request.form.items():
            if key.startswith("item"):
                user_input.append(val)
        result = user_input
        # flash('New user input', category='success')
        return redirect(url_for('views.view_recommendations', result=result))
    return render_template("select_items.html")


@views.route('/custom/view_recommendations/<result>')
def view_recommendations(result):
    df_team = pd.read_csv("website\\data\\team_comps")
    df_items = pd.read_csv("website\\data\\item_list")
    data = recommendation(result, df_team, df_items)
    html = pretty_html(data)
    return render_template("view_recommendations.html", tables=html)


@views.route('/team/<team_id>')
def team(team_id):
    df_team = pd.read_csv("website\\data\\team_comps")
    df_char = pd.read_csv("website\\data\\team_chars_items")
    name, html = build_team_view(team_id, df_team, df_char)
    return render_template("team.html", team_id=int(team_id), table_name=name, table=html)


@views.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        with open("website/data/patch_update_history.csv", "r") as f1:
            current_patch = f1.readlines()[-1].strip('\n')
        with open("website/data/patch_check_history.csv", "r") as f1:
            latest_patch = f1.readlines()[-1].strip('\n')
        return render_template("config.html", current_patch=current_patch, latest_patch=latest_patch)
    if request.method == 'POST':
        with open("website/data/patch_update_history.csv", "r") as f1:
            current_patch = f1.readlines()[-1].strip('\n')
        latest_patch = get_patch()
        return render_template("config.html", current_patch=current_patch, latest_patch=latest_patch)


@views.route('/config/load')
def load():
    df_items, df_recipe, df_char, df_team = scrap_all()
    db_to_csv(df_items, df_recipe, df_char, df_team)
    return redirect(url_for('views.config'))
