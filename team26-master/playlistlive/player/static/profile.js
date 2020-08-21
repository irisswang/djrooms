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
function profileToggle(requestedUser) {
    console.log("FOLLOW FUNCTION");

    $.ajax({
        url: "/player/profile/"+requestedUser+"/",
        type: "POST",
        data: "csrfmiddlewaretoken=" + getCSRFToken(),
        dataType: "text",
        success: function (response) {
            console.log("something")
            console.log(response)
            
            var itemTextElement = $("#id_follow_toggle");
            var currVal = itemTextElement.val();
            if(currVal.localeCompare("Follow")==0){
                itemTextElement.val("Unfollow")
            }
            else {
                itemTextElement.val("Follow")
            }
        }
    });










}