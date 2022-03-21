const ip = "192.168.86.77";//"35.225.161.102"
let childSettingsForm;
let googleAccountForm;

let reportLevelElement;
let blockVideoElement;
let blockAndReportNoTranscriptElement;
let currentGoogleAccountsList;
let deleteChildButton;

window.onload = () => {
    googleAccountForm = document.forms['addChildGoogleAccountForm'];

    deleteChildButton = document.getElementById("delete-child-button");
    deleteChildButton.addEventListener('click', e => {
        fetch(`http://${ip}/delete_child`, data={
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                {
                    childName
                }
            )
        })
        .then(response => response.json())
        .then(response => {
            if (response.status != "success") {
                alert(response.message);
            }
            else {
                alert('Child Deleted');
                window.location.replace(window.origin + "/dashboard");
            }
        });
    });

    currentGoogleAccountsList = document.getElementById("current-google-accounts-list");
    for (let i in childGoogleAccounts) {
        const account = childGoogleAccounts[i]
        const wrapper = document.createElement("li");
        const label = document.createElement("label");
        label.textContent = account;
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Remove Account";
        deleteButton.addEventListener('click', e => {
            fetch(`http://${ip}/delete_google_account`, data={
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(
                    {
                        childName,
                        account
                    }
                )
            })
            .then(response => response.json())
            .then(response => {
                if (response.status != "success") {
                    alert(response.message);
                }
                else {
                    alert('Google Account Deleted');
                    window.location.reload();
                }
            });
        });
        wrapper.append(label, deleteButton);
        currentGoogleAccountsList.appendChild(wrapper);
    }

    childSettingsForm = document.forms['childSettings'];

    reportLevelElement = childSettingsForm['freportLevel'];
    blockVideoElement = childSettingsForm['fblockVideo'];
    blockAndReportNoTranscriptElement = childSettingsForm['fwhenTranscript'];

    reportLevelElement.value = childSettings['reportLevel'];
    blockVideoElement.checked = childSettings['blockVideo'];
    blockAndReportNoTranscriptElement.checked = childSettings['blockAndReportNoTranscript'];
};

const validateAddChildGoogleAccountForm = () => {
    const email = googleAccountForm['faccount'].value;
    
    if (!email) {
        alert("No Account Provided");
        return false;
    }

    if (childGoogleAccounts.includes("email")) {
        alert("Google Account Already Added");
        return false;
    }
    
    fetch(`http://${ip}/add_child_account_email`, data={
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                email,
                childName
            }
        )
    })
    .then(response => response.json())
    .then(response => {
        if (response.status != "success") {
            alert(response.message);
        }
        else {
            alert(`A Verification Email Has Been Sent to ${email} with Instructions`);
        }
    });

    return false;
};

const validateChildSettingsForm = () => {
    const reportLevel = reportLevelElement.value;
    const blockVideo = blockVideoElement.checked;
    const blockAndReportNoTranscript = blockAndReportNoTranscriptElement.checked;

    fetch(`http://${ip}/modify_child_settings`, data={
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                childName,
                new_settings: {
                    toEmail: parentEmail,
                    reportLevel,
                    blockVideo,
                    blockAndReportNoTranscript
                }
            }
        )
    })
    .then(response => response.json())
    .then(response => {
        if (response.status != "success") {
            alert(response.message);
        }
        else {
            alert("Settings Updated");
            window.location.replace(window.origin + "/dashboard");
        }
    });

    return false;
};