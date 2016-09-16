
//Lists of strings used for yAxis labels
var timeList_short = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"];
var timeList_long = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"];
var dayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

//Declaring the charts as variables before creation for the sake of destroying them
//TODO: Updating the content might be a better option
var AverageHourlyChart = null;
var fiveCategoryChart = null;
var threeCategoryChart = null;
var frequencyOfUseChart = null;
var OccupancyRatingChart = null;
var ModuleDataChart = null;
var utilisationChart = null;

function createHourlyAverageChart(hourly_averages){
    //Get our data
    hourly_data = []
    for (var i = 0; i < hourly_averages.length; i++){
        hourly_data.push(hourly_averages[i].occupancy_category_5);
    }
    console.log(hourly_data);

    var ctx = document.getElementById("dailyAverageChart");
    averageHourlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeList_long,
            datasets: [{
                fill: true,
                label: '# of Devices',
                data: hourly_data,
                backgroundColor:
                'rgba(255, 99, 132, 0.2)'
                ,
                borderColor:'rgba(255,99,132,1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    scaleLabel:{
                        //used for y axis title
                    },
                    ticks: {
                        callback: function(label, index, labels) {
                            return Math.round(label*100) + "%";
                        },
                        min: 0,
                        max: 1
                    }
                }]
            },
            maintainAspectRatio: false,
            responsive: true,
            title: {
                fontSize: 10,
                fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                display: false,
                text: "Daily Average Associated Devices"
            },
            legend: {
                display: false
            },
            elements:{
                line:{
                    tension: 0
                }
            }

        }
    });
}

function createOccupancyChart(occu){
    //Destroy the chart if it already exists
    if(window.OccupancyRatingChart !== null){
        window.OccupancyRatingChart.destroy()
    }

    var data_points = [occu, 100-occu];

    var ctz = document.getElementById("occupancy_chart");
    var data = {
        labels: [
        "In Use",
        "Unused"
        ],
        datasets: [
        {
            data: data_points,
            backgroundColor: ["rgba(255,99,132,1)","rgb(128, 0, 0)"],
            hoverBackgroundColor: [
            "#FF6384",
            "#36A2EB"
            ]
        }]
    };

    OccupancyRatingChart = new Chart(ctz, {
        type: 'doughnut',
        data: data,
        options:{
            cutoutPercentage: 70,
            title: {
                fontSize: 15,
                fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                display: false,
                text: "Occupancy Rating"
            },
            rotation: 0,
            maintainAspectRatio: false,
            responsive: true,
            legend:{
                display: false,
                position: "top",
                labels:{

                    boxWidth: 20

                }
            }
        }
    });
}
function createFrequencyOfUseChart(stuff){

    //Destroy the chart if it already exists
    if(window.frequencyOfUseChart !== null){
        window.frequencyOfUseChart.destroy()
    }

    var ctz = document.getElementById("fou_chart");
    var data = {
        labels: [
        "In Use",
        "Unused"
        ],
        datasets: [
        {
            data: stuff,
            backgroundColor: ["rgb(102, 255, 153)","rgb(0, 153, 51)"],
            hoverBackgroundColor: [
            "#FF6384",
            "#36A2EB"
            ]
        }]
    };

    frequencyOfUseChart = new Chart(ctz, {
        type: 'doughnut',
        data: data,
        options:{
            cutoutPercentage: 70,
            title: {
                fontSize: 15,
                fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                display: false,
                text: "Frequency of Use"
            },
            rotation: 0,
            maintainAspectRatio: false,
            responsive: true,
            legend:{
                display: false,
                position: "top",
                labels:{
                    boxWidth: 20

                }
            }
        }
    });
}


function drawPredictedValueCharts(predictedValues){
    //This function takes the predicted values for occupancy returned via the JSON file and plots them onto
    //the 5-category and 3 category charts

    var dataLength = Object.keys(predictedValues).length;
    var occupancy_data = [];
    var predicted_data_5_cat = [];
    var associated_devices = [];
    var predicted_data_3_cat = [];

    for (i = 0; i < dataLength; i++){
        occupancy_data.push(predictedValues[i].occupancy);
        predicted_data_5_cat.push(predictedValues[i].occupancy_category_5);
        associated_devices.push(predictedValues[i].assoc_devices);
        predicted_data_3_cat.push(predictedValues[i].occupancy_category_3);
    }
    associated_devices = convertToPercentage(associated_devices, predictedValues[0].capacity);
    drawFiveCateogryChart(occupancy_data, predicted_data_5_cat, associated_devices);
    drawThreeCategoryChart(predicted_data_3_cat);
}

