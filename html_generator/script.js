var playing_audio = false;

var playAudio = function(event) {
    console.log(event.srcElement, event.target);

    if (playing_audio && playing_audio.src !== url) {
        playing_audio.pause();
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
