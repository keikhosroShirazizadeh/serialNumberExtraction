# serialNumberExtraction
This project detect and extract the back of the national card of Iran national card identication and extract the serial number from it and serve it as rest service

it use opencv BFMactcher to find the card based on template card in the image. crop the card from the image then compute and estimate the place of the serial number
crop the area of that and use that image as input of tesseract engine.
and finally validate the output to pass some tests and respond the request of an image with a serial number value of iran national card identiacation.

based on python(opencv,pil,numpy,flask,pytesseract)
