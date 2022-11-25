
app.controller("mainCtrl",['$scope', 'restapiServivce',  '$location',
	function($scope, restapiServivce,$location ) {

        // call rest api in order to get all data and add binding
        $scope.schema = null

        // get band information with members
        $scope.items = null
        $scope.item_choose = null
        $scope.htmlFormUpload = null

        $scope.htmlForm = null
        $scope.login = null
        $scope.password = null
        $scope.target = null
        $scope.detailTarget = false;
        $scope.listTarget = false;
        $scope.fields = []

        this.$onInit = function () {
            self.getItems();
            w_current_location = window.location.href
            w_query_suburl = w_current_location.split("#")
            if( w_query_suburl.length > 1){
                query = w_current_location.split("#")[1]
                if( query == "!" && w_query_suburl.length > 2){
                    query = w_current_location.split("#")[2]
                }
                list_query_param =  query.split("&");
                $scope.target = ""
                w_model_id = ""
                list_query_param.forEach(function(w_param){
                    w_part = w_param.split("=")
                    if( w_part.length > 1){
                        w_key = w_part[0]
                        w_value = w_part[1]
                        if (w_key == "target"){
                            $scope.target = w_value
                        }else if(w_key == "id"){
                            w_model_id = w_value
                        }else if(w_key == "item"){
                            $scope.item_choose = w_value
                        }
                    }
                })
                if( $scope.target ){
                    if( $scope.target == "read" && w_model_id ){
                        $scope.read(w_model_id)
                        $scope.detailTarget = $scope.loginOk
                    }else if( $scope.target == "list"){
                        $scope.list($scope.item_choose)
                        $scope.listTarget = $scope.loginOk

                    }
                }
            }

        };


        // get gig informations
        getItems = function() {
            if( !$scope.item  ){
                restapiServivce["items"].get({},function(aData) {
                    if( aData.data ){
                        $scope.items = []
                        aData.data.forEach(function(wItem){
                            $scope.items.push(wItem.id);

                        })
                    }
                })
            }
        }
       $scope.loginOk = false;

        // get gig informations
        $scope.auth = function() {
            if( $scope.login != null && $scope.password != null){
                w_login = new restapiServivce.service_login({
                    'login':$scope.login,
                    'password':$scope.password
                });
                w_login.$save(function(aData) {
                   $scope.loginOk = true;
                })
            }
        }
        var model = {}
        $scope.create = function() {
            $scope.loadForm()
            $scope.detailTarget = $scope.loginOk
            $scope.listTarget = !$scope.detailTarget

        }


        $scope.read = function(a_model_id) {
            $scope.loadSchema($scope.item_choose)
            $scope.loadForm()

            if( $scope.schema.properties ){
                Object.keys($scope.schema.properties).forEach(function(key){
                   model[key] = document.getElementById(key).value
                });
            }
              if ($scope.multipart && a_model_id ) {

                    $scope.htmlFormUpload='<form action="/api/'+$scope.item_choose+'s/'+a_model_id+'/blob"  method="post" enctype="multipart/form-data">'+
                      '<div>'+
                        '<label for="file">Choose file to upload</label>'+
                        '<input type="file" id="file" name="file" multiple />'+
                     ' </div>'+
                      '<div>'+
                       ' <button>upload</button>'+
                      '</div>'+
                    '</form>'

                }
                document.getElementById("htmlForm").innerHTML = $scope.htmlForm + $scope.htmlFormUpload
            if ( a_model_id ){
                restapiServivce[$scope.item_choose].get({"id":a_model_id},function(aData) {
                    var w_read_model = aData.data
                    Object.keys($scope.schema.properties).forEach(function(key){
                        if( w_read_model[key] ){
                            document.getElementById(key).value = w_read_model[key];
                        }
                        $scope.detailTarget = $scope.loginOk
                        $scope.listTarget = !$scope.detailTarget

                    });
                })
            }
        }

        $scope.list = function(a_item) {
            $scope.loadSchema(a_item)
            $scope.list_model = []
            restapiServivce[$scope.item_choose].get({},function(aData) {
                $scope.list_model = aData.data
                $scope.listTarget = $scope.loginOk
                $scope.detailTarget = !$scope.listTarget
            })
        }
        $scope.remove = function(a_model_id) {
            restapiServivce[$scope.item_choose].delete({id:a_model_id},function(aData) {
                $scope.listTarget = $scope.loginOk
                $scope.detailTarget = !$scope.listTarget
            })
        }
        $scope.update = function() {
          if( $scope.schema.properties ){
                Object.keys($scope.schema.properties).forEach(function(key){
                   model[key] = document.getElementById(key).value
                });
            }
           if ( model["_id"] ){
                var w_update = new restapiServivce[$scope.item_choose](model)
                w_update.$update({"id":model["_id"]}, function(aData) {
                    $scope.listTarget = $scope.loginOk
                    $scope.detailTarget = !$scope.listTarget
                })

            }
        }

        // get gig informations
        $scope.loadSchema = function(a_item) {
            $scope.item_choose = a_item

            restapiServivce[a_item+"sSchema"].get({},function(aData) {
                $scope.schema = aData.data;
                $scope.fields = []
                Object.keys($scope.schema.properties).forEach(function(key){
                    if (key == "_id"){
                        $scope.fields.push("id")
                    }else{
                        $scope.fields.push(key)
                    }
                });
            })

            restapiServivce[a_item+"sMultipart"].get({},function(aData) {
                $scope.multipart = aData.data.is_multipart

            })
        }
        // get gig informations
        $scope.loadForm = function() {
            if( $scope.schema.properties ){
                  $scope.htmlForm = ""
                  Object.keys($scope.schema.properties).forEach(function(key){
                    var w_label = $scope.schema.properties[key].description;
                    if(  $scope.schema.properties[key].maxLength && $scope.schema.properties[key].maxLength > 20 ){
                         $scope.htmlForm+="<label  class='col-sm-2 col-form-label'>"+w_label +"</label><textarea id='"+key+"' rows='10' cols='100'></textarea>\n</br>"
                    }else{
                        $scope.htmlForm+="<label  class='col-sm-2 col-form-label'>"+w_label +"</label><input id='"+key+"' ></input>\n</br>"
                    }
                });

                document.getElementById("htmlForm").innerHTML = $scope.htmlForm

            }
        }



}]);
