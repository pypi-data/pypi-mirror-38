/*
	Кодировка: utf8
*/
'use strict';


$(function(){
	showNavbar ('menu-db');
});

var g_UpdateRatioMs = 500;
var g_SvcPrefix = '/'

angular.module('app', []).controller('indexController', ['$scope', indexContoller]);

var g_QualityNames = [
	 {m: 1 << 16, t: 'NotInit'}
	,{m: 1 << 17, t: 'Low'}
	,{m: 1 << 18, t: 'High'}
	,{m: 1 << 19, t: 'Comm'}
	,{m: 1 << 20, t: 'Convert'}
	,{m: 1 << 21, t: 'NA'}
	,{m: 1 << 22, t: 'NA (temp)'}
	,{m: 1 << 23, t: 'DB 00'}
	,{m: 1 << 24, t: 'DB 11'}
];

function getQualityStr(q){
	
	if ( !q )
		return '';
	
	var comments = [];
	g_QualityNames.forEach (function(x){
		if ( q & x.m )
			comments.push(x.t);
	});
	
	if ( comments.length )
		return '0x' + q.toString(16) + ' [' + comments.join(', ') + ']';
	else
		return '0x' + q.toString(16);
}

function indexContoller($scope){
	var self = $scope;
	self.$ctrl = self;
	
	self.DATA = {
		 nodes: []							// узлы в таблице (потомки текущего тега). Структуру см. ls()
		,path: [{title: 'Root', href: ''}]
		,webCtrlEnabled: false
	}
	
	self.init = async function(){
		var url = new URL(window.location);
		var cr_tag_name = url.searchParams.get("tag");
		
		// Draw path
		if ( cr_tag_name )
		{
			var prev_href = null
			cr_tag_name.split ('.').forEach(function(name){
				var href = prev_href ? prev_href + '.' + name : name 
				prev_href = href
				self.DATA.path.push ({
					href: href
				   ,title: name
			   });
		   });
		}
		self.DATA.nodes = await ls(cr_tag_name);
		var info = await ajax_get(g_SvcPrefix + 'info.json');
		self.DATA.webCtrlEnabled = info.web.ctrl;
		
		$scope.$apply ();

		self.readValues ();
	}
	self.init();
	
	self.onValueClick = async function(tag){
		var val = prompt("Value");
		if ( val ){
			var rs = await ajax_get ('/volcano/web/write.json?tag=' + tag.id + '&val=' + val);
			console.log ( "ok" );
		}
	}
	
	self.options = { month: 'short', day: 'numeric', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit'};

	self.readValues = async function(){
		
		var names = self.DATA.nodes.filter(x=>x.type!='void').map(x=>x.fullName);
		if ( names.length == 0)
			return;

		var d = await Promise.all (names.map(x=>ajax_get (g_SvcPrefix + 'read.json?tag=' + x)));

		for (var i = 0; i < d.length; i++){
			var node = d[i];
			
			var name = names[i];
			var value = node.v;
			var quality = node.q;
			var time = node.t;
			
			var src = self.DATA.nodes.find (x=>x.fullName==name);
			if ( src ){
				
				if ( value===null && (src.type=='f32' || src.type=='f64') )
					src.value = 'NaN';
				else{
					if ( src.eu )
						src.value = value + ' ' + src.eu;
					else
						src.value = value;
				}
				src.quality_int = quality;
				src.quality_str = getQualityStr(quality);
				
				// time
				if ( time===null ) { // invalid date
					src.timeStamp = 'N/A';
				} else {
					var dtm = new Date (time);  // creates date in local timezone from UTC string (string should end with Z)
					src.timeStamp = dtm.toLocaleString('ru-RU', self.options) + '.' + dtm.getMilliseconds();
				}
			}
		}

		$scope.$apply ();
	}
	setInterval (self.readValues, g_UpdateRatioMs);
}

async function ls (tag_full_name_n){
	// d: ['name', 'name', 'name']
	var d = await ajax_get ( g_SvcPrefix + (tag_full_name_n ? 'ls.json?tag=' + tag_full_name_n : 'ls.json'), true);
	var dd = await Promise.all (d.map(async function(short_name){
		var full_name = tag_full_name_n ? tag_full_name_n + '.' + short_name : short_name
		var tag = await ajax_get (g_SvcPrefix + 'stat.json?d=ntcTU&tag=' + full_name, true);

		return {
			 name: 		tag.name
			,fullName:	full_name
			,type: 		tag.type
			,hasNodes:	tag.hasChildren
			,title:		tag.title
			//,eu:		tag.eu
			//,writable:	tag.type != 'void'//!tag.private && !tag.flags.const
			
			,value:			undefined
			,quality_int:	undefined
			,quality_str:	undefined
			,timeStamp:		undefined
		};
	}));

	return dd.sort (function(a,b){
		if ( a.hasNodes == b.hasNodes ){
			if ( a.name < b.name )
				return -1;
			else 
				return 1;
		} else {
			
			if ( a.hasNodes && !b.hasNodes )
				return -1;
			else 
				return 1;
		}
	});
}
