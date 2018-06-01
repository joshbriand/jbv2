$(document).ready(function(){
	function init() {
		console.log('init');
		$('#submit').bind('click', calculate);
	}

	function calculate() {
		console.log('calculate');
		gross = $('#gross').val();

		tax_1_name = $('#tax-1-name').val();
		tax_1_rate = $('#tax-1-rate').val() / 100;
		tax_1_venue_percentage = $('#tax-1-retained').val() / 100;
		tax_1_artist_percentage = 1 - tax_1_venue_percentage;
		console.log(tax_1_artist_percentage);

		tax_2_name = $('#tax-2-name').val();
		tax_2_rate = $('#tax-2-rate').val() / 100;
		tax_2_venue_percentage = $('#tax-2-retained').val() / 100;
		tax_2_artist_percentage = 1 - tax_2_venue_percentage;

		total_tax = tax_1_rate + tax_2_rate;

		cc_gross = $('#cc-gross').val();
		cc_percentage = $('#cc-percentage').val();

		venue_percentage = $('#venue-percentage').val() / 100;
		artist_percentage = 1 - venue_percentage;

		after_tax = ((gross / (1 + total_tax))).toFixed(2);

		tax_1 = (after_tax * tax_1_rate).toFixed(2);
		tax_2 = (after_tax * tax_2_rate).toFixed(2);

		cc_fee = (cc_gross * cc_percentage / 100).toFixed(2);

		adjusted = (after_tax - cc_fee).toFixed(2);

		tax_1_artist = parseFloat((tax_1 * tax_1_artist_percentage).toFixed(2));
		tax_2_artist = parseFloat((tax_2 * tax_2_artist_percentage).toFixed(2));
		artist = parseFloat((adjusted * artist_percentage).toFixed(2));
		artist_net = (artist + tax_1_artist + tax_2_artist).toFixed(2);

		tax_1_venue = parseFloat((tax_1 * tax_1_venue_percentage).toFixed(2));
		tax_2_venue = parseFloat((tax_2 * tax_2_venue_percentage).toFixed(2));
		venue = parseFloat((adjusted * venue_percentage).toFixed(2));
		venue_net = parseFloat((venue + tax_1_venue + tax_2_venue).toFixed(2));

		$('.tax-1-name').text(tax_1_name)
		$('.tax-2-name').text(tax_2_name)

		$('#tax-1-total').text('$' + tax_1);
		$('#tax-2-total').text('$' + tax_2);
		$('#after-tax').text('$' + after_tax);
		$('#cc-fee').text('$' + cc_fee);
		$('#adjusted').text('$' + adjusted);
		$('#artist').text('$' + artist);
		$('#venue').text('$' + venue);

		$('#artist-tax-1').text('$' + tax_1_artist);
		$('#artist-tax-2').text('$' + tax_2_artist);
		$('#artist-take').text('$' + artist);
		$('#artist-net').text('$' + artist_net);

		$('#venue-tax-1').text('$' + tax_1_venue);
		$('#venue-tax-2').text('$' + tax_2_venue);
		$('#venue-take').text('$' + venue);
		$('#venue-net').text('$' + venue_net)

	}

	init ()
});
