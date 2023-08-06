
function ajax_get (url, log_reply)
{
	if ( log_reply )
		console.log ("GET " + url + " ...");
	
	return new Promise (function(resolve, reject){
		$.ajax ({
			 type: 			"GET"
			,url: 			url
			,cache:			false
			,success: function(d){
				if ( log_reply )
					console.log ("GET " + url + " =>",  d );
				resolve ( d );
			}
			,error:	function(xhr, ajaxOptions, thrownError){
				console.error ("Failed GET '" + url + "': " + xhr.statusText + " (" + xhr.status + "): " + xhr.responseText);
				reject ({
					status:			xhr.status
					,status_text:	xhr.statusText
					,message:		xhr.responseText || "Ответ отсутствует"
				});
			}
		});
	});
}

function ajax_post (url, opt_d, log_reply)
{
	if ( log_reply )
		console.log ("POST " + url + " ...");

	if ( opt_d )
	{
		return new Promise (function(resolve, reject){
			$.ajax ({
				 type: 			"POST"
				,url: 			url
				,dataType:		"text"
				,data:			JSON.stringify(opt_d, undefined, "\t" )
				,contentType:	"application/json; charset=UTF-8"
				,processData:	false
				,success:		function(d, p1, p2){
					if ( log_reply )
						console.dir ("POST " + url + " =>", d );
					
					if ( d && typeof(d)==="string" && url.indexOf(".json")!=-1 )
						d = JSON.parse(d);
					
					resolve ( d );
				}
				,error:	function(xhr, ajaxOptions, thrownError){
					console.error ("Failed POST '" + url + "': " + xhr.statusText + " (" + xhr.status + "): " + xhr.responseText);
					reject ({
						status:			xhr.status
						,status_text:	xhr.statusText
						,message:		xhr.responseText || "Ответ отсутствует"
					});
				}
			});
		});
	}
	else
	{
		return new Promise (function(resolve, reject){
			$.ajax ({
				 type: 			"POST"
				,url: 			url
				,success:		function(d, p1, p2){
					//console.log ("POST " + url + " OK");
					if ( log_reply )
						console.dir ("POST " + url + " =>", d );
					resolve ( d );
				}
				,error:	function(xhr, ajaxOptions, thrownError){
					console.error ("Failed POST '" + url + "': " + xhr.statusText + " (" + xhr.status + "): " + xhr.responseText);
					reject ({
						status:			xhr.status
						,status_text:	xhr.statusText
						,message:		xhr.responseText || "Ответ отсутствует"
					});
				}
			});
		});
	}
}


