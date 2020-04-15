$(function() {
    console.log( "ready2!" );
    setActiveChannel();
    // print to
    $.ajax({
        type: "GET",
        //the url where you want to sent the userName and password to
        url: '/channels/members/'+ sessionStorage.current_admin_channel,
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data){
            createMembershipTable(data);
        }
    });
});

function setActiveChannel(){
     var buttonList = $('#channel_select');
     var button_li = buttonList.find('li');
     var channel_permalink = button_li.find('.channel_btn').attr("id");
     sessionStorage.current_admin_channel = channel_permalink;
     $('button.list-group-item.active').removeClass("active");
     $('#'+channel_permalink).addClass("active");
}

function createMembershipTable(data){
         var master = $('#member_table_holder');
         master.empty();
         var $table = $('<table>');
            // set attribute
            $table.attr("class", "table table-striped table-dark")
                // thead
                .append('<thead>').children('thead')
                .append('<tr />').children('tr').append('<th class="text-center">Username</th><th class="text-center">Account Permalink</th>' +
                '<th class="text-center">Last Login</th><th class="text-center">isAdmin</th><th class="text-center">Options</th>');
            //tbody
            var $tbody = $table.append('<tbody />').children('tbody');
            // add row
            $.each(data, function(obj, item) {
                var permalink = item['permalink'];
                var options = item['is_admin'] ? "</td>" :'<button class="btn btn-secondary"' +
                    ' onclick="removeUser('+"'"+permalink+"'"+')">Remove User</button></td>';
                $tbody.append('<tr />').children('tr:last')
                    .append("<td class=\"text-center\">" + item['username'] + "</td>")
                    .append("<td class=\"text-center\">" + permalink + "</td>")
                    .append("<td class=\"text-center\">" + item['login'] + "</td>")
                    .append("<td class=\"text-center\">" + item['is_admin'] + "</td>")
                    .append("<td class=\"text-center\">" + options);
                $tbody.children('tr:last').attr('id', 'tr_'+permalink);
            });

            if(data.length !== 0) {
                $tbody.append('<tr />').children('tr:last')
                    .append("<td class=\"text-center\"> </td>")
                    .append("<td class=\"text-center\"> </td>")
                    .append("<td class=\"text-center\"> </td>")
                    .append("<td class=\"text-center\"> </td>")
                    .append('<td class="text-center"><a href="/add/member">Add User</a></td>');
            }
            // add table to dom
            $table.appendTo(master);
}

function changeChannel(id) {
    $('button.list-group-item.active').removeClass("active");
    $('#'+id).addClass("active");
    console.log("BEFORE:" + sessionStorage.current_admin_channel)
    sessionStorage.current_admin_channel=id;
    console.log("AFTER:" + sessionStorage.current_admin_channel)
        $.ajax({
        type: "GET",
        //the url where you want to sent the userName and password to
        url: '/channels/members/'+ sessionStorage.current_admin_channel,
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data){
            createMembershipTable(data);
        }
    });
}

function deleteChannel(){
    // send POST request to delete the channel
    $.ajax({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/delete/channel/'+sessionStorage.current_admin_channel,
        async: true,
        //json object to sent to the authentication url
        success: function (){
            $('#'+sessionStorage.current_admin_channel).remove();
            setActiveChannel();
            $.ajax({
                type: "GET",
                //the url where you want to sent the userName and password to
                url: '/channels/members/'+ sessionStorage.current_admin_channel,
                dataType: 'json',
                contentType: 'application/json',
                async: true,
                //json object to sent to the authentication url
                success: function (data){
                    console.log("CHANGE: " + data);
                    createMembershipTable(data);
                }
        });
        }
    })

    // will need to automatically change active channel to another one
}

function removeUser(user){
      var data = {"permalink":user, 'channel':sessionStorage.current_admin_channel}
    $.ajax({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/remove/member',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        data: JSON.stringify(data),
        success: function (){
            // delete row with tr_permalink
            var row = $('#tr_'+user);
            row.remove();
            console.log(row.val())
        }
    });
}