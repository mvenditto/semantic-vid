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

def q_find_concepts_by_keyword(expr, max_len=2): 
    return _find_concepts_by_keyword.render(cfg={
        'expr': expr,
        'max_len': max_len
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

if __name__ == '__main__':
    t0 = q_find_concepts_by_keyword("*water")

    t1 = q_find_videos_by_concepts([':Sport', ':WaterParkTour'])

    t2 = q_get_all_scenes_from_video('https://www.youtube.com/watch?v=vDR6ObwuUFM')
    
    t3 = q_get_all_video_features('https://www.youtube.com/watch?v=vDR6ObwuUFM')
    
    t4 = q_get_all_videos()
    
    print(t0, t1, t2, t3, t4)