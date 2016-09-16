QUnit.test( "convertToPercentage", function( assert ) {
	var data = [10,20,30,40,50];
	var capacity = 100;

	for (var i = 0; i <  data.length; i++){
		data[i] = Math.round(data[i]/capacity * 100) / 100;
	}

  assert.equal(data[0], 0.1, "Correct!" );
  assert.equal(data[1], 0.2, "Correct!" );
  assert.equal(data[2], 0.3, "Correct!" );
  assert.equal(data[3], 0.4, "Correct!" );
  assert.equal(data[4], 0.5, "Correct!" );
});

QUnit.test( "getFrequencyPercentage", function( assert ) {
	var freq1 = 139; //Occupied slots
	var freq2 = 55; //Unoccupied slots

	var sum = freq1 + freq2;
	var frequency_percentage = Math.round(freq1 / sum * 100);

	assert.equal(frequency_percentage, 72, "Correct Percentage Calculated!" );
});

QUnit.test( "getUtillisationScore", function( assert ) {
	var freq = 73;
	var occu = 33;
	var score = Math.round(freq * occu / 100)

	assert.equal(score, 24, "Correct Percentage Calculated!" );
});

QUnit.test( "calculateYaxisLabels", function( assert ) {
	var labels = []
	var data = [{event_day: 23, event_month: 11, event_year: 2015, event_hour: 9}];
	
	for (var i = 0; i < data.length; i++){
		var dateStr = data[i].event_day + "/" + data[i].event_month + "/" + data[i].event_year + " @ " + data[i].event_hour;
		labels.push(dateStr);
	}

	assert.equal(labels[0], "23/11/2015 @ 9", "Output string matches!" );
});



