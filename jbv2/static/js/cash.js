$(document).ready(function(){
	function init() {
		console.log('init');
		$('#submit').bind('click', calculate);
	}

	function calculate() {
		console.log('calculate');
		if ($('#hundreds').val()) {
			hundreds = $('#gross').val();
		}
		else {
			hundreds = 0;
		}
		console.log(hundreds);
		hundreds_value = hundreds * 100;
		console.log(hundreds_value);
		hundreds_float_value = parseFloat(hundreds * 100);
		console.log(hundreds_float_value)
		hundreds_float_value_2 = parseFloat(hundreds * 100).toFixed(2);
		console.log(hundreds_float_value_2);
		$('#artist-net').text('$' + artist_net.toFixed(2));
	}

	init ()
});
