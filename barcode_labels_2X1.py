# build pdf labels size 2'X1' using reportlab. 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from reportlab.graphics.barcode import code128

# the label contains 4 elements. The barcode is generated from the item_number
item_number = '990089'
item_name = 'ZEBRA 2X1 test'
case_qty = '4'

# path to folder where the label pdf's are saved
save_to_folder = 'labels_supply'
# prefix added to label name for quick identification. item_name is added to the end of the prefix for the full pdf name.
label_name_prefix = 'barcode_supply'

# label size variable which is equiveolent to 2" X 1" used in the next step creating canvas (pagesize=mall_label).  
small_label = (50.0*mm, 25.4*mm)

# generate a canvas size to small label
c=canvas.Canvas(f"{save_to_folder}/{label_name_prefix} {item_name}.pdf", pagesize=small_label)
# create a barcode object not used until the .drawOn method is called
# barHeight encodes the bars height. 
# barWidth encodes how wide the "narrowest" barcode unit is
barcode=code128.Code128(item_number, barWidth=0.4*mm, barHeight=10*mm)

#item_code_number drawString puts the string on the canvas at the specified coordinates
c.drawString(20,50,item_number)

#case_qty drawString puts the string on the canvas at the specified coordinates
c.drawString(120,50,case_qty)

#item_barcode drawOn puts the barcode on the canvas at the specified coordinates
barcode.drawOn(c,0*mm,6*mm)

#item_name drawString puts the string on the canvas at the specified coordinates
c.drawString(10,2,item_name)

# now create the actual PDF, must save page before starting another page. no settings are saved between pages
c.showPage()
c.save()
