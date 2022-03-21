const ip = "192.168.86.77";//"35.225.161.102"
let form;

window.onload = () => {
    form = document.forms['addChildGoogleAccountForm'];
};

const validateAddChildGoogleAccountForm = () => {
    const email = form['faccount'].value;
    
    if (!email) {
        alert("No Account Provided");
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