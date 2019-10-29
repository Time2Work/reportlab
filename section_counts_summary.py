import pandas as pd
import csv 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from random import randint
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer


# ___________Input needed :________________________________________________________________
#                                                                                          |
input_csv_name = 'meat.bunker.csv'  #### ENTER INFO HERE (Include .csv extension) !!!!!!!  |
section = 'meat_bunker'             #### ENTER INFO HERE  (section  counted) !!!!!!!!!     |
#                                                                                          |
# _________________________________________________________________________________________|

input_folder = 'input'
output_folder = 'reports'
csv_input_path = f'{input_folder}/{input_csv_name}'
inventory_section_name = section 

# Functions to Create pdf Report to scan containing barcode, Quantity,and Price from summarized info

# barcode needs to be exactly 6 characters regardless of price.
def conv_price_to_barcode(num):
  string_price = num
  if len(string_price) == 3:
    low_random = randint(1,9)
    last_digits = '00' + str(low_random)
  elif len(string_price) == 4:
    last_digits = str(randint(10,99))
  else:
    just_random = randint(0,9)
    last_digits = str(just_random)
  code = string_price.replace('.','0') + last_digits
  return code

def single_pdf_line(retail_price,qty):
  # each line contains 4 elements. 
  price = retail_price
  qty = qty
  string_qty = str(qty)   
        
  # create barcode number. price= whole $ +  0 representing a decimal + two digit cents + random 2 digits. for a 6 digit code.
  price = float(price)
  string_price = str(price)

  code = conv_price_to_barcode(string_price)

  info = [code,string_price,string_qty]
  return info

# start the work:

# path and name of input file:  
csv_input = csv_input_path 

data = pd.read_csv(csv_input)

# ____STAGE 1_____:  Use pandas to total all counts for each price point.
# from data select all rows, col 1 (Quantity) and col 3 (PRICE)
df = data.iloc[:, [1,3]]
# group by price point with sum of all counts for that price.
report = df.groupby(['PRICE']).sum()
# save as csv to process further.
report.to_csv(f'report.csv')

total_rows = report.count()
print(total_rows)
# ____STAGE 2 ____: create "PAGE" with barcode, and Total Quantity for each price point:

# SECTION NAME FOR INVENTORY
section_name =  inventory_section_name     

doc_name = f'{output_folder}/Inventory_Report_{section_name}.pdf'
doc = SimpleDocTemplate(doc_name, pagesize=letter)

story = []

# first row of table is title of report
data = [[section_name,'','','']] # 4 columns to span the title in
tbl = Table(data) # add data to the table

# first row Span Title all the rest set Font and size
tblstyle = TableStyle([('SPAN',(0,0),(0,-1)),('FONT',(0,0),(-1,-1),'Helvetica-Bold', 18)]) 
tbl.setStyle(tblstyle)

story.append(tbl)
story.append(Spacer(0,10))

with open('report.csv') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)
    
    for row in reader:
        price = row[0]
        qty = row[1]
        # set the info into correct formats for further proccessing
        data_P_Q = single_pdf_line(price, qty)
        # get the proccessed info to use on each line of the report
        code = data_P_Q[0]
        price = data_P_Q[1]
        qty = data_P_Q[2]
        
        # create a barcode object not used until the .drawOn method is called
        # barHeight encodes the bars height.Width encodes how wide the "narrowest" barcode unit is 
        barcode=code128.Code128(code, barWidth=0.5*mm, barHeight=10*mm)
        
        data = [[code,barcode,qty,price]]
        tbl = Table(data)
        
        story.append(tbl)
        story.append(Spacer(0,5)) # add additional vertical space between rows
        
print(f'pdf file saved as {doc_name}')
doc.build(story) 
