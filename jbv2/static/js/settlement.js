$(document).ready(function(){
	function init() {
		console.log('init');
		$('#submit').bind('click', calculate);
	}

	function calculate() {
		console.log('calculate');
		gross = $('#gross').val();
		cc_gross = $('#cc-gross').val();
		cc_percentage = $('#cc-percentage').val();
		venue_percentage = $('#venue-percentage').val() / 100;
		artist_percentage = 1 - venue_percentage;
		temp_after_tax = ((gross / 1.12));
		after_tax = parseFloat(temp_after_tax);
		gst = (after_tax * .05);
		pst = (after_tax * .07);
		temp_cc_fee = cc_gross * cc_percentage / 100
		cc_fee = parseFloat(temp_cc_fee);
		adjusted = after_tax - cc_fee;
		artist = (adjusted * artist_percentage);
		venue = (adjusted * venue_percentage);
		venue_pst = pst;
		artist_pst = (0);
		venue_take = venue;
		artist_take = artist;
		artist_has_gst = $('#artist-gst-number').is(":checked");
		if (artist_has_gst) {
			artist_gst = (gst * artist_percentage);
			venue_gst = (gst * venue_percentage);
		} else {
			artist_gst = (0);
			venue_gst = gst;
		}
		artist_net = artist_gst + artist_pst + artist_take;
		venue_net = venue_gst + venue_pst + venue_take;
		$('#gst').text('$' + gst.toFixed(2));
		$('#pst').text('$' + pst.toFixed(2));
		$('#after-tax').text('$' + after_tax.toFixed(2));
		$('#adjusted').text('$' + adjusted.toFixed(2));
		$('#artist').text('$' + artist.toFixed(2));
		$('#venue').text('$' + venue.toFixed(2));
		$('#venue-gst').text('$' + venue_gst.toFixed(2));
		$('#venue-pst').text('$' + venue_pst.toFixed(2));
		$('#cc-fee').text('$' + cc_fee.toFixed(2));
		$('#venue-take').text('$' + venue_take.toFixed(2));
		$('#venue-net').text('$' + venue_net.toFixed(2))
		$('#artist-gst').text('$' + artist_gst.toFixed(2));
		$('#artist-pst').text('$' + artist_pst.toFixed(2));
		$('#artist-take').text('$' + artist_take.toFixed(2));
		$('#artist-net').text('$' + artist_net.toFixed(2));
	}

	init ()
});
