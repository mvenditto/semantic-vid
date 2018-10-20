from flask import Flask, render_template, url_for
from utils import *
from stardog_util import Stardog, search_videos

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

db = Stardog(db_name='semantic-vid_3')

@app.route('/')
def index():
	return render_template('search_page_sui.html')


@app.route('/search/<keyword>')
def search(keyword):
	test = list(paginate(list(search_videos(db, keyword).values())))
	return render_template('video_card_template_yt_sui.html', vid_pages=test)
	