$(function() {
    console.log( "ready2!" );
    setActiveDasboardChannel();
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
