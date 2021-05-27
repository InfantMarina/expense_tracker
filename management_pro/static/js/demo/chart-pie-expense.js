// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// for dynamically adding labels to the pie chart
var label = [];
$.each(json_keys, function(i,v){
  label.push(v);
});

// for dynamically adding data to the pie chart
var data_item = [];
$.each(json_values, function(i,v){
  data_item.push(v);
});

// for dynamically adding colors to pie chart
var colors = [];
for(let i=0;i<this.json_keys.length;i++){
  this.colors.push('#'+Math.floor(Math.random()*16777215).toString(16));
}

// for dynamically adding hover colors to pie chart
var hover_colors = [];
for(let i=0;i<this.json_keys.length;i++){
  this.hover_colors.push('#'+Math.floor(Math.random()*16777215).toString(16));
}

// Today Pie Chart
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: label,
    datasets: [{
      data: data_item,
      backgroundColor: this.colors,
      hoverBackgroundColor: this.hover_colors,
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 60,
  },
});

var custom_label = [];
$.each(custom_json_keys, function(i,v){
  custom_label.push(v);
});

// for dynamically adding data to the pie chart
var custom_data_item = [];
$.each(custom_json_values, function(i,v){
  custom_data_item.push(v);
});

// for dynamically adding colors to pie chart
var custom_colors = [];
for(let i=0;i<this.custom_json_keys.length;i++){
  this.custom_colors.push('#'+Math.floor(Math.random()*16777215).toString(16));
}

// for dynamically adding hover colors to pie chart
var custom_hover_colors = [];
for(let i=0;i<this.custom_json_keys.length;i++){
  this.custom_hover_colors.push('#'+Math.floor(Math.random()*16777215).toString(16));
}

// Custom Pie Chart
var ctx_custom = document.getElementById("custom_myPieChart");
var myPieChart = new Chart(ctx_custom, {
  type: 'doughnut',
  data: {
    labels: custom_label,
    datasets: [{
      data: custom_data_item,
      backgroundColor: custom_colors,
      hoverBackgroundColor: custom_hover_colors,
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 60,
  },
});
