function mapComplete(tf) {
	if(tf === true) {
		return "fas fa-check"
	} else { 
		return "fas fa-times"
	}	
}

function createRowHead() {
	var th = $(
		`<thead>
			<tr>
				<th>Topic</th>
                <th>Grade</th>
                <th>Complete</th>
                <th>Correct</th>
                <th>Total</th>
                <th>Comments</th>
			</tr>
		</thead>`);

	return th
}

function createRowBody(r) {
	var topic = r[0]; 
	var grade = r[1];
	var complete = mapComplete(r[2]);
 	var correct = r[3];
	var total = r[4];
	var comments = r[5].join("\n");

	var th = $(
		`<tbody>
			<tr>
				<td>${topic}</td>
                <td>${grade}</td>
                <td><i class="${complete}"></i></td>
                <td>${correct}</td>
                <td>${total}</td>
                <td>${comments}</td>
			</tr>
		</tbody>`);

	return th
}

function createTable(topics, i) {
	h2 = $(`<h2 style="margin-left: 15%; text-align: left;">Homework ${i}</h2>`);
	div1 = $(`<div id="homework${i}"  style="margin-bottom: 5%;"></div>`);
	div2 = $(`<div style="text-align: center;"></div>`);
	div3 = $(`<div class="table-responsive" style="max-width: 70%; display: inline-block"></div>`);
	table = $(`<table class="table table-striped table-sm" id="homeworktable${i}"></table>`);

	table.append(createRowHead());

	for (j = 0; j < topics.length; j++) {
		table.append(createRowBody(topics[j]));
	}
	// table appends head, bodys
	// div3 appends table
	// div2 appends h2, div3
	// div1 appends div2

	div3.append(table);
	div2.append(h2);
	div2.append(div3);
	div1.append(div2);

	console.log(div1);

	return div1
}

function correctTotal(hw) {
	var currsum = 0
	for (i = 0; i<hw.length; i++) {
		for (j = 0; j<hw[i].length; j++) {
			currsum += hw[i][j][3];
		}
	}
	return currsum
}

function qnsTotal(hw) {
	var currsum = 0
	for (i = 0; i<hw.length; i++) {
		for (j = 0; j<hw[i].length; j++) {
			currsum += hw[i][j][4];
		}
	}
	return currsum
}

$(document).ready(function(){

  var rTest1 = new Array("Surds", 4, true, 15, 17, ["khalid", "hassan"])
  var rTest2 = new Array("Fluids", 1, false, 73, -23, ["Need extra time", "translate welsh"])
  var rTest3 = new Array("Alg Top", 60, true, 150, 11237, ["trivial", "cauchar birkar smells of bread"])

  var rTest4 = new Array("Number Theory", 4, true, 15, 17, ["khalid", "hassan"])
  var rTest5 = new Array("Stats", 1, false, 73, -23, ["Need extra time", "translate welsh"])
  var rTest6 = new Array("Mechanics", 60, true, 150, 11237, ["trivial", "cauchar birkar smells of bread"])


  var hw = [
  		[rTest1, rTest2, rTest3],
  		[rTest4, rTest5, rTest6]
  ];

  var qns = qnsTotal(hw);
  var correct = correctTotal(hw);
  var pctg = 100*(correct/qns);


  // add user data scores
  $("#qns").append(String(qns));
  $("#correct").append(String(correct));
  $("#pctg").append(String(pctg).slice(0, 4) + "%");




  for (i = 1; i < hw.length + 1; i++) {
  	var topics = hw[i-1];

  	var homeworktable = createTable(topics, i);

  	//console.log(homeworktable);

  	$("#homeworkchris").append(homeworktable);
  }

  	$.get("https://ssaichack19.heroku.com/get_fractions_score", function(data){
	  alert("Data: " + data);
	});

});