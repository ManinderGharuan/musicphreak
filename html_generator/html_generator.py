from os import path


def get_download_links_html(mp3_links):
    template = "<a download class='download-link'\
    href={href}>{bitrate}kbps</a>"

    html = "<span class='download-icon'></span>"

    for bitrate in mp3_links.keys():
        html += template.format(bitrate=bitrate, href=mp3_links[bitrate])

    return html


def get_song_html(song):
    """Returns HTML to represent a single son"""
    template = """
    <li class='song' data-mp3='{playable_mp3}'>
        <span class='status-icon'></span>
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
    song['playable_mp3'] = song['mp3_links']['48'].strip()

    return template.format(
        mp3_links_html=get_download_links_html(song['mp3_links']),
        **song
    )


def get_html(data):
    """Returns complete HTML"""

    template = """
    <html>
    <head>
         <nav>
            <ul class='nav-bar'>
              <li style="float:left"><a class="nav-links" \
               href="#">MusicFreak.com</a></li>
              <li class='nav-items'><a class='nav-links' href=\"#\">About \
              </a></li>
           </ul>
         </nav>
        <title>Top 20 Punjabi songs</title>
        <style>{styles}</style>
        <script>{script}</script>
    </head>
    <body>
        <div class='container'>
            <h1 class='header'>Top 20 punjabi songs</h1>
            <ul class='songs-list'>{}</ul>
        </div>
        <footer class='footer'>
           <div class='footer-div'>Music Freak &copy; 2017 &copyYoFreak; \
             <a class="footer link" href="#">Privacy</a>
          </div>
       </footer>

    </body>
    </HTML>
    """

    html = ''.join([get_song_html(song) for song in data])
    css_file_path = path.dirname(__file__) + '/styles.css'
    script_file_path = path.dirname(__file__) + '/script.js'

    with open(css_file_path, 'r') as f:
        styles = f.read()

    with open(script_file_path, 'r') as f:
        script = f.read()

    return template.format(html, styles=styles, script=script)
