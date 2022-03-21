const ip = "192.168.86.77";//"35.225.161.102"
let form;

window.onload = () => {
    form = document.forms['contact-form'];
};

const validateContactForm = () => {
    const name = form['fname'].value;
    const email = form['femail'].value;
    const message = form['fmessage'].value;

    if (!name) {
        alert("Please Provide a Name");
        return false;
    }

    if (!email) {
        alert("Please Provide an Email");
        return false;
    }

    if (!email.includes("@") || !email.includes(".")) {
        alert("Please Provide a Valid Email Address");
        return false;
    }

    if (!message) {
        alert("Please Provide a Message");
        return false;
    }

    fetch(`http://${ip}/contact`, data={
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                name,
                email,
                message
            }
        )
    })
    .then(response => response.json())
    .then(response => {
        if (response.status != "success") {
            alert(response.message);
        }
        else {
            alert('Message Sent');
        }
    });

    form['fname'].value = "";
    form['femail'].value = "";
    form['fmessage'].value = "";
    return false;
};