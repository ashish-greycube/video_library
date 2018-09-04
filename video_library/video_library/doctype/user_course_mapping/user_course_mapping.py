# -*- coding: utf-8 -*-
# Copyright (c) 2018, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UserCourseMapping(Document):
	pass

@frappe.whitelist()
def get_user_with_role(rolename):
	user_list = frappe.db.sql("""select user.name
				from `tabUser` user
				inner join `tabHas Role` role
				on user.name=role.parent and role.role=%s and role.parenttype='User' and role.parentfield='roles' and user.frappe_userid is not null
				""",rolename,as_list=1)
	user_list = "\n".join([d[0] for d in user_list])
	return user_list