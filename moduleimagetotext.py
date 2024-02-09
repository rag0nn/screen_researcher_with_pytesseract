import pytesseract
from PIL import Image
import cv2
import matplotlib.pyplot as plt

# Kullanılacak Tesseract dosyası 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# görseli içeri aktar
def read_image(path):
    im = cv2.imread(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im

# Görseli Göster
def show_image(image):
    plt.imshow(image)
    cv2.imshow("q",image)
    cv2.waitKey(0)
    
def get_current_usable_langs():
    """
    Kullanılabilen dillerinin kısaltmalarını döndürür.
    """
    return pytesseract.get_languages(config='')

def image_texts(image:list):
    """
    Bulunan her karakteri kutusuyla (bounding box ile) beraber döndürür.
    """

    #im = read_image(image_path)

    texts = pytesseract.image_to_string(image,lang='tur')
    print(texts)
    #show_image(image)
    return texts

def image_boxes(image_path:str):
    """
    Bulunan her karakteri kutusuyla (bounding box ile) beraber döndürür.
    """

    im = read_image(image_path)

    boxes = pytesseract.image_to_boxes(im,lang='tur')
    return boxes

def image_data(image_path:str):
    """
    Görselden alınabilen tüm çıktılarını döndürür.
    """
    im = read_image(image_path)
    return pytesseract.image_to_data(im,lang='tur')

def image_osd(image_path):
    """
    Görselin oryantasyonu ve yazı türü hakkında bilgileri döndürür.
    """
    im = read_image(image_path)
    return pytesseract.image_to_osd(im)

def image_to_pdf(image_path):
    """
    Görseli pdf' ye dönüştürür.
    
    pdf_outputs klasörüne kaydeder.
    """
    im = read_image(image_path)
    pdf = pytesseract.image_to_pdf_or_hocr(im,extension='pdf',lang='tur')
    with open(f'pdf_outputs/{image_path.split("/")[-1].split(".")[0]}.pdf',"w+b") as f:
        f.write(pdf)