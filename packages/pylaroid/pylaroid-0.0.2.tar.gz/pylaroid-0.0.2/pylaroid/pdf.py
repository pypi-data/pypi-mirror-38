from datetime import datetime
from os.path import join
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
from PIL import Image


def generate_pdf(img_list, rootpath):
    date = datetime.now()
    pdf_name = "{}.pdf".format(date.strftime('%d-%m-%Y_%Hh%Mm%S'))
    pdf_path = join(rootpath, "pdf", pdf_name)
    c = Canvas(pdf_path, pagesize=letter)
    x = 0.5
    y = 1
    for img_path in img_list[:2]:
        img = Image.open(img_path)
        reportlab_img = ImageReader(img)
        c.drawImage(reportlab_img, x*cm, y*cm, width=8.91*cm, height=10.67*cm)
        y += 10.67
    x = 9.41
    y = 1
    for img_path in img_list[2:]:
        img = Image.open(img_path)
        img = img.rotate(90, expand=1)
        reportlab_img = ImageReader(img)
        c.drawImage(reportlab_img, x*cm, y*cm, width=10.67*cm, height=8.91*cm)
        y += 8.91
    c.showPage()
    c.save()
    return pdf_path
