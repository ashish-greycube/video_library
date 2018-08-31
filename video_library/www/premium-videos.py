import frappe
def get_context(context):
    context.premium-videos = frappe.db.sql("select user.user, user.course_name,vimeo.vimeo_url
from `tabUser Video Course Enrolment` user
inner join `tabCourses Video Links` vimeo
on user.course_name=vimeo.course_name
order by user.user, user.course_name")