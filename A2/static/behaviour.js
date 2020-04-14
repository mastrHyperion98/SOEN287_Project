
function chatContent(id) {
    $('button.list-group-item.active').removeClass("active");
    $('#'+id).addClass("active");
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
    // remove the button
    //$('#'+id).remove()

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
            $('#'+data['permalink']).remove()
        }
    })
}