# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, nowdate, cint
from video_library.video_library.doctype.video_category.video_category import get_item_for_list_in_html

no_cache = 1
no_sitemap = 1

def get_context(context):
    context.show_search = True
    context.cache=False


@frappe.whitelist(allow_guest=True)
def get_video_library_contact_email():
    return cstr(frappe.db.get_single_value('Video Library Settings', 'video_library_contact_email')) 

@frappe.whitelist(allow_guest=True)
def get_product_list(search=None, start=0, limit=12):
    # base query
    course_sort_order=None
    course_sort_order=cstr(frappe.db.get_single_value('Video Library Settings', 'course_sorting_by')) or 'Most Recent First'
    video_sort_order=cstr(frappe.db.get_single_value('Video Library Settings', 'video_sorting_by')) or 'Most Recent First'
    logged_in_user_roles_search=cstr("'"+"','".join(frappe.get_roles(frappe.session.user))+"'").replace('"','')
    query = """select VC.name as course, VV.video_caption as video,VV.vimeo_code as vimeo
from `tabVideo Category` CAT
inner join `tabCategory Course Mapping` CCM
on CAT.name=CCM.name
inner join `tabCategory Course Detail` CCD
on CCM.name=CCD.parent
inner join `tabVideo Course` VC
on CCD.course=VC.name
inner join `tabCourse Video Mapping` CVM
on VC.name=CVM.name
inner join `tabCourse Video Detail` CVD
on CVM.name=CVD.parent
inner join `tabVideo Vimeo` VV
on CVD.video=VV.name
where CONCAT('/',CAT.route) IN (
select distinct(route) from `tabPortal Menu Item`
where parentfield='custom_menu'
and reference_doctype='Video Category'
and role IN (%s))"""%(logged_in_user_roles_search)
    # search term condition
    if search:
        query += """ and (VV.video_name like %(search)s
                or  VC.course_name like %(search)s
                or VV.description like %(search)s
                or VV.keyword_fields like %(search)s
                or VV._user_tags like %(search)s
                )"""
        search = "%" + cstr(search) + "%"

    # order by
    if course_sort_order == 'Most Recent First':
        course_sort_order = 'CCD.idx desc'
    elif course_sort_order == 'Alphabetical':
        course_sort_order = 'CCD.course asc'
    elif course_sort_order == 'WYSIWYG':
        course_sort_order = 'CCD.idx asc'
    if video_sort_order == 'Most Recent First':
        video_sort_order = ' , CVD.idx desc'
    elif video_sort_order == 'Alphabetical':
        video_sort_order = ', CVD.caption asc'
    elif video_sort_order == 'WYSIWYG':
        video_sort_order = ', CVD.idx asc'

    query += """ order by %s %s limit %s, %s""" % (course_sort_order,video_sort_order,cint(start), cint(limit))
    data = frappe.db.sql(query, {
        "search": search		
    }, as_dict=1)
    return [get_item_for_list_in_html(r) for r in data or {}]