import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def customer_list_property_setter():
    make_property_setter("Customer", "customer_type", "reqd", 0, "Check")
    make_property_setter("Customer", "customer_group", "reqd", 0, "Check")
    make_property_setter("Customer", "territory", "reqd", 0, "Check")
    make_property_setter("Customer", "posa_referral_code", "allow_in_quick_entry", 0, "Check")
    make_property_setter("Customer", "posa_referral_company", "allow_in_quick_entry", 0, "Check")
    make_property_setter("Customer", "posa_referral_company", "bold", 0, "Check")
    make_property_setter("Customer", "tax_category", "allow_in_quick_entry", 0, "Check")
  