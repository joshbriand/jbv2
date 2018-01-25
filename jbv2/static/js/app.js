var downContent = '';
var downLink = '';
var downSection = '';

$('#joshbriand').click(function(){
	if (downContent !== '') {
		up(downContent, downLink);
                $('#slogan').css('display', 'table');
                $('#actualSlogan').fadeIn(1200);
	}
})

$('#navSpacer').click(function(){
	if (downContent !== '') {
		up(downContent, downLink);
	}
})

$('#webDevLink').click(function(){
	if (downSection === 'webDev') {
		up(downContent, downLink);
		$('#slogan').css('display', 'table');
		$('#actualSlogan').fadeIn(1200);
	} else if (downSection !== '') {
		downContent.slideUp('slow', function(){
			up(downContent, downLink);
			$('#actualSlogan').fadeOut(400, function() {
				$('#slogan').css('display', 'none');
				$('#webDevContent').slideDown('slow');
				$('#webDevContent').css('display','flex');
				$('#webDevLink').css('text-decoration', 'underline');
				$('#merchLink').css('color', 'rgba(0,0,0,.15)');
				$('#contactLink').css('color', 'rgba(0,0,0,.15)');
				$('#portfolioLink').css('color', 'rgba(0,0,0,.15)');
				downContent = $('#webDevContent');
				downLink = $('#webDevLink');
				downSection = 'webDev';
			});
		});
	} else {
		$('#actualSlogan').fadeOut(400, function(){
			$('#slogan').css('display', 'none');
			$('#webDevContent').slideDown('slow');
			$('#webDevContent').css('display','flex');
			$('#webDevLink').css('text-decoration', 'underline');
			$('#merchLink').css('color', 'rgba(0,0,0,.15)');
			$('#contactLink').css('color', 'rgba(0,0,0,.15)');
			$('#portfolioLink').css('color', 'rgba(0,0,0,.15)');
			downContent = $('#webDevContent');
			downLink = $('#webDevLink');
			downSection = 'webDev';
		});
	};
});


$('#merchLink').click(function(){
	if (downSection === 'merch') {
		up(downContent, downLink);
		$('#slogan').css('display', 'table');
		$('#actualSlogan').fadeIn(1200);
	} else if (downSection !== '') {
		downContent.slideUp('slow', function(){
			up(downContent, downLink);
			$('#actualSlogan').fadeOut(400, function(){
				$('#slogan').css('display', 'none');
				$('#merchContent').slideDown('slow');
				$('#merchContent').css('display','flex');
				$('#merchLink').css('text-decoration', 'underline');
				$('#webDevLink').css('color', 'rgba(0,0,0,.15)');
				$('#contactLink').css('color', 'rgba(0,0,0,.15)');
				$('#portfolioLink').css('color', 'rgba(0,0,0,.15)');
				downContent = $('#merchContent');
				downLink = $('#merchLink');
				downSection = 'merch';
			});
		});
	} else {
		$('#actualSlogan').fadeOut(400, function(){
			$('#merchContent').slideDown('slow');
			$('#merchContent').css('display','flex');
			$('#merchLink').css('text-decoration', 'underline');
			$('#webDevLink').css('color', 'rgba(0,0,0,.15)');
			$('#contactLink').css('color', 'rgba(0,0,0,.15)');
			$('#portfolioLink').css('color', 'rgba(0,0,0,.15)');
			downContent = $('#merchContent');
			downLink = $('#merchLink');
			downSection = 'merch';
		});
	};
});


$('#portfolioLink').click(function(){
	if (downSection === 'portfolio') {
		up(downContent, downLink);
		$('#slogan').css('display', 'table');
		$('#actualSlogan').fadeIn(1200);
	} else if (downSection !== '') {
		downContent.slideUp('slow', function(){
			up(downContent, downLink);
			$('#actualSlogan').fadeOut(400, function() {
				$('#slogan').css('display', 'none');
				$('#portfolioContent').slideDown('slow');
				$('#portfolioContent').css('display','flex');
				$('#portfolioLink').css('text-decoration', 'underline');
				$('#webDevLink').css('color', 'rgba(0,0,0,.15)');
				$('#merchLink').css('color', 'rgba(0,0,0,.15)');
				$('#contactLink').css('color', 'rgba(0,0,0,.15)');
				downContent = $('#portfolioContent');
				downLink = $('#portfolioLink');
				downSection = 'portfolio';
			});
		});
	} else {
		$('#actualSlogan').fadeOut(400, function() {
			$('#slogan').css('display', 'none');
			$('#portfolioContent').slideDown('slow');
			$('#portfolioContent').css('display','flex');
			$('#portfolioLink').css('text-decoration', 'underline');
			$('#webDevLink').css('color', 'rgba(0,0,0,.15)');
			$('#merchLink').css('color', 'rgba(0,0,0,.15)');
			$('#contactLink').css('color', 'rgba(0,0,0,.15)');
			downContent = $('#portfolioContent');
			downLink = $('#portfolioLink');
			downSection = 'portfolio';
		});
	};
});


$('#contactLink').click(function(){
	if (downSection === 'contact') {
		up(downContent, downLink);
		$('#slogan').css('display', 'table');
		$('#actualSlogan').fadeIn(1200);
	} else if (downSection !== '') {
		downContent.slideUp('slow', function(){
			up(downContent, downLink);
			$('#actualSlogan').fadeOut(400, function() {
				$('#slogan').css('display', 'none');
				$('#contactContent').slideDown('slow');
				$('#contactContent').css('display','flex');
				$('#contactLink').css('text-decoration', 'underline');
				$('#webDevLink').css('color', 'rgba(0,0,0,.15)');
				$('#merchLink').css('color', 'rgba(0,0,0,.15)');
				$('#portfolioLink').css('color', 'rgba(0,0,0,.15)');
				downContent = $('#contactContent');
				downLink = $('#contactLink');
				downSection = 'contact';
			});
		});
	} else {
		$('#actualSlogan').fadeOut(400, function() {
			$('#slogan').css('display', 'none');
			$('#contactContent').slideDown('slow');
			$('#contactContent').css('display','flex');
			$('#contactLink').css('text-decoration', 'underline');
			$('#webDevLink').css('color', 'rgba(0,0,0,.15)');
			$('#merchLink').css('color', 'rgba(0,0,0,.15)');
			$('#portfolioLink').css('color', 'rgba(0,0,0,.15)');
			downContent = $('#contactContent');
			downLink = $('#contactLink');
			downSection = 'contact';
		});
	};
});

function up (content, link) {
	if (content !== '') {
		content.slideUp('slow');
	};
	$('#merchLink').css('color', 'rgba(0,0,0,1)');
	$('#webDevLink').css('color', 'rgba(0,0,0,1)');
	$('#contactLink').css('color', 'rgba(0,0,0,1)');
	$('#portfolioLink').css('color', 'rgba(0,0,0,1)');
	$('#merchLink').css('text-decoration', 'none');
	$('#webDevLink').css('text-decoration', 'none');
	$('#contactLink').css('text-decoration', 'none');
	$('#portfolioLink').css('text-decoration', 'none');
	downContent = '';
	downLink = '';
	downSection = '';
};
