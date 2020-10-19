const sub_playlist = document.getElementById('submit_playlist');
const name_playlist = document.getElementById('playlist_name');
const accordion = document.getElementById('accordion');
const fgtl = document.getElementById('add_pl_formgrp');
var listOfplaylist;

let init_listOplaylist = () =>{
    listOfplaylist = document.querySelectorAll('a.card-link');
    return listOfplaylist;
};

let isPlaylistSaved = () =>{
    const accLC = accordion.lastChild;
    if((accordion.childElementCount > 0 && acclC.tagName == "DIV" && acclC.className == "card"
    && acclC.dataset['status'] == 'saved') || accordion.childElementCount == 0){
        return true;
    }else
        return false;
};

sub_playlist.addEventListener('click', function(){
    //if(isPlaylistSaved == true){
        let divcard = document.createElement('div');
        divcard.className = "card";
        let divcardHeader = document.createElement('div');
        divcardHeader.className = "card-header";
        let acardLink = document.createElement('a');
        acardLink.className = "card-link";
        acardLink.id = "card-link_" + name_playlist.value;
        acardLink.dataset['toggle'] = "collapse";
        let hrefAtt = document.createAttribute('href');
        hrefAtt.value = `#${name_playlist.value}`;
        acardLink.setAttributeNode(hrefAtt);
        acardLink.innerHTML = name_playlist.value;
        divcardHeader.appendChild(acardLink);
        divcard.appendChild(divcardHeader);

        let divcolapse = document.createElement('div');
        divcolapse.id = `${name_playlist.value}`;
        divcolapse.className = "collapse show";
        divcolapse.dataset['parent'] = "#accordion";
        let divcardbody = document.createElement('form');
        divcardbody.className = "card-body";

        let action = document.createAttribute('action');
        action.value = "/profile/create-playlist";
        divcardbody.setAttributeNode(action);

        let method = document.createAttribute('method');
        method.value = "POST";
        divcardbody.setAttributeNode(method);

        divcolapse.appendChild(divcardbody);
        divcard.appendChild(divcolapse);

        accordion.appendChild(divcard);
    /*}else{
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        if( fgtl.contains(document.getElementById('savedBefore')) ){
            document.getElementById('savedBefore').remove();
        }
        let xbtn = document.createElement('button');
        xbtn.type = "button";
        xbtn.className = "close";
        xbtn.dataset['dismiss'] = "alert";
        xbtn.innerHTML = "&times;";

        let avert = document.createElement('div');
        avert.id = 'savedBefore';
        avert.className = 'alert alert-warning';
        vaert.appendChild(xbtn);
        avert.innerHTML = '<strong>Attention!</strong> Sauvegardez d\'abord votre playlist';
        fgtl.appendChild(avert);
    }*/
});

let count_label_elem = () => {
    const cb = document.querySelector('form.card-body');
    let count_label = [];
    cb.childNodes.forEach(function(lab){
        if(lab.localName == 'label'){
            count_label.push(lab);
        }
    });
    return count_label.length;
};

