import re
from urllib.request import urlopen
from flask import *
from data import *
from bs4 import BeautifulSoup
from passward import pwd
import pyodbc

app = Flask(__name__)


def github_data():
    projects.clear()
    user = "Yakov-Bader"
    url = f"https://github.com/{user}?tab=repositories"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser").find_all("h3", {"class": "wb-break-all"})
    for proj in soup:
        name = proj.find("a").text
        name = name.replace("\n", "")
        name = name.replace(" ", "")

        link = f"https://github.com/{user}/{name}"
        page = urlopen(link).read()
        bs = BeautifulSoup(page, "html.parser")
        s = bs.find("article", {"class": "markdown-body entry-content container-lg"})
        readme = s.text
        readme = readme.replace("\n", ' ')
        if bs.find("h1", {"dir": "auto"}):
            h1 = bs.find("h1", {"dir": "auto"}).text
            readme = readme.lstrip(h1)

        projects.append({'name': name, 'link': link, 'text': readme})

        lan = bs.find("li", {"class": "d-inline"})
        language = lan.text
        language = language.replace("\n", '').replace(".", '').replace("%", '')
        pattern = r'[0-9]'
        language = re.sub(pattern, '', language)
        if language not in catigory[0]["skills"]:
            catigory[0]["skills"].append(language)


def SQL_data():
    string = f"workstation id=ybResume.mssql.somee.com;packet size=4096;user id=YakovBader;pwd={pwd};data source=ybResume.mssql.somee.com;persist security info=False;initial catalog=ybResume"
    conn = pyodbc.connect(string)
    cursor = conn.cursor()
    cursor.execute("select * from f")
    for row in cursor:
        print(f'{row}')


@app.route('/', methods=["POST", "GET"])
def get_data():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    github_data()
    #SQL_data()
    return jsonify(catigories, information, catigory, projects, infor)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


