from os import path

def get_download_links_html(mp3_links):
    template = "<a download class='download-link' href={href}>{bitrate}kbps</a>"
    html = "<span class='download-icon'></span>"

    for bitrate in mp3_links.keys():
        html += template.format(bitrate=bitrate, href=mp3_links[bitrate])

    return html


def get_song_html(song):
    """Returns HTML to represent a single son"""
    template = """
    <li class='song'>
        <div class='thumb' style="background-image: url({image_link})"></div>
        <div class='tile-contents'>
            <h2 class='song-name'>{name}</h2>
            <p class='song-artist'>{artist}</p>
            <div class='download-links'>
                {mp3_links_html}
            </div>
        </div>
    </li>
    """
    song['artist'] = ', '.join(song['artist'])

    return template.format(
        mp3_links_html=get_download_links_html(song['mp3_links']),
        **song
    )


def get_html(data):
    """Returns complete HTML"""

    template = """
    <html>
    <head>
        <title>Top 20 Punjabi songs</title>
        <style>{styles}</style>
    </head>
    <body>
        <div class='container'>
            <h1 class='header'>Top 20 punjabi songs</h1>
            <ul class='songs-list'>{}</ul>
        </div>
    </body>
    </HTML>
    """

    html = ''.join([get_song_html(song) for song in data])
    css_file_path = path.dirname(__file__) + '/styles.css'

    with open(css_file_path, 'r') as f:
        styles = f.read()

    return template.format(html, styles=styles)
