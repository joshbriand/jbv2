$(document).ready(function(){
	function init() {
		console.log('init');
		$('#submit').bind('click', calculate);
	}

	function calculate() {
		console.log('calculate');
		gross = $('#gross').val();
		temp_adjusted = ((gross / 1.12));
		console.log(temp_adjusted);
		adjusted = parseFloat(temp_adjusted);
		console.log(adjusted);
		gst = (adjusted * .05);
		pst = (adjusted * .07);
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
		$('#adjusted').text('$' + adjusted.toFixed(2));
		$('#artist').text('$' + artist.toFixed(2));
		$('#venue').text('$' + venue.toFixed(2));
		$('#venue-gst').text('$' + venue_gst.toFixed(2));
		$('#venue-pst').text('$' + venue_pst.toFixed(2));
		$('#venue-20').text('$' + venue_20.toFixed(2));
		$('#venue-net').text('$' + venue_net.toFixed(2))
		$('#artist-gst').text('$' + artist_gst.toFixed(2));
		$('#artist-pst').text('$' + artist_pst.toFixed(2));
		$('#artist-80').text('$' + artist_80.toFixed(2));
		$('#artist-net').text('$' + artist_net.toFixed(2));
	}

	init ()
});
