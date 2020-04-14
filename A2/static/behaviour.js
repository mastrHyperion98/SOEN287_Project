
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