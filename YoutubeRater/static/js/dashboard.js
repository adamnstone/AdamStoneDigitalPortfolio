const ip = "192.168.86.77";//"35.225.161.102"
let form;
let currentChildrenList;

window.onload = () => {
    form = document.forms['newChild'];
    currentChildrenList = document.getElementById("current-children-list");
    addCurrentChildren();
};

const validateNewChildForm = () => {
    if (!form['fname'].value) {
        alert("No Name Provided");
        return false;
    }
    
    const name = form['fname'].value;

    const OKChars = " -qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM,.";

    for (let i in name) {
        if (!OKChars.includes(name[i])) {
            alert("Invalid Character In Child Name");
            return false;
        }
    }
    
    fetch(`http://${ip}/add_child`, data={
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                name,
                settings: {},
                emails: []
            }
        )
    })
    .then(response => response.json())
    .then(response => {
        if (response.status != "success") {
            alert(response.message);
        }
        else {
            window.location.replace(window.origin + `/child_settings/${name}`);
        }
    });

    return false;
};

const wrapInListElement = element => {
    const li = document.createElement("li");
    li.appendChild(element);
    return li;
};

const addCurrentChildren = () => {
    for (let childName in allChildrenSettings) {
        const childSettings = allChildrenSettings[childName][0];
        const childGoogleAccounts = allChildrenSettings[childName][1];

        const liWrapper = document.createElement("li");
        const details = document.createElement("details");
        const summary = document.createElement("summary")
        summary.textContent = childName;
        const settingsList = document.createElement("ul");
        const reportLevelLabel = document.createElement("label");
        reportLevelLabel.textContent = `Report Level: ${childSettings['reportLevel']}`;
        const blockVideoLabel = document.createElement("label");
        blockVideoLabel.textContent = `Block Video: ${childSettings['blockVideo']}`;
        const blockAndReportNoTranscriptLabel = document.createElement("label");
        blockAndReportNoTranscriptLabel.textContent = `Block/Report When Transcript is Not Available: ${childSettings['blockAndReportNoTranscript']}`;
        const childGoogleAccountsListLabel = document.createElement("label");
        childGoogleAccountsListLabel.textContent = "Google Accounts:";
        const childGoogleAccountsList = document.createElement("ul");
        for (let i = 0; i < childGoogleAccounts.length; i++) {
            const googleAccount = childGoogleAccounts[i];
            const googleAccountLabel = document.createElement("label");
            googleAccountLabel.textContent = googleAccount;
            childGoogleAccountsList.appendChild(wrapInListElement(googleAccountLabel));
        }
        const editChildButton = document.createElement("button");
        editChildButton.textContent = "Edit Child";
        editChildButton.addEventListener('click', e => {
            window.location.replace(window.origin + `/child_settings/${childName}`);
        });

        liWrapper.appendChild(details);
        details.append(summary, settingsList);
        settingsList.append(wrapInListElement(reportLevelLabel), wrapInListElement(blockVideoLabel), wrapInListElement(blockAndReportNoTranscriptLabel), wrapInListElement(childGoogleAccountsListLabel), childGoogleAccountsList, editChildButton);

        currentChildrenList.appendChild(liWrapper);
    }
};