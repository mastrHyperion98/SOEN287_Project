$(function() {
    console.log( "ready2!" );
    // fetch all members from currently active
     $.ajax({
        type: "GET",
        //the url where you want to sent the userName and password to
        url: '/channels/active',
        dataType: 'json',
        contentType: 'application/json',
        async: true,
        //json object to sent to the authentication url
        success: function (data){
            $('button.list-group-item.active').removeClass("active");
            $('#'+data['permalink']).addClass("active");

            if(data !== null){
                $.ajax({
                    type: "GET",
                    //the url where you want to sent the userName and password to
                    url: '/channels/members',
                    dataType: 'json',
                    contentType: 'application/json',
                    async: true,
                    //json object to sent to the authentication url
                    success: function (data){
                        console.log(data);
                        var $table = $('<table>');
                        // set attribute
                        $table.attr("class", "table table-striped table-dark")
                        // thead
                        .append('<thead>').children('thead')
                        .append('<tr />').children('tr').append('<th scope="col">Username</th><th scope="col">Account Permalink</th>' +
                            '<th scope="col">Last Login</th><th scope="col">isAdmin</th><th scope="col">Options</th>');
                        //tbody
                        var $tbody = $table.append('<tbody />').children('tbody');
                        // add row
                        $.each(data, function(obj, item) {
                            var permalink = item['permalink'];
                            console.log(permalink)
                            var options = !item['is_admin'] ? "</td>" :'<button class="btn btn-secondary"' +
                                ' onclick="removeUser('+"'"+permalink+"'"+')">Remove User</button></td>';
                            console.log(options)
                            $tbody.append('<tr />').children('tr:last')
                            .append("<td>" + item['username'] + "</td>")
                            .append("<td>" + permalink + "</td>")
                            .append("<td>" + item['login'] + "</td>")
                            .append("<td>" + item['is_admin'] + "</td>")
                            .append("<td>" + options);
                        });
                        // add table to dom
                        $table.appendTo('#member_table_holder');
                    }
                })
            }
        }
    })


});


function removeUser(user){
    console.log(user)
}
/*
  <table class="table table-striped table-dark" id="member_table" >
                            <thead>
                            <tr>
                                <th scope="col">Username</th>
                                <th scope="col">Account Permalink</th>
                                <th scope="col">Last Login</th>
                                <th scope="col">Is Admin</th>
                                <th scope="col">Options</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for user in users %}
                                {% if user['is_admin'] %}
                                    <tr>
                                        <td>{{ user['username'] }}</td>
                                        <td>{{ user['permalink'] }}</td>
                                        <td>{{ user['login'] }}</td>
                                        <td>{{ user['is_admin'] }}</td>
                                        <td> </td>
                                    </tr>
                                {% else %}
                                    <tr>
                                        <td>{{ user['username'] }}</td>
                                        <td>{{ user['permalink'] }}</td>
                                        <td>{{ user['login'] }}</td>
                                        <td>{{ user['is_admin'] }}</td>
                                        <td><a href="/remove_user/{{ user['permalink'] }}">Remove</a></td>
                                    </tr>
                                {% endif %}
                            {% endfor %}

                                <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td><a href="/add_user">Add User</a></td>
                            </tr>

                            </tbody>
                        </table>



             var $table = $('<table>');
            // caption
            $table.attr("class", "table table-striped table-dark")
            // thead
            .append('<thead>').children('thead')
            .append('<tr />').children('tr').append('<th scope="col">Username</th><th>Account Permalink</th><th>Last Login</th><th>isAdmin</th><th>Options</th>');

            //tbody
            var $tbody = $table.append('<tbody />').children('tbody');

            // add row
            $tbody.append('<tr />').children('tr:last')
            .append("<td></td>")
            .append("<td>val</td>")
            .append("<td>val</td>")
            .append("<td>val</td>");

            // add table to dom
            $table.appendTo('#member_table_holder');
 */