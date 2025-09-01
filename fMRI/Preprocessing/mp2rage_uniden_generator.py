import numpy as np
import nibabel as nib

############################################
# Note: Matlab implementation:
# https://github.com/khanlab/mp2rage_genUniDen/blob/master/mp2rage_genUniDen.m
# Note: Python implemention of Matlab code:
# https://github.com/khanlab/mp2rage_genUniDen/blob/master/mp2rage_genUniDen.py
# Date: 2019/09/25
# Author: YingLi Lu
# Fully tested on python3 (can run on python2.7 as well), get exactly same result image with Matlab.
############################################

# Set NumPy to ignore all floating-point errors
# Ignore RuntimeWarning: invalid value encountered in true_divide
np.seterr(all='ignore')

def MP2RAGErobustfunc(INV1, INV2, beta):
    # matalb: MP2RAGErobustfunc=@(INV1,INV2,beta)(conj(INV1).*INV2-beta)./(INV1.^2+INV2.^2+2*beta);
    return (np.conj(INV1)*INV2-beta)/(INV1**2+INV2**2+2*beta)

def rootsquares_pos(a, b, c):
    # matlab: rootsquares_pos=@(a, b, c)(-b+sqrt(b. ^ 2 - 4 * a.*c))./(2*a)
    return (-b+np.sqrt(b**2 - 4*a*c))/(2*a)

def rootsquares_neg(a, b, c):
    # matlab: rootsquares_neg = @(a, b, c)(-b-sqrt(b. ^ 2 - 4 * a.*c))./(2*a)
    return (-b-np.sqrt(b**2 - 4*a*c))/(2*a)

def mp2rage_genUniDen(MP2RAGE_filenameUNI, MP2RAGE_filenameINV1, MP2RAGE_filenameINV2, MP2RAGE_uniden_output_filename, chosenFactor):

    # ---------- load data ----------
    MP2RAGEimg = nib.load(MP2RAGE_filenameUNI)
    INV1img = nib.load(MP2RAGE_filenameINV1)
    INV2img = nib.load(MP2RAGE_filenameINV2)

    MP2RAGEimg_img = MP2RAGEimg.get_fdata()
    INV1img_img = INV1img.get_fdata()
    INV2img_img = INV2img.get_fdata()

    if MP2RAGEimg_img.min() >= 0 and MP2RAGEimg_img.max() >= 0.51:
        # converts MP2RAGE to -0.5 to 0.5 scale - assumes that it is getting only positive values
        MP2RAGEimg_img = (
        MP2RAGEimg_img - MP2RAGEimg_img.max()/2)/MP2RAGEimg_img.max()
        integerformat = 1
    else:
        integerformat = 0

    # ---------- computes correct INV1 dataset ----------
    # gives the correct polarity to INV1
    INV1img_img = np.sign(MP2RAGEimg_img)*INV1img_img

    # because the MP2RAGE INV1 and INV2 is a sum of squares data, while the
    # MP2RAGEimg is a phase sensitive coil combination. some more maths has to
    # be performed to get a better INV1 estimate which here is done by assuming
    # both INV2 is closer to a real phase sensitive combination

    # INV1pos = rootsquares_pos(-MP2RAGEimg.img,INV2img.img,-INV2img.img.^2.*MP2RAGEimg.img);
    INV1pos = rootsquares_pos(-MP2RAGEimg_img,
    INV2img_img, -INV2img_img**2*MP2RAGEimg_img)
    INV1neg = rootsquares_neg(-MP2RAGEimg_img,
    INV2img_img, -INV2img_img**2*MP2RAGEimg_img)

    INV1final = INV1img_img

    INV1final[np.absolute(INV1img_img-INV1pos) > np.absolute(INV1img_img-INV1neg)
    ] = INV1neg[np.absolute(INV1img_img-INV1pos) > np.absolute(INV1img_img-INV1neg)]
    INV1final[np.absolute(INV1img_img-INV1pos) <= np.absolute(INV1img_img-INV1neg)
    ] = INV1pos[np.absolute(INV1img_img-INV1pos) <= np.absolute(INV1img_img-INV1neg)]

    # usually the multiplicative factor shouldn't be greater then 10, but that
    # is not the ase when the image is bias field corrected, in which case the
    # noise estimated at the edge of the imagemight not be such a good measure

    multiplyingFactor = chosenFactor
    noiselevel = multiplyingFactor*np.mean(INV2img_img[:, -11:, -11:])

    # % MP2RAGEimgRobustScanner = MP2RAGErobustfunc(INV1img.img, INV2img.img, noiselevel. ^ 2)
    MP2RAGEimgRobustPhaseSensitive = MP2RAGErobustfunc(
    INV1final, INV2img_img, noiselevel**2)

    if integerformat == 0:
        MP2RAGEimg_img = MP2RAGEimgRobustPhaseSensitive
    else:
        MP2RAGEimg_img = np.round(4095*(MP2RAGEimgRobustPhaseSensitive+0.5))

    # ---------- save image ----------
    MP2RAGEimg_img = nib.casting.float_to_int(MP2RAGEimg_img,'int16')
    new_MP2RAGEimg = nib.Nifti1Image(MP2RAGEimg_img, MP2RAGEimg.affine, MP2RAGEimg.header)
    nib.save(new_MP2RAGEimg, MP2RAGE_uniden_output_filename)
