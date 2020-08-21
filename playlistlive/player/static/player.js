var myVar;
var curr;  

var player;

function newPlayer(){

  // get access token
  const token = '{{access_token}}';
  player = new Spotify.Player({
    name: 'Web Playback SDK Quick Start Player',
    getOAuthToken: cb => { cb(token); }
  });

  // Error handling
  player.addListener('initialization_error', ({ message }) => { console.error(message); });
  player.addListener('authentication_error', ({ message }) => { console.error(message); });
  player.addListener('account_error', ({ message }) => { console.error(message); });
  player.addListener('playback_error', ({ message }) => { console.error(message); });

  // Playback status updates
  player.addListener('player_state_changed', state => { console.log(); });

  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
  });

  // Connect to the player!
  player.connect();

  console.log("connected to the player");

}

function getCurrentState(){
  player.getCurrentState().then(state => {
    if (!state) {
      console.log('User is not playing music through the Web Playback SDK');
      return;
    }

    let {
      current_track,
      next_tracks: [next_track]
    } = state.track_window;

    curr = current_track;
    // console.log("currently playing: ", curr);

    title = curr.name;
    artist = curr.artists[0].name;
    album_img = curr.album.images[0].url;

    $("#currsong-title").html(title); // display time on the page
    $("#currsong-artist").html(artist);
    $("#currsong-img").attr("src", album_img);
  });
}

window.onSpotifyWebPlaybackSDKReady = newPlayer();

window.setInterval(getCurrentState, 1000);