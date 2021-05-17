
app.controller("mainCtrl",['$scope', 'restapiServivce',  '$location',
	function($scope, restapiServivce,$location ) {

	// call rest api in order to get all data and add binding 
	$scope.news = null

	// get band information with members
	$scope.band = null

	self.videoIdx = 0

	// get albums with music informations 
	$scope.albums = null

	// get gigs list 
	$scope.gigs = null
	function changeDateGroup(idMontrer, objectACacher) {
		objectACacher.removeClass( "table-date-visible" );
		objectACacher.addClass("hidden-date");
		$( "#date-"+idMontrer ).animate({opacity: 1}, 1000 );
		$( "#date-"+idMontrer ).removeClass( "hidden-date" );
		$( "#date-"+idMontrer ).addClass( "table-date-visible" );
	}

	$scope.clickOnDate=function(idElt) {
		var tableVisble = $('.table-date-visible');

		tableVisble.animate({
			opacity: 0
		}, 1000 );

		setTimeout(function(){ changeDateGroup(idElt, tableVisble) }, 1000);
	}
	this.$onInit = function () {



		console.log("main::onInit band="+self.band );
		self.getBand();
		self.getAlbum();
		self.getVideos();
		self.getGigs();

	};      
	$scope.selectyGigYear=function(year){
		self.gigYearSelect = year;

	}
	$scope.gigYearSelect = null
	$scope.news = null;
	// get gig informations
	self.getGigs = function() {      
		if (!$scope.gigs) { 
			$scope.gigs = [];
			let idx = (new Date()).getFullYear();
			wLastYear=null;
			restapiServivce.gigs.get({sort:"date(desc)"},function(aData) {
				aData.data.forEach(function(gig){
					wDate = new Date(gig.date);
					wYear = wDate.getFullYear()
					$scope.gigYearSelect =  $scope.gigYearSelect ==null || $scope.gigYearSelect < wYear? wYear: $scope.gigYearSelect;
					if (!$scope.gigs[Math.abs(wYear-idx)] || !$scope.gigs[Math.abs(wYear-idx)].gigs){
						
						wLastYear = wYear;
						$scope.gigs[Math.abs(wYear-idx)] ={
								klass : "hidden-date",
								year : wYear,
								gigs : []
						}

					}
					gig.dateOfMonth = wDate.getDate();
					if( String(gig.dateOfMonth).length < 2 ){
						gig.dateOfMonth = "0"+gig.dateOfMonth
					}
					gig.month = wDate.getMonth()+1;
					if( String(gig.month).length < 2 ){
						gig.month = "0"+gig.month
					}
					gig.name = gig.name || gig.place
					
					$scope.gigs[Math.abs(wYear-idx)].gigs.push(gig);
				});
				$scope.clickOnDate(idx)

				$scope.gigs[0].klass = "table-date-visible"

					console.log("get gigs");
			});  
		}
	}
	self.getBand = function() {      
		if (!$scope.band) {    
			restapiServivce.band.get({id:"yblues",expand:"member"},function(aData) {
				$scope.band = aData.data;

				console.log("get band");
			});
			restapiServivce.members.get({"filter":{"band.ref":"yblues"}},function(aData) {
                $scope.members =  aData.data;
				console.log("get member");
			});


		}
	}
	self.getAlbum = function() {      
		if (!$scope.albums) {    
			restapiServivce.albums.get({},function(aData) {
				$scope.albums = aData.data;
				//sort music
				$scope.albums && $scope.albums.forEach(function(album){
				    restapiServivce.musics.get({"filter":{"album.ref":album.id}},function(aData) {
				        album.music_docs = aData.data;

                        album.music_docs.sort(function(a,b){
                            return a.album.properties.numero < b.album.properties.numero ? -1:1;
                        });
                    });

				}) 

				console.log("get albums");
			});  
		}
	}
	
	
	self.onChangeVideo = function(b){
		if( b) {
			self.videoIdx++
		}else{
			self.videoIdx--
		} 
		if(self.videoIdx < 0 ){
			self.videoIdx = $scope.div_videos.length-1;
		}else if ( self.videoIdx >= $scope.div_videos.length ){
			self.videoIdx = 0;
		}
		$( "#vid-grp-1").animate({
                opacity: 0
            }, 1000 , function(){
                $scope.div_video = $scope.div_videos[self.videoIdx];
                $scope.div_video.forEach(function(video,idx){
                    console.log("set src for the rframe with ", video)
                    document.getElementById("video-"+idx).src = video.url;
                })
                setTimeout(function(){
                    $( "#vid-grp-1" ).animate({opacity: 1}, 1000 );
                    $( "#vid-grp-1" ).removeClass( "hidden-vid-grp" )
                },1000);
        });
		
	}
	self.getVideos = function() {      
		if (!$scope.div_video) {    
			restapiServivce.videos.get(function(aData) {
				$scope.div_videos = [];
				let idx = 0;
				for(i=0;i< aData.data.length;i++){
					if ( $scope.div_videos[idx] == null){
						$scope.div_videos[idx]= []
					} 
					$scope.div_videos[idx].push(aData.data[i])
					if (i>0 && (i+1) %4 == 0){
						idx++;
					}

				}
				div_video = $scope.div_videos && $scope.div_videos[self.videoIdx];
				div_video && div_video.forEach(function(video,idx){
					console.log("set src for the rframe with "+ video.url)
					document.getElementById("video-"+idx).src =video.url;

				})
				$scope.div_video = $scope.div_videos[0] 
				console.log("get videos");
			});  
		}
	}

}]);