let setInList = elemSet =>{
    let album_title = document.getElementsByClassName('player_album_title')[0].innerHTML;
    let player_img = document.getElementsByClassName('player_img')[0].src;
    let artist = document.getElementsByClassName('player_figcap')[0].innerHTML;

    let zic_id = elemSet.parentElement.parentElement.previousElementSibling.id;
    let zic_elem = document.getElementById(zic_id);
    let data_id = zic_elem.dataset['id'];
    let track_title = zic_elem.children[1].innerHTML;
    let track_duration = zic_elem.children[2].innerHTML;

    let elemid = document.getElementById(elemSet.innerHTML);
    let card_body = elemid.children[0];

    // pl = playlist
    let pl_album_label = document.createElement('label');
    let pl_album_img = document.createElement('img');
    pl_album_img.src = player_img;
    let pl_album_img_w = document.createAttribute('width');
    pl_album_img_w.value = "15px";
    let pl_album_img_h = document.createAttribute('height');
    pl_album_img_h.value = "15px";
    pl_album_img.setAttributeNode(pl_album_img_w);
    pl_album_img.setAttributeNode(pl_album_img_h);
    let span_form = document.createElement('span');
    let innerLabel = artist +" - "+ track_title +" - "+ track_duration +" - "+ album_title;
    span_form.innerHTML = innerLabel;
    pl_album_label.appendChild(pl_album_img);
    pl_album_label.appendChild(span_form);

    card_body.appendChild(pl_album_label);

    let tab = {
        "album_title" : album_title,
        "album_img" : player_img,
        "album_artist" : artist,
        "album_track" : track_title,
        "album_duration" : track_duration,
        "album_data" : data_id
    };

    let input_album = document.createElement('input');
    let hidden = document.createAttribute('type');
    let name = document.createAttribute('name');
    hidden.value = "hidden";
    name.value = "musicObj_" + count_label_elem();
    input_album.setAttributeNode(hidden);
    input_album.setAttributeNode(name);
    input_album.value = JSON.stringify(tab);
    //input_album.value = tab;
    card_body.appendChild(input_album);

    let sub_id = "saveList_" + elemSet.innerHTML;
    let make_btn_sub =()=>{
        let input_album_sub = document.createElement('input');
        input_album_sub.id = sub_id;
        let input_sub = document.createAttribute('type');
        input_sub.value = "button";
        input_album_sub.setAttributeNode(input_sub);
        let input_style = document.createAttribute('style');
        input_style.value = "display:block;";
        input_album_sub.setAttributeNode(input_style);
        let input_oclick = document.createAttribute('onclick');
        // input_oclick.value = "set_pypost("+ tab +","+ elemSet.innerHTML +")";
        input_oclick.value = "test_this(this)";
        input_album_sub.setAttributeNode(input_oclick);
        input_album_sub.value = "save";
        card_body.appendChild(input_album_sub);
    };

    if( !(card_body.contains(document.getElementById(sub_id))) ){
        make_btn_sub();
    }else{
        document.getElementById(sub_id).remove();
        make_btn_sub();
    }
};

let addToPlaylist = function(prim){
    prim.nextElementSibling.innerHTML = "<h6>Add to a playlist</h6>";
    listOfplaylist = 'undefined';
    init_listOplaylist();

    listOfplaylist.forEach(function(elem){
        let a_mendrop = document.createElement('a');
        a_mendrop.className = "that_playlist dropdown-item pointer";
        let a_mendrop_oclick = document.createAttribute('onclick');
        a_mendrop_oclick.value = "setInList(this)";
        a_mendrop.setAttributeNode(a_mendrop_oclick);
        a_mendrop.innerHTML = elem.innerHTML;
        prim.nextElementSibling.appendChild(a_mendrop);
    });
};

let test_this =(me)=>{
    let par =  me.parentElement;
    let tab = [];
    let playlist_name;
    for(let i=0; i<par.childElementCount - 1; i ++){
        let data_song = par.childNodes[i].value;
        if(playlist_name != par.childNodes[i].parentNode.parentElement.id){
            playlist_name = par.childNodes[i].parentNode.parentElement.id;
            tab.push(JSON.stringify({'playlist_name':playlist_name}));
        }
        console.log(par.childNodes[i]);
        if(par.childNodes[i].localName == "input" && par.childNodes[i].type == "hidden"){
            tab.push(data_song);
        }
    }
    let json_tab = JSON.stringify(tab);
    set_pypost(json_tab);
};
// FETCH ... JS API
function status_data_fetch(response){
    if(response.status !== 200){
        console.log(`Response is not 200 : ${response.status}`);
        return;
    }
    response.json().then(function(data){
        console.log(data);
    })
}

