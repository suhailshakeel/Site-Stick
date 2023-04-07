let my_loc = document.getElementById('m_loc');
let c_loc = document.getElementById('c_loc');
let loc_display = document.getElementById('loc_display');
let cd;
let id;
let webSocket;
let ucd = 0;
let map;
let gui_map = 0;
let r_onet = 0;

//Markers
let c_mark;
let s_mark;
const redIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

check_net_stat();

//Ask for permission
update_my_loc()

function check_net_stat() {
  if (navigator.onLine == true) {
    //console.log(1111);
    gui_map = 1;
    loc_display.innerHTML = '<div id="map" style="height: 100%;"></div>';
  }
}

function start_f(){
  //Start Following
  //cd = setInterval(update_my_loc, 1000); //Testing
  update_my_loc();
  ucd = 1;
}

function cancel_f(){
  //Stop Following
  //clearInterval(cd);
  navigator.geolocation.clearWatch(id);
  ucd = 0;
}

function update_my_loc() {
  //Update my location
  //console.log(1);
  if (navigator.geolocation) {
    id = navigator.geolocation.watchPosition(showPosition);
  } else {
    my_loc.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {

  //Update my location
  if (gui_map == 1) {
   //Using OpenStreetMap
   //console.log("Updateing my location.")
   //Running at once
   if (r_onet == 0) {

    //Adding Map and Client Marker
    map = L.map('map').setView([position.coords.latitude, position.coords.longitude], 18);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    c_mark = L.marker([position.coords.latitude, position.coords.longitude]).addTo(map);
    r_onet = 1;
    } else {

      //Updating Client Marker Location
      var newLatLng = new L.LatLng(position.coords.latitude, position.coords.longitude);
      c_mark.setLatLng(newLatLng);
    }
  } else{
    //Updating Client Location(Lati, Long) if internet is not available
    my_loc.innerHTML = "[" + position.coords.latitude + ", " + position.coords.longitude+"]";
  }
}

start_WS();

function start_WS() {
  //Starting Websocket
  webSocket = new WebSocket('ws://' + window.location.host + '/ws/broadcast/');
  
  /*
  webSocket.onopen = function(e) {
    console.log("Connection established!");
  };  
  */
  webSocket.onmessage = function(e) {
    //console.log(typeof(e.data));
    //console.log(e.data);
    if (ucd == 1) {
      if (gui_map == 1) {
        //console.log("Updateing client location.")
        //console.log(e.data[0], e.data[1]);
        d = JSON.parse(e.data);

        //Running at once
        if (r_onet == 1){
          //Adding Server Marker
          s_mark = L.marker([d[0], d[1]],{icon: redIcon}).addTo(map);
          r_onet = 2;
        } else {
          //Updating Server Marker Location
          var newLatLng = new L.LatLng(d[0], d[1]);
          s_mark.setLatLng(newLatLng);
        }

       } else{
        //Updating Server Location(Lati, Long) if internet is not available
        c_loc.innerHTML = e.data;
       }
    };
  };

  webSocket.onclose = function(event) {
    cancel_f();
  };

  webSocket.onerror = function(error) {
    console.log(`[error]`);
  };
}

function close_WS() {
  //Close Websocket
  webSocket.close();
}

//Scroll and height fix of editor and outputwindow
var r1 = document.getElementById("infod");
var r0 = document.getElementById("infod1");
var r2 = document.getElementById("llocs");
var r3 = document.getElementById("llocs1");
var r4 = document.getElementById("llocs2");
addEventListener('resize', changeLay);
changeLay();
function changeLay(){
    var width = document.body.clientWidth;
    if (width <768){
        r1.style.height = "35%";
        r2.style.height = "65%";
        r3.style.height = "10%";
        r4.style.height = "68%";
        r0.style.height = "100%";
    }
    else{
        r1.style.height = "100%";
        r2.style.height = "100%";
        r3.style.height = "16%";
        r4.style.height = "66%";
        r0.style.height = "34%";
    }
}