'use strict';

$(function(){
	showNavbar ('menu-diag');
	
	ajax_get('/info.json', true).then(function(d){
		
		var modes = {
			 'on':	'Включено'
			,'off':	'Отключено'
			,'pwd':	'Защищено паролем'
		}
		
		$('#control-mode').text (modes[d.web.ctrlMode]);
	});
	
	setInterval (readAlarms, 1000);
});

async function showLog(name){
	var d = await ajax_get ('/log/' + name);
	$('#preview').text ( d );	
}


