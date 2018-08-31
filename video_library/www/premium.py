from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.www.list

def get_context(context):
    if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    context.video_data = frappe.db.sql("""select user.user as user, user.course_name as course ,vimeo.vimeo_url as vimeo
from `tabUser Video Course Enrolment` user
inner join `tabCourses Video Links` vimeo
on user.course_name=vimeo.course_name
where user.user=%s
order by user.user, user.course_name""",frappe.session.user,as_dict=1)
    context.show_sidebar=False