$(function() {
    setActiveDasboardChannel();
        $.ajax({
        type: "GET",
        //the url where you want to sent the userName and password to
        url: '/user/username',
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data){
            var input = $('#message_input')
            input.attr('placeholder', data['username'] + ' please input a message to send!')
        }
    });
    // print to
});

function setActiveDasboardChannel(){
     var buttonList = $('#dash_channel_select');
     var button_li = buttonList.find('li');
     var channel_permalink = button_li.find('.channel_btn').attr("id");
     sessionStorage.current_dashboard_channel = channel_permalink;
     $('button.list-group-item.active').removeClass("active");
     $('#'+channel_permalink).addClass("active");
}

function changeDashboardChannel(id) {
    $('button.list-group-item.active').removeClass("active");
    $('#'+id).addClass("active");
    sessionStorage.current_dashboard_channel=id;
    /*
        $.ajax({
        type: "GET",
        //the url where you want to sent the userName and password to
        url: '/user/username'+ sessionStorage.current_admin_channel,
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data){
            createMembershipTable(data);
        }
    });*/
}