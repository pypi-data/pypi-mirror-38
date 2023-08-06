/*
	Кодировка: Utf-8
	
	Перевод.
	
	В браузере:

		<script src=".../the_time.js></script>
		<script>
			the_time.lang = {НОВЫЙ СЛОВАРЬ};
		</script>
		
	Npm:
		const the_time = require("ops-time");
		the_time.lang = {НОВЫЙ СЛОВАРЬ};
*/
!function(ns)
{
	ns.lang = {
		 "the-time:period-short-name:s":	"Сек"
		,"the-time:period-short-name:m":	"Мин"
		,"the-time:period-short-name:h":	"Час"
		,"the-time:period-short-name:D":	"Ден"
		,"the-time:period-short-name:W":	"Нед"
		,"the-time:period-short-name:M":	"Мес"
		,"the-time:period-short-name:Y":	"Год"
		,"the-time:month-short:jan": 		"Янв"
		,"the-time:month-short:feb": 		"Фев"
		,"the-time:month-short:mar": 		"Мар"
		,"the-time:month-short:apr": 		"Апр"
		,"the-time:month-short:may": 		"Май"
		,"the-time:month-short:jun": 		"Июн"
		,"the-time:month-short:jul": 		"Июл"
		,"the-time:month-short:aug": 		"Авг"
		,"the-time:month-short:sep": 		"Сен"
		,"the-time:month-short:oct": 		"Окт"
		,"the-time:month-short:nov": 		"Ноя"
		,"the-time:month-short:dec": 		"Дек"
		
		,"the-time:dow-short:mon": 			"пн"
		,"the-time:dow-short:tue": 			"вт"
		,"the-time:dow-short:wed": 			"ср"
		,"the-time:dow-short:thu": 			"чт"
		,"the-time:dow-short:fri": 			"пт"
		,"the-time:dow-short:sat": 			"сб"
		,"the-time:dow-short:sun": 			"вс"
	}



	
	// this list is always sorted from less to greater. You can use .indexOf() function to compare ivl types
	ns.ivl_list = ['s', 'm', 'h', 'D', 'W', 'M', 'Y'];

	/*
		ivl_type: 	предназначен для тех случаев, когда хочется более ясно описать тип интервала, не используя 
					односимвольное определение, например:
				
		switch ( xxx )
		{
			case the_time.ivl_type.Minutes:		...
			case the_time.ivl_type.Hours:		...
			...
		}
	*/
	ns.ivl_type = {
		 Seconds: 	's'
		,Minutes: 	'm'
		,Hours: 	'h'
		,Days:		'D'
		,Weeks:		'W'
		,Months:	'M'
		,Years:		'Y'
	}
	
	ns.ivl_info_map = {
		 's': {short_name: ns.lang["the-time:period-short-name:s"]}
		,'m': {short_name: ns.lang["the-time:period-short-name:m"]}
		,'h': {short_name: ns.lang["the-time:period-short-name:h"]}
		,'D': {short_name: ns.lang["the-time:period-short-name:D"]}
		,'W': {short_name: ns.lang["the-time:period-short-name:W"]}
		,'M': {short_name: ns.lang["the-time:period-short-name:M"]}
		,'Y': {short_name: ns.lang["the-time:period-short-name:Y"]}
	}
	
	function ivl_def (nb, type){
		this.nb = parseInt(nb);
		this.type = type;
		
		if ( isNaN(this.nb) )
			throw new Error ("Invalid time interval definition '" + nb + "'");
		
		if ( !ns.ivl_info_map[ type ] )
			throw new Error ("Invalid time interval definition '" + type + "'");
	}
	
	ns.createIvlDef = function (nb, type){
		return new ivl_def(nb, type);
	}
	
	ns.ivl_1s = ns.createIvlDef (1, 's');
	ns.ivl_1m = ns.createIvlDef (1, 'm');
	ns.ivl_1h = ns.createIvlDef (1, 'h');
	ns.ivl_1D = ns.createIvlDef (1, 'D');
	ns.ivl_1W = ns.createIvlDef (1, 'W');
	ns.ivl_1M = ns.createIvlDef (1, 'M');
	ns.ivl_1Y = ns.createIvlDef (1, 'Y');
	
	ivl_def.prototype.toString = function (){
		return "" + this.nb + this.type;
	}
	
	ivl_def.prototype.normalized = function (){
		return new ivl_def(1, this.type);
	}
	
	ivl_def.prototype.getDefaultSubIvlNull = function ()	{
		if ( this.nb > 1 )
			return this.normalized ();
		
		switch ( this.type )
		{
			case 's':	return null;
			case 'm':	return new ivl_def (1, 's');
			case 'h':	return new ivl_def (1, 'm');
			case 'D':	return new ivl_def (1, 'h');
			case 'W':	return new ivl_def (1, 'D');
			case 'M':	return new ivl_def (1, 'D');
			case 'Y':	return new ivl_def (1, 'M');
			default:	throw new Error (this.toString());
		}
	}
	
	ivl_def.prototype.addTo = function (dtm, nb_times){
		if ( nb_times === undefined )
			nb_times = 1;
		
		var d = new Date(dtm.valueOf());   // can use cloneDate from lib, but dont want to include lib in sake of single fn
		var n = this.nb * nb_times;
		
		switch ( this.type )
		{
			case 's': d.setSeconds	(d.getSeconds() + n);	break;
			case 'm': d.setMinutes	(d.getMinutes() + n);	break;
			case 'h': d.setHours	(d.getHours() 	+ n);	break;
			case 'D': d.setDate		(d.getDate() 	+ n);	break;
			case 'W': d.setDate		(d.getDate() 	+ 7 * n);	break;
			case 'M': d.setMonth	(d.getMonth() 	+ n);	break;
			case 'Y': d.setFullYear	(d.getFullYear()+ n);	break;
			default:	throw new Error ();
		}
		return d;
	}
	
	ivl_def.prototype.subtractFrom = function (dtm, nb_times){
		if ( nb_times === undefined )
			nb_times = 1;
		return this.addTo (dtm, -nb_times);
	}
	
	ns.parseIvlDef = function (s){
		if ( !s || s.length < 2 )
			throw new Error ("Invalid string: "+s);
		
		var nb = s.substr(0, s.length - 1);
		var t = s[s.length - 1];
		
		return new ivl_def (nb, t);
	}
	
	// align_dir:	
	//		forward
	//		backward
	//		test		- returns [d] itself (aligned) if align is possible, otherwise null
	ivl_def.prototype.tryAlignNull = function (d, align_dir){
		var Y = d.getFullYear();
		var M = d.getMonth();
		var D = d.getDate();
		var h = d.getHours();
		var m = d.getMinutes();
		var s = d.getSeconds();

		var nb = this.nb;
		
		switch ( this.type )
		{
			case 's':	
			{
				if ( nb >= 60 || (60 % nb) != 0 )
					return null;
				
				if ( align_dir === "test" )
					return d;
				
				var x = s - (s % nb);

				var d2 = new Date(Y, M, D, h, m, x);
			
				if ( align_dir === "forward" && d != d2 )
					d2.setSeconds (x + nb);

				return d2;
			}
			case 'm':	
			{
				if ( nb >= 60 || (60 % nb) != 0 )
					return null;
				
				if ( align_dir === "test" )
					return d;
				
				var x = m - (m % nb);

				var d2 = new Date(Y, M, D, h, x);
			
				if ( align_dir === "forward" && d != d2 )
					d2.setMinutes (x + nb);

				return d2;
			}
			case 'h':
			{
				if ( nb >= 24 || (24 % nb) != 0 )
					return null;
				
				if ( align_dir === "test" )
					return d;
				
				var x = h - (h % nb);

				var d2 = new Date(Y, M, D, x);
			
				if ( align_dir === "forward" && d != d2 )
					d2.setHours (x + nb);

				return d2;
			}
			case 'D':
			{
				if ( nb != 1 )		// двудневный интервал уже непонятно к чему приводить.. В разные месяцы он будет попадать то на четные, то на нечетные числа
					return null;
				
				if ( align_dir === "test" )
					return d;
				
				var d2 = new Date(Y, M, D);

				if ( align_dir === "forward" && d != d2 )
					d2.setDate (D + nb);

				return d2;
			}
			case 'W':	
			{
				if ( nb != 1 )		// двухнедельный интервал уже непонятно к чему приводить..
					return null;
				
				if ( align_dir === "test" )
					return d;

				var d2 = new Date(Y, M, D);

				var dow = d2.getDay()
		
				if ( dow != 1 )	// 0 (Sunday) and 6 (Saturday)
				{
					var nb_days_to_subtract = dow == 0 ? 6 : (dow-1)

					d2.setDate (D - nb_days_to_subtract);
				}
				
				if ( align_dir === "forward" && d != d2 )
					d2.setDate (d2.getDate() + 7);

				return d2;
			}
			case 'M':	
			{
				if ( nb >= 12 || (12 % nb) != 0 )
					return null;
				
				if ( align_dir === "test" )
					return d;
				
				var x = M - (M % nb);

				var d2 = new Date(Y, M, 1);
			
				if ( align_dir === "forward" && d != d2 )
					d2.setMonth (x + nb);

				return d2;
			}
			case 'Y':
			{
				if ( nb != 1 )
					return null;
				
				if ( align_dir === "test" )
					return d;
				
				var d2 = new Date(Y, 0, 1);
			
				if ( align_dir === "forward" && d != d2 )
					d2.setFullYear (Y + nb);

				return d2;
			}
			default: throw new Error();
		}	
	}
	
	ns.cloneDate = function ( d ){
		return new Date(d.valueOf());
	}

	ns.now = function (){
		return new Date(Date.now());
	}
	
	ns.parseDate = function (s){
		if ( !s )
		{
			var msg = "parseDate(): value is null";
			console.warn (msg);
			throw new Error (msg);
		}

		if ( s instanceof Date )
			return s;
		
		if ( typeof(s) === "number" )	// consider it as valueOf()
			return new Date (s);

		// parseInt will try to parse prefix of string, so "2017-04-03" => 2017. Thats why I use nb == v instead of isNaN()
		var num = parseInt(s);	// maybe it is "13123123"?
		if ( num == s  )			// it is Date().valueOf
			return new Date (num);
		
		if ( typeof(s) === "string" )	
		{
			var a = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}(?:\.\d*)?)Z$/.exec(s); // ISO
			if ( a ) 
				return new Date(Date.UTC(+a[1], +a[2] - 1, +a[3], +a[4], +a[5], +a[6]));
			else
				return new Date (s);
		}
		else
		{
			var msg = "parseDate(): cannot convert value to Date()";
			console.error (msg, "value=", s);
			throw new Error (msg);
		}
	}
	
	ns.serializeDate = function (d){
		return d.toISOString ();
	}
	/*
		Возвращает дату в формате UTC. Если переданная дата - local, то преобразует ее в UTC.
		timeZone:	"local" / "UTC"
		rval: 2010-07-30T15:05:00.000Z
	*/
	ns.dateToUtcString = function (d, timeZone){
		if ( timeZone!=="local" && timeZone!=="UTC" )
			throw new Error ("dateToUtcString(): invalid parameter timeZone='"+timeZone+"'. Valid values: 'local', 'UTC'");

		return timeZone==="local" ? this.localToUtc(d).toISOString () : d.toISOString ();
	}
	
	ns.localToUtc = function (d){
		return new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(),  d.getUTCHours(), d.getUTCMinutes(), d.getUTCSeconds(), d.getUTCMilliseconds ());	
	}
	
	ns.getComponents = function ( d ){
		return {
			year:	d.getFullYear()
			,month:	d.getMonth() + 1
			,day:	d.getDate ()
			,hour:	d.getHours()
			,minute:d.getMinutes()
			,second:d.getSeconds()
			,ms:	d.getMilliseconds()
		}
	}

	ns.getUTCComponents = function ( d ){
		return {
			year:	d.getUTCFullYear()
			,month:	d.getUTCMonth() + 1
			,day:	d.getUTCDate ()
			,hour:	d.getUTCHours()
			,minute:d.getUTCMinutes()
			,second:d.getUTCSeconds()
			,ms:	d.getUTCMilliseconds()
		}
	}	

	ns.ShortMonthNames = {};
	ns.ShortMonthNames[1] = ns.lang["the-time:month-short:jan"];
	ns.ShortMonthNames[2] = ns.lang["the-time:month-short:feb"];
	ns.ShortMonthNames[3] = ns.lang["the-time:month-short:mar"];
	ns.ShortMonthNames[4] = ns.lang["the-time:month-short:apr"];
	ns.ShortMonthNames[5] = ns.lang["the-time:month-short:may"];
	ns.ShortMonthNames[6] = ns.lang["the-time:month-short:jun"];
	ns.ShortMonthNames[7] = ns.lang["the-time:month-short:jul"];
	ns.ShortMonthNames[8] = ns.lang["the-time:month-short:aug"];
	ns.ShortMonthNames[9] = ns.lang["the-time:month-short:sep"];
	ns.ShortMonthNames[10] = ns.lang["the-time:month-short:oct"];
	ns.ShortMonthNames[11] = ns.lang["the-time:month-short:nov"];
	ns.ShortMonthNames[12] = ns.lang["the-time:month-short:dec"];

	ns.ShortWeekDayNames = {};
	ns.ShortWeekDayNames[1] = ns.lang["the-time:dow-short:mon"];
	ns.ShortWeekDayNames[2] = ns.lang["the-time:dow-short:tue"];
	ns.ShortWeekDayNames[3] = ns.lang["the-time:dow-short:wed"];
	ns.ShortWeekDayNames[4] = ns.lang["the-time:dow-short:thu"];
	ns.ShortWeekDayNames[5] = ns.lang["the-time:dow-short:fri"];
	ns.ShortWeekDayNames[6] = ns.lang["the-time:dow-short:sat"];
	ns.ShortWeekDayNames[7] = ns.lang["the-time:dow-short:sun"];
	//	like .net
	// 	yyyy	=>	2016
	//	MMM		=>	янв
	//	MM		=>	01
	//	HH		=>	01
	//	mm		=>	01
	//	ss		=>	01
	//	d		=>	1
	//	dd		=>	01
	//	ddd		=>	пн
	ns.formatDateTime = function (d, format)
	{
		function starts (str, substr)
		{
			return str.substr(0, substr.length) === substr;
		}

		var rs = "";
		
		var Y 	= d.getFullYear();
		var M1 	= d.getMonth() + 1;
		var D 	= d.getDate();
		var h 	= d.getHours();
		var m 	= d.getMinutes();
		var s 	= d.getSeconds();
		
		while ( format )
		{
			if ( starts(format, "yyyy") )
			{
				rs += Y;
				format = format.substr (4);
			}
			else if ( starts(format, "MMM") )
			{
				rs += ns.ShortMonthNames [M1];
				format = format.substr (3);
			}
			else if ( starts(format, "ddd") )
			{
				rs += ns.ShortWeekDayNames [M1];
				format = format.substr (3);
			}
			else if ( starts(format, "yy") )
			{
				var y = Y - 2000;
				rs += y < 10 ? "0"+y : y
				format = format.substr (2);
			}
			else if ( starts(format, "MM") )
			{
				rs += M1 < 10 ? "0"+M1: M1;
				format = format.substr (2);
			}
			else if ( starts(format, "dd") )
			{
				rs += D < 10 ? "0"+D : D;
				format = format.substr (2);
			}
			else if ( starts(format, "HH") )
			{
				rs += h < 10 ? "0"+h : h;
				format = format.substr (2);
			}
			else if ( starts(format, "mm") )
			{
				rs += m < 10 ? "0"+m : m;
				format = format.substr (2);
			}
			else if ( starts(format, "ss") )
			{
				rs += s < 10 ? "0"+s : s;
				format = format.substr (2);
			}
			else if ( starts(format, "d") )
			{
				rs += D;
				format = format.substr (1);
			}
			else
			{
				rs += format[0];
				format = format.substr (1);
			}
		}
		
		return rs;
	}
	
	/*
	*/
	ns.clonePeriodDef = function (pd)
	{
		var rs = {};
		for (var k in pd)
			rs[k] = pd[k];
		return rs;
	}
	/*
		p:
			variant 1:
				start	- any type valid for parseDate()
				end		- any type valid for parseDate()
				[sub_ivl] - string / ivl_def
				[last]	"strict", "less_or_equal", "greater_or_equal"
				
			variant 2:	"5 дней назад от указанной точки"
				setpt	- any type valid for parseDate() | "now"
				[setpt_offset] - "7D"
				[setpt_offset_dir] - "past" / "future". Default - "past"
				
				[dir]	- "past" / "future". Default - "past"
				all_ivl - string / ivl_def 
				[sub_ivl] - string / ivl_def / null for automatic dividing
				use_only_finished - bool
				
				[offset]		-	string / ivl_def	Позволяет сместить результат от указанной точки
				[offset_dir]	-	"past" / "future". Default - "past"
				
		rval:{
			[sub_ivl]:		ivl_def
			all_dates_list:	[]			// includes start, end. Length >= 2
		}
	*/
	ns.getDates = function ( p )
	{
		if ( p.setpt )
		{
			var setpt;
			if 	( p.setpt==="now" )		
				setpt = ns.now();
			else 
				setpt = ns.parseDate (p.setpt);
			
			if ( p.setpt_offset ){
				var offs = typeof(p.setpt_offset)==="string" ? this.parseIvlDef(p.setpt_offset) : p.setpt_offset;
				
				if ( !p.setpt_offset_dir || p.setpt_offset_dir==="past" )
					setpt = offs.subtractFrom (setpt);
				else if ( p.setpt_offset_dir==="future" )
					setpt = offs.addTo (setpt);
				else
					throw new Error ("Invalid setpt_offset_dir: " + p.setpt_offset_dir);
			}
			
			var dir;
			if 		( p.dir==="past" || !p.dir ) 	dir = "past";
			else if ( p.dir==="future" ) 			dir = "future";
			else 
				throw new Error ("Unknown value: "+ p.dir);
			
			var all_ivl = typeof(p.all_ivl)==="string" ? ns.parseIvlDef(p.all_ivl) : p.all_ivl;

			var align_dir = p.use_only_finished ? "backward" : "forward";

			var alignedEnd = all_ivl.tryAlignNull (setpt, align_dir);
			// Во многих случаях базовый интервал не может быть выровнен, потому что выравниванию подлежат в основном канонические
			// интервалы. при этом установка базового интервала, например, 2 недели ничего криминального в себе не несет.
			// В таких ситуациях мы для выравнивания используем соответствующий единичный интервал.
			if ( !alignedEnd )
			{
				alignedEnd = all_ivl.normalized().tryAlignNull (setpt, align_dir);

				if ( !alignedEnd )
				{
					console.warn ("Cant align report period", setpt, p);
					throw new Error ("Cant align report period");
				}
			}
			
			if ( p.offset )
			{
				var offset_ivl = typeof(p.offset)==="string" ? ns.parseIvlDef(p.offset) : p.offset;
				
				if ( p.offset_dir==="past" || !p.offset_dir )
					alignedEnd = offset_ivl.subtractFrom (alignedEnd);
				else if ( p.offset_dir==="future" )
					alignedEnd = offset_ivl.addTo (alignedEnd);
				else
					throw new Error ("Offset dir is invalid: " + p.offset_dir);
			}
			
			p = {
				start: 		all_ivl.subtractFrom (alignedEnd)
				,end:		alignedEnd
				,sub_ivl:	p.sub_ivl
			}
			// just proceed to next if-block
		}

		if ( p.start ) // no ELSE! this can contnue from prev "if"
		{
			var s = ns.parseDate(p.start);
			var e = ns.parseDate(p.end);
			
			if ( e <= s )
				throw new Error ("e <= s");
			
			
			if ( p.sub_ivl )
			{
				var rs = {
					all_dates_list:[]
					,sub_ivl: typeof(p.sub_ivl)==="string" ? ns.parseIvlDef(p.sub_ivl) : p.sub_ivl
				}
				
				var	d = s;
				
				// in jscript you can compare a<b, a>b, but == gives always false (compares references??)
				while ( d.valueOf() <= e.valueOf() )
				{
					rs.all_dates_list.push (d);

					if ( d.valueOf() < e.valueOf() )
						d = rs.sub_ivl.addTo (d);
					else
						break;
				}
				
				var eq = d.valueOf() == e.valueOf();

				if ( p.last === "strict" )
				{
					if ( !eq )
						throw new Error ("Невозможно создать массив дат: дата окончания не совпала с границей интервала");
				}
				else if ( p.last === "less_or_equal" )
				{
				}
				else if ( p.last === "greater_or_equal" || !p.last )
				{
					if ( !eq )
						rs.all_dates_list.push (d);
				}
				else
					throw new Error ("Invalid options");
			}
			else
			{
				return {
					all_dates_list: [s, e]
				}
			}
		}
		else
		{
			console.error (p);
			throw new Error ("Invalid period setup options");
		}
		
		return rs;
	}
	
} ( typeof(__dirname) !== "undefined" ? module.exports : (window.the_time = {}))