function set_pypost(entry){
    console.log("set_pypost entry => "+ entry);
    fetch(`${window.origin}/profile/create-playlist`, {
        method: "POST",
        credentials: "include",
        body: entry,
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(response){
        status_data_fetch(response);
    }).catch(function(error){
        console.log("Fetch error: "+ error);
    })
}

function set_selected_albums(entry){
    console.log("start => titre: "+ entry['title']);
    console.log("start => artist: "+ entry['artist']);
    fetch(`${window.origin}/set_selected_album`, {
        method: 'POST',
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(response){
        status_data_fetch(response);
    }).catch(function(error){
        console.log("Fetch error: "+ error);
    })
}
//*********************************
const ytb = document.getElementById("youtube-audio");
const albums = document.querySelectorAll('div.uniqAlbum');
const trackslist = document.querySelector('ul.trackslist');

const track_title = document.getElementsByClassName('track_title');

const player_album_title = document.querySelector('p.player_album_title');
const player_img = document.querySelector('img.player_img');
const player_figcap = document.querySelector('figcaption.player_figcap');
const player_genre = document.querySelector('h6.player_genre');

let moveon = function(current_track){
    let video_id = current_track.dataset['id'];
    let pos = current_track.children[0].innerHTML;
    let title = current_track.children[1].innerHTML;
    track_title[0].innerHTML = pos +" - "+ title;
    ytb.attributes[0].value = video_id;
    onYouTubeIframeAPIReady();
};

let prevOrNext = function(arg){
    track.forEach(function(elemT){
        if(ytb.dataset["video"] == elemT.dataset["id"]){
            if(arg == 1){
                ytb.dataset["video"] = elemT.nextElementSibling.dataset["id"];
            }
            else if(arg == 2){
                ytb.dataset["video"] = elemT.previousElementSibling.dataset["id"];
            }
            onYouTubeIframeAPIReady();
        }
    });
};
albums.forEach(function(elem){
    elem.addEventListener("click", function(){
        player_album_title.innerHTML = elem.children[0].innerText;
        player_img.attributes['src'].value = elem.children[2].children[0].currentSrc;
        player_figcap.innerHTML = elem.children[2].children[1].innerText;
        player_genre.innerHTML = elem.children[1].innerText;
        trackslist.innerHTML = "";

        let entry = {
            title: player_album_title.innerHTML,
            artist: player_figcap.innerHTML
        }
        set_selected_albums(entry);

        let obj = JSON.parse(elem.children[3].firstChild.data);
        let i = 1;
        obj.forEach(function(tr){
            let dinlineflex = document.createElement('div');
            dinlineflex.className = "d-inline-flex";
            let a = document.createElement('a');
            a.className = 'track text-light pointer';
            a.id = "track_nb" + i;
            let pos = "<span class='pos'>"+ tr['position'] +"</span>";
            let title = " - <span class='title'>"+ tr['title'] +"</span>";
            let duration = " - <span class='duration'>"+ tr['duration'] +"</span>";
            let zic = ' -- <i class="text-danger fa fa-times-circle" aria-hidden="true"></i>';
            if(typeof tr['url'] !== 'undefined'){
                let ytb_url = tr['url'].split('=');
                a.dataset['id'] = ytb_url[1];
                zic = ' -- <i class="text-success fa fa-check-circle" aria-hidden="true"></i>';
            }

            let dropup = document.createElement('div');
            dropup.className = "dropup";

            let btndropdown = document.createElement('button');
            btndropdown.id = "btn_track_nb" + i;

            let btnoclick = document.createAttribute('onclick');
            btnoclick.value = "addToPlaylist(this)";
            btndropdown.setAttributeNode(btnoclick);
            let btndropdown_type = document.createAttribute('type');
            btndropdown_type.value = "button";

            btndropdown.className = "btn btn-primary dropdown-toggle p-0 ml-2 text-height-0";
            btndropdown.dataset['toggle'] = "dropdown";

            btndropdown.setAttributeNode(btndropdown_type);

            let divdropmenu = document.createElement('div');
            divdropmenu.className = "dropdown-menu";

            dropup.appendChild(btndropdown);
            dropup.appendChild(divdropmenu);

            a.innerHTML = pos + title + duration + zic;
            let oclick = document.createAttribute('onclick');
            oclick.value = "moveon(this)";
            a.setAttributeNode(oclick);
            dinlineflex.appendChild(a);
            dinlineflex.appendChild(dropup);
            trackslist.appendChild(dinlineflex);
            if(tr['position'] == 1){
                moveon(a);
            }
            i ++;
        });
    });
});

let player, time_update_interval = 0;
function onYouTubeIframeAPIReady() {
    ytb.innerHTML = '<div id="youtube-player"></div>';
    ytb.style.cssText = 'width:150px;margin:2em auto;cursor:pointer;cursor:hand;display:none';
    let pa = document.getElementById("play_audio");
    pa.innerHTML = '<i id="youtube-icon" class=""></i>';
    pa.onclick = toggleAudio;
    player = new YT.Player('youtube-player', {
        height: '0',
        width: '0',
        videoId: ytb.dataset.video,
        playerVars: {
            autoplay: ytb.dataset.autoplay,
            loop: ytb.dataset.loop,
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}
function togglePlayButton(play) {
    document.getElementById("youtube-icon").className = play ? "fa fa-pause" : "fa fa-play";
}
function toggleAudio() {
    if ( player.getPlayerState() == 1 || player.getPlayerState() == 3 ) {
        player.pauseVideo();
        togglePlayButton(false);
    } else {
        player.playVideo();
        togglePlayButton(true);
    }
}
//********************* DURATION & TIMER
let formatTime = function(time){
    time = Math.round(time);

    let minutes = Math.floor(time / 60),
    seconds = time - minutes * 60;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    return minutes + ":" + seconds;
};

function updateTimerDisplay(){
    // Update current time text display.
    let curtime = document.getElementById('current_time');
    curtime.innerHTML = formatTime( player.getCurrentTime() );
    let duration = document.getElementById('duration');
    duration.innerHTML = formatTime( player.getDuration() );
}
//********************** PROGRESS BAR
$('#progress-bar').on('mouseup touchend', function (e) {
    // Calculate the new time for the video.
    // new time in seconds = total duration in seconds * ( value of range input / 100 )
    var newTime = player.getDuration() * (e.target.value / 100);
    // Skip video to new time.
    player.seekTo(newTime);
});

// This function is called by initialize()
function updateProgressBar(){
    // Update the value of our progress bar accordingly.
    $('#progress-bar').val((player.getCurrentTime() / player.getDuration()) * 100);
}
//********************** SOUND VOLUME
$('#mute-toggle').on('click', function() {
    var mute_toggle = $(this);
    if(player.isMuted()){
        player.unMute();
        mute_toggle.html("<i class=\"fa fa-volume-up\"></i>");
    }else{
        player.mute();
        mute_toggle.html("<i class=\"fa fa-volume-off\"></i>");
    }
});

$('#volume-input').on('change', function () {
    player.setVolume($(this).val());
});
//****************** INIT
function onPlayerReady(event) {
    player.setPlaybackQuality("small");
    // document.getElementById("youtube-audio").style.display = "block";
    togglePlayButton(player.getPlayerState() !== 5);
    // Update the controls on load
    updateTimerDisplay();
    updateProgressBar();
    // Clear any old interval.
    clearInterval(time_update_interval);
    // Start interval to update elapsed time display and
    // the elapsed part of the progress bar every second.
    time_update_interval = setInterval(function () {
        updateTimerDisplay();
        updateProgressBar();
    }, 1000);
}

function onPlayerStateChange(event) {
    if (event.data === 0) {
        togglePlayButton(true);
    }
}
