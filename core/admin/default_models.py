from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from common.admin import BaseAdmin
# from core.models import ()

# @admin.register(Case)
# class CaseAdmin(BaseAdmin):
#     search_fields = ["name"]
#     autocomplete_fields = ["client"]
#     autocomplete_filter_fields = ["client"]
#     list_display = [
#         "name",
#         "client",
#         "created_at",
#         "updated_at",
#     ]
#     readonly_fields = ["created_at", "updated_at"]
#     list_filter = ["client"]

#     object_fieldsets = [
#         [
#             [
#                 "name",
#                 "client",
#                 "tags",
#                 "description",
#                 "additional_info",
#                 "case_summary",
#                 "assistant_status",
#                 "assistant_id"
#             ],
#             _("Case"),
#         ]
#     ]
#     safe_m2m_fields = ["tags"]


# @admin.register(Workspace)
# class WorkspaceAdmin(BaseAdmin):
#     search_fields = ["business_name", "root_user__email", "root_user__first_name", "root_user__last_name"]
#     autocomplete_fields = ["root_user", "users"]
#     autocomplete_filter_fields = ["root_user", "users"]
#     list_display = [
#         "business_name",
#         "root_user",
#         "created_at",
#         "updated_at",
#     ]
#     readonly_fields = ["created_at", "updated_at"]

#     object_fieldsets = [
#         [
#             [
#                 "business_name",
#                 "root_user",
#                 "website_url",
#                 "users",
#                 "vector_id",
#                 "assistant_id",
#             ],
#             _("Workspace"),
#         ]
#     ]
