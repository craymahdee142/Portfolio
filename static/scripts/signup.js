function signUp(event) {
  event.preventDefault();

  let fullname = document.getElementById("fullname").value;
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let verify_password = document.getElementById("verify_password").value;

  // validate the inputs
  if (!fullname || !username || !password || !verify_password) {
    alert("All fileds are required");
    return;
  }

  fetch('signup', {
    method: 'POST',
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({
        //fullname: fullname,
        username: username,
        password: password,
        verify_password: verify_password,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.success) {
        alert('Sign up successfully');
    } else {
        alert('Falied to sign up. Please try again');
    }
  })
  .catch((error) => {
    console.error('Error signing up', error.message);
    alert('Error occured while signing up. Please try again')
  });
  return false;
}
