$(function() {
    $.ajax({
        type: "GET",
        //the url where you want to sent the userName and password to
        url: '/user/username',
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data) {
            var input = $('#user')
            input.text('Logged in user: ' + data['username'])
        }
    });
});