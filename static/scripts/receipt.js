document.getElementById("generate-invoice").addEventListener("click", function() {
    // Extract invoice data from the HTML
    var invoices = JSON.parse(document.getElementById("invoiceData").textContent);
    var total = parseFloat(document.getElementById("totalAmount").textContent);

    // Open a new window and populate it with invoice data
    var newWindow = window.open("", "_blank", "width=600,height=400");
    newWindow.document.write("<h1>Invoices</h1>");
    newWindow.document.write("<table border='1'>");
    newWindow.document.write("<thead><tr><th>Product Code</th><th>Product Name</th><th>Price</th><th>Quantity</th><th>Amount</th></tr></thead>");
    newWindow.document.write("<tbody>");

    invoices.forEach(function(invoice) {
        newWindow.document.write("<tr>");
        newWindow.document.write("<td>" + invoice.prod_code + "</td>");
        newWindow.document.write("<td>" + invoice.prod_name + "</td>");
        newWindow.document.write("<td>" + invoice.price + "</td>");
        newWindow.document.write("<td>" + invoice.qty + "</td>");
        newWindow.document.write("<td>" + invoice.amt + "</td>");
        newWindow.document.write("</tr>");
    });

    newWindow.document.write("</tbody></table>");
    newWindow.document.write("<p>Total Amount: " + total + "</p>");
});