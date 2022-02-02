
import numpy as np
import imutils
import cv2

class Panorama_Class:

    def stitch_img(self, images, ratio_=0.75, thresh_=5.0):

        (img_B, img_A) = images
        (kp_A, feat_A) = self.find_feat_kp(img_A)
        (kp_B, feat_B) = self.find_feat_kp(img_B)

        Values = self.match_keypoints(kp_A, kp_B,feat_A, feat_B, ratio_, thresh_)

        if Values is None:
            return None

        (matches, _homography, status) = Values
        res_img = self.apply_transformation(img_A,img_B,_homography)
        res_img[0:img_B.shape[0], 0:img_B.shape[1]] = img_B


        return res_img

    def find_feat_kp(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        descriptors = cv2.xfeatures2d.SIFT_create()
        (Keypoints, features) = descriptors.detectAndCompute(image, None)

        Keypoints = np.float32([i.pt for i in Keypoints])
        return (Keypoints, features)

    def match_keypoints(self, kp_A, kp_B, featuresA, featuresB,ratio_, thresh_):

        matches_vals = self.findAll_matches(featuresA,featuresB)
        valid_matches = self.findValid_matches(matches_vals,ratio_)

        if len(valid_matches) > 4:
            # construct the two sets of points
            pointsA = np.float32([kp_A[i] for (_,i) in valid_matches])
            pointsB = np.float32([kp_B[i] for (i,_) in valid_matches])

            (_homography, status) = self.calc_homography(pointsA, pointsB, thresh_)

            return (valid_matches, _homography, status)
        else:
            return None

    def findAll_matches(self,featuresA,featuresB):

        match_instance = cv2.DescriptorMatcher_create("BruteForce")
        All_Matches = match_instance.knnMatch(featuresA, featuresB, 2)

        return All_Matches

    def findValid_matches(self,matches_vals,ratio_):

        valid_matches = []

        #Ratio Test
        for val in matches_vals:
            if len(val) == 2 and val[0].distance < val[1].distance * ratio_:
                valid_matches.append((val[0].trainIdx, val[0].queryIdx))

        return valid_matches



    def calc_homography(self,pointsA,pointsB,thresh_):

        (H, status) = cv2.findHomography(pointsA, pointsB, cv2.RANSAC, thresh_)
        return (H,status)


    def apply_transformation(self,img_A,img_B,_homography):
        val = img_A.shape[1] + img_B.shape[1]
        res_img = cv2.warpPerspective(img_A, _homography, (val , img_A.shape[0]))

        return res_img

     


def stitchdriver(filename,output):

    #filename = ["im1.jpeg","im2.jpeg","im3.jpeg"]
    # filename = ["1.jpeg","2.jpeg","3.jpeg"]
    no_of_images=len(filename)

    images = []

    for i in range(no_of_images):
        images.append(cv2.imread("static/uploads/"+filename[i]))


    for i in range(no_of_images):
        images[i] = imutils.resize(images[i], width=400)

    for i in range(no_of_images):
        images[i] = imutils.resize(images[i], height=400)


    panorama_var = Panorama_Class()

    result = panorama_var.stitch_img([images[no_of_images-2], images[no_of_images-1]])
    for i in range(no_of_images - 2):
        result = panorama_var.stitch_img([images[no_of_images-i-3],result])

    cv2.imwrite(output,result)




# if __name__ == '__main__':
#     main()
