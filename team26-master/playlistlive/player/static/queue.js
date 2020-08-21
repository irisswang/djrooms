function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}
function updateQueueResults(searchResults) {
    $("#search_results").empty()
    console.log(searchResults);
    if (searchResults === null) {
        $("#search_results").empty()
    } else {
        $(searchResults.tracks.items).each(function () {
            console.log(searchResults.tracks.items);
            my_id = "id_search_results_" + this.id
            my_class = "class_search_results"
            btn_id = "btn_search_track_" + this.id
            if (document.getElementById(my_id) == null) {
                $("#search_results").append(
                    '<li id=' + my_id + ' class=' + my_class +'>' + 
                    '<a class="search_title" href=' + '"javascript:queueFunction(\'' + this.uri + '\')"' + '>' + this.name +'</a>' +
                    '</li>' 
                )
            }
        })
    }
}

function clearSearch() {
    $("#search_results").empty();
    document.getElementById("id_search_input").value = "";
    console.log("Queue Function is called");
}

function queueFunction(songURI) {
    console.log("Queue Function is called");

    $.ajax({
        url: "/player/queue/",
        type: "POST",
        data: "songURI=" + songURI + "&csrfmiddlewaretoken=" + getCSRFToken(),
        dataType: "json",
        success: function (response) {
            console.log("added song" +songURI+ " to the queue")
            clearSearch();
        }
    });
}