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
		console.log(cc_gross);
		console.log(cc_percentage)
		temp_after_tax = ((gross / 1.12));
		after_tax = parseFloat(temp_after_tax);
		gst = (after_tax * .05);
		pst = (after_tax * .07);
		temp_cc_fee = cc_gross * cc_percentage / 100
		cc_fee = parseFloat(temp_cc_fee);
		console.log('temp cc fee');
		console.log(temp_cc_fee);
		console.log('cc fee');
		console.log(cc_fee);
		adjusted = after_tax - cc_fee;
		artist = (adjusted * .8);
		venue = (adjusted * .2);
		venue_pst = pst;
		artist_pst = (0);
		venue_20 = venue;
		artist_80 = artist;
		artist_has_gst = $('#artist-gst-number').is(":checked");
		if (artist_has_gst) {
			artist_gst = (gst * .8);
			venue_gst = (gst * .2);
		} else {
			artist_gst = (0);
			venue_gst = gst;
		}
		artist_net = artist_gst + artist_pst + artist_80;
		venue_net = venue_gst + venue_pst + venue_20;
		$('#gst').text('$' + gst.toFixed(2));
		$('#pst').text('$' + pst.toFixed(2));
		$('#after-tax').text('$' + after_tax.toFixed(2));
		$('#artist').text('$' + artist.toFixed(2));
		$('#venue').text('$' + venue.toFixed(2));
		$('#venue-gst').text('$' + venue_gst.toFixed(2));
		$('#venue-pst').text('$' + venue_pst.toFixed(2));
		$('#cc-fee').text('$' + cc_fee.toFixed(2));
		$('#venue-20').text('$' + venue_20.toFixed(2));
		$('#venue-net').text('$' + venue_net.toFixed(2))
		$('#artist-gst').text('$' + artist_gst.toFixed(2));
		$('#artist-pst').text('$' + artist_pst.toFixed(2));
		$('#artist-80').text('$' + artist_80.toFixed(2));
		$('#artist-net').text('$' + artist_net.toFixed(2));
	}

	init ()
});
