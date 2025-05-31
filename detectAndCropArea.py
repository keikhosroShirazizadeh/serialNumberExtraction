import cv2
import numpy as np

# import pytesseract

def detect_and_crop_object(image_path, template_path, output_path):

    # Load images
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    # Convert images to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Initialize the ORB detector

    orb = cv2.ORB_create(nfeatures=8000)

    # Find the keypoints and descriptors with ORB

    kp1, des1 = orb.detectAndCompute(template_gray, None)

    kp2, des2 = orb.detectAndCompute(img_gray, None)

    # Create a BFMatcher object.

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw the first 10 matches.
    img_matches = cv2.drawMatches(template, kp1, img, kp2, matches[:800], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Extract location of good matches
    points = []
    for match in matches[:800]:  # considering the first 10 good matches
        img_idx = match.trainIdx
        (x, y) = kp2[img_idx].pt
        points.append((int(x), int(y)))

    if points:
        # Get bounding box coordinates
        points = np.array(points)
        x, y, w, h = cv2.boundingRect(points)

        # Crop the detected region
        #make cropption more accurate by comparing template width and height 
        print("template image size:", template.shape)
        tempalteH=template.shape[0]
        tempalteW=template.shape[1]
        print("different bettween h and templateH:",tempalteH-h)
        print("different bettween w and templateW:",tempalteW-w)
        # if(h>tempalteH and h-tempalteH<100):
        #     h=h-(h-tempalteH)
        # elif(h<tempalteH and tempalteH-h<100):
        #     h=h+(tempalteH-h)
        # if(w>tempalteW and w-tempalteW<100):
        #     w=w-(w-tempalteW)
        # elif(w<tempalteW and tempalteW-w<100):
        #     w=w+(tempalteW-w)
        # #end of 
        cropped_img = img[y:y+h, x:x+w]
        # print("cropped_img: ",cropped_img.shape)
        cropped_img_width=cropped_img.shape[1]
        cropped_img_height=cropped_img.shape[0]

        #id card postion extraction
        serialx=int(((0.0)/(8.5))*cropped_img_width)
        serialy=int(((0.0)/(5.5))*cropped_img_height)
        serialh=int(((2.5)/(5.5))*cropped_img_height)
        serialw=int(((0.8)/(8.5))*cropped_img_width)
        # print("id boundry:", idx,idy,idh,idw)
        serial_img=cropped_img[serialy:serialy+serialh,serialx:serialx+serialw]
        serial_img=cv2.rotate(serial_img, cv2.ROTATE_90_CLOCKWISE)
        # serial_img=cv2.threshold(serial_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Save the cropped image
        cv2.imwrite(output_path, cropped_img)

        img1=cv2.bilateralFilter(serial_img,9,75,75)
        kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
        image_sharp = cv2.filter2D(src=img1, ddepth=-1, kernel=kernel)

        img2=cv2.cvtColor(image_sharp,cv2.COLOR_BGR2GRAY)

        #save the id card
        cv2.imwrite("serial.jpg",img2)
        print(f'Cropped image saved to {output_path}')
    else:
        print('No good matches found!')



# image_path = 'test4.jpg'
# template_path = 'template4.jpg'
# output_path = './out10.jpg'
# Example usage
# detect_and_crop_object(image_path, template_path, output_path)