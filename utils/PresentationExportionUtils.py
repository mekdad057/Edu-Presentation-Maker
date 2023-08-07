def replace_with_image(img, shape, slide):
    """
    replaces the shape with an image and make sure it's not cropped
    and resized properly
    :param img: path of the image
    :param shape: the shape which the image will be inserted into,
     usually it's a placeholder.
    :param slide: the current slide the image will be inserted in.
    :return:
    """
    pic = slide.shapes.add_picture(img, shape.left, shape.top)

    # calculate max width/height for target size
    ratio = min(shape.width / float(pic.width), shape.height / float(pic.height))

    pic.height = int(pic.height * ratio)
    pic.width = int(pic.width * ratio)

    pic.left = int(shape.left + ((shape.width - pic.width) / 2))
    pic.top = int(shape.top + ((shape.height - pic.height) / 2))

    placeholder = shape.element
    placeholder.getparent().remove(placeholder)
