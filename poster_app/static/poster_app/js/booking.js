function chooseTickets(btn) {

    //Меняем стоимость при бронировании
    const ticket_price_str = document.getElementById("price-ticket").textContent;
    var ticket_price_int = parseInt(ticket_price_str);
    const all_price_str = document.getElementById("all-price-ticket").textContent;
    var all_price_int = parseInt(all_price_str);


    //Меняем цвет кнопки, если выделено место
    if(btn.classList.contains('btn-booking')){
        btn.classList.add('btn-booking-active')
        btn.classList.remove('btn-booking')

        all_price_int += ticket_price_int
    }
    else{
        btn.classList.add('btn-booking')
        btn.classList.remove('btn-booking-active')

        all_price_int -= ticket_price_int
        if (all_price_int <0) {
            all_price_int=0;
        }
    }

    //Меняем выбраное место при бронировании
    var booking_choice_p = document.getElementById("booking_choice_p");
    const p = booking_choice_p.textContent
    const btn_text = btn.value
    if (p.includes(btn_text)){
         new_str = p.replace(btn_text, '');
         booking_choice_p.innerHTML = new_str
    }
    else{
        booking_choice_p.innerHTML += "<br>" + btn.value;
    }

    var booking_choice_price_p = document.getElementById("booking-choice-price-p")
    document.getElementById("all-price-ticket").innerHTML = all_price_int
    if (all_price_int===0){
        booking_choice_price_p.innerHTML = ''
    }
    else{
        booking_choice_price_p.innerHTML = 'Билетов выбрано на: ' + all_price_int + ' рублей'
    }

    //Устанавливаем значение hidden input с местом для POST запроса
    const booking_choice_label = document.getElementById("booking_choice_p").textContent
    document.getElementById("booking_place_input").value = booking_choice_label


}

function bookingTickets() {
    const booking_choice_p = document.getElementById('booking-choice-p').textContent;
    const event_id = document.getElementById('event-id').textContent;
    const url = "http://127.0.0.1:8000/booking/" + event_id;
    const data = {booking_choice_p: booking_choice_p};
    $.ajax({
        type: "POST",
        url: url,
        data: data,
		contentType: false,
            processData: false,
            success : function(post_data) {

                if (post_data === "Error sign in") {
                    $(".error_auth_label").text("Неверный пароль");
                }

                else {
                    window.location = "http://127.0.0.1:8000"
                }
            }
    });
}
