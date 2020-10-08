$(document).ready(function() {
    $('.btn-danger').on('click', function() {
        return confirm('Are you sure?');
    });
    $('#icon').click(function() {
        $('#side-menu').slideToggle(1000);
    });
    $('#catg-add').click(function() {
        $('#cansel').style.display = "block";
    });
    $('#show-icon').click(function() {

        $('#show-catg').animate({
            width: 'toggle'
        }, 1000);
    });

});