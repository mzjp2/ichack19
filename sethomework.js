function submit(myData) {
	var myData = {
		"topic": $("#inputTopic").val(),
		"amount": $("#inputAmt").val(),
		"grade": $("#inputLevel").val()
	}

	// var myData = "This is my data string."
	// $.post("https://ssaichack19.herokuapp.com/homework", data)

	$.ajax({
            url: 'https://ssaichack19.herokuapp.com/homework',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: myData,
            success: function (data) {
                console.log('sent data ninja')
            }
        });

	console.log(data);	
}


$(document).ready(function(){
	btn = $(`<button onclick=submit() style="margin-left: 15%" class="btn btn-primary">Submit</button>`);

	$("#forms").append(btn);

});