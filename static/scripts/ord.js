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
let amount;
let prod_name;
let ids;

function calculate() {
  ids = getValue("ids");
  price = getValue("prc");
  qty = getValue("qty");

  if (ids && price && qty) {
    const isValidProduct = productList.some((product) => product.code === ids);

    if (!isValidProduct) {
      alert("Invalid Product Code");
      return;
    }

    amount = price * qty;
    setValue("amt", amount);
  }
}

function populateProductName() {
  const productId = getValue("ids");
  const productNameField = document.getElementById("product");

  const selectedProduct = productList.find((product) => product.code === productId);

  if (selectedProduct) {
    setValue("product", selectedProduct.name);
    prod_name = selectedProduct.name;
  } else {
    setValue("product", "");
    prod_name = "";
  }
}

function addData() {
  if (ids && price && qty) {
    const isValidProduct = productList.some((product) => product.code === ids);

    if (!isValidProduct) {
      alert("Invalid Product Code");
      return;
    }

    amount = price * qty;

    const newRow = `<tr id="row-${ids}"><td>${ids}</td><td>${prod_name}</td><td>${price}</td><td>${qty}</td><td>${amount}</td><td><button onclick="deleteRow('${ids}')">&#10006</button></td></tr>`;
    document.getElementById("newtr").innerHTML += newRow;

    clearInputFields();
    updateTotal(amount);
  }
}

function deleteRow(rowId) {
  const deletedAmount = parseFloat(document.getElementById(`row-${rowId}`).querySelector("td:nth-child(5)").textContent);
  document.getElementById(`row-${rowId}`).remove();
  recalculateTotal(deletedAmount);
}

function recalculateTotal(deletedAmount) {
  let total = parseFloat(document.getElementById("total").innerText) || 0;
  total -= deletedAmount;
  updateTotal(total);
}

function updateTotal(value) {
  document.getElementById("total").innerText = value.toFixed(2);
}

document.getElementById("addBtn").addEventListener("click", function () {
  calculate();
  populateProductName();
  addData();
});

document.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    calculate();
    populateProductName();
    addData();
  }
});

document.getElementById("generate-invoice").addEventListener("click", function () {
  generateInvoice();
});

function getValue(id) {
  return document.getElementById(id).value;
}

function setValue(id, value) {
  document.getElementById(id).value = value;
}

function clearInputFields() {
  setValue("ids", "");
  setValue("prc", "");
  setValue("amt", "");
  setValue("qty", "");
}



function generateInvoice() {
  // Get cart data from the table rows
  const tableRows = document.querySelectorAll("#newtr tr");
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

  // Send cart data to the server to generate an invoice
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
        alert(`Invoice generated successfully! Total amount: ${data.total.toFixed(2)}`);
        
        // Optionally, you can clear the cart or perform other actions on the client side
        clearCart();
      } else {
        alert("Failed to generate invoice. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error generating invoice:", error);
      alert("An error occurred while generating the invoice. Please try again.");
    });
}





/*
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
let amount;
let prod_name;
let ids;

function calculate() {
  ids = getValue("ids");
  price = getValue("prc");
  qty = getValue("qty");

  if (ids && price && qty) {
    const isValidProduct = productList.some((product) => product.code === ids);

    if (!isValidProduct) {
      displayError("Invalid Product Code");
      return;
    }

    amount = price * qty;
    setValue("amt", amount);
  }
}

function populateProductName() {
  const productId = getValue("ids");
  const productNameField = document.getElementById("product");

  const selectedProduct = productList.find((product) => product.code === productId);

  if (selectedProduct) {
    setValue("product", selectedProduct.name);
    prod_name = selectedProduct.name;
  } else {
    setValue("product", "");
    prod_name = "";
  }
}

function addData() {
  if (ids && price && qty) {
    const isValidProduct = productList.some((product) => product.code === ids);

    if (!isValidProduct) {
      displayError("Invalid Product Code");
      return;
    }

    amount = price * qty;

    const newRow = `<tr id="row-${ids}"><td>${ids}</td><td>${prod_name}</td><td>${price}</td><td>${qty}</td><td>${amount}</td><td><button onclick="deleteRow('${ids}')">&#10006</button></td></tr>`;

    try {
      document.getElementById("newtr").innerHTML += newRow;
    } catch (error) {
      console.error("Error adding row to table:", error);
    }

    clearInputFields();
    updateTotal(amount);
  }
}

function deleteRow(rowId) {
  const deletedAmount = parseFloat(document.getElementById(`row-${rowId}`).querySelector("td:nth-child(5)").textContent);
  document.getElementById(`row-${rowId}`).remove();
  recalculateTotal(deletedAmount);
}

function recalculateTotal(deletedAmount) {
  let total = 0;
  const tableRows = document.querySelectorAll("#newtr");
  tableRows.forEach((row) => {
    const amount = parseFloat(row.querySelectorAll("td:nth-child(5").textContent) || 0;
    total += amount;
  });
  updateTotal(total);
}

function updateTotal(value) {
  document.getElementById("total").innerText = value.toFixed(2);
}

document.getElementById("addBtn").addEventListener("click", function () {
  calculate();
  populateProductName();
  addData();
});

document.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    calculate();
    populateProductName();
    addData();
  }
});

document.getElementById("generate-invoice").addEventListener("click", function () {
  generateInvoice();
});

function getValue(id) {
  return document.getElementById(id).value;
}

function setValue(id, value) {
  document.getElementById(id).value = value;
}

function clearInputFields() {
  setValue("ids", "");
  setValue("prc", "");
  setValue("amt", "");
  setValue("qty", "");
}




function generateInvoice() {
  // Get cart data from the table rows
  const tableRows = document.querySelectorAll("#newtr");
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

  // Send cart data to the server to generate an invoice
  fetch("/generate_invoice", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cartData),
  })
    .then((response) => {
      console.log("Response:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Data received:", data);
      if (data.success) {
        alert(`Invoice generated successfully! Total amount: ${data.total.toFixed(2)}`);
        
        const invoiceList = data.invoices;

        // Display the list in a table
        displayInvoicesTable(invoiceList);
        // Clear cart list after action
      } else {
        alert("Failed to generate invoice. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error generating invoice:", error);
      alert("An error occurred while generating the invoice. Please try again.");
    });
}*/