function postTransaction() {
  let document_number = document.getElementById("document_number").value;
  let total = document.getElementById("total").value;
  let description = document.getElementById("description").value;
  let account = document.getElementById("account").value;

  // validate inputs
  if (!document_number || !total || !description) {
    alert("Please fill in all fields with valid values ");
    return;
  }

  fetch("/post_transaction", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document_number: document_number,
      total: total,
      description: description,
      account: account,
    }),
  })
    .then((response) => {
      return response.text();
    })
    .then((responseText) => {
      console.log(responseText);
      return JSON.parse(responseText);
    })
    .then((data) => {
      if (data.success) {
        alert("Transaction posted successfully");
      } else {
        alert("Failed to post transaction. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error posting transaction", error.message);
      alert("An error occurred while posting transaction. Please try again.");
    });
}
