from __future__ import unicode_literals
import frappe
from frappe.sessions import Session
from frappe.utils import flt, has_common

# @frappe.whitelist()
# def get_website_user_role(username):
    
#     logged_in_user_roles=frappe.get_roles(username)
#     print logged_in_user_roles
#     premium_video_roles="Video Premium"
#     print premium_video_roles
#     if premium_video_roles in logged_in_user_roles:
#         return 'premiumuser'
#     else:
#         return 'nonpremiumuser'