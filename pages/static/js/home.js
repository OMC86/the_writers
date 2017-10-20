/**
 * Created by Chris on 19/09/2017.
 */
$(document).ready(function() {

    $('#showList').hide();

    $('#hideList').click(function(){
        $('.homeList').slideUp('slow');
        $('#hideList').hide();
        $('#showList').show();
    });

    $('#showList').click(function() {
        $('.homeList').slideDown('slow');
        $('#hideList').show();
        $('#showList').hide();
    });

});