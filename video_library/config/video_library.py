from frappe import _

def get_data():
	return [
		{
			"label": _("Master Data"),
			"icon": "fa fa-print",
			"items": [
				{
					"type": "doctype",
					"name": "Video Category",
					"label": _("Video Category"),
					"hide_count": False
				},
                {
					"type": "doctype",
					"name": "Video Course",
					"label": _("Video Course"),
					"hide_count": False
				},
                {
					"type": "doctype",
					"name": "Video Vimeo",
					"label": _("Video Vimeo"),
					"hide_count": False
				}
			]
		},
		{
			"label": _("Mapping Data"),
			"icon": "fa fa-print",
			"items": [
				{
					"type": "doctype",
					"name": "Category Course Mapping",
					"label": _("Category Course Mapping"),
					"hide_count": False
				},
                {
					"type": "doctype",
					"name": "Course Video Mapping",
					"label": _("Course Video Mapping"),
					"hide_count": False
				}
			]
		},
        {
			"label": _("Settings"),
			"icon": "fa fa-print",
			"items": [
				{
					"type": "doctype",
					"name": "Video Library Settings",
					"label": _("Video Library Settings"),
					"hide_count": True
				},
                {
					"type": "doctype",
					"name": "Portal Settings",
					"label": _("Portal Settings"),
				},
                				{
					"type": "doctype",
					"name": "User",
					"description": _("System and Website Users")
				},
				{
					"type": "doctype",
					"name": "Role",
					"description": _("User Roles")
				}
			]
		}
    ]