$(document).ready(function(){
	function init() {
		console.log('init');
		$('#submit').bind('click', calculate);
	}

	function calculate() {
		console.log('calculate');
		if $('#gross').val() {
			hundreds = parseFloat($('#gross').val());
		}
		else {
			hundreds = 0.00;
		}
		console.log(hundreds);


		$('#artist-net').text('$' + artist_net.toFixed(2));
	}

	init ()
});
