from query import *
from urllib.parse import urljoin
import jinja2
import re
import requests
import json
import datetime

def scene_time_s(scene_url):
        start_time = scene_url.split('#t')[1].split(',')[0]
        return datetime.datetime.strptime(start_time, "%H:%M:%S").second

def get_video_scenes(db, video_url):
	query = q_get_all_scenes_from_video(video_url)
	r = db.do_query(query)['results']['bindings']
	def _map(x):
		s = scene_time_s(x['url']['value'])
		return {
			'url': x['url']['value'],
			'start_time': s,
			'start_time_fmt': str(datetime.timedelta(seconds=int(s))),
			'label': x['label']['value']
		}
	return list(map(_map, r))

def get_tourism_features(db, video_url):
	query = q_get_all_video_features(video_url)
	print(query)
	r = db.do_query(
		query,
		reasoning=True
	)['results']['bindings']

	result = { }
	for i in r:
		print(i)
		for k in i.keys():
			result[k] = int(i[k]['value']) > 0
	return result


def get_all_videos(db):
	r = db.do_query(q_get_all_videos())['results']['bindings']
	return list(map(lambda x: {
		'id': x[1],
		'url': x[0]['url']['value'],
		'title': x[0]['title']['value'],
		'description': x[0]['desc']['value'],
		'keywords': x[0]['tags']['value'].split(),
		'scenes': get_video_scenes(db, x[0]['url']['value'])
	}, zip(r, range(len(r)))))

_id = 0
def _map_result(db, r, expr):
	global _id
	n = 2
	l = list(filter(lambda x: x != {}, r))
	r2 = [ l[i:i+n] for i in range(0, len(l), n) ]
	
	rmap = {}
	for res in r2:
		a,b = res
		url = b['v']['value'].split('#')[0]
		matched_concept = a['y']['value']
		desc = re.sub(
			expr, 
			r'<code>\g<0></code>', 
			b['desc']['value'],
			flags=re.IGNORECASE)

		if not url in rmap.keys():
			rmap[url] = dict(
				id = _id,
				concepts = {matched_concept},
				n_concepts = 1,
				scenes = get_video_scenes(db, url),
				url = url,
				title = b['title']['value'],
				description = desc,
				keywords = b['tags']['value'].split(),
				tourism_features = get_tourism_features(db, url)
			)
			_id = _id + 1
		else:
			rmap[url]['concepts'].add(matched_concept)
			rmap[url]['n_concepts'] = len(rmap[url]['concepts'])

	return rmap

def search_videos(db, expr):
	query = q_find_concepts_by_keyword(expr)
	r0 = db.do_query(query)['results']['bindings']
	r0 = set(map(lambda x: x['x']['value'], 
		filter(lambda x: 'x' in x and not x['x']['value'].startswith('bnode'), r0)))
	r0 = map(lambda x: '<' + x + '>', r0)
	query2 = q_find_videos_by_concepts(r0)
	r = db.do_query(query2)['results']['bindings']
	r1 = set(map(lambda x: x['x']['value'] , filter(lambda x: 'x' in x, r)))
	
	return _map_result(db, r, expr)

def search_activity(db, expr, type_=":Activity"):
	query = q_find_activity_by_type_keyword(expr, type_)
	r0 = db.do_query(query, reasoning=True)['results']['bindings']
	
	return list(map(lambda x: dict(
		activity=x['a']['value'], label=x['label']['value']), r0))

def search_activity_dbpedia(db, expr):
	query = q_find_dbpedia_tourist_activity_by_regex(expr)
	print(query)
	r0 = db.do_query(query)
	r0 = r0['results']['bindings']
	return list(map(lambda x: dict(
		activity=x['a']['value'], label=x['label']['value']), r0))

def add_video(db, video_data):
	query = q_insert_video(video_data)
	print(query)
	r = db.do_update_query(query)
	print(r)

def get_activity_classes(db):
	query = q_get_activity_class()
	r = db.do_query(query, reasoning=True)['results']['bindings']
	r = dict(
			results=list(map(lambda x: dict(
				uri=x['a']['value'], label=x['label']['value']),r))
		)
	return r

def create_activity(db, activity):
	query = q_create_activity(activity)
	print(query)
	r = db.do_update_query(query)
	print(r)

class Stardog():
	def __init__(self, db_name,  auth=('admin', 'admin'), server_url='http://localhost:5820/'):
		self.server_url = server_url
		self.db_name = db_name
		self._base_url = urljoin(self.server_url, self.db_name)
		self.query_url = self._base_url + "/query"
		self.update_url = self._base_url + "/update"

		self.auth = auth
		self._query_headers = {
			'Content-Type': 'application/sparql-query',
			'Accept': 'application/sparql-results+json'
		}
		self._update_headers = {
			'Content-Type': 'application/sparql-update',
			'Accept': 'application/sparql-results+json'
		}

	def do_update_query(self, sparql_query, reasoning=False):
		try:
			r = requests.post(
				url=self.update_url,
				auth=self.auth, 
				data=sparql_query, 
				headers=self._update_headers,
				params= { } if not reasoning else {"reasoning": "true"}
			)
			return r.json()
		except:
			return None
			
	def do_query(self, sparql_query, reasoning=False):
		try:
			r = requests.post(
				url=self.query_url,
				auth=self.auth, 
				data=sparql_query, 
				headers=self._query_headers,
				params= { } if not reasoning else {"reasoning": "true"}
			)
			return r.json()
		except:
			return None

if __name__ == '__main__':
	
	db = Stardog(db_name='semantic-vid_3')
	# r = related2(db, 'water*')
	# r = get_tourism_features(db, "https://www.youtube.com/watch?v=vDR6ObwuUFM")
	# r2 = search_videos(db, 'surf*')
	# scenes = get_video_scenes(db, "https://www.youtube.com/watch?v=6bY1EpDaJ0c")
	r = search_activity(db, "surf*", type_=":Activity")
	#r = search_activity_dbpedia(db, "dolphins")
	print(get_activity_classes(db))
	


