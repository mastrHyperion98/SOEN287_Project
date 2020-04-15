$(function() {
    console.log( "ready!" );
});
function changeChannel(id) {
    $('button.list-group-item.active').removeClass("active");
    $('#'+id).addClass("active");
    localStorage.current_admin_channel=id;
    var data = {"permalink":id}
    $.ajax({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/changeChannel',
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        data: JSON.stringify(data)
    })
}


function deleteChannel(){
    // send POST request to delete the channel
    $.ajax({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/delete/channel',
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data){
            $('#'+data['permalink']).remove();
            $('#'+data['next_active']).addClass("active");
            $("#member_table").empty();
        }
    })

    // will need to automatically change active channel to another one
}

function removeUser(user){
      var data = {"permalink":user}
    $.ajax({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/remove/member',
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        data: JSON.stringify(data)
    })
}