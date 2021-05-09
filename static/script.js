
function loadColumn(cars) {
	var i = 1;
	for(i;i<=20; i++){
		var textuse='Image'+i;
		document.getElementById(textuse).src=cars[i.toString()]['image'];
	}
};