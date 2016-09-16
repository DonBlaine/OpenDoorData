//When the page loads we want to automatically query the DB and plot
//plot the information on the chart

var room_selection;
function displayDate(){
	var date = new Date(document.getElementById("datething").value);
	getPredictedInfo(date.getDate(), date.getMonth() + 1, date.getFullYear())
}

function getPredictedInfo(date, month, year){
	var xmlhttp = new XMLHttpRequest();
	
	var url = "/predicted/" + room_selection + "/" + date + "/" + month + "/" + year;
	console.log(url);

	xmlhttp.onreadystatechange = function() {
	    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	        var predictedValues = JSON.parse(xmlhttp.responseText);
	        //Once we've got the data from our database in JSON format we then
	        //proceed to draw the chart
	        console.log(predictedValues);
	        
	        drawPredictedValueCharts(predictedValues);
	    }
	    else if (xmlhttp.status == 500){
	    	console.log("no data available");
	    }
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}
//Using XMLHttpRequest() to query flask application
function getRoomInfo(){
	//get the room selected by the user
	var selector = document.getElementById("room_select");
	room_selection = selector.options[selector.selectedIndex].value;


	//Then do a AJAX request for data about this room
	sendJSONRequest(room_selection);
	
}

function sendJSONRequest(room){
	var xmlhttp = new XMLHttpRequest();
	var url = "/dailyavg/" + room;
	

	xmlhttp.onreadystatechange = function() {
	    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	        var general_hourly_average = JSON.parse(xmlhttp.responseText);
	        //Once we've got the data from our database in JSON format we then
	        //proceed to draw the chart
	        // TODO: If a chart has already been drawn 
	        // then it needs to be refreshed rather than drawn again
	        console.log(general_hourly_average);
	        var freq_percentage = getFrequencyPercentage(general_hourly_average[0].Frequency);
	       	var utilisationScore = getUtilisationScore(freq_percentage, general_hourly_average[0].Occupancy_Rating);
	        createHourlyAverageChart(general_hourly_average[0].Daily);
	        createFrequencyOfUseChart(general_hourly_average[0].Frequency);
	        setOccupancyPercentage(general_hourly_average[0].Occupancy_Rating);
	        createOccupancyChart(general_hourly_average[0].Occupancy_Rating);
	        createUtilisationChart(general_hourly_average[0].Occupancy_Rating);
	    }
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

function getBuildingInfo(){
	//get the code for the building selected
	var selector = document.getElementById("building_select");
	building_selection = selector.options[selector.selectedIndex].value;
	
	//query the information from the controller
	queryBuildingInfo(building_selection);
}

function queryBuildingInfo(building_code){
	var xmlhttp = new XMLHttpRequest();
	var url = "/getBuildingInfo/" + building_code;
	
	

	xmlhttp.onreadystatechange = function() {
	    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	        var b_info = JSON.parse(xmlhttp.responseText);
	        
	        //Update the marker on the map
	        addMarker(b_info.building_info[9], b_info.building_info[10]);

	        //insert the building information into hidden divs
	        insertBuildingInfo(b_info);
	    }
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

function getModuleInfo(){
	var xmlhttp = new XMLHttpRequest();

	var selector = document.getElementById("module_select");
	var module_selected = selector.options[selector.selectedIndex].value;
	var url = "/getModuleInfo/" + module_selected;
	
	

	xmlhttp.onreadystatechange = function() {
	    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	        var m_info = JSON.parse(xmlhttp.responseText);
	        
	        //plot the module information on a chart
	        plotModuleStastics(m_info.module_info, m_info.registered_students)

	    }
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}