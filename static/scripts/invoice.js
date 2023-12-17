// Sample product list
const productList = [
  { code: "00", name: "Jollof rice" },
  { code: "01", name: "Plain rice" },
  { code: "02", name: "Fried rice" },
  { code: "03", name: "Fufu" },
  { code: "04", name: "Kokonte" },
  { code: "05", name: "Banku" },
  { code: "06", name: "Rice ball" },
  { code: "07", name: "Tilapia" },
  { code: "08", name: "Dried Salmond" },
  { code: "09", name: "Fresh salmond" },
  { code: "10", name: "Poku fish" },
  { code: "11", name: "Red fish" },
  { code: "12", name: "Elban dried" },
  { code: "13", name: "Tuna" },
  { code: "14", name: "Goat meat" },
  { code: "15", name: "Cow meat" },
  { code: "16", name: "Chicken" },
  { code: "17", name: "Egg" },
  { code: "18", name: "Sobolo" },
  { code: "19", name: "Can malt" },
  { code: "20", name: "Can fanta" },
];

let price;
let qty;
let amt;
let prod_name;
let ids;

function getValue(elementId) {
  return document.getElementById(elementId).value.trim();
}

function setValue(elementId, value) {
  document.getElementById(elementId).value = value;
}

function calculate() {
  ids = getValue("ids");
  price = parseFloat(getValue("prc")) || 0;
  qty = parseFloat(getValue("qty")) || 0;

  if (ids && price && qty) {
    const isValidProduct = productList.some((product) => product.code === ids);

    if (!isValidProduct) {
      alert("Invalid Product Code");
      return;
    }

    amt = price * qty;
    setValue("amt", amt);
  }
}

function populateProductName() {
  ids = getValue("ids");

  const selectedProduct = productList.find((product) => product.code === ids);

  if (selectedProduct) {
    setValue("product", selectedProduct.name);
    prod_name = selectedProduct.name;
  } else {
    setValue("product", "");
    prod_name = "";
  }
}

// Function to delete a row
function deleteRow(rowId) {
  // fund row by id
  const deleteAmount = parseFloat(
    document.getElementById(`row-${rowId}`).querySelector("td:nth-child(5)")
      .textContent
  );
  document.getElementById(`row-${rowId}`).remove();
  recalculateTotal(deleteAmount);
}

function recalculateTotal(deletedAmount) {
  // update total amount after deletion
  let total = parseFloat(document.getElementById("total").innerHTML) || 0;
  total -= deletedAmount;
  document.getElementById("total").innerHTML = total;
}

function addData() {
  // Check if all required fields are filled
  if (ids && price && qty !== null && qty !== null && amt !== null) {
    // Check if the entered product code exists in the product list
    const isValidProduct = productList.some((product) => product.code === ids);

    if (!isValidProduct) {
      // Handle the case of an invalid product code (display an alert, for example)
      alert("Invalid Product Code");
      return;
    }

    // Calculate amount for the current item
    amt = price * qty;

    const rowId = ids;

    // Append a new row to the table with a delete button
    const newRow = `<tr id="row-${ids}"><td>${ids}</td><td>${prod_name}</td><td>${price}</td><td>${qty}</td><td>${amt}</td><td><button onclick="deleteRow('${ids}')">&#10006</button></td></tr>`;
    document.getElementById("newtr").innerHTML += newRow;

    // Clear input fields
    document.getElementById("ids").value = "";
    document.getElementById("prc").value = "";
    document.getElementById("amt").value = "";
    document.getElementById("qty").value = "";

    // Update total
    let total = parseFloat(document.getElementById("total").innerHTML) || 0;
    total += amt;
    document.getElementById("total").innerHTML = total;
  } else {
    alert("Please fill in all required fields ");
  }
}

// Attach event listener to the "add" button
document.getElementById("addBtn").addEventListener("click", function () {
  calculate();
  populateProductName();
  addData();
});

// attach event listener for document for the keydown
document.addEventListener("keydown", function (event) {
  //check if enter key is pressed
  if (event.key === "Enter") {
    calculate();
    populateProductName();
    addData();
  }
});

document
  .getElementById("generate-invoice")
  .addEventListener("click", function () {
    generateInvoice();
  });

function getValue(id) {
  return document.getElementById(id).value;
}

function clearInputFields() {
  setValue("ids", "");
  setValue("prc", "");
  setValue("amt", "");
  setValue("qty", "");
}

function displayInvoiceInNewWindow(invoiceData) {
  const newWindow = window.open("", "_blank");

  if (newWindow) {
    newWindow.document.write("<h2>Invoice</h2>");
    // Add other organistion information
    // Display customer info
    // Display customer info if present in the first item of the invoiceData array
    if (invoiceData.length > 0 && invoiceData[0].customer_info) {
      const customerInfo = invoiceData[0].customer_info;

      newWindow.document.write("<table border='1'>");
      newWindow.document.write(
        "<thead><tr><th colspan='2'>Customer Information</th></tr></thead>"
      );
      newWindow.document.write(
        "<tr><td>Customer Name:</td><td>" +
          customerInfo.customer_name +
          "</td></tr>"
      );
      newWindow.document.write(
        "<tr><td>Telephone Number:</td><td>" +
          customerInfo.telephone_number +
          "</td></tr>"
      );
      newWindow.document.write(
        "<tr><td>Location:</td><td>" + customerInfo.location + "</td></tr>"
      );
      newWindow.document.write(
        "<tr><td>Description:</td><td>" +
          customerInfo.description +
          "</td></tr>"
      );
      newWindow.document.write("</table>");
    }

    newWindow.document.write("<table border='1'>");
    newWindow.document.write(
      "<thead><tr><th>Prod Code</th><th>Prod Name</th><th>Price</th><th>Qty</th><th>Amt</th></tr></thead>"
    );
    newWindow.document.write("<tbody>");

    invoiceData.forEach(function (item) {
      newWindow.document.write("<tr>");
      newWindow.document.write("<td>" + item.prod_code + "</td>");
      newWindow.document.write("<td>" + item.prod_name + "</td>");
      newWindow.document.write("<td>" + item.price + "</td>");
      newWindow.document.write("<td>" + item.qty + "</td>");
      newWindow.document.write("<td>" + item.amt + "</td>");
      newWindow.document.write("</tr>");
    });

    newWindow.document.write("</tbody></table>");

    // Display the total
    newWindow.document.write(
      "<p><strong>Total:</strong> " +
        document.getElementById("total").innerHTML +
        "</p>"
    );
  } else {
    alert("Failed to open a new window. Please allow pop-ups for this site.");
  }
}

function getCustomerInfo() {
  const storedCustomerInfo = localStorage.getItem('customerInfo');
  if(storedCustomerInfo) {
    // Clear customer info from local storage after retrieving
    localStorage.removeItem('customerInfo');
    return JSON.parse(storedCustomerInfo);
  } else {
    return null;
  }
  
}

function getCartData() {
  const tableRows = document.querySelectorAll("#newtr tr");

  if (tableRows.length === 1) {
    alert("Cart is empty. Add items to generate invoice");
    return [];
  }

  const cartData = [];

  tableRows.forEach((row) => {
    const cells = row.querySelectorAll("td");
    const rowData = {
      prod_code: cells[0].textContent,
      prod_name: cells[1].textContent,
      price: parseFloat(cells[2].textContent),
      qty: parseInt(cells[3].textContent),
      amt: parseFloat(cells[4].textContent),
    };
    cartData.push(rowData);
  });

  return cartData;
}

function addCustomerInfoToCart(cartData, customerInfo) {
  return cartData.map((item) => {
    return { ...item, customer_info: customerInfo };
  });
}

function generateInvoice() {
  const customerInfo = getCustomerInfo();
  const cartData = getCartData();

  if (cartData.length === 0) {
    return; // Cart is empty, no need to proceed
  }

  const cartDataWithCustomerInfo = addCustomerInfoToCart(cartData, customerInfo);

  // Send only cartData to the server
  fetch("/generate_invoice", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cartData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        displayInvoiceInNewWindow(cartDataWithCustomerInfo);
        alert("Invoice generated successfully!");
      } else {
        alert("Failed to generate invoice. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error generating invoice:", error);
      alert("An error occurred while generating the invoice. Please try again.");
    });
}

// Helper function to calculate total
function getTotal(cartData) {
  return cartData.reduce((total, item) => total + item.amt, 0);
}
