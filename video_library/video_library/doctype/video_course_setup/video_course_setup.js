// Copyright (c) 2018, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Video Course Setup', {
	refresh: function(frm) {
	var df = frappe.meta.get_docfield("User Video Course Enrolment","user", 'Video Course Setup');
	frappe.call({
		method: 'video_library.video_library.doctype.video_course_setup.video_course_setup.get_user_with_role',
		args: {
			rolename: 'Video Premium' 
		},
		callback: function (r) {
			if(r.message!=''){
				df.options = r.message;
			}
		}
	})

	}
});
