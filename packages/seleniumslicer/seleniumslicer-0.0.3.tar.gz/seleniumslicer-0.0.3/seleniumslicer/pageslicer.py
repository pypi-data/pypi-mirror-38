from io import BytesIO
from PIL import Image
def save_element(driver, element, fileName):
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()
    byteimg = BytesIO(png)
    im = Image.open(byteimg)

    left = location['x']
    top = location['y']
    right = location['x']+size['width']
    bottom = location['y']+size['height']

    im = im.crop((left, top, right, bottom))
    im.save(fileName)
