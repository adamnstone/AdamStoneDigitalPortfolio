let email;
let reportLevel;
let blockVideo;
let blockAndReportNoTranscript;

const updateSettings = () => {
    loadSettings(settingsJSON => {
        if (settingsJSON.status != "success") {
            console.log(settingsJSON.message);
            return;
        }
        const settings = settingsJSON.settings;
        console.log("Loading Settings: ", settings);
        email = settings.toEmail;
        reportLevel = settings.reportLevel;
        blockVideo = settings.blockVideo;
        blockAndReportNoTranscript = settings.blockAndReportNoTranscript;
    });
};

updateSettings();

setInterval(updateSettings, 1000 * 60 * 2); // update settings every 5 minutes

const videoRe = /https:\/\/www.youtube(|kids).com\/watch/;
const ip = "192.168.86.77";//"35.225.161.102"

let prevBlocked = false;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    rate(request.currentTab);
});

chrome.tabs.onUpdated.addListener(
    (tabId, changeInfo, tab) => {
        if (changeInfo.url){
            if (prevBlocked) {
                reload();
            }
            else {
                if (isVideo(changeInfo.url)) {
                    rate(changeInfo.url);
                }
            }
        }
    }
);

function getEmail(callback) {
    chrome.identity.getProfileUserInfo(info => callback(info.email));
} 

function loadSettings(callback) {
    getEmail(googleAccountEmail => {
        fetch(`http://${ip}/get_settings`, data={
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                {
                    email: googleAccountEmail
                }
            )
        })
        .then(response => response.json())
        .then(response => callback(response));
    });
}

const getDateAndTime = () => {
    const date = new Date();
    let str = "";
    str += `${date.getHours().toString()}:${date.getMinutes().toString()} on ${date.getMonth().toString()}/${date.getDay().toString()}/${date.getFullYear().toString()}`;
    return str;
};

const isVideo = url => {
    return videoRe.test(url);
};

const formatInfo = info => {
    let str = "";
    for (let i = 0; i < info.length; i++) {
        let tup = info[i];
        str += `"${tup[0]}:" ${tup[1]}` + (i == info.length - 1 ? "" : ", ");
    }
    return str;
};

function rate(url) {
    if (!isVideo(url)) {
        console.log("Not video - skipping");
        return;
    }
    const currentTab = url;
    console.log("fetching", {
        link: currentTab,
        email,
        block_video: blockVideo,
        report_level: reportLevel,
        block_report_no_transcript: blockAndReportNoTranscript,
        date_time: getDateAndTime()
    });
    fetch(`http://${ip}/rate`, data={
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                link: currentTab,
                email,
                block_video: blockVideo,
                report_level: reportLevel,
                block_report_no_transcript: blockAndReportNoTranscript,
                date_time: getDateAndTime()
            }
        )
    })
    .then(response => response.json())
    .then(response => {
        if (response['status'] == 'error') {
            console.log(`Error: ${reponse['message']}`);
        }
        else
        {
            const has_transcript = response['transcript'];
            console.log(`Has Transcript: ${has_transcript}`);
            const level = response['level'];
            // if ((has_transcript && level >= reportLevel) || (!has_transcript && blockAndReportNoTranscript)) {block()};
            if (has_transcript) {
                console.log(`Level: ${level}`);
                console.log(`Report Threshold: ${reportLevel}`);
                if (level >= reportLevel) {
                    block(url);
                }
            }
            else {
                if (blockAndReportNoTranscript) {
                    block(url);
                }
            }
            console.log("Success");
        }
    });
}
    
function block(url) {
    prevBlocked = true;
    chrome.tabs.query({url: url}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "block"}, response => {});
      });
}

function reload(url) {
    chrome.tabs.query({active: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "reload"}, response => {});
    });
}
