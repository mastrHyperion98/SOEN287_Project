
function chatContent() {
    $(document).ready(function() {
            $('button').click(function() {
                $('button.list-group-item.active').removeClass("active");
                $(this).addClass("active");
            });
    });
}