import cv2 as cv
import numpy as np
import array
import random
import unittest



def LabImage(image_file):
    bgr_image = cv2.imread(image_file)
    h, w, channels = bgr_image.shape
    lab_image = cv.cvtColor(bgr_image, cv.COLOR_BGR2LAB)
    # Split LAB channels
    L, a, b = cv.split(lab_image)
    return (L, a, b)



def LabJointHistogram(L,a,b):

    print(str(np.min(a)) + '  ' + str(np.average(a)) + '  ' + str(np.max(a)))
    print(str(np.min(b)) + '  ' + str(np.average(b)) + '  ' + str(np.max(b)))

    xedges, yedges = np.linspace(np.min(a), np.max(a), 128), np.linspace(np.min(b), np.max(b), 128)
    hist, xedges, yedges = np.histogram2d(a.flatten(), b.flatten(), (xedges, yedges))
    xidx = np.clip(np.digitize(a.flatten(), xedges), 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(b.flatten(), yedges), 0, hist.shape[1] - 1)
    c = hist[xidx, yidx]
    return (a.flatten(), b.flatten(), c)

def find_template(fixed, roi, template):
    h, w = template.shape
    roi_window = fixed[roi[0]:roi[1], roi[2]:roi[3]]

    res = cv.matchTemplate(roi_window, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    tl = max_loc
    br = (tl[0] + w, tl[1] + h)
    return (res, max_val, tl, br)


def compare_mse(image_a, image_b):
    diff = image_a - image_b
    diff = diff * diff
    r = np.sum(diff)
    r /= float(image_a.shape[0] * image_a.shape[1])
    return (1.0 - r)


def correlate(cvma, cvmb, mask=None):
    ha, wa = cvma.shape[:2]
    hb, wb = cvmb.shape[:2]

    if ha != hb or wa != wb:
        print("Same Size Required")
        return 0.0

    mean_a, stddev_a = cv.meanStdDev(cvma, mask=mask)
    mean_b, stddev_b = cv.meanStdDev(cvma, mask=mask)
    n_pixels = hb * wa

    covar = (cvma - mean_a).dot(cvmb - mean_b) / n_pixels
    correlation = covar / (stddev_a * stddev_b)

    return correlation



def make_gauss(centre, amp, sig, shapdim):
    gauss = np.zeros(shapdim, np.float32)
    sidelenx = shapdim[1]
    sideleny = shapdim[0]
    l = np.zeros(shapdim, np.float32)

    for i in range(0, sideleny):
        for j in range(0, sidelenx):
            l[i, j] = np.sqrt((centre[0] - i) ** 2 + (centre[1] - j) ** 2)
    gaussblob = amp * np.exp(-(l ** 2) / sig)
    return gaussblob


__all__ = ['TestCorrelate']

winName = "Match Test"
cv.namedWindow(winName, cv.WINDOW_NORMAL)


class TestCorrelate(unittest.TestCase):

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

    def test_correlate(self):
        self.test_basic()

    def test_basic(self):
        g1 = make_gauss([80, 80], 3.14, 0.5, [160, 160])
        g2 = make_gauss([7, 7], 3.14, 0.5, [16, 16])
        roi = [70, 90, 70, 90]
        res = find_template(g1, roi, g2)
        self.assertTrue(res[2] == (3, 3))
        self.assertTrue(res[3] == (19, 19))
        self.assertAlmostEqual(res[1], 1.0, 4)



if __name__ == '__main__':
    unittest.main()
