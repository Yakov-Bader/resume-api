import os
from flask import *
from dotenv import load_dotenv
import requests
# from pprint import pprint

load_dotenv()
app = Flask(__name__)

API_SRT = f"{os.getenv('API_KEY')}"
infor = ["profile", "contact", "project", "skills"]
catigories = [
   {'key': "profile", 'value': "Israeli American citizen, 19 years old, finishing BCs in Computer Sience in Ashkelon College....."},
   {'key': "education", 'value':"For high school Mesivta Beit Shemesh, afeter went for a nother 3 years in Beit Medrash Derech Chaim and Ashkelon college "},
   {'key': "Languages", 'value': "speak English and Hebrew native speaker, and a bit of Arabic"},
   {'key': "volunteering", 'value': "EMT MDA Israel, Yedidim volunteer"}]
information = [{'key': "name", 'value': "Yakov Bader"}, {'key': "address", 'value': "Matityahu ......"}, {'key': "phone", 'value': "+972 53 734 4943"},
               {'key': "linkin", 'value': "link"}, {'key': "email", 'value': "yakovbader@gmail.com"}, {'key': "github", 'value': "link........."}]
catigory = [{'cati': "Languages", 'skills': []},
            {'cati': "tools", 'skills': ["Full stack development", "MongoDB"]}]
projects = []


@app.route('/', methods=["POST", "GET"])
def hello_world():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    user = "Yakov-Bader"
    url = f"https://api.github.com/users/{user}/repos"
    user_data = requests.get(url).json()
    for p in user_data:
        urlLanguages = f"https://api.github.com/repos/{user}/{p['name']}/languages"
        languages = requests.get(urlLanguages).json()
        for lan in languages:
            if lan not in catigory[0]["skills"]:
                catigory[0]["skills"].append(lan)

        projects.append({'name': p['name'], 'text': "blabla", 'link': p['html_url']})

    return jsonify(catigories, information, catigory, projects, infor)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

# https://www.techwithtim.net/tutorials/flask/http-methods-get-post/

