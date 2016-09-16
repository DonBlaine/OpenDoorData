function convertToPercentage(data, capacity){
	//This function takes in a set of data points and returns them as a percentage
	//of a rooms capacity

	for (var i = 0; i <  data.length; i++){
		data[i] = Math.round(data[i]/capacity * 100) / 100;
	}
	return data
}

function getFrequencyPercentage(freq){
	//This function calculates and displays the frequency of use of a particular room according to the JSON data
	var sum = parseInt(freq[0]) + parseInt(freq[1]);
	var frequency_percentage = Math.round(freq[0] / sum * 100);
	document.getElementById("general_fou_percent").innerHTML = frequency_percentage.toString() + "%";
	return frequency_percentage;
}

function getUtilisationScore(freq, occu){
	var score = Math.round(freq * occu / 100)
	document.getElementById("utilisation_percent").innerHTML = score.toString() + "%"; 
	return score;
}

function setOccupancyPercentage(occu){
	//This function calculates and displays the occupancy rating of a particular room according to the JSON data
	document.getElementById("general_occupancy_percent").innerHTML = occu.toString() + "%";
}

function calculateYaxisLabels(minfo){
	//Based on the times supplied in the JSON data this function will create the Y axis labels that are used on the historial 
	//module data graph

	//initiate labels to an empty array
	var labels = [];

	//loop through each class that has been recorded and create a yaxis label string consisting of the date format = 'day' of 'month' 'yea' @ 'TIME'
	for (var i = 0; i < minfo.length; i++){
		var dateStr = minfo[i].event_day + "/" + minfo[i].event_month + "/" + minfo[i].event_year + " @ " + minfo[i].event_hour;
		labels.push(dateStr);
	}

	return labels;
}
