frec = document.getElementById("fbtn");

function check_input() {
    image = document.getElementById("image");
    user_name = document.getElementById("name");
    phone = document.getElementById("phone");
    address = document.getElementById("address");
    paswd = document.getElementById("paswd");
    hint = document.getElementById("phint");

    flag = 1;

    if (user_name.value == ''){
        flag = 0;
        alert("Please fill name!");
    }
    if (phone.value == ''){
        flag = 0;
        alert("Please fill Phone Number!");
    }
    if (address.value == ''){
        flag = 0;
        alert("Please fill address!");
    }
    if (paswd.value == ''){
        flag = 0;
        alert("Please fill password!");
    }
    if (hint.value == ''){
        flag = 0;
        alert("Please fill password hint!");
    }
    //console.log("L", image.files.length);
    //console.log("P", (image.files[0].size/1024).toFixed(1));
    if (image.files.length == 0){
        flag = 0;
        alert("Please select a photo in jpg!");
    } else{
        if ((image.files[0].size/1024).toFixed(1) > 512){
            flag = 0;
            alert("Size of the file should be less than 512 kb!");
        }
    }
    if (frec.className == "btn btn-danger"){
        flag = 0;
        alert("Please Record Finger Print!");
    }

    if (flag == 1){
        check_rec();
    }
}

function check_rec() {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    var data = JSON.stringify({"is_done":0, "time_out": 0});                                                     
    xhttp.send(data);

    frec.className = "btn btn-warning";
    frec.innerHTML = "Recording";
    frec.disabled = true;

    xhttp.onload = function() {
        res = JSON.parse(xhttp.responseText);

        if (res["is_done"] == 1){
            frec.className = "btn btn-success";
            frec.innerHTML = "Recorded";
            frec.disabled = false;
        }
        else{
            var cf = setInterval(check_SSF(),2000);
        }
    }
}

function check_SSF(){
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    var data = JSON.stringify({"is_done":0, "time_out": 0});                                                     
    xhttp.send(data);

    xhttp.onload = function() {
        res = JSON.parse(xhttp.responseText);

        if (res["is_done"] == 1){
            frec.className = "btn btn-success";
            frec.innerHTML = "Recorded";
            clearInterval(cf);
            frec.disabled = false;
            return;
        }
        if (rs["time_out"] == 1){
            frec.className = "btn btn-danger";
            frec.innerHTML = "Record";
            clearInterval(cf);
            alert("Recording failed please try again!");
            frec.disabled = false;
        }
    }
}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }