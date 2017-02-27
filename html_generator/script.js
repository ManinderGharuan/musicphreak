var remove_showPlayIcon = function(event) {
    event.querySelector('span').classList.remove('playing');
};

var add_showPauseIcon = function(event) {
    event.querySelector('span').classList.add('paused');
};

var remove_showPauseIcon = function(event) {
    event.querySelector('span').classList.remove('paused');
};

var playing_audio = null;
var old_parentNode = null;

var playAudio = function(event) {
    let target = event.target;
    let parentNode = target.parentNode;

    if (parentNode.querySelector('span') === target) {
        let url = parentNode.querySelector(".download-link").href;

        if (playing_audio && playing_audio_src.src !== url) {
            playing_audio_src.pause();
            playing_audio = null;

            remove_showPauseIcon(old_parentNode);
            remove_showPlayIcon(old_parentNode);

            old_parentNode.addEventListener('mouseenter', showPlayIcon);
            old_parentNode.addEventListener('mouseleave', hidePlayIcon);
        }

        if (playing_audio) {
            if (playing_audio_src.paused) {
                playing_audio_src.play();

                remove_showPlayIcon(parentNode);
                add_showPauseIcon(parentNode);

            } else {
                playing_audio_src.pause();

                remove_showPauseIcon(parentNode);
                target.classList.add('playing');

            }
        } else {
            playing_audio_src = new Audio(url);
            playing_audio_src.play();

            playing_audio = true;
            old_parentNode = parentNode;

            parentNode.removeEventListener('mouseenter', showPlayIcon);
            parentNode.removeEventListener('mouseleave', hidePlayIcon);

            remove_showPlayIcon(parentNode);
            add_showPauseIcon(parentNode);
        }
    }
};

var showPlayIcon = function(event) {
    var target = event.target;

    target.children[0].classList.add('playing');
};

var hidePlayIcon = function(event) {
    var target = event.target;

    target.children[0].classList.remove('playing');
};

document.addEventListener('DOMContentLoaded', () => {
    document
        .querySelectorAll('.song')
        .forEach((el) => {
            el.addEventListener('click', playAudio, true);
            el.addEventListener('mouseenter', showPlayIcon);
            el.addEventListener('mouseleave', hidePlayIcon);
        });
}, false);
