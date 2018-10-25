$(document).ready(function(){

    window.semanticVid = {videos: {}}

    $("#btn-search").click(function(){
        $("#search-loader").dimmer("show")
        var searchInput = $("#search-bar").val()
        $.get("http://localhost:5000/search/"+searchInput, function(data, status){
           $("#main-container").empty();
           $("#main-container").append(data)
           $("#search-loader").dimmer("hide")
        });
    });

    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    
});