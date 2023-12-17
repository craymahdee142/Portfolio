function balanceSheet() {
    let formData = new FormData(document.getElementById("balanceSheet"));

    fetch("/balance_sheet", {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const newWindow = window.open("", "_blank", "width=400, height=200");
            newWindow.document.write("<h2 style='text-align: center;'>Balance Sheet</h2>");
            newWindow.document.write(`<p style='text-align: center;'>Net Income: ${data.net_income}</p>`);
            newWindow.document.write(`<p style='text-align: center;'>Total Receivables: ${data.total_receivables}</p>`);
            newWindow.document.write(`<p style='text-align: center;'>Total Payables: ${data.total_payables}</p>`);
            newWindow.document.write(`<p style='text-align: center;'>Balance Sheet: ${data.balance_sheet}</p>`);
        }
    })
    .catch(error => {
        console.error('Error', error);
        document.getElementById("balanceSheet").innerHTML = "Error generating the report.";
    });
}

// Attached event listener
document.getElementById("income-statement").addEventListener("click", function() {
    balanceSheet();
});
