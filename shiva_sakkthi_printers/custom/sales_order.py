import frappe
import json
from erpnext.controllers.item_variant import get_variant as gv

def abcd(self,method):
        self.submit()
        

@frappe.whitelist()
def get_attribute_value(attribute):
	d = frappe.get_all('Item Attribute Value',{"parent":attribute},['attribute_value'],pluck="attribute_value")
	return d


@frappe.whitelist()
def get_template(item):
	d = frappe.get_all('Item Variant Attribute',{"parent":item},['attribute'],pluck='attribute')
	return d

@frappe.whitelist()
def get_variant(template=None,attribute_table=None):
	attribute_table = json.loads(attribute_table)
	att_dict = {}
	for data in attribute_table:
		frappe.errprint( data.keys())
		if 'value' not in data.keys():
			var = data['attribute']
			frappe.throw(f'Enter Attribute value for {var}')
		else:
			att_dict.update({
				data['attribute']:data['value']
			})
	
	return gv(template,att_dict)
	# d = frappe.get_all('Item Variant Attribute',{"parent":item},['attribute'],pluck='attribute')
	# return d
	