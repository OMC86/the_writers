/**
 * Created by Chris on 19/09/2017.
 */
$(document).ready(function(){

    if(window.location.href == "http://127.0.0.1:8000/search/")
        $('table').hide();
    else
        $('table').show();

});