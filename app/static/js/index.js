$(document).ready(function() {
    $('#bg').foggy({
        blurRadius: 5,
        opacity: 0.8
    });
    var $button = $('#search-input');
    $button.focusin(function() {
        console.log("in")
        $('#search-form').css('opacity', 0.9);
    });
    $button.focusout(function() {
        console.log("out")
        $('#search-form').css('opacity', '');
    });
});