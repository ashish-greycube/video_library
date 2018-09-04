// Copyright (c) 2018, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('User Course Mapping', {
	onload: function(frm) {
		var user_field = frm.get_field("user");
		frappe.call({
			method: 'video_library.video_library.doctype.user_course_mapping.user_course_mapping.get_user_with_role',
			args: {
				rolename: 'Video Premium' 
			},
			callback: function (r) {
				if(r.message!=''){
					user_field.df.options  = r.message;
					user_field.refresh();
				}
			}
		})

	}
});