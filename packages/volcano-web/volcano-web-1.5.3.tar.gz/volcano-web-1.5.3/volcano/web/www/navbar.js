/*
	Кодировка
*/
'use strict';

function showNavbar (activeLink){
	$('body').prepend('<!-- -->\
		<nav class="navbar navbar-default">\
			<div class="container-fluid">\
				<div class="navbar-header">\
					<a class="navbar-brand" href="#">Schneider Electric</a>\
				</div>\
				<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">\
					<ul class="nav navbar-nav">\
						<li id="menu-db"><a href="/index.html">Tags<span class="sr-only">(current)</span></a></li>\
						<li id="menu-ivl"><a href="/meters.html">Meters</a></li>\
						<li id="menu-diag"><a href="/diag.html">Diagnose</a></li>\
					</ul>\
					<p class="navbar-text navbar-right">Version <span id="version"></span></p>\
					<p id="comm_failure" class="navbar-text navbar-right"></p>\
				</div>\
			</div>\
		</nav>\
	');

	$('#' + activeLink).addClass ('active');

	readVersion();
//	setInterval (readVersion, 2000);
}

function readVersion (){
	ajax_get('/info.json', true).then(function(d){
		$('#version').text (d.version.major + "." + d.version.minor + "." + d.version.patch);
		$('#comm_failure').text ('');
	}).catch(function(e){
		$('#comm_failure').text ('NO CONNECTION TO SERVER');
	});
}
