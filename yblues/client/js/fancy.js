
function removeFancy() {
	$('#fancy-container').animate({opacity: 0}, 800);
	setTimeout(function(){ $('#fancy-background-and-all').animate({opacity: 0}, 100); }, 800);
	setTimeout(function(){ document.getElementById("fancy-background-and-all").remove() }, 900);
}

function showFancyWithThisContent(content) {

	var allTheFancy ='<div id="fancy-background-and-all" onclick="javascript:removeFancy();">';
	allTheFancy += 	'	<div id="fancy-container">';
	allTheFancy += 	'		<div id="fancy-content">';
	allTheFancy += 				content;
	allTheFancy += '		</div>';
	allTheFancy += '		<div id="fancy-bottom">';
	allTheFancy += '			<a href="javascript:removeFancy();"> [ close ]</a>';
	allTheFancy += '		</div>';
	allTheFancy += '	</div>';
	allTheFancy += '</div>';

	
	$('body').append(allTheFancy);
	$('#fancy-container').animate({opacity: 1}, 1000);
}