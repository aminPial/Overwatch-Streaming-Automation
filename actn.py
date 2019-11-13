import pytesseract, cv2



def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def return_text(slice_list):


    result_action = []

    template = cv2.imread('./template.png', 0)

    w, h = template.shape[::-1]

    method = eval('cv2.TM_CCOEFF')

    for j in range(len(slice_list)):

        im_array_xcv = cv2.imread(slice_list[j], 0)
        im_array = cv2.imread(slice_list[j])

        res = cv2.matchTemplate(im_array_xcv, template, method)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        i = im_array[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]  # use the main image

        ar = image_resize(i, width=400, height=600)  # tweak w,h ++ other params

        a = pytesseract.image_to_string(ar, config='-psm 6', lang='eng', )

        n = ['ENEMY', 'SLEPT', '+25', '25', 'SLEPI']

        if len([j for j in n if j in a]) >= 1:

            result_action.append(1)

        else:
            result_action.append(0)


    return result_action


