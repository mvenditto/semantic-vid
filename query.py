import os
from jinja2 import Environment, FileSystemLoader

_QUERY_TEMPLATES = os.path.join(os.getcwd(), 'templates', 'query')
_ENV = Environment(
    loader=FileSystemLoader(_QUERY_TEMPLATES)
)

_find_concepts_by_keyword = _ENV.get_template('find_concepts_by_keyword.sparql')
_find_videos_by_concepts = _ENV.get_template('find_videos_by_concepts.sparql')
_get_all_scenes_from_video = _ENV.get_template('get_all_scenes_from_video.sparql')
_get_all_video_features = _ENV.get_template('get_all_video_features.sparql')
_get_all_videos = _ENV.get_template('get_all_videos.sparql')
_find_activity_by_type_keyword = _ENV.get_template('find_activity_by_type_keyword.sparql')
_find_dbpedia_tourist_activity_by_regex = _ENV.get_template('find_dbpedia_tourist_activity_by_regex.sparql')
_insert_video = _ENV.get_template('insert_video.sparql')
_get_all_activity_class = _ENV.get_template('get_all_activity_class.sparql')
_create_activity = _ENV.get_template('create_activity.sparql')

def q_insert_video(video_data):
    return _insert_video.render(cfg=video_data)

def q_find_concepts_by_keyword(expr, max_len=2): 
    return _find_concepts_by_keyword.render(cfg={
        'expr': expr,
        'max_len': max_len
    })

def q_find_dbpedia_tourist_activity_by_regex(expr):
    return _find_dbpedia_tourist_activity_by_regex.render(cfg={
        'expr': expr
    })

def q_find_activity_by_type_keyword(expr, type_):

    return _find_activity_by_type_keyword.render(cfg={
        'expr': expr,
        'type': type_
    })

def q_find_videos_by_concepts(concepts, max_len=3):
    return _find_videos_by_concepts.render(cfg={
        'concepts': " ".join(concepts),
        'max_len': max_len
    })

def q_get_all_scenes_from_video(video_url):
    return _get_all_scenes_from_video.render(
        video_url=video_url)

def q_get_all_video_features(video_url):
    return _get_all_video_features.render(
        video_url=video_url)

def q_get_all_videos(): 
    return _get_all_videos.render()

def q_get_activity_class():
    return _get_all_activity_class.render()

def q_create_activity(new_activity):
    return _create_activity.render(cfg=new_activity)

if __name__ == '__main__':
    t0 = q_find_concepts_by_keyword("*water")

    t1 = q_find_videos_by_concepts([':Sport', ':WaterParkTour'])

    t2 = q_get_all_scenes_from_video('https://www.youtube.com/watch?v=vDR6ObwuUFM')
    
    t3 = q_get_all_video_features('https://www.youtube.com/watch?v=vDR6ObwuUFM')
    
    t4 = q_get_all_videos()

    t5 = q_find_dbpedia_tourist_activity_by_regex('dolphins')

    v = {
        'url': 'https://www.youtube.com/watch?v=mss8WYVVf3o', 
        'title': 'Virtual Spiders Evolution', 
        'description': 'sdffsdfsdf', 
        'tags': 'A B C', 
        'scenes': [
            {
                'start': 'PT0H5M44S', 'end': 'PT0H5M44S', 
                'label': 'maldives resort',
                'concepts': [
                    'http://www.owl-ontologies.com/travel.owl#KanuhuraMaldivesResort', 
                    'http://www.owl-ontologies.com/travel.owl#Surf']
            }
        ]}
    
    t6 = q_insert_video(v)
    
    print(q_create_activity(dict(name="activity", label="dasdsad", type="http://www.owl-ontologies.com/travel.owl#Relaxation")))
    # print(t0, t1, t2, t3, t4, t5)