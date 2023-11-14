$(document).ready(() => {
    // Add your code here
    url = window.location.origin;

    request = $.ajax({
        url: `${url}/api/books`,
        type: "GET",
        dataType: "json",
    });

    request.done((data) => {
        if (data.length === 0) {
            $("#books").append(
                `<div class="book">
                    <h2>No books available</h2>
                </div>`
            );
        }  

        for (let i = 0; i < data.length; i++) {
            $("#books").append(
                `<div class="book">
                    <img src="/static/default_book.jpg" alt="Book 1">
                    <h2>${data[i].title}</h2>
                    <p><b>Author:</b> ${data[i].author}</p>
                    <p><b>Description:</b> ${data[i].description}</p>
                    <p><b>Price:</b> ₦${data[i].price}</p>
                </div>`
            );
        }
    });


    $('#download').submit((event) => {
        event.preventDefault();
        const code = $('#download-code').val();
        window.location.href = `${url}/api/download/${code}`;
    });
});