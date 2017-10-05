/**
 * Created by Chris on 19/09/2017.
 */
$(document).ready(function(){

    if(window.location.href == "https://thewriters.herokuapp.com/search/")
        $('table').hide();
    else
        $('table').show();


    $('tbody tr').mouseenter(function() {
        $(this).addClass('tableColour')
    });

    $('tbody tr').mouseleave(function() {
        $(this).removeClass('tableColour')
    })



})

