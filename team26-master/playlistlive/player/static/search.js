function updateSearchResults(searchResults) {
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


function displayError(message) {
    $("#error").html(message);
}

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

// Calls the add_post function in the views file 
function searchFunction() {
    console.log("SEARCH FUNCTION");
    var itemTextElement = $("#id_search_input");
    
    var itemTextValue = itemTextElement.val();

    // Clear input box and old error message (if any)
    displayError('');

    $.ajax({
        url: "/player/search",
        type: "GET",
        data: "search-box=" + itemTextValue + "&csrfmiddlewaretoken=" + getCSRFToken(),
        dataType: "json",
        success: function (response) {
            console.log(response)
            updateSearchResults(response);
        }
    });
}