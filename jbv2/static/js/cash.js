$(document).ready(function(){
	var total = 0;
	var summary = [0,0,0,0,0,0,0,0,0,0,0];
	var summaryCodec = [100, 50, 20, 10, 5, 2, 1, .25, .1, .05, .01]
	function init() {
		console.log('init');
		$('#hundreds').bind('change', {value: 100, destination: '#hundreds-value', source: '#hundreds'}, calculateRow);
		$('#fifties').bind('change', {value: 50, destination: '#fifties-value', source: '#fifties'}, calculateRow);
		$('#twenties').bind('change', {value: 20, destination: '#twenties-value', source: '#twenties'}, calculateRow);
		$('#tens').bind('change', {value: 10, destination: '#tens-value', source: '#tens'}, calculateRow);
		$('#fives').bind('change', {value: 5, destination: '#fives-value', source: '#fives'}, calculateRow);
		$('#twoonies').bind('change', {value: 2, destination: '#twoonies-value', source: '#twoonies'}, calculateRow);
		$('#loonies').bind('change', {value: 1, destination: '#loonies-value', source: '#loonies'}, calculateRow);
		$('#quarters').bind('change', {value: .25, destination: '#quarters-value', source: '#quarters'}, calculateRow);
		$('#dimes').bind('change', {value: .1, destination: '#dimes-value', source: '#dimes'}, calculateRow);
		$('#nickels').bind('change', {value: .05, destination: '#nickels-value', source: '#nickels'}, calculateRow);
		$('#pennies').bind('change', {value: .01, destination: '#pennies-value', source: '#pennies'}, calculateRow);
	}

	function calculateRow(info) {
		console.log('calculate row');
		value = info.data.value;
		destination = info.data.destination;
		source = info.data.source;
		destination_value = parseFloat(value * $(source).val());
		$(destination).text('$' + destination_value.toFixed(2));
		total = 0;
		for (var x=0; x<summaryCodec.length; x++) {
			if (value == summaryCodec[x]) {
				summary[x] = destination_value;
			}
			total = total + summary[x];
		}
		$('#total-value').text('$' + total.toFixed(2));
	}

	init ()
});
