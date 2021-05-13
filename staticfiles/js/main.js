$(document).ready(function() {
    $('.btn-danger').on('click', function() {
        return confirm('Are you sure?');
    });
    $('#icon').click(function() {
        $('#side-menu').slideToggle(1000);
        $('#side-menu').css({
            'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'
        })
    });
    $('#catg-add').click(function() {
        $('#cansel').style.display = "block";
    });
    $('#show-icon').click(function() {

        $('#show-catg').animate({
            width: 'toggle',
        }, 1000);
    });
    $('.close').click(function() {
        $('.alert-success').css({
            'display': 'none'
        });
    });

    $('.del_button').on('click', function() {
        return confirm('Are you sure?');
    });


});