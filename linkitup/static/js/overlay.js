(function() {
	var $overlay = $('<div>Here I am</div>');
	var orginalContent = $('#body_left').children();
	orginalContent.hide();
	$('#body_left').append($overlay);
	$overlay.css({
	//     position: 'absolute',
	//     top: '1px',
	//     right: '1px',
	//     width: '100px',
	//     height: '100px',
		backgroundColor: 'red',
		// font
	});
})();