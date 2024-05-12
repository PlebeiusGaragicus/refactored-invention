# https://www.youtube.com/watch?v=8OJC21T2SL4

# Function to convert image to base64
def image_to_base64 (image_path) :
    with Image.open (image_path) as image:
    buffered = io.BytesIO()
    image. save (buffered, format=image. format)
    img_str = base64. b64encode (buffered getvalue ())
    return img_str. decode ('utf-8' )

image_str = image_to_base64(". /RetrievalTutorials/static/pdfImages/figure-15-6.jpg")

