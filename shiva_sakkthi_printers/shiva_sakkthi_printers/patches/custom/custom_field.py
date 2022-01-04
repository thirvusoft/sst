import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	custom_fields = {
		'Item': [
			dict(fieldname='tray_no', label='Tray No',fieldtype='Data', insert_after='item_code'),
			dict(fieldname='customer_name', label='Customer Name', fieldtype='Data', insert_after='tray_no'),
            dict(fieldname='design_upload', label='Design Upload', fieldtype='Attach Image', insert_after='customer_name'),
		]
	   
	}

	create_custom_fields(custom_fields, update=True)


	
