import frappe
import math
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
    work_order=[frappe.get_doc("Work Order",wo) for wo in frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":['not in',['Cancelled','Closed','Completed']],"docstatus":1})]
    work_order_dict=[{
      'workorder':i.item_name,
      'qty':int(i.qty),
      'stock':int(i.produced_qty),
      'production':int(i.qty)-int(i.produced_qty),
      'raw_material_qty':int(i.required_items[0].required_qty),
      'raw_material':i.required_items[0].item_name,
      'bomquantity':math.ceil(( (i.qty or 0)-(i.produced_qty or 0))/((frappe.db.get_value("BOM", i.bom_no,"quantity")/((frappe.get_doc("BOM", i.bom_no)).items[0].qty or 1) or 0)))
}  for i in work_order]
    work_order_attr=workorderfunc(work_order_dict)
    work_order_dict=work_order_sep(work_order_attr)
    
        
    
    html=jobcardhtml(work_order_dict,salesorder,work_order_attr)
    
    if(len(work_order_dict)>0):
      return html
    elif(len(frappe.get_all("Work Order",filters={'sales_order':salesorder,"status":'Completed',"docstatus":1}))>0):
      return '<center><b class="bold"> All Jobs are Completed </b></center>'
    else:
      return '<center><b class="bold"> No Job Cards Found </b></center>'
 
    
    
 
 

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
     
        
        
        
 

def jobcardinfohtml(salesorder,wo):
  total_papers=sum([i['bomquantity'] for i in wo])
  total_production=sum([i['production'] for i in wo])
  so=frappe.get_doc('Sales Order',salesorder)
  infohtml=f'''
    <div class='div'>
      <div class='jobcardinfo'> 
        Customer Name : {so.customer}<br>
        Delivery Date : {'-'.join(str(so.delivery_date).split('-')[::-1])}<br>
        TOTAL PAPERS : {total_papers}<br>
        TOTAL PRODUCTION : {total_production}<br><br>
      </div>
      <div class='jobcardinfo'>
        Job Card NO : <span class="jobno">{str((so.name).split('-')[3::])[1:-1].replace("'","").replace(", ","-") }</span><br>        PO No : {so.po_no or '-'}<br><br>
      </div>
      <div class="buttondiv">
        <button class="button" onclick="finishjobs('{salesorder}')">Finish All Jobs</button>
      </div>
    </div>
    
  '''
  return infohtml


def js_script():
  script='''
  <script>
    function finishjobs(so){
      frappe.call({
        method:"shiva_sakkthi_printers.shiva_sakkthi_printers.page.manufacturing_jobcard.manufacturing_jobcard.finish_work_orders",
        args:{
              "so":so
             },
        callback: function(r){
          if(r.message==1){ 
            frappe.show_alert({message: __("Jobs are Completed Successfully"),indicator: 'green'});
          }
          else if(r.message==2){
            frappe.show_alert({message: __("Already Jobs are Completed!"),indicator: 'orange'});
          }
          else{
            frappe.show_alert({message: __("Can't Complete all jobs"),indicator: 'red'});
          }
        }
      })
    }
  </script>
  '''
  return script



@frappe.whitelist()
def finish_work_orders(so):
  doc=frappe.get_all("Work Order",{'sales_order':so})
  completed_doc=frappe.get_all("Work Order",{'sales_order':so,'status':['in',['Completed','Closed']]})
  if(len(doc)==len(completed_doc)):
    return 2
  else:
    workorder=frappe.get_all("Work Order",{'sales_order':so,'status':['not in',['Completed','Closed']]})
  for work_order in workorder:
    wo=work_order.name
    wo_doc=frappe.get_doc('Work Order',wo)
    bom_qty=math.ceil((frappe.db.get_value("BOM", {"item_name": wo_doc.item_name, 'is_default':1},"quantity") or 0))
    if(wo_doc.qty-wo_doc.material_transferred_for_manufacturing >0):
      makese('Material Transfer for Manufacture',wo_doc.name,wo_doc.production_item,wo_doc.required_items[0],bom_qty,wo_doc.bom_no,wo_doc.qty-wo_doc.material_transferred_for_manufacturing,wo_doc.source_warehouse,wo_doc.wip_warehouse,wo_doc.fg_warehouse)
    wo_doc=frappe.get_doc('Work Order',wo)
    makese('Manufacture',wo_doc.name,wo_doc.production_item,wo_doc.required_items[0],bom_qty,wo_doc.bom_no,wo_doc.material_transferred_for_manufacturing-wo_doc.produced_qty,wo_doc.source_warehouse,wo_doc.wip_warehouse,wo_doc.fg_warehouse)
  return 1



def makese(type,wo,item,bomdet,bom_qty,bom,qty,sw,ww,fw):
  doc=frappe.new_doc('Stock Entry')
  doc.update(dict(
    stock_entry_type=type,
    work_order=wo,
    from_bom=1,
    bom_no=bom,
    fg_completed_qty=qty,
  ))
  items=[dict(
      s_warehouse=sw,
      t_warehouse=ww,
      item_code=bomdet.item_code,
      qty=math.ceil(qty/bom_qty),
      uom='Nos',
  )]
  if(type=='Manufacture'):
          items=[dict(
          s_warehouse=ww,
          item_code=bomdet.item_code,
          qty=math.ceil(qty/bom_qty),
          uom='Nos',
      ),dict(
          t_warehouse=fw,
          item_code=item,
          qty=qty,
          uom='Nos',
      )        ]
  doc.set('items',items)
  doc.save()
  doc.submit()




def html_style():
  style='''
    <style>
    hr{
      border: 0.2px solid #d9d9d9;
    }
      .designdiv{
        border: 1px solid black;
        padding: 10px;
        border-radius: 5px;
        margin-top: 15px;
      }
      .buttondiv{
        float: right;
        position: relative;
      }
      .button{
        font-size: 17px;
        border-radius: 5px;
        font-weight: bold;
        padding: 5px;
        background-color: #4da6ff;
      }
      .table1{
        margin-bottom: 5px;
        margin-left: auto; 
        margin-right: auto;
      }
      .heading{
        font-weight: bold;
        font-size:17px;
        width:160px;
        background-color: #ccccff;
        padding: 6px;
        border: 1px solid black;
      }
      .data{
        font-size:18px;
        text-align:center;
        width:160px;
        padding: 6px;
        border: 1px solid black;
        font-weight:bold;
      }
      
      .jobcardinfo{
        float:left;
        width:43%;
      }
      .div{
        background-color:#33307c;
        color:white;
        font-weight:bold;
        border-radius:10px;
        height:178px;
        width:100%;
        margin-bottom:5px;
        padding:20px;
        font-size:17px;
        line-height:2;
      }
      .bold{
        font-size:25px;
      }
      .image{
        height: 150px;
        width: 150px;
        float: right;
        border: 1px solid black;
      }
      img{
        height: 150px;
        width: 150px;
        float: right;
      }
      .nop{
        text-align: center;
        background-color:#33307c;
        color:white;
        border-radius: 5px;
        width: 400px;
        font-weight: bold;
        font-size: 25px;
        position: absolute;
        left: 50%;
        transform: translate(-50%, 10%);
      }
      .jobno{
        font-size:40px;
        color:#e6b800;
      }
      
    </style>
  '''
  return style


def no_of_paper(wo):
  return f'''
      <div class='nop'>
          No of Papers : {sum([i["noofpaper"] for i in wo])}<br>
          No of Production : {sum([i["production"] for i in wo])}
      </div>'''


def htmlfortable(paper,color,wo):
  workorder=[{'size':i['size'],'qty':i['qty'],'stock':i['stock'],
      'production':i['production'],'noofpaper':i['bomquantity']} for i in wo]
  wo_list=list(zip(*[list(i.values()) for i in workorder]))
  html=f'''
    <h3>Paper : {paper}<br></h3>
    <h4>Colour : {color}<br><br><br></h4>
  '''
  trs=['<tr style="font-weight:bold;background-color: #ccccff;"><td class="heading">Size</td>',
      '<tr><td class="heading">Qty</td>',
      '<tr><td class="heading">Stock</td>',
      '<tr style="font-weight:bold;"><td class="heading">Production</td>',
      '<tr style="font-weight:bold"><td class="heading">No of Paper</td>'] 
  table='<table class="table1">'
  for i,j in zip(trs,wo_list):
    table+=i+''.join( [f'<td class="data">{x}</td>' for x in j] )+'</tr>'
  html+=html_style()
  html+=table+'</table>'+no_of_paper(workorder)+'<BR><br><br><br><hr>'
  return html


def htmlforpaper(paper,wo):
  html=''
  for color in wo:
    html+=htmlfortable(paper,color,wo[color])
  return html
  

def htmlfordesign(design,wo,count):
  url=frappe.get_value('Item',design,'image')
  html=f'''
    <div class="designdiv">
      <div class="image">
      <button id="{count}" onclick=show_img{count}({count})><img src="{url}"></img></button>
      </div>
    <h2>Design : {design}<br></h2>
    
    <script>
    function show_img{count}(count){{
      var img{count} = new frappe.ui.Dialog({{
      title: '<b>{design}</b>',
      size: 'large',
      fields: [
        {{fieldname:'image',label:'Image',fieldtype:'HTML',options:'<img alt="Image not found." style="height:100%;width:100%;" src="{url}"></img>'}}
      ]
      
      }})
      img{count}.show()
    }}
    </script>
    '''
  
  for paper in wo:
    html+=htmlforpaper(paper,wo[paper])
  return html+'</div>'


def jobcardhtml(wo,so,unsepwo):
  htmlcode=jobcardinfohtml(so,unsepwo) + js_script()
  count=1
  for design in wo:
    htmlcode+=htmlfordesign(design,wo[design],count)+'<br><br>  '
    count+=1
  return htmlcode

    
    
