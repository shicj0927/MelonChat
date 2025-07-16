$(document).ready(function(){
    var username = document.cookie.split('; ').find(row => row.startsWith('username='));
    var password = document.cookie.split('; ').find(row => row.startsWith('password='));
    console.log("Username: ", username);
    if (username && password) {
        $.get("/api/login", function(data) {
            console.log("Login: ", data);
            if (data == "OK") {
                window.location.href = "/chat";
            }
        }, "text");
    }
});

function login(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    if (username && password) {
        document.cookie = "username=" + username + "; path=/";
        document.cookie = "password=" + password + "; path=/";
        $.get("/api/login", function(data) {
            console.log("Login: ", data);
            if (data == "OK") {
                window.location.href = "/chat";
            }
            else if (data == "Not found") {
                alert("Username or password is incorrect.");
            }
            else {
                alert("Something went wrong with the server, please try again later.");
            }
        }, "text");
    }
    else {
        alert("Please enter both username and password.");
    }
}

function register(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    document.cookie = "username=" + username + "; path=/";
    document.cookie = "password=" + password + "; path=/";
    if (username && password) {
        $.get("/api/register", function(data) {
            console.log("Register: ", data);
            if (data == "OK") {
                window.location.href = "/chat";
            }
            else if (data == "Already exists") {
                alert("Username already exists, please choose another one.");
            }
            else {
                alert("Something went wrong with the server, please try again later.");
            }
        }, "text");
    }
    else {
        alert("Please enter both username and password.");
    }
}