window.onload = function() {
    setTimeout(function(){
    chrome.runtime.sendMessage({currentTab: location.href})}, 1000);
};

chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
    console.log("Recieved:");
    console.log(request);
    if (request.action == 'block') {
        console.log("Blocking");
        const blockDiv = document.getElementsByClassName("html5-video-container")[0];
        blockDiv.innerHTML = `
        <div style="width: 879px; height: 494px; left: 0px; top: 0px;">
            <span style="position: absolute; top: 50%; left: 0; right: 0; text-align: center; font-size: 100px; color: white; transform: translateY(-100%);">
                Blocked
            </span>
        </div>`;
        const playerDiv = document.getElementById("movie_player");
        const playerDivParent = playerDiv.parentElement;
        const playerDivInnerHTML = playerDiv.innerHTML;
        playerDiv.remove();
        playerDivParent.innerHTML = playerDivInnerHTML + playerDivParent.innerHTML;
    }
    else if (request.action == "reload") {
        location.reload();
    }
    sendResponse("Success");
 });
