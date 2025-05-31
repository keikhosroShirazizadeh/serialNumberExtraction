

from PIL import Image
import pytesseract

# Set the path to the Tesseract executable (only needed for Windows users)
# For example: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
custom_config2 = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
custome_config3=r'--oem 3 --psm 6'


# custom_config = r'--oem 3 --psm 7 '
def extract_text_from_image(image_path):
    try:
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Use Tesseract to extract text from the image
        textNumber = pytesseract.image_to_string(image,lang='eng',config=custom_config).strip().split("\n")[0]
        text= pytesseract.image_to_string(image,lang='eng',config=custom_config2).strip().split("\n")[0]
        wholeText=pytesseract.image_to_string(image,lang='eng',config=custome_config3).strip().split("\n")[0]

        print("textNUmber:",textNumber, "size", len(textNumber))
        print("text:",text, "size", len(text),"text lines: ")
        print("whole text: ",wholeText," size: ",len(wholeText))
   
        if(len(text)==1):
            if(len(textNumber)<=9):
                
                res=textNumber[0]+text[0]+textNumber[1:len(textNumber)]
            else:
                res=textNumber[0]+text[0]+textNumber[2:len(textNumber)]
        else:
            if(not wholeText[1].isdigit()):
               if(len(textNumber)<=9):
                   res=textNumber[0]+wholeText[1]+textNumber[1:len(textNumber)]
               else:
                   res=textNumber[0]+wholeText[1]+textNumber[2:len(textNumber)]                    
            else:
                if(wholeText[0]=="0" or wholeText[0]=="G"):
                    if(len(textNumber)<=9):
                        res=textNumber[0]+text[1]+textNumber[1:len(textNumber)] 
                    else:
                       res=textNumber[0]+text[1]+textNumber[2:len(textNumber)]                    
                else:
                    if(len(textNumber)<=9):
                       res=textNumber[0]+text[0]+textNumber[1:len(textNumber)]
                    else:
                        res=textNumber[0]+text[0]+textNumber[2:len(textNumber)]
                        
            
       
       
        print("res:",res," ",len(res))
        if(len(res)<10):
            raise Exception("coudn't find a good result send another pic")
        else:
            return res[0:10]
        
        
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    # Path to the image
    image_path = "serial.jpg"  # Replace with your image file path
    
    # Extract text
    extracted_text = extract_text_from_image(image_path)
    print("Extracted Text:")
    print(extracted_text)

# from PIL import Image
# import pytesseract
# import matplotlib.pyplot as plt


# # Path to the Tesseract executable (update the path if needed)
# # Uncomment the next line and provide the path to tesseract if not in PATH
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Load the image
# image_path = "serial.jpg"  # Replace with your image file path
# image = Image.open(image_path)
# # Convert the image to grayscale
# gray_image = image.convert("L")
# # Convert the grayscale image to black and white using a threshold
# threshold = 128  # Set the threshold value (adjust if needed)
# bw_image = gray_image.point(lambda x: 0 if x > threshold else 255, mode='1')
# imgplot = plt.imshow(bw_image)
# plt.show()
# bw_image.save("bw_id.jpg")



# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# # Perform OCR using Tesseract
# # extracted_text = pytesseract.image_to_string(bw_image,lang="fas")
# # persian_digits = re.findall(r'[۰-۹]', extracted_text)
# # extracted_digits = ''.join(persian_digits)
# custom_config = r'--oem 3 --psm 6'
# # extracted_text = pytesseract.image_to_string(bw_image,lang='eng+fas')
# extracted_text = pytesseract.image_to_string(bw_image,lang='eng+fas',config=custom_config)


# # Print the extracted text
# print("Extracted Text:")
# print(extracted_text)