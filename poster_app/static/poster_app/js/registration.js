$("#registration_block").submit(function (event) {
		event.preventDefault();

    const form = $(this);
    const url = form.attr('action');
    const formData = new FormData(this);

    $.ajax({
        type: "POST",
        url: url,
        data: formData,
		contentType: false,
        processData: false,
        success : function(post_data) {
            if (post_data === "Пароли не совпадают") {
                $(".error_auth_label").text("Пароли не совпадают");
            }
            else if(post_data === "Логин занят. Попробуйте другой"){
                $(".error_auth_label").text("Логин занят. Попробуйте другой");
            }
            else {
                window.location = "http://127.0.0.1:8000"
            }
        }
    });
});