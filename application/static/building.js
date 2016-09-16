function insertBuildingInfo(binfo){
	///This function inserts the building information returned from the database into the 'building_info_section' div.

	//insert picture into left div
	//The image source is returned as part of the JSON file
	var image_source = "/static/" + binfo.building_info[0][11]; 
	document.getElementById('building_image').src = image_source;

	//insert contact information into the middle div
	var middle_div_content = `<div id="contact_info">
							<h3 class="table_title">
								Contact Information:
							</h3>
							<table class="info_table">
								<tr>
									<td>Phone: </td>
									<td> ` + binfo.building_info[0][3] + `</td>
								</tr>
								<tr>
									<td>e-mail: </td>
									<td>` + binfo.building_info[0][4] + `</td>
								</tr>
							</table>
							<h3 class="table_title">Opening Hours:</h3>
							<table class="info_table">
								<tr>
									<td>Monday-Friday</td>
									<td>` + binfo.building_info[0][5] + `-` + binfo.building_info[0][6] + `</td>
								</tr>
								<tr>
									<td>Saturday</td>
									<td>Closed</td>
								</tr>
									<td>Sunday</td>
									<td>Closed</td>
								</tr>
							</table>
						</div>`;
	document.getElementById("contact_info_div").innerHTML = middle_div_content;

	//insert the general occupancy stats in the right column
	
	//Calculate the building total capacity according to the room capacity
	var total_capacity = 0
	for (var i = 0; i < binfo.room_list.length; i++){
		total_capacity += binfo.room_list[i][1];
	}


	var right_div_content = `<div id="general_info">
							<h3 class="table_title">
								General Information:
							</h3>

							<table class="info_table">
								<tr>
									<td>Maximum Capacity:</td>
									<td>` + total_capacity + `</td>
								</tr>
								<tr>
									<td>Number of Rooms Monitored:</td>
									<td>` + binfo.room_list.length + `</td>
								</tr>
							</table>

							<h3 class="table_title">Room List:
							</h3>
	
							<table class="capacity_table">
								<tr>
									<th>Room</th>
									<th>Capacity</th>
									</tr>`;

	for (var i = 0; i < binfo.room_list.length; i++){
		right_div_content += `<tr>
								<td>` + binfo.room_list[i][0] + `</td>
								<td>` + binfo.room_list[i][1] + `</td>
							  </tr>`;
	}

	right_div_content += `</table>
						</div>`;

	document.getElementById('capacity_info_div').innerHTML = right_div_content;
}