$(document).ready(function() {
    $('.data_del').on('click', function() {
        return confirm('Are you sure?');
    });
    $('#icon').click(function() {
        $('#side-menu').slideToggle(1000);
    });
});