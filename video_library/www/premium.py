from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.www.list

def get_context(context):
    if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    context.video_data = frappe.db.sql("""select user.user as user, course.video_course as course,vimeo.video_name as video,vimeo.vimeo_code as vimeo from `tabUser Course Mapping` user
inner join `tabVideo Course Detail` video
on video.parent=user.name
inner join `tabCourse Video Mapping` course
on course.video_course=video.video_course
inner join `tabVimeo Video` vimeo
on vimeo.parent=course.name
where user.user=%s order by course, video""",frappe.session.user,as_dict=1)
    context.show_sidebar=False