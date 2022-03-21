const formatInfo = info => {
    let str = "";
    for (let i = 0; i < info.length; i++) {
        let tup = info[i];
        str += `"${tup[0]}:" ${tup[1]}` + (i == info.length - 1 ? "" : ", ");
    }
    return str;
};

window.onload = function() {
    const wordElement = document.getElementById("rating");
    const infoElement = document.getElementById("word-info");
    const root = document.querySelector(":root");

    const query = { active: true, currentWindow: true };

    function callback(tabs) {
        const currentTab = tabs[0].url;

        fetch(`http://192.168.86.77?link=${currentTab}`)
        .then(response => response.json())
        .then(response => {
            if (response['status'] == 'error') {
                root.style.setProperty("--rating-text-font-size", "30px");
                root.style.setProperty("--rating-text-color", "#000000")
                root.style.setProperty("--background-color", "#FFFFFF");

                wordElement.innerText = "Error: Transcript Not available";
                infoElement.innerText = "Error";
            }
            else
            {
                const tup = response['data'];
                const ratingLevel = tup[0];
                const ratingWord = tup[1];
                const info = tup[2]

                wordElement.innerText = ratingWord;
                infoElement.innerText = formatInfo(info);
                
                root.style.setProperty("--rating-text-font-size", "60px");
                root.style.setProperty("--rating-text-color", (ratingLevel == 5 ? "#FFFFFF" : "#000000"))
                root.style.setProperty("--background-color", getComputedStyle(root).getPropertyValue(`--${ratingWord.toLowerCase().replace(" ", "-")}`));
            }
        })  
    };

    chrome.tabs.query(query, callback);

};