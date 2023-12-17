/*function incomeStatement() {
    let formData = new FormData(document.getElementById("incomeStatement"));
    
    // Send request to server
    fetch('/income_statement', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Open window
        let newWindow = window.open('', '_blank', "width: 300px; height: 50px; background-color: seablue;");
        // write data to the new window
        newWindow.document.write(`
        <html>
            <head>
                <title></title>
            </head>
            <body>
                <h3>Income Statement</h3>
                <p>Total Income: ${data.total_income}</p>
                <p>Total Expenses: ${data.total_expenses}</p>
                <p>Net Income: ${data.net_income}</p>
            </bod>
        </html>
    `);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("incomeStatement").innerHTML = "Error generating the report. Try again later";
    });
}

// Attach event listener
document.getElementById("income-statement").addEventListener("click", function () {
    incomeStatement();
})
*/


function incomeStatement() {
    let formData = new FormData(document.getElementById("incomeStatement"));

    fetch("/income_statement", {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const newWindow = window.open("", "_blank", "width=400, height=200");
            newWindow.document.write("<h2 style='text-align: center;'>Income Statement</h2>");
            newWindow.document.write(`<p style='text-align: center;'>Total Income: ${data.total_income}</p>`);
            newWindow.document.write(`<p style='text-align: center;'>Total Expenses: ${data.total_expenses}</p>`); 
            newWindow.document.write(`<p style='text-align: center;'>Net Income: ${data.net_income}</p>`);
        }
    })
    .catch(error => {
        console.error('Error', error);
        document.getElementById("incomeStatement").innerHTML = "Error generating the report.";
    });
}

// Attached event listener
document.getElementById("income-statement").addEventListener("click", function() {
    incomeStatement();
});