function drawFiveCateogryChart(occupancy_data, predicted_data, associated_devices){
    var ctx = document.getElementById("predictedHourly-5-cat");    
    console.log(associated_devices);

    if(window.fiveCategoryChart !== null){
        window.fiveCategoryChart.destroy();
        console.log("destroyed");
    }

    fiveCategoryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeList_short,
            datasets: [{
                fill: true,
                label: 'Actual Occupancy',
                data: occupancy_data,
                backgroundColor: 
                'rgba(255, 99, 132, 0.2)',
                borderColor:'rgba(255,99,132,1)',
                borderWidth: 1
            },
            {
                fill: true,
                label: 'Predicted Occupancy',
                data: predicted_data,
                backgroundColor:
                'rgba(100, 230, 184, 0.2)',
                borderColor:"rgba(100, 230, 184, 0.2)",
                borderWidth: 1
            },

            {
                fill: false,
                label: 'Associated Devices',
                data: associated_devices,
                backgroundColor:
                "rgba(51, 133, 255, 0.2)",
                borderColor:"#3385ff",
                borderWidth: 1}]
            },
            options: {

                scales: {
                    yAxes: [{
                        scaleLabel:{
                        //used for y axis title
                    },
                    ticks: {
                        callback: function(label, index, labels) {
                            return Math.round(label*100) + "%";
                        }
                    }
                }]
            },
            elements:{
                line:{
                    tension: 0
                }
            },
            
            maintainAspectRatio: false,
            responsive: true,
            title: {
                fontSize: 15,
                fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                display: false,
                text: "5-Category Occupancy Stastics"
            },
            legend: {
                display: true
            }

        }
    });
    
}

function drawThreeCategoryChart(predicted_data_3_cat){

    var options = {
        maintainAspectRatio: false,
        responsive: true,
        elements:{
            line:{
                tension: 0
            }
        },
        scales: {
            yAxes: [
            {
              ticks: {
                 callback: function(label, index, labels) {
                    if (label == 1){
                        return "Full";
                    }
                    else if (label == 0.5){
                        return "Occupied";
                    }
                    else{
                       return "Empty";
                   }
               },
               min: "0",
               max: "1",
               fixedStepSize: 0.5
           },
       }]
   }
}
var ctx = document.getElementById("predictedHourly-3-cat");
if(window.threeCategoryChart !== null){
    window.threeCategoryChart.destroy();
    console.log("got to three");
}

threeCategoryChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: timeList_short,
        datasets: [{
            fill: true,
            label: 'Predited Occupancy',
            data: predicted_data_3_cat,
            backgroundColor:
                'rgba(100, 230, 184, 0.2)',
                borderColor:"rgba(100, 230, 184, 0.2)",
            borderWidth: 1}]
        },

        options
    });


}



function plotModuleStastics(m_info, reg_stu){
    //we need to dynamially create the date timestamps that are placed on the chart y-axis because the number of 
    //classess of a particular model that has taken place is not predefined
    var ylabels = calculateYaxisLabels(m_info);

    //Now we get the data points
    var module_data_points = [];
    for (var i = 0; i < m_info.length; i++){
        var p = Math.round(m_info[i].occupancy_pred / reg_stu * 100);
        module_data_points.push(p);
    } 
    //pass the labels to the chart creation function
    createModuleChart(ylabels, module_data_points);
}

function createModuleChart(ylabels, ydata){
    var ctx = document.getElementById("moduleInfoChart");

    if(window.ModuleDataChart !== null){
        window.ModuleDataChart.destroy();
    }
    ModuleDataChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ylabels,
            datasets: [{
                fill: true,
                label: '# of Devices',
                data: ydata,
                backgroundColor:
                'rgba(255, 99, 132, 0.2)'
                ,
                borderColor:'rgba(255,99,132,1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    scaleLabel:{
                        //used for y axis title
                    },
                    ticks: {
                        min: 0,
                        max: 100
                    }
                }],
                xAxes: [{
                    ticks: {
                        minRotation: 0,
                        maxRotation: 90
                    }
                }]

            },
            maintainAspectRatio: false,
            responsive: true,
            title: {
                fontSize: 10,
                fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                display: false,
                text: "Daily Average Associated Devices"
            },
            legend: {
                display: false
            }

        }
    });

}

function createUtilisationChart(uti){

    //Destroy the chart if it already exists
    if(window.utilisationChart !== null){
        window.utilisationChart.destroy()
    }

    var data_points = [uti, 100-uti];
    var ctz = document.getElementById("utilisation_chart");
    var data = {
        labels: [
        "In Use",
        "Unused"
        ],
        datasets: [
        {
            data: data_points,
            backgroundColor: ["rgb(255, 255, 128)","rgb(179, 179, 0)"],
            hoverBackgroundColor: [
            "#FF6384",
            "#36A2EB"
            ]
        }]
    };

    utilisationChart = new Chart(ctz, {
        type: 'doughnut',
        data: data,
        options:{
            cutoutPercentage: 70,
            title: {
                fontSize: 15,
                fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                display: false,
                tuext: "Frequency of Use"
            },
            rotation: 0,
            maintainAspectRatio: false,
            responsive: true,
            legend:{
                display: false,
                position: "top",
                labels:{

                    boxWidth: 20

                }
            }
        }
    });
}

function destroyCharts(){
    if(window.fiveCategoryChart !== null){
        window.fiveCategoryChart.destroy();
    }
    if(window.threeCategoryChart !== null){
        window.threeCategoryChart.destroy()
    }
    if(window.dailyAverageChart !== null){
        window.dailyAverageChart.destroy()
    }
    if(window.frequencyOfUseChart !== null){
        window.frequencyOfUseChart.destroy()
    }
}   