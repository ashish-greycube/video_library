// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

window.get_product_list = function() {

	frappe.call({
		method: "video_library.www.video_product_search.get_video_library_contact_email",
		callback: function(r) {
			window.email_id=r.message
		}
	});

	$(".more-btn .btn").click(function() {
		if(window.stores==window.start){

		}
		else{
		window.get_product_list()
		window.stores=window.start;
		window.storel=window.limit;
		}
	});

	if(window.start==undefined) {
		throw "product list not initialized (no start)"
	}

	$.ajax({
		method: "GET",
		url: "/",
		data: {
			cmd: "video_library.www.video_product_search.get_product_list",
			start: window.start,
			limit:window.limit,
			search: window.search,
		},
		dataType: "json",
		success: function(data) {
			window.render_product_list(data.message);
		}
	})
}

window.render_product_list = function(data) {
	console.log(data)
	console.log(window.start)
	var table = $("#search-list .table");
	
	if ((data == undefined && window.start == 0) || (data.length == 0 && window.start == 0) ){
		message="<div class='alert alert-warning'>Sorry no video found for your search. Please email us at "+window.email_id+" with your requirements. Thanks!</div>"
				$(".more-btn").replaceWith(message);
				return true
	}

	if(data == undefined || data.length == 0) {
		$(".more-btn")
		.replaceWith("<div class='text-muted'>{{ _("Nothing more to show.") }}</div>");
		return
	}
	if(data.length > 0) {
		if(!table.length)
			var table = $("<table class='table'>").appendTo("#search-list");

		$.each(data, function(i, d) {
			$(d).appendTo(table);
		});
	}

	if(data.length > 0 && data.length<12) {
		if(!table) {
			$(".more-btn")
				.replaceWith("<div class='alert alert-warning'>{{ _("No products found.") }}</div>");
		} else {
			$(".more-btn")
				.replaceWith("<div class='text-muted'>{{ _("Nothing more to show.") }}</div>");
		}
	} 
	else {
		$(".more-btn").toggle(true)



	}
	window.limit  = window.start + 12;
	window.start += (data.length || 0);
	// window.start += 4;
}
