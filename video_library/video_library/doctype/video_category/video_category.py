# -*- coding: utf-8 -*-
# Copyright (c) 2019, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import nowdate, cint, cstr
from frappe.sessions import Session
from frappe.utils import flt, has_common

class VideoCategory(WebsiteGenerator):
    website = frappe._dict(
        template = "video_library/templates/generators/video_category.html",
        condition_field = "is_published",
        page_title_field = "category_name",)

    def validate(self):
		self.make_route()

    def make_route(self):
		'''Make website route'''
		if not self.route:
			self.route = ''
			self.route += self.scrub(self.name)
			return self.route

    def get_context(self, context):
		# webpage settings
		context._login_required = True
		context.allow_guest = False
		if frappe.session.user == "Guest":
			context._login_required = True
			frappe.throw(_("You don't have the permissions to access this document"), frappe.PermissionError)
		else:
			if (check_access(self.name)==None):
				context._login_required = True
				frappe.throw(_("You don't have the permissions to access this document"), frappe.PermissionError)			
		context.no_cache = 1
		context.search_link = '/video_product_search'
		context.show_search=True
		context.show_sidebar=False

		# get video settings
		context.page_length = cint(cint(frappe.db.get_single_value('Video Library Settings', 'video_per_page'))) or 7
		context.no_of_featured_videos=cint(frappe.db.get_single_value('Video Library Settings', 'no_of_featured_videos')) or 4
		context.course_sort_order=cstr(frappe.db.get_single_value('Video Library Settings', 'course_sorting_by')) or 'Most Recent First'
		context.video_sort_order=cstr(frappe.db.get_single_value('Video Library Settings', 'video_sorting_by')) or 'Most Recent First'

		#pagination
		start = int(frappe.form_dict.start or 0)
		if start < 0:
			start = 0
		context.update({
			"featured_video_data":get_featured_video_list(category= self.name, start=0,limit=context.no_of_featured_videos),
			"video_data": get_video_list_for_category(category= self.name, start=start,
				limit=start+context.page_length, search=None,course_sort_order=context.course_sort_order,video_sort_order=context.video_sort_order),
			"parents": [{'name': 'video', 'title': _('My Account'),'route': 'me' }],
			"title": self.category_name,
		})	
		trailing_count=get_video_list_for_category(category= self.name, start=0,
				limit=start+context.page_length, search=None,course_sort_order=context.course_sort_order,video_sort_order=context.video_sort_order)
		print 'lentrailing_count'
		print start
		print start+context.page_length
		print len(trailing_count)
		print '---------'
		for v in trailing_count:
			print v.video
			print len(trailing_count)
		print '---------'
		total_video_count=cint(get_total_video_count(category=self.name))
		context.total_video_count=total_video_count
		current_trailing_count=cint(len(trailing_count))
		if total_video_count==current_trailing_count:
			show_next=0
		else:
			show_next=1
		context.update({
			"show_next":show_next
		})
		print get_total_video_count(category=self.name)
		return context

    def get_list_context(self,context):
		context.title = self.category_name

@frappe.whitelist(allow_guest=True)
def check_access(category):
	logged_in_user_roles_search=cstr("'"+"','".join(frappe.get_roles(frappe.session.user))+"'").replace('"','')
	query = """select distinct(CAT.name)
from `tabVideo Category` CAT
inner join `tabPortal Menu Item` PMT
on CONCAT('/',CAT.route) = PMT.route
where PMT.role IN (%s) """%(logged_in_user_roles_search)
	query += """ and CAT.name ='%s'""" % (category)
	data = frappe.db.sql(query, as_list=1)
	return data[0][0] if data else None



