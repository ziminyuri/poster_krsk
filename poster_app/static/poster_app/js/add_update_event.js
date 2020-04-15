$(document).ready(function(){
    var maxCount = 2000;

    $("#counter").html();

    $("#description").keyup(function() {
    var revText = this.value.length;

        if (this.value.length > maxCount)
            {
            this.value = this.value.substr(0, maxCount);
            }
        var cnt = (maxCount - revText);
        if(cnt <= 0){$("#counter").html('0');}
        else {$("#counter").html(cnt);}

    });
});


$('#isfree').click(function(){
	if ($(this).is(':checked')){
		$('#price').hide();
	} else {
		$('#price').show();
	}
});

function changeType() {
var eID = document.getElementById("exhibition_type");
var exhibition_type = eID.options[eID.selectedIndex].text;

if (exhibition_type === 'постоянная экспозиция'){
    document.getElementById("date_begin").classList.add('d-none');
    document.getElementById("date_end").classList.add('d-none');
    document.getElementById("label_date_begin").classList.add('d-none');
    document.getElementById("label_date_end").classList.add('d-none');
}
else {
    document.getElementById("date_begin").classList.remove('d-none');
    document.getElementById("date_end").classList.remove('d-none');
    document.getElementById("label_date_begin").classList.remove('d-none');
    document.getElementById("label_date_end").classList.remove('d-none');
}
//document.getElementById('colorDiv').style.background=colortxt;
}