""" image module of dozy. """
import glob
import os

import cv2
import numpy as np

from . import utils


def combine(img1, img2, axis=0):
    r""" Combine two images img1 and img2 to one image horizionly or vertically.

    Args:
        img1 (np.ndarray): first image to combine.
        img2 (np.ndarray): second image to combine.
        axis (int, optional): which axis to combine images. 0 for vertically, 1
            for horizon. default: 0.

    Returns:
        np.ndarray: combined image.

    Example:
        >>> img1 = image.load('/path/to/img1.jpg')
        >>> img2 = image.load('/path/to/img2.jpg')
        >>> img3 = image.combine(img1, img2, axis=0)
        >>> image.show(img3, 'combined image')

    """
    res = np.concatenate((img1, img2), axis=axis)
    return res


def combine_list(imgs, axis=0):
    r""" Combine multiple images to one image horizionly or vertically.

    Args:
        imgs (list): list of np.ndarray, i.e., images to combine.
        axis (int, optional): which axis to combine images. 0 for vertically, 1
            for horizon. default: 0.

    Returns:
        np.ndarray: combined image.

    Example:
        >>> img1 = image.load('/path/to/img1.jpg')
        >>> img2 = image.load('/path/to/img2.jpg')
        >>> img3 = image.load('/path/to/img3.jpg')
        >>> img4 = image.combine([img1, img2, img3], axis=0)
        >>> image.show(img4, 'combined image')

    """
    res = np.concatenate(imgs, axis=axis)
    return res


def crop(img, x0=None, y0=None, x1=None, y1=None):
    """Crop img[y0:y1, x0:x1] from img and return this part.

    Args:
        img (numpy.ndarray): an RGB or grayscale image. For RGB image,  shape
            is [h, w, c]. for grayscale image, shape is [h, w].
        y0 (int): top y coordinates of target part of img to crop.
        y1 (int): bottom y coordinates of target part of img to crop.
        x0 (int): left x coordinates of target part of img to crop.
        x1 (int): right x coordinates of target part of img to crop.

    Returns:
        img[y0:y1, x0:x1].

    Raises:
        ValueError: if value of coordinates < 0.

    Example:
        >>> img = imagel.load('/path/to/img1.jpg')
        >>> sub_img = image.crop(img, x0=10, y=10, x1=200, y1=200)

    """

    h, w = img.shape[:2]
    y0 = 0 if y0 is None else y0
    y1 = h if y1 is None else y1
    x0 = 0 if x0 is None else x0
    x1 = w if x1 is None else x1

    assert isinstance(img, np.ndarray), 'img is not a np.ndarray'
    assert img.ndim in [2, 3], 'img must be RGB image or grayscale image'
    assert isinstance(y0, int), 'y0 is not a int'
    assert isinstance(y1, int), 'y1 is not a int'
    assert isinstance(x0, int), 'x0 is not a int'
    assert isinstance(x1, int), 'x1 is not a int'

    if y0 < 0:
        raise ValueError('y0 is < 0')
    if y1 < 0:
        raise ValueError('y1 is < 0')
    if x0 < 0:
        raise ValueError('x0 is < 0')
    if x1 < 0:
        raise ValueError('x1 is < 0')

    return img[y0:y1, x0:x1]


def load(img_path):
    """ Load an image from a given path.

    Args:
        img_path (str): where to load the image . must have extension.

    Return:
        An image has type np.ndarray.

    Example:
        >>> img = image.load('/path/to/img.jpg')
        >>> print(type(img))
        <class 'numpy.ndarray'>
        >>> print(img.shape)
        (340, 325, 3)

    """
    assert isinstance(img_path, str), 'img_path must be a str'
    utils.complaint_file_absence(img_path)

    img = cv2.imread(img_path)
    return img


def merge_masks(masks):
    """ Merge multiple mask images into one image.

    We assume the mask of images have no intersection. Otherwise, the mask of
    latter image will override the previous images.

    Args:
        masks (list): a list contain multiple grayscale images only containng
        valule 0 and 255, and all have same size

    Returns:
        np.ndarray: One grayscale image

    Example:
        >>> img1 = image.load('/path/to/mask1.png')
        >>> img2 = image.load('/path/to/mask2.png')
        >>> merged_mask = image.merge_masks([img1, img2])

    Raises:
        ValueError: If length of masks is zero.
    """

    assert isinstance(masks, list), 'masks must be a list.'
    if len(masks) < 1:
        raise ValueError('length of masks is zero.')

    res_img = masks[0]
    for img in masks[1:]:
        res_img[img > 0] = img[img > 0]

    return res_img


def merge_masks_folder(folders, ptn="*.*"):
    """ Merge grayscale images in mutiple directories according names.

    Note:
        In order to support any length of folders, we assume the corresponding
        images in different dir have same name (extension can be different).

    Args:
        folders (list): a str list containing abs folder paths.
        ptn (str): the pattern to search wanted images in each folder.

    Raises:
        ValueError: If length of folders is zero.

    Yields:
        np.ndarray: next merged image.
        str: The basename of next operated image.

    Example:
        >>> fd1 = '/path/to/dir1'
        >>> fd2 = '/path/to/dir2'
        >>> for img in merge_masks_folder([fd1, fd2]):
                print(img.shape)

    """
    assert isinstance(folders, list), 'folders must be a list.'
    if len(folders) < 1:
        raise ValueError('length of folder is zero.')
    for fd in folders:
        utils.complaint_dir_absence(fd)

    first_fd = folders[0]
    sample_img_paths = sorted(glob.glob(os.path.join(first_fd, ptn)))
    for img_path in sample_img_paths:
        first_ext = os.path.splitext(img_path)[1]
        print(img_path, first_ext)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        imgs = [img]
        for cur_fd in folders[1:]:
            cur_ext = os.path.splitext(os.listdir(cur_fd)[0])[1]
            print(cur_ext)
            cur_img_path = img_path.replace(first_fd, cur_fd).replace(
                first_ext, cur_ext)
            print(cur_img_path)
            cur_img = cv2.imread(cur_img_path, cv2.IMREAD_GRAYSCALE)
            imgs.append(cur_img)

        yield merge_masks(imgs), os.path.basename(img_path)


def resize(img, h, w):
    """ Resize img to target shape [h, w].

    Args:
        img (np.ndarray): image to resize.
        h (int): height of target image.
        w (int): width of target image.

    Returns:
        np.ndarray with shape [h, w] or [h, w, 3].

    Example:
        >>> img = image.load('/path/to/img.jpg')
        >>> img_re = image.resize(img, h=256, w=256)

    """

    assert isinstance(h, int), 'h must be an int'
    assert isinstance(w, int), 'w must be an int'
    assert h > 0, 'h must be larger than 0'
    assert w > 0, 'h must be larger than 0'

    return cv2.resize(img, (w, h))


def save(save_path, img):
    """ Save an image.

    Args:
        save_path (str): where to save the image. must have extension.
        img (np.ndarray): an image has shape [h, w, c] or [h, w].

    Returns:
        return True if save successfully else False.

    Example:
        >>> img = image.load(/path/to/img.jpg')
        >>> image.save('/path/to/img_new.jpg', img)

    """
    assert isinstance(save_path, str), 'save_path must be a str'
    utils.complaint_dir_absence(os.path.dirname(save_path))

    res = cv2.imwrite(save_path, img)

    if res is None:
        print('Image saving failed. Please check whethe the save_path exists.')
        return False
    return True


def show(img, show_name='img', delay=0):
    """ Show an image.

    Args:
        img (np.ndarray): an image has shape [h, w, c] or [h, w].
        show_name (str, optional): the name of the show window. Default: 'img'.
        delay (int, optional): how many milliseconds to wait the window then
            close. 0 means forever util key pressed. Default: 0.

    Example:
        >>> img = image.load('/path/to/img.jpg')
        >>> image.show(img, show_name="img")

    """
    assert isinstance(img, np.ndarray), 'img must be a np.ndarray'

    cv2.imshow(show_name, img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()


def show_pair(img1, img2, show_name="img_pair", delay=0):
    """ Show two images in a row.

    Args:
        img1 (np.ndarray): First image to show.
        img2 (np.ndarray): Second image to show.
        show_name (str, optional): name for the window to show image. Default:
            'img_pair'.
        delay (int, optional): how many milliseconds to wait the window then
            close. 0 means forever util key pressed. default: 0

    Example:
        >>> img1 = image.load('/path/to/img1.jpg')
        >>> img2 = image.load('/path/to/img2.jpg')
        >>> image.show_pair(img1, img2, show_name="img_pair")

    """
    img_combine = combine(img1, img2, axis=1)
    show(img_combine, show_name=show_name, delay=delay)


def show_pair_folder(dir1, dir2, dir1_ptn="*.*", dir2_ptn="*.*"):
    r""" Show images in two folder to compare them easily.

    Args:
        dir1 (str): path of first directory.
        dir2 (str): path of second directory.
        dir1_ptn(str, optional): pattern for filtering image in dir1. Default:
            '*.*'
        dir2_ptn(str, optional): pattern for filtering image in dir2. Default:
            '*.*'

    Example:
        >>> dir1 = image.load('/path/to/dir1')
        >>> dir2 = image.load('/path/to/dir2')
        >>> image.show_pair_folder(img1, img2, show_name="img_pair_folder")

    """
    utils.complaint_dir_absence(dir1)
    utils.complaint_dir_absence(dir2)

    dir1_full_pth = os.path.join(dir1, dir1_ptn)
    dir2_full_pth = os.path.join(dir2, dir2_ptn)
    imgs_path1 = sorted(glob.glob(dir1_full_pth))
    imgs_path2 = sorted(glob.glob(dir2_full_pth))
    assert len(imgs_path1) == len(imgs_path2), 'images in two dir must be equal'

    def update(imgs_path1, imgs_path2, idx):
        """ Update shown images. """
        img1 = load(imgs_path1[idx])
        img2 = load(imgs_path2[idx])
        img_comb = combine(img1, img2, axis=1)
        cv2.imshow('img_comb', img_comb)

    idx = 0
    update(imgs_path1, imgs_path2, idx)
    while True:
        ch = cv2.waitKeyEx()
        if ch & 0xFF == ord('q'):
            break
        if ch == 65361 or ch == 65362 or ch == ord('h') or ch == ord('k'):
            idx = max(0, idx-1)
            update(imgs_path1, imgs_path2, idx)
            idx -= 1
        elif ch == 65363 or ch == 65364 or ch == ord('l') or ch == ord('j'):
            idx = min(idx, len(imgs_path1))
            update(imgs_path1, imgs_path2, idx)
            idx += 1
        else:
            print(ch)

    cv2.destroyAllWindows()