@frappe.whitelist(allow_guest=True)
def get_video_list_for_category(category=None, start=0, limit=2, search=None,course_sort_order='Most Recent First',video_sort_order='Most Recent First'):
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

	# base query
	query = """select VC.name as course, VV.video_caption as video,VV.vimeo_code as vimeo
from `tabVideo Category` CAT
inner join `tabCategory Course Mapping` CCM
on CAT.name=CCM.name
inner join (select parent,course,idx from `tabCategory Course Detail` CCD where CCD.parent='%s' order by %s limit %s,%s) CCD
on CCM.name=CCD.parent
inner join `tabVideo Course` VC
on CCD.course=VC.name
inner join `tabCourse Video Mapping` CVM
on VC.name=CVM.name
inner join `tabCourse Video Detail` CVD
on CVM.name=CVD.parent
inner join `tabVideo Vimeo` VV
on CVD.video=VV.name
where CAT.name='%s'
order by %s %s """% (cstr(category),course_sort_order,cint(start),cint(limit),cstr(category),course_sort_order,video_sort_order)
	print query
	print (course_sort_order,cint(start),cint(limit),cstr(category),course_sort_order,video_sort_order)
	data = frappe.db.sql(query,as_dict=1)
	print 'data---------------'
	print data
	return data

def get_item_for_list_in_html(context):
	products_template = "video_library/templates/includes/video_products_as_list.html"
	print context
	return frappe.get_template(products_template).render(context)

@frappe.whitelist(allow_guest=True)
def get_total_video_count(category=None):
	return frappe.db.sql("""select count(*) from `tabCategory Course Mapping` CCM
inner join `tabCategory Course Detail` CCD
on CCM.name=CCD.parent
inner join `tabCourse Video Mapping` CVM
on  CCD.course=CVM.name
inner join `tabCourse Video Detail` CVD
on CVM.name=CVD.parent
where CCM.name=%s""",category,as_list=1)[0][0]

@frappe.whitelist(allow_guest=True)
def get_featured_video_list(category=None, start=0, limit=4):
	# base query
	query = """select VC.name as course, VV.video_caption as video,VV.vimeo_code as vimeo
from `tabCategory Course Mapping` CCM
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
where CCM.name=%(category)s
			"""
	# order by
	query += """ and VV.is_featured=1 order by VV.modified desc limit %s, %s""" % (cint(start), cint(limit))

	data = frappe.db.sql(query, {
		"category": category
	}, as_dict=1)
	print query
	print 'get_featured_video_list---------------'
	print data
	return data


@frappe.whitelist(allow_guest=True)
def get_video_list_for_category_1(category=None, start=0, limit=2, search=None,course_sort_order='Most Recent First',video_sort_order='Most Recent First'):
	# base query
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
where CAT.name=%(category)s
			"""
	# search term condition
	if search:
		query += """ and (vimeo.video_name like %(search)s
				or  course.video_course like %(search)s
				)"""
		search = "%" + cstr(search) + "%"

	# order by
	if course_sort_order == 'Most Recent First':
		course_sort_order = 'VC.modified desc'
	elif course_sort_order == 'Earliest First':
		course_sort_order = 'VC.modified asc'
	elif course_sort_order == 'Alphabetical':
		course_sort_order = 'VC.name asc'
	elif course_sort_order == 'WYSIWYG':
		course_sort_order = 'CCD.idx asc'

	if video_sort_order == 'Most Recent First':
		video_sort_order = ' , CVD.idx desc'
	elif video_sort_order == 'Alphabetical':
		video_sort_order = ', CVD.caption asc'
	elif video_sort_order == 'WYSIWYG':
		video_sort_order = ', CVD.idx asc'



	query += """ order by %s %s limit %s, %s""" % (course_sort_order,video_sort_order,cint(start), cint(limit))
	print query
	data = frappe.db.sql(query, {
		"search": search,
		"category": category
	}, as_dict=1)
	print 'data---------------'
	print data
	return data
	#return [get_item_for_list_in_html(r) for r in data]

# def get_item_for_list_in_html(context):
# 	products_template = 'video_library/templates/includes/video_products_as_grid.html'
# 	return frappe.get_template(products_template).render(context)