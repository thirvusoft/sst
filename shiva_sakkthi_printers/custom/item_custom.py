import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def item_list_property_setter():
    make_property_setter("Item", "item_group", "reqd", 0, "Check")
    make_property_setter("Item", "stock_uom", "reqd", 0, "Check")
    make_property_setter("Item", "item_name", "allow_in_quick_entry", 1, "Check")
    make_property_setter("Item", "gst_hsn_code", "allow_in_quick_entry", 1, "Check")
    make_property_setter("Item", "variant", "allow_in_quick_entry", 1, "Check")
    make_property_setter("Item", "is_stock_item", "bold", 0, "Check")