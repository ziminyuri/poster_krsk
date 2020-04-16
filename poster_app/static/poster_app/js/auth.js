function addBlock(){

}
$("#auth_block").submit(function (event) {
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
                //console.log(post_data);

                if (post_data == "Error sign in") {
                    $(".error_auth_label").text("Неверный пароль");
                }

                else {
                    //$(".error_auth_label").text("Sign in1");
                    //console.log('Sign in1');
                    window.location = "http://127.0.0.1:8000/events"
                }
            }
    });
});
