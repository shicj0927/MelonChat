function logout(){
    console.log("logout!")
    document.cookie = "username=; Max-Age=0; path=/";
    document.cookie = "password=; Max-Age=0; path=/";
    window.location.href = "/";
}

function displayMessage(user, message, type, color = "black") {
    $('#chat-area').append(
        '<div class="mb-2"><strong style="color:'+color+';">'+user+'</strong>: '+message+'</div>'
    );
    $('#chat-area').scrollTop($('#chat-area')[0].scrollHeight);
}

function max(a, b) {
    return a > b ? a : b;
}

function sendMsg() {
    var username = document.cookie.split('; ').find(row => row.startsWith('username=')).replace('username=', '');
    text = document.getElementById("chat-input").value;
    if (text) {
        $.ajax({
            url: "/api/sendMsg/",
            type: "POST",
            data: text,
            contentType: "application/text",
            success: function(data) {
                console.log(data)
                if(data != "OK"){
                    alert("Failed to send message. Please try again later.")
                }
                else{
                    document.getElementById("chat-input").value = "";
                }
            },
            error: function(xhr, status, error) {
                console.error("Error sending message:", error);
                alert("Failed to send message. Please try again later.");
            }
        });
    }
    else {
        alert("Please enter a message before sending.");
    }
}

$(document).ready(function(){
    try {
        var username = document.cookie.split('; ').find(row => row.startsWith('username=')).replace('username=', '');
        var password = document.cookie.split('; ').find(row => row.startsWith('password=')).replace('password=', '');
    }
    catch (error) {
        logout();
    }
    console.log("Username: ", username);
    if (username && password) {
        $.get("/api/login/", function(data) {
            if (data != "OK") {
                console.log("Not OK!")
                logout();
            }
        }, "text");
    }
    else{
        logout();
    }
    msgNum = 0;
    $.ajax({
        url: "/api/getMsgNum/",
        type: "GET",
        async: false,
        success: function(data) {
            console.log(data);
            msgNum = parseInt(data);
        },
        error: function(xhr, status, error) {
            console.error(error);
            alert("Failed to fetch data from the server. Please try again later.");
        }
    });
    fromId = max(1, msgNum - 99);
    toId = msgNum;
    $.ajax({
        url: "/api/getMsgList/from=" + fromId + "&to=" + toId,
        type: "GET",
        async: false,
        success: function(data) {
            console.log("Messages: ", data);
            data = JSON.parse(data);
            if (data.length > 0) {
                data.forEach(function(msg) {
                    console.log(msg[2],username);
                    displayMessage(msg[2], msg[3], msg[4], msg[2] == username ? "blue" : "black");
                });
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
            alert("Failed to fetch data from the server. Please try again later.");
        }
    });
    setInterval(function() {
        $.ajax({
            url: "/api/getMsgNum/",
            type: "GET",
            success: function(data) {
                console.log("New message count: ", data);
                if (parseInt(data) > msgNum) {
                    fromId = msgNum + 1;
                    toId = parseInt(data);
                    $.ajax({
                        url: "/api/getMsgList/from=" + fromId + "&to=" + toId,
                        type: "GET",
                        success: function(data) {
                            console.log("New messages: ", data);
                            data = JSON.parse(data);
                            data.forEach(function(msg) {
                                displayMessage(msg[2], msg[3], msg[4], msg[2] == username ? "blue" : "black");
                            });
                            msgNum = parseInt(data[data.length - 1][0]);
                        },
                        error: function(xhr, status, error) {
                            console.error(error);
                            alert("Failed to fetch new messages. Please try again later.");
                        }
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
                alert("Failed to fetch message count. Please try again later.");
            }
        });
    }, 200);
    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMsg();
        }
    });
});

function sendImg() {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = function(event) {
        var file = event.target.files[0];
        if (file) {
            var formData = new FormData();
            formData.append('image', file);
            $.ajax({
                url: '/api/sendImg/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log(data);
                    if (data == "No file part") {
                        alert("No file selected. Please choose an image to upload.");
                    }
                    else if (data == "No selected file") {
                        alert("No file selected. Please choose an image to upload.");
                    }
                    else if (data == "File too large") {
                        alert("File is too large. Please select a smaller image.");
                    }
                    else if (data != "OK") {
                        alert("Failed to send image. Please try again later.");
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error sending image:", error);
                    alert("Failed to send image. Please try again later.");
                }
            });
        }
    };
    input.click();
}

function sendFile() {
    var input = document.createElement('input');
    input.type = 'file';
    input.onchange = function(event) {
        var file = event.target.files[0];
        if (file) {
            var formData = new FormData();
            formData.append('file', file);
            $.ajax({
                url: '/api/sendFile/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log(data);
                    if (data == "No file part") {
                        alert("No file selected. Please choose a file to upload.");
                    }
                    else if (data == "No selected file") {
                        alert("No file selected. Please choose a file to upload.");
                    }
                    else if (data == "File too large") {
                        alert("File is too large. Please select a smaller file.");
                    }
                    else if (data != "OK") {
                        alert("Failed to send file. Please try again later.");
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error sending file:", error);
                    alert("Failed to send file. Please try again later.");
                }
            });
        }
    };
    input.click();
}