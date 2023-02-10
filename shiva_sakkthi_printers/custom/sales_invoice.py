import json 
import requests
import json
import frappe
from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_data
import requests
from frappe import _
import base64
import os

def validate_item_variants(document):
          item_dict={}
          items = document.items
          for item in items:
                    item_doc=frappe.get_doc('Item',item.item_code)
                    variant=item_doc.variant_of or item.item_code
                    item_variant=item_doc.variant_of or item.item_code
                    if (variant not in item_dict):
                             item_dict[variant]={'hsn':frappe.get_value('Item', item_variant, 'gst_hsn_code'),'qty':0,'rate':0,'attribute':'', 'cgst':0, 'sgst':0, 'igst':0, 'taxable_amount':0}
                    item_dict[variant]['qty']+=item.qty
                    item_dict[variant]['rate'] +=item.rate
                    item_dict[variant]['cgst'] +=item.cgst
                    item_dict[variant]['sgst'] +=item.sgst
                    item_dict[variant]['igst'] +=item.igst
                    item_dict[variant]['taxable_amount'] +=item.taxable_amount
                    
                    for attr in item_doc.attributes:
                              if (attr.attribute == "Size"):
                                        item_dict[variant]['attribute']+=attr.attribute_value+'/'+str(int(item.qty))+' '
                                        
          item_list=[]
          for value in item_dict:
                    item_list.append({
                              "items":value,
                              "variants":item_dict[value]['attribute'],
                              "hsn":item_dict[value]['hsn'],
                              "qty":item_dict[value]['qty'],
                              "rate":item_dict[value]['rate'],
                              "sgst":item_dict[value]['sgst'],
                              "cgst":item_dict[value]['cgst'],
                              "igst":item_dict[value]['igst'],
                              "taxable_amount":item_dict[value]['taxable_amount']
                    })
                
          document.update({
                    'print_items':item_list
          })
          return 0 

def tax_finder(document, event):
       
          if document:
                  if document.tax_category:
                        si_items=document.items
                        if document:   
                                itemised_tax, itemised_taxable_amount = get_itemised_tax_breakup_data(document)
                                if itemised_tax:
                                                item_name=list(itemised_tax.keys())
                                                item_tax=list(itemised_tax.values())
                                if itemised_taxable_amount:
                                                taxable_amount=list(itemised_taxable_amount.values())
                                if item_name:
                                                item_d2=[]
                                                for i in range(0,len(item_tax),1):
                                                        item_d2.append(list(item_tax[i].values()))
                                                if(document.tax_category=="In-State"):
                                                        tax_sgst=[]
                                                        tax_cgst=[]
                                                        for i in range(0,len(item_d2),1):
                                                                tax_sgst.append(item_d2[i][0]["tax_amount"])
                                                                tax_cgst.append(item_d2[i][1]["tax_amount"])
                                                        for i in range (0,len(item_name),1):
                                                                si_items[i].update({
                                                                        "taxable_amount":taxable_amount[i],
                                                                        "sgst":tax_sgst[i],
                                                                        "cgst":tax_cgst[i],
                                                                        "igst":0
                                                                    
                                                                })
                                                        document.update({
                                                                'items':si_items
                                                        })
                                                if(document.tax_category=="Out-State"):
                                                        tax_igst=[]
                                                        for i in range(0,len(item_d2),1):
                                                                tax_igst.append(item_d2[i][0]["tax_amount"])
                                                        print(document.tax_category)
                                                        print(item_d2)
                                                        print(tax_igst)
                                                        for i in range (0,len(item_name),1):
                                                                si_items[i].update({
                                                                        "taxable_amount":taxable_amount[i],
                                                                        "sgst":0,
                                                                        "cgst":0,
                                                                        "igst":tax_igst[i]

                                                                })
                                                        document.update({
                                                                'items':si_items,
                                                                
                                                        })
          validate_item_variants(document)

