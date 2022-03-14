import frappe

@frappe.whitelist()
def sofilter(status='',customer=''):
    filters={'status':['!=',"Completed"]}
    if(customer!=""):
      filters['customer']=customer
    so=salesorder=[i.name for i in frappe.get_all("Sales Order",filters)]
    if(status!=''):
      salesorder=[]
      for sales in so:
        tag=frappe.get_value("Sales Order",sales,"_user_tags")
        if(tag!=None):
          if(status in tag.split(',')):
            salesorder.append(sales)
    return ['']+salesorder
    
    
    
@frappe.whitelist()
def setup():
  filters={'status':['!=',"Completed"]}
  return { 
  "tags":['']+[i.name for i in frappe.get_all("Tag")],
  "salesorder":['']+[i.name for i in frappe.get_all("Sales Order",filters=filters)],
  "customer":list(set(['']+[ i.customer for i in frappe.get_all("Sales Order",filters=filters,fields="customer")]))
  }
  
  
@frappe.whitelist()
def jobcarddetails(salesorder):
  if(salesorder!=''):
    work_order=[frappe.get_doc("Work Order",i) for i in frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":['!=','Cancelled'],"docstatus":1})]
    work_order_dict=[{
      'workorder':i.item_name,
      'qty':int(i.qty),
      'stock':int(i.produced_qty),
      'production':int(i.qty)-int(i.produced_qty),
      'raw_material_qty':int(i.required_items[0].required_qty),
      'raw_material':i.required_items[0].item_name }  for i in work_order]
    work_order_attr=workorderfunc(work_order_dict)
    work_order_dict=work_order_sep(work_order_attr)
    
        
    
    html=jobcardhtml(work_order_dict,salesorder,work_order_attr)
    return html if(len(work_order_dict)>0) else '<center><b> NO JOB CARDS </b></center>'
 
    
    
 
 

def work_order_sep_attr(wo, attr):
  workorder={}
  for i in wo:
    if(i[attr] in workorder):
      workorder[i[attr]].append(i)
    else:
      workorder[i[attr]]=[i]
  return workorder



def work_order_sep_attr2(wo, attr):
  workorder={}
  for i in wo:
    workorder[i]=work_order_sep_attr(wo[i],attr)
  return workorder
  


def work_order_sep_attr3(wo, attr):
  workorder={}
  for i in wo:
    if(i[attr] in workorder):
      workorder[i[attr]].append(i)
    else:
      workorder[i[attr]]=[i]
  return workorder



def work_order_sep_color(wo):
  workorder={}
  for i in wo:
    worder={}
    for j in wo[i]:
      worder[j]=work_order_sep_attr3(wo[i][j],'colour')
    workorder[i]=worder
  return workorder
  


def work_order_sep(wo):
  wo=work_order_sep_attr(wo, 'design')
  wo=work_order_sep_attr2(wo, 'raw_material')
  wo=work_order_sep_color(wo)
  return wo
  

def workorderfunc(wo):
    workorder=[]
    for i in wo:
      item=i['workorder']
      docs=frappe.get_all('Item',{'item_name':item})
      doc=frappe.get_doc('Item',docs[0].name)
      attr={}
      for j in doc.attributes:
        attr[j.attribute]=j.attribute_value
      i['size']=attr['Size']
      i['colour']=attr['Colour']
      i['design']=doc.variant_of
      workorder.append(i)
    return workorder
     
        
        
        
 

def jobcardinfohtml(salesorder):
  so=frappe.get_doc('Sales Order',salesorder)
  infohtml=f'''
    <div class='div'>
      <div class='jobcardinfo'>
        Customer Name : {so.customer}<br>
        Delivery Date : {'-'.join(str(so.delivery_date).split('-')[::-1])}<br><br>
      </div>
      <div class='jobcardinfo'>
        Job Card NO : {so.name}<br>
        PO No : {so.po_no}<br><br>
      </div>
    </div>
  '''
  return infohtml


def description(wo):
  total_papers=sum([i['raw_material_qty'] for i in wo])
  return f'''
    <div class='div'>
    Total No of Papers: {total_papers}
    </div>
  '''


def html_style():
  style='''
    <style>
      td{
        padding: 6px;
      }
      .table1{
        width:100%;
        text-align:center;
        margin-bottom: 5px;
      }
      .heading{
        font-weight: bold;
        font-size:17px;
        width: 10%;
      }
      .data{
        font-weight: 600;
        font-size:16px;
      }
      td {
        border: 1px solid black;
      }
      .jobcardinfo{
        float:left;
        width:50%;
      }
      .div{
        background-color:#33307c;
        color:white;
        font-weight:bold;
        border-radius:10px;
        height:100px;
        width:100%;
        margin-bottom:5px;
        padding:20px;
        font-size:17px;
        line-height:2;
      }
      b{
        font-size:19px;
      }
    </style>
  '''
  return style


def no_of_paper(wo):
  return f'''
      <b>
        No of Papers: {sum([i["noofpaper"] for i in wo])}
      </b>'''


def htmlfortable(color,wo):
  workorder=[{'size':i['size'],'qty':i['qty'],'stock':i['stock'],
      'production':i['production'],'noofpaper':i['raw_material_qty']} for i in wo]
  wo_list=list(zip(*[list(i.values()) for i in workorder]))
  html=f'''
    <h4>Colour : {color}<br></h4>
  '''
  trs=['<tr><td class="heading">Size</td>',
      '<tr><td class="heading">Qty</td>',
      '<tr><td class="heading">Stock</td>',
      '<tr><td class="heading">Production</td>',
      '<tr><td class="heading">No of Paper</td>'] 
  table='<table class="table1">'
  for i,j in zip(trs,wo_list):
    table+=i+''.join( [f'<td class="data">{x}</td>' for x in j] )+'</tr>'
  html+=html_style()
  html+=table+'</table>'+no_of_paper(workorder)+'<BR><br><br>'
  return html


def htmlforpaper(paper,wo):
  html=f'''
    <h3>Paper : {paper}<br></h3>
  '''
  for color in wo:
    html+=htmlfortable(color,wo[color])
  return html
  

def htmlfordesign(design,wo):
  html=f'''
    <h2>Design : {design}<br></h2>
  '''
  for paper in wo:
    html+=htmlforpaper(paper,wo[paper])
  return html


def jobcardhtml(wo,so,unsepwo):
  htmlcode=jobcardinfohtml(so)
  print('\n'*10)
  for design in wo:
    htmlcode+=htmlfordesign(design,wo[design])+'<br><br>  '
  return htmlcode+description(unsepwo)

    
    
