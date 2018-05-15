$(document).ready(function(){
	function init() {
		console.log('init');
		$('#submit').bind('click', calculate);
	}

	function calculate() {
		console.log('calculate');
		if ($('#hundreds').val()) {
			hundreds = $('#hundreds').val();
		}
		else {
			hundreds = 0;
		}
		hundreds_value = parseFloat(hundreds * 100);
		$('#hundreds-value').text('$' + hundreds_value.toFixed(2));

		//hundreds
		if ($('#hundreds').val()) {
			hundreds = $('#hundreds').val();
		}
		else {
			hundreds = 0;
		}
		hundreds_value = parseFloat(hundreds * 100);
		$('#hundreds-value').text('$' + hundreds_value.toFixed(2));

		//fifties
		if ($('#fifties').val()) {
			fifties = $('#fifties').val();
		}
		else {
			fifties = 0;
		}
		fifties_value = parseFloat(fifties * 50);
		$('#fifties-value').text('$' + fifties_value.toFixed(2));

		//twenties
		if ($('#twenties').val()) {
			twenties = $('#twenties').val();
		}
		else {
			twenties = 0;
		}
		twenties_value = parseFloat(twenties * 20);
		$('#twenties-value').text('$' + twenties_value.toFixed(2));

		//tens
		if ($('#tens').val()) {
			tens = $('#tens').val();
		}
		else {
			tens = 0;
		}
		tens_value = parseFloat(tens * 10);
		$('#tens-value').text('$' + tens_value.toFixed(2));

		//fives
		if ($('#fives').val()) {
			fives = $('#fives').val();
		}
		else {
			fives = 0;
		}
		fives_value = parseFloat(fives * 5);
		$('#fives-value').text('$' + fives_value.toFixed(2));

		//twoonies
		if ($('#twoonies').val()) {
			twoonies = $('#twoonies').val();
		}
		else {
			twoonies = 0;
		}
		twoonies_value = parseFloat(twoonies * 2);
		$('#twoonies-value').text('$' + twoonies_value.toFixed(2));

		//loonies
		if ($('#loonies').val()) {
			loonies = $('#loonies').val();
		}
		else {
			loonies = 0;
		}
		loonies_value = parseFloat(loonies * 1);
		$('#loonies-value').text('$' + loonies_value.toFixed(2));

		//quarters
		if ($('#quarters').val()) {
			quarters = $('#quarters').val();
		}
		else {
			quarters = 0;
		}
		quarters_value = parseFloat(quarters * .25);
		$('#quarters-value').text('$' + quarters_value.toFixed(2));

		//dimes
		if ($('#dimes').val()) {
			dimes = $('#dimes').val();
		}
		else {
			dimes = 0;
		}
		dimes_value = parseFloat(dimes * .10);
		$('#dimes-value').text('$' + dimes_value.toFixed(2));

		//nickels
		if ($('#nickels').val()) {
			nickels = $('#nickels').val();
		}
		else {
			nickels = 0;
		}
		nickels_value = parseFloat(nickels * .05);
		$('#nickels-value').text('$' + nickels_value.toFixed(2));

		//pennies
		if ($('#pennies').val()) {
			pennies = $('#pennies').val();
		}
		else {
			pennies = 0;
		}
		pennies_value = parseFloat(pennies * .01);
		$('#pennies-value').text('$' + pennies_value.toFixed(2));

		total_value = hundreds_value + fifties_value + twenties_value + tens_value + fives_value + twoonies_value + loonies_value + quarters_value + dimes_value + nickels_value + pennies_value;
		$('#total-value').text('$' + total_value.toFixed(2));

	}

	init ()
});
