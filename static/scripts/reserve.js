// Function to save customer info to local storage
function saveCustomerInfoToLocalStorage(customerInfo) {
  localStorage.setItem('customerInfo', JSON.stringify(customerInfo));
}

// Add details
document.getElementById("apply").addEventListener("click", function () {
  // Retrieve values from input fields and assign them to variables
  const customer_name = document.getElementById("customer_name").value;
  const telephone_number = document.getElementById("telephone_number").value;
  const customerLocation = document.getElementById("location").value;
  const description = document.getElementById("description").value;

  // Create an object with the collected information
  const customerInfo = {
    "customer_name": customer_name,
    "telephone_number": telephone_number,
    "location": customerLocation,
    "description": description
  };

  // Save customer info to local storage AFTER retrieving values
  saveCustomerInfoToLocalStorage(customerInfo);

  // The rest of your code remains unchanged
  fetch('/book_reserve', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(customerInfo),
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.success) {
      console.log("Customer information saved successfully in db");
    } else {
      console.error("Failed to save customer information in the database");
    }
  })
  .catch((error) => {
    console.error("Error saving customer information:", error);
  });
});

// Add event listener for "addLine" element
document.getElementById("addLine").addEventListener("click", function (event) {
  event.preventDefault();
  // Redirect to the order.html page
  window.location.href = "/invoice";
});
