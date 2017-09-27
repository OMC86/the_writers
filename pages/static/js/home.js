/**
 * Created by Chris on 19/09/2017.
 */
$(document).ready(function() {

    $('#showList').hide();

    $('#hideList').click(function(){
        $('.homeList').slideUp('slow');
        $('#hideList').hide(500);
        $('#showList').show(500);
    });

    $('#showList').click(function() {
        $('.homeList').slideDown('slow');
        $('#hideList').show(500);
        $('#showList').hide(500);
    });

});