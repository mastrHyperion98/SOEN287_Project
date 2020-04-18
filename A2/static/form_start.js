/*
Created by Steven Smith 40057065
Created for: SOEN 287 W 2020 Concordia

Generic logged in user message on page load. Not used on Dashboard or channels as they display it elsewhere
 */
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