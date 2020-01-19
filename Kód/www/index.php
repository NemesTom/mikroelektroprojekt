<!DOCTYPE HTML>
<html>
<head>  
<meta charset="UTF-8">

<script>

var datas={};
var chartData=[];
var points=[{x: 0, y: 2},];

window.onload = function () {

var ajax=new XMLHttpRequest();
    ajax.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
	    var data= JSON.parse(this.responseText);
	    for(var i=0;i<data.length;i++){
		points.push(JSON.parse(JSON.stringify(points[0])));
		points[points.length-1].x=parseFloat(data[i].time);
		points[points.length-1].y=parseInt(data[i].value);
	    }
	    chart.render();
        }
    }
    ajax.open("GET","getdata.php",true);
    ajax.send();

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,  
	title:{
		text: "Speed by second"
	},
	axisY: {
		title: "Speed Level",
		valueFormatString: "#",
		suffix: ""
	},
	data: [{
		yValueFormatString: "#",
		xValueFormatString: "#.###",
		type: "spline",
		dataPoints: points
	}]
});

console.log(points);
}
</script>
</head>
<body>
<div id="chartContainer" style="height: 370px; max-width: 920px; margin: 0px auto;"></div>
<script src="canvasjs.min.js"></script>
</body>
</html>
