/*unction incomeStatement(event) {
    let income_statment = document.getElementById("income-statement").value;
    event.preventDefault();

    let formData = newForm(this);

    fetch("income_statement", {
        method: 'POST',
        body: formData 
    })
    .then(response => response.text())
    .then(data => {
    
        document.getElementById("income-statement").innerHTML = data;
    })
    .catch(error => console.error('Error', error));
}*/