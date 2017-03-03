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
    const target = event.currentTarget;
    const url = target.dataset.mp3;

    if (playing_audio && playing_audio.src !== url) {
        playing_audio.pause();
        playing_audio.currentTime = 0;
        playing_audio = null;
    }

    if (playing_audio) {
        if (playing_audio.paused)
            playing_audio.play();

        else
            playing_audio.pause();
    } else {
        playing_audio = new Audio(url);
        playing_audio.play();
    }
};

var showPlayIcon = function(event) {
    var target = event.target;

    target.children[0].classList.add('playing');
};

var showPauseIcon = function(event) {
    var target = event.target;
    target.children[0].classList.add('paused');
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
