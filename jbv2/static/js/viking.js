$(document).ready(function(){
	function init() {
		$('#art').hover(focus, unfocus);
		$('#words').hover(focus, unfocus);
		$('#yoga').hover(focus, unfocus);
		$('#contact').hover(focus, unfocus);
		$('#tangible').hover(focus, unfocus);
		$('#photography').hover(focus, unfocus);
		$('#normal').hover(focus, unfocus);
		$('#IR').hover(focus, unfocus);
		$('#all').hover(focus, unfocus);
		$('#art').click(redirect);
		$('#words').click(redirect);
		$('#yoga').click(redirect);
		$('#contact').click(mail);
	}

	function focus() {
		if ($(this).attr('class') != 'col-2 active') {
			console.log($(this).attr('class'));
			$(this).css('text-decoration', 'underline');
			$(this).css('background', 'rgba(255,255,255,.8)')
		}
	}

	function unfocus() {
		if ($(this).attr('class') != 'col-2 active') {
			$(this).css('text-decoration', 'initial');
			$(this).css('background', 'rgba(255,255,255,.6)')
		}
	}

	function redirect() {
		destination = 'vikinghill/' + $(this).attr('id');
		window.location.href = destination;
	}

	function mail() {
		window.location.href = "mailto:vikinghillproductions@gmail.com";
	}

	init();
})
