/*
 * Usage of $resource:
 *  $resource(url, [paramDefaults], [actions], options);
 *  see : https://docs.angularjs.org/api/ngResource/service/$resource
 */
angular.module('restapi').
  factory('restapiServivce', ['$resource', '$rootScope',
    function($resource, $rootScope) {   
	  current_url = window.location.protocol+"//"+window.location.hostname;
	  if( window.location.port ){
		  current_url=current_url+":"+window.location.port;
	  }
	  current_url+="/api"
      return {
        bands: $resource(current_url+'/bands'),
        news: $resource(current_url+'/news'),
        videos: $resource(current_url+'/videos'),

        albums: $resource(current_url+'/albums'),
        gigs: $resource(current_url+'/gigs'),
        band: $resource(current_url+'/bands/:id'),
        new: $resource(current_url+'/news/:id'),
        album: $resource(current_url+'/albums/:id'),
        gig: $resource(current_url+'/gigs/:id'),
        members: $resource(current_url+'/members'),
        musics: $resource(current_url+'/musics'),

       
        
      }
    }
  ]);
