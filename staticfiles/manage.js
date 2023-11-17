$(document).ready(function () {
    // Get books from API
    $.get("/api/books/", function (books) {
        // Loop through books and create book cards
        books.forEach(function (book) {
            var bookCard = $("<div>").addClass("col-md-4 book-card");
            var title = $("<h3>").text(book.title);
            var author = $("<p>").text("Author: " + book.author);
            var description = $("<p>").text(book.description);
            var price = $("<p>").text("Price: $" + book.price); // Include the book price
            var deleteBtn = $("<button>").addClass("btn btn-danger").text("Delete");
            var editBtn = $("<button>").addClass("btn btn-primary").text("Edit");

            // Add click event to delete button
            deleteBtn.click(function () {
                $("#deleteModal").modal("show");
                $("#deleteBookBtn").off("click").on("click", function () {
                    $.ajax({
                        url: "/api/books/" + book.id + "/",
                        type: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf
                        },
                        success: function (result) {
                            location.reload();
                        }
                    });
                });
            });

            // Add click event to edit button
            editBtn.click(function () {
                // Populate modal fields with book details
                $("#editBookId").val(book.id);
                $("#editTitle").val(book.title);
                $("#editAuthor").val(book.author);
                $("#editDescription").val(book.description);
                $("#editPrice").val(book.price);
                $("#editModal").modal("show");
            });

            bookCard.append(title, author, description, price, deleteBtn, editBtn);
            $("#books-container").append(bookCard);
        });
    });

    // Submit edited book details
    $("#editBookForm").submit(function (event) {
        event.preventDefault();
        var bookId = $("#editBookId").val();
        var editedBook = {
            title: $("#editTitle").val(),
            author: $("#editAuthor").val(),
            description: $("#editDescription").val(),
            price: $("#editPrice").val()
        };

        $.ajax({
            url: "/api/books/" + bookId + "/",
            type: "PUT",
            data: editedBook,
            headers: {
                "X-CSRFToken": csrf
            },
            success: function (result) {
                $("#editModal").modal("hide");
                location.reload();
                // You may choose to update the book details displayed on the page here
            }
        });
    });
});
