import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def image_to_text(img_path):
    try:
        img = cv2.imread(img_path)
        img = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img)
        image_with_detected_text(img)
        return [text, img]
    except:
        return [None, None]


def image_with_detected_text(img):
    boxes = pytesseract.image_to_data(img)

    h_img, w_img, _ = img.shape

    for x, b in enumerate(boxes.splitlines()):
        if x > 0:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w + x, h + y), (200, 0, 0), 2)
    return img


def save_img(img_file_path, img):
    cv2.imwrite(img_file_path, img)