function submitForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Successful login, you can redirect or perform other actions here
            alert('Login successful');
        } else {
            alert('Invalid username or password');
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        alert('An error occurred while submitting the form');
    });
}


