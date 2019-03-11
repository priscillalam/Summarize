function updateDimensions() {
    $("#player").height($("#player").width() * 9 / 16);
    $("#sidebar").height($("#player").height() - 40);
}

function keyDown(event) {
    if(event.keyCode == 13) {
        video_id = $("#header_input").val().indexOf("v=");
        document.location.href = "/summarize/" + $("#header_input").val().substr(video_id + 2);
    }
}

function setUpPlayer() {
    let tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    let firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function onYouTubeIframeAPIReady() {
    window.player = new YT.Player('player', {
        height: '390',
        width: '100%',
        videoId: window.videoId,
        events: {
            "onReady": () => window.player.playVideo()
        }
    });
}

function skipTo(playerTime) {
    window.player.seekTo(playerTime, true);
}

function skipIntervals(playerTime) {
    for (let index = 0; index < window.intervalsToSkip.length; index++) {
        let interval = window.intervalsToSkip[index];
        if (playerTime > interval[0] && playerTime < interval[1]) {
            player.seekTo(Math.min(interval[1], player.getDuration()));
            break;
        }
    }
}

function updateItemSelection(playerTime, itemsScrolledToVisible) {
    let items = document.getElementsByClassName("item");
    for (let index = 0; index < items.length; index++) {
        let item = items[index];
        let start = parseInt(item.getAttribute('data-time-start'));
        let end = parseInt(item.getAttribute('data-time-end'));
        if (playerTime > (start - 6) && playerTime < (end + 6)) {
            item.style.backgroundColor = "#EFEFEF";

            if (itemsScrolledToVisible.indexOf(item) == -1) {
                item.parentNode.scrollTop = item.offsetTop - 20;
                itemsScrolledToVisible.push(item);
            }
        } else {
            item.style.backgroundColor = "#FFFFFF";
        }
    }
}

function setUpTimer() {
    var previousPlayerTime = -1;
    var itemsScrolledToVisible = [];
    window.playIntervalsOnly = true;
    window.setInterval(() => {
        if (!player || !player.getCurrentTime) {
            return;
        }

        let playerTime = parseInt(player.getCurrentTime());

        if (playerTime < previousPlayerTime) {
            itemsScrolledToVisible = [];
        }

        if (window.playIntervalsOnly) {
            skipIntervals(playerTime);
        }
        
        updateItemSelection(playerTime, itemsScrolledToVisible);

        previousPlayerTime = playerTime;
    }, 500);
}

function setUpToggle() {
    $('input[type=checkbox]').change(function() {
        window.playIntervalsOnly = $(this).is(":checked");
    });
}

$(document).ready(() => {
    updateDimensions();
    setUpPlayer();
    setUpTimer();
    setUpToggle();
});
