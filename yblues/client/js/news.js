var fullNews=false;
var linkBlocker=false;


		$(document).ready(function() {	
				$( ".actu a" ).click(function() {
					if ($(this).attr("class") != "a-news title") {
						linkBlocker = true;
					}
				});
		}); 

		function showHideNews(id) {
				if(linkBlocker == false) {
						if(fullNews == false) {
						 i = 1;
						 while (i < 6) {
							if(i != id) {
								$("#actu"+i).hide(1000);
							}
							i++;
						 } 
						$("#"+id).siblings('#info').animate({height: "540px"}, 1500 );	
						fullNews = true;	
					} else {
						$("#"+id).siblings('#info').animate({height: "40px"}, 1500 );
						i = 1;
						while (i < 6) {
							if(i != id) {
								$("#actu"+i).show(1000);
							}
							i++;
						 } 
						 fullNews = false;
					}
				} else {
					linkBlocker = false;
				}
		}