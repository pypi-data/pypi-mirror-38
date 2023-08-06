/*
	Кодировка: utf8
*/
'use strict';

async function readAlarms (){
	var d = await ajax_get ('alarms.json');
	/*
		stats:[
			{id:XX, name: XX, ...}, ...
		]
	*/
	var stats = await Promise.all(d.map(function(id){
		return ajax_get ('stat.json?filter=pN&tag=' + id)
	}));
	
	var html = stats.map (x=>"<a href='/index.html?id="+x.parentId+"' class='list-group-item list-group-item-danger'>" + x.fullName + "</a>");
	
	$('#alarms').html (html);
}