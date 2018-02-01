var downContent = '';
var downLink = '';
var downSection = '';
var downHeader = '';
var subHeader = '';

$('#vikingHill').click(function(){
	if (downContent !== '') {
		up(downContent, downLink);
	}
})

$('#blank').click(function(){
	if (downContent !== '') {
		up(downContent, downLink);
	}
})

$('#circles').click(function(){
	if (downContent !== '') {
		up(downContent, downLink);
	}
})

$('#art-photos-all').click(function(){

});

$('#art-photos-ir').click(function(){

});

$('#art-photos-normal').click(function(){

});

$('#words-blog').click(function(){
	$('#words-blog').css('text-decoration', 'underline');
	$('#words-thoughts').css('text-decoration', 'none');
	$('#words-stories').css('text-decoration', 'none');
	$('#words-blog').css('color', 'rgba(0,0,0,1)');
	$('#words-thoughts').css('color', 'rgba(0,0,0,.5)');
	$('#words-stories').css('color', 'rgba(0,0,0,.5)');
	$('#siteContent').children().css('display', 'none');
	$('#words-blog-content').css('display', 'flex');
});

$('#words-thoughts').click(function(){
	$('#words-thoughts').css('text-decoration', 'underline');
	$('#words-blog').css('text-decoration', 'none');
	$('#words-stories').css('text-decoration', 'none');
	$('#words-thoughts').css('color', 'rgba(0,0,0,1)');
	$('#words-blog').css('color', 'rgba(0,0,0,.5)');
	$('#words-stories').css('color', 'rgba(0,0,0,.5)');
	$('#siteContent').children().css('display', 'none');
	$('#words-thoughts-content').css('display', 'flex');
});

$('#words-stories').click(function(){
	$('#words-stories').css('text-decoration', 'underline');
	$('#words-thoughts').css('text-decoration', 'none');
	$('#words-blog').css('text-decoration', 'none');
	$('#words-stories').css('color', 'rgba(0,0,0,1)');
	$('#words-thoughts').css('color', 'rgba(0,0,0,.5)');
	$('#words-blog').css('color', 'rgba(0,0,0,.5)');
	$('#siteContent').children().css('display', 'none');
	$('#words-stories-content').css('display', 'flex');
});

$('#art-tangible').click(function(){
	$('#photosSubHeader').css('display', 'none');
	$('#art-tangible').css('text-decoration', 'underline');
	$('#art-photos').css('text-decoration', 'none');
	$('#art-photos').css('color', 'rgba(0,0,0,.5)');
	$('#art-tangible').css('color', 'rgba(0,0,0,1)');
	$('#siteContent').children().css('display', 'none');
	$('#art-tangible-content').css('display', 'flex');
});


$('#art-photos').click(function(){
	$('#photosSubHeader').css('display', 'table');
	$('#art-photos').css('text-decoration', 'underline');
	$('#art-tangible').css('color', 'rgba(0,0,0,.5)');
	$('#art-photos').css('color', 'rgba(0,0,0,1)');
	$('#art-tangible').css('text-decoration', 'none');
	$('#art-photos-all').css('text-decoration', 'underline');
	$('#art-photos-ir').css('color', 'rgba(255,255,255,.5)');
	$('#art-photos-normal').css('color', 'rgba(255,255,255,.5)');
	$('#siteContent').children().css('display', 'none');
	$('#art-photos-all-content').css('display', 'flex');
});

$('#art').click(function(){
	if (downSection === 'art') {
		up(downContent, downLink);
		$('#artHeader').css('display','none');
		$('#artContent').css('display','none');
		$('#slider').css('display', 'table');
	}  else {
		up(downContent, downLink);
		$('#slider').css('display', 'none');
		$('#artHeader').css('display','table');
		$('#artContent').css('display','flex');
		$('#art').css('text-decoration', 'underline');
		$('#words').css('color', 'rgba(0,0,0,.5)');
		$('#yoga').css('color', 'rgba(0,0,0,.5)');
		$('#contact').css('color', 'rgba(0,0,0,.5)');
		downContent = $('#artContent');
		downLink = $('#art');
		downSection = 'art';
		downHeader = $('#artHeader');
	};
});

$('#words').click(function(){
	if (downSection === 'words') {
		up(downContent, downLink);
		$('#wordsHeader').css('display','none');
		$('#wordsContent').css('display','none');
		$('#slider').css('display', 'table');
	}  else {
		up(downContent, downLink);
		$('#slider').css('display', 'none');
		$('#wordsHeader').css('display','table');
		$('#wordsContent').css('display','flex');
		$('#words').css('text-decoration', 'underline');
		$('#art').css('color', 'rgba(0,0,0,.5)');
		$('#yoga').css('color', 'rgba(0,0,0,.5)');
		$('#contact').css('color', 'rgba(0,0,0,.5)');
		downContent = $('#wordsContent');
		downLink = $('#words');
		downSection = 'words';
		downHeader = $('#wordsHeader');
	};
});

$('#yoga').click(function(){
	if (downSection === 'yoga') {
		up(downContent, downLink);
		$('#yogaHeader').css('display','none');
		$('#yogaContent').css('display','none');
		$('#slider').css('display', 'table');
	}  else {
		up(downContent, downLink);
		$('#slider').css('display', 'none');
		$('#yogaHeader').css('display','table');
		$('#yogaContent').css('display','flex');
		$('#yoga').css('text-decoration', 'underline');
		$('#words').css('color', 'rgba(0,0,0,.5)');
		$('#art').css('color', 'rgba(0,0,0,.5)');
		$('#contact').css('color', 'rgba(0,0,0,.5)');
		downContent = $('#yogaContent');
		downLink = $('#yoga');
		downSection = 'yoga';
		downHeader = $('#yogaHeader');
	};
});

$('#contact').click(function(){
	if (downSection === 'contact') {
		up(downContent, downLink);
		$('#contactHeader').css('display','none');
		$('#contactContent').css('display','none');
		$('#slider').css('display', 'table');
	}  else {
		up(downContent, downLink);
		$('#slider').css('display', 'none');
		$('#contactHeader').css('display','table');
		$('#contactContent').css('display','flex');
		$('#contact').css('text-decoration', 'underline');
		$('#words').css('color', 'rgba(0,0,0,.5)');
		$('#yoga').css('color', 'rgba(0,0,0,.5)');
		$('#art').css('color', 'rgba(0,0,0,.5)');
		downContent = $('#contactContent');
		downLink = $('#contact');
		downSection = 'contact';
		downHeader = $('#contactHeader');
	};
});

function up (content, link) {
	if (content !== '') {
		$('#photosSubHeader').css('display', 'none');
		content.css('display','none');
		downHeader.css('display', 'none');
	};
	$('#art').css('color', 'rgba(0,0,0,1)');
	$('#yoga').css('color', 'rgba(0,0,0,1)');
	$('#contact').css('color', 'rgba(0,0,0,1)');
	$('#words').css('color', 'rgba(0,0,0,1)');
	$('#art').css('text-decoration', 'none');
	$('#yoga').css('text-decoration', 'none');
	$('#contact').css('text-decoration', 'none');
	$('#words').css('text-decoration', 'none');
	downContent = '';
	downLink = '';
	downSection = '';
	downHeader = '';
};
