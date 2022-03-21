let input;

function runSearch() {
    window.location = window.origin + `/dashboard?query=${(input.value ? input.value : input.placeholder)}`; // tenrary expression to prevent searching twice from deleting the query
    return false; // to prevent normal form behavior
}

window.onload = function() {
    input = document.getElementById("query");
    input.addEventListener("keydown", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            runSearch();
        }
    });
};

