var remove_showPlayIcon = function(event) {
    event.querySelector('span').classList.remove('playing');
};

var add_showPauseIcon = function(event) {
    event.querySelector('span').classList.add('paused');
};

var remove_showPauseIcon = function(event) {
    event.querySelector('span').classList.remove('paused');
};

var playing_audio = false;
var old_parentNode = null;

var playAudio = function(event) {
    let parentNode = event.target.parentNode;
    let url = parentNode.querySelector(".download-link").href;

    if (playing_audio && playing_audio_src.src !== url) {
        if (parentNode.querySelector('span') === event.target){
            playing_audio_src.pause();
            playing_audio = null;

            remove_showPauseIcon(old_parentNode);

            old_parentNode.addEventListener('mouseenter', showPlayIcon);
            old_parentNode.addEventListener('mouseleave', hidePlayIcon);
        }
    } else if (!playing_audio && typeof playing_audio_src !== 'undefined' && playing_audio_src !== url) {
        if (parentNode.querySelector('span') === event.target) {
            remove_showPlayIcon(old_parentNode);

            old_parentNode.addEventListener('mouseenter', showPlayIcon);
            old_parentNode.addEventListener('mouseleave', hidePlayIcon);
        }
    }

    if (playing_audio) {
        if (parentNode.querySelector('span') === event.target){
            if (playing_audio_src.paused){
                playing_audio_src.play();

                remove_showPlayIcon(parentNode);
                add_showPauseIcon(parentNode);

                playing_audio = true;
            } else{
                playing_audio_src.pause();

                remove_showPauseIcon(parentNode);

                parentNode.querySelector("span").classList.add('playing');
                parentNode.addEventListener('mouseenter', showPlayIcon);
                parentNode.addEventListener('mouseleave', hidePlayIcon);

                playing_audio = false;
            }
        }
    } else {
        if (parentNode.querySelector('span') === event.target){
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
