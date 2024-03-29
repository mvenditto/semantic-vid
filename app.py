from flask import Flask, render_template, request, url_for, jsonify
from flask_cors import CORS
from utils import *
from stardog_util import *
import requests

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
CORS(app)

db = Stardog(db_name='semantic-vid_3')

@app.route('/')
def index():
	return render_template('search_page_sui.html')

@app.route('/add_video_wizard')
def add_video_wizard():
	return render_template('add_video_wizard.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
	content = request.get_json(silent=True)
	add_video(db, content)
	return jsonify(dict(result="success"))

@app.route('/activity_search/<atype>/<expr>')
def activity_search(atype, expr):
	try:
		result = dict(success=True, results=search_activity(db, expr+'*', type_=atype))
		return jsonify(result)
	except Exception as e:
		return jsonify(dict(success=False, msg=str(e)))

@app.route('/activity_classes/')
def activity_classes():
	return jsonify(get_activity_classes(db))

@app.route('/add_activity', methods=['POST'])
def add_activity():
	content = request.get_json(silent=True)
	create_activity(db, content)
	return jsonify(dict(result="success"))

@app.route('/yt_video_info/<video_id>')
def yt_video_info(video_id):
	r = requests.get(f"http://youtube.com/get_video_info?video_id={video_id}")
	return jsonify(dict(map(lambda v: v.split("="), r.text.split("&"))))

@app.route('/search/<keyword>')
def search(keyword):
	test = list(paginate(list(search_videos(db, keyword).values())))
	return render_template('video_card_template_yt_sui.html', vid_pages=test)

	