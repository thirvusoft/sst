import json
import frappe
from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_data

def validate_item_variants(document):
          item_dict={}
          items = document.items
          for item in items:
                    item_doc=frappe.get_doc('Item',item.item_code)
                    variant=item_doc.variant_of
                    item_variant=item_doc.variant_of
                    for attr in item_doc.attributes:
                              if (attr.attribute == "Colour"):
                                      variant+=' '+attr.attribute_value
                              if (attr.attribute == "Paper Quality"): 
                                       variant+=' '+attr.attribute_value                 
                    
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
                                               

                                                       
                        
                        

                                                
