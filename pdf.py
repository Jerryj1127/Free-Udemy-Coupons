#!/usr/bin/env python3
import os
from reportlab.platypus import Paragraph, Spacer, Table,TableStyle,Image,PageBreak,SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from datetime import date
from shutil import rmtree


class pdf():

  def __init__(self):
    if not os.path.isdir('temp'):
      os.mkdir('temp')
    self.today = str(date.today())
    self.format_imgs()
    

  def crop_img(self, imgname): #function to crop an image to the sesired size
      from PIL import Image
      im = Image.open(imgname)
      top,bottom = 270,530       
      left,right = 101, 1250
      im.crop((left, top, right, bottom)).save(imgname)

  def format_imgs(self):
      img_list = os.listdir(os.path.join(os.getcwd(),'temp'))
      self.img_list = [os.path.join(os.getcwd(),'temp',name) for name in img_list]
      [self.crop_img(img) for img in self.img_list] # Why should i waste time writing multiple lines?


  def create_pdf(self, course_list):
    '''A dictionary containg the courses registered has to be passed'''

    report = SimpleDocTemplate(f"{self.today}.pdf") #Initializing the filename
    styles = getSampleStyleSheet()
    report_title = Paragraph(f"Udemy Course Registration Report: {self.today} \n\n", styles["h1"])
    line_break = Paragraph('<br/><br/><br/>', ParagraphStyle('body')) #The breakline to sepatate title and table
    
    elements = [report_title, line_break] #elements is kinda wishlist of things to be built 

    #Creating the table data
    table_data = []
    for name, status in course_list.items():
      if status.upper().startswith(('ERROR', 'FAILED')):
        temp = status.split('|')
        status_ = temp[0] + f'<a href={temp[1]} color="RED"><u>Retry now</u></a>'
        status = Paragraph(status_, ParagraphStyle('body'))
      elif status.upper().startswith('SUCCESS'):
        temp = status.split('|')
        status = f'<a  href={temp[1]} color="Green"><b>{temp[0]}</b></a>'
        status = Paragraph(status, ParagraphStyle('body'))
      table_data.append([name, status])
    #Adding the grid and box elements
    styled_table = Table(data=table_data)
    styled_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.35,
    colors.black),('BOX', (0,0), (-1,-1), 0.45, colors.black)]))

    elements.append(styled_table) #Adding the table data to the wishlist ;)


    #ADDING THE COURSE REGISTRATION SCREENSHOTS

    for i,img in enumerate(self.img_list):
      if i%4==0: #Making sure only 4 items get onto a page:)
        elements.append(PageBreak())

      title = os.path.basename(img.split('.png')[0]) #Getting the Title from the filename
      title = Paragraph(title, styles["h3"] )
    
      I = Image(img) # Initializing the Image object
      I.drawHeight = I.drawHeight/2 #resizing the image to a factor of 2
      I.drawWidth = I.drawWidth/2

      elements.append(title) # adding the title & image to the wishlist
      elements.append(I)

    #Buiding the PDF from the wishlist
    report.build(elements)
    rmtree('temp')