@frappe.whitelist()                                              
def generate_ewb(doc):
        import requests
        import json
        doc = json.loads(doc)
        url = "https://gsp.adaequare.com/test/enriched/ewb/ewayapi?action=GENEWAYBILL"
        company_address = frappe.get_doc("Address", doc.company_address)
        billing_address = frappe.get_doc("Address", doc.customer_address)
        disable_rounded = frappe.db.get_single_value("Global Defaults", "disable_rounded_total")

        payload = json.dumps({
        "supplyType": "O",
        "subSupplyType": "1",
        "subSupplyDesc": "",
        "docType": "INV",
        "docNo": doc.name,
        "docDate": frappe.utils.formatdate(doc.posting_date, "dd/mm/yyyy"),
        "fromGstin": doc.company_gstin,
        "fromTrdName": doc.company,
        "fromAddr1": company_address.address_line1,
        "fromAddr2": company_address.address_line2,
        "fromPlace": company_address.city,
        "fromPincode": 410207,
        "actFromStateCode": 27,
        "fromStateCode": 27,
        "toGstin": doc.billing_address_gstin,
        "toTrdName": doc.customer_name,
        "toAddr1": shipping_address.address_line1,
        "toAddr2": shipping_address.address_line2,
        "toPlace": shipping_address.city,
        "toPincode": 400707,
        "actToStateCode": 27,
        "toStateCode": 27,
        "transactionType": 1,
        "dispatchFromGSTIN": "",
        "dispatchFromTradeName": "Birla Carbon India Pvt Ltd-Production Unit Patalaganga",
        "shipToGSTIN": "",
        "shipToTradeName": "Eu-Retec (Pvt) Ltd",
        "otherValue": "",
        "totalValue": 999.6735,
        "cgstValue": 0,
        "sgstValue": 0,
        "igstValue": 0,
        "cessValue": 0,
        "cessNonAdvolValue": "",
        "totInvValue": doc.grand_total if disable_rounded else doc.rounded_total,
        "transporterId": "",
        "transporterName": doc.transporter_name,
        "transDocNo": doc.lr_no,
        "transMode": "1",
        "transDistance": "100",
        "transDocDate": "30/01/2023",
        "vehicleNo": "AP29TA0123",
        "vehicleType": "R",
        "itemList": [
        {
        "productName": "N375-12173",
        "productDesc": "BIRLA CARBON-N375-CARBON BLACK",
        "hsnCode": 28030010,
        "quantity": 1,
        "qtyUnit": "MTS",
        "cgstRate": 0,
        "sgstRate": 0,
        "igstRate": 0,
        "cessRate": 0,
        "cessNonAdvolValue": "",
        "taxableAmount": 999.6735
        }
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'username': '05AAACG2115R1ZN',
        'password': 'abc123@@',
        'gstin': '05AAACG2115R1ZN',
        'requestid': str(base64.b64encode(os.urandom(18))),
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJnc3AiXSwiZXhwIjoxNjc3MzgwOTQ2LCJhdXRob3JpdGllcyI6WyJST0xFX1NCX0FQSV9UQVhfQ0FMQ1VMQVRJT04iLCJST0xFX1NCX0FQSV9HU1RfQ09NTU9OIiwiUk9MRV9TQl9FX0FQSV9HU1RfUkVUVVJOUyIsIlJPTEVfU0JfQVBJX0dTVF9SRVRVUk5TIiwiUk9MRV9TQl9BUElfRVdCIiwiUk9MRV9TQl9FX0FQSV9FV0IiLCJST0xFX1NCX0VfQVBJX0dTVF9DT01NT04iLCJST0xFX1NCX0FQSV9FSSIsIlJPTEVfU0JfRV9BUElfRUkiLCJST0xFX1NCX0FQSV9HU1BfT1RIRVJTIl0sImp0aSI6IjFlZTcwY2U3LWMwYWYtNDk4Ny05ODAxLWFlN2ZhNzVhYWE2NSIsImNsaWVudF9pZCI6IkVERjZFMkExMjdFNTQyQkVBMzk3MjVCODQ1MkZEMUM0In0.PiwKlCcTvINlw120M1z09zo-D7gsCvHiDgVNuDt7eSk'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        frappe.msgprint(_(f"{response.text}"), alert=True)
       

# {"success":false,"message":"Invalid Consignee GSTIN, Invalid or Blank Supplier Ship-to State Code, Invalid or Blank Consignee Ship-to State Code, HSN code of at least one item should be of goods to generate e-Way Bill, Invalid Vehicle Number Format, Transporter document date cannot be earlier than the invoice date, Transaction type is mandatory"}

# {
# 	"supplyType": "O",
# 	"subSupplyType": "1",
# 	"subSupplyDesc": "",
# 	"docType": "INV",
# 	"docNo": "SRET-23-00001",
# 	"docDate": "30/01/2023",
# 	"fromGstin": "05AAACG2115R1ZN",
# 	"fromTrdName": "Birla Carbon India Pvt Ltd-Production Unit Patalaganga",
# 	"fromAddr1": " Village Lohop 410207 Patalganga",
# 	"fromAddr2": "410207 Patalganga",
# 	"fromPlace": "Patalganga",
# 	"fromPincode": 410207,
# 	"actFromStateCode": 27,
# 	"fromStateCode": 27,
# 	"toGstin": "URP",
# 	"toTrdName": "Eu-Retec (Pvt) Ltd",
# 	"toAddr1": "Eu-Retec (Pvt) Ltd-",
# 	"toAddr2": "",
# 	"toPlace": "Colombo",
# 	"toPincode": 400707,
# 	"actToStateCode": 27,
# 	"toStateCode": 27,
# 	"transactionType": 1,
# 	"dispatchFromGSTIN": "",
# 	"dispatchFromTradeName": "Birla Carbon India Pvt Ltd-Production Unit Patalaganga",
# 	"shipToGSTIN": "",
# 	"shipToTradeName": "Eu-Retec (Pvt) Ltd",
# 	"otherValue": "",
# 	"totalValue": 999.6735,
# 	"cgstValue": 0.0,
# 	"sgstValue": 0.0,
# 	"igstValue": 0.0,
# 	"cessValue": 0.0,
# 	"cessNonAdvolValue": "",
# 	"totInvValue": 999.6735,
# 	"transporterId": "",
# 	"transporterName": "TESTING TRAVEL",
# 	"transDocNo": "",
# 	"transMode": "1",
# 	"transDistance": "100",
# 	"transDocDate": "30/01/2023",
# 	"vehicleNo": "AP29TA0123",
# 	"vehicleType": "R",
# 	"itemList": [
# 		{
# 			"productName": "N375-12173",
# 			"productDesc": "BIRLA CARBON-N375-CARBON BLACK",
# 			"hsnCode": 28030010,
# 			"quantity": 1.0,
# 			"qtyUnit": "MTS",
# 			"cgstRate": 0.0,
# 			"sgstRate": 0.0,
# 			"igstRate": 0.0,
# 			"cessRate": 0.0,
# 			"cessNonAdvolValue": "",
# 			"taxableAmount": 999.6735
# 		}
# 	]
# }