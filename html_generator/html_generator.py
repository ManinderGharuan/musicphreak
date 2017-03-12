from jinja2 import Template
from os import path


def get_html(data):
    """Returns complete HTML"""
    TEAMPLATES_PATH = path.dirname(__file__)

    with open(path.join(TEAMPLATES_PATH, 'styles.css'), 'r') as f:
        styles = f.read()

    with open(path.join(TEAMPLATES_PATH, 'script.js'), 'r') as f:
        script = f.read()

    with open(path.join(TEAMPLATES_PATH, 'template.html'), 'r') as f:
        template = Template(f.read())

    for song in data:
        song['smallest_bitrate'] = min(song.get('mp3_links').keys())

    html = template.render(styles=styles, script=script, songs=data)

    return html
