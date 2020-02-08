import requests  
# requests to access a url of a page
from bs4 import BeautifulSoup
import smtplib
# it enables us to send emails via this code
import time
from sensitive_data import sender, receiver, password

# grafica RTX 2070
URL = 'https://www.amazon.es/MSI-GeForce-RTX-2070-OC/dp/B07TWX22ZQ/ref=pd_sbs_147_1/262-4454882-4175743?_encoding=UTF8&pd_rd_i=B07TTSVC7K&pd_rd_r=f2929857-3653-4f5c-b3d7-1acc80045328&pd_rd_w=q3WfW&pd_rd_wg=D25dF&pf_rd_p=ef1c414f-f8bd-43e1-88ba-b13f180fe4ad&pf_rd_r=GSNT686MKEJEE7W1WKG2&refRID=GSNT686MKEJEE7W1WKG2&th=1'

# SSD EVO 500GB
URL2 = 'https://www.amazon.es/Samsung-860-EVO-Estado-megabytes/dp/B078WQT6S6/ref=sr_1_10?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1UQQ34ZFLFQTW&keywords=informatica&qid=1581168153&rnid=667050031&s=computers&sprefix=infroma%2Caps%2C170&sr=1-10&th=1'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
RTX = 0
SSD = 0
def check_prices():
    global RTX, SSD

    ######  GRAPHICS CARD RTX 2070  ######
    page = requests.get(URL, headers=headers)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    # we do this second soup and have the first one act as a bait, otherwise with just one soup wont work

    title = soup2.find(id= "productTitle").get_text()
    print(title.strip())
    # to use the method strip (only getting the text with no whitespace) we need to use the method get_text

    price = soup2.find(id="priceblock_ourprice").get_text()
    round_price_RTX = (price[0:3])
    print('Precio final: ' + price.strip())

    if int(round_price_RTX) < 700:
        RTX = 1

    #####  SOLID STATE DRIVE EVO 500GB  ######
    page2 = requests.get(URL2, headers=headers)
    soup3 = BeautifulSoup(page2.content, "html.parser")
    soup4 = BeautifulSoup(soup3.prettify(), "html.parser")
    title2 = soup4.find(id="productTitle").get_text()
    price2 = soup4.find(id="priceblock_ourprice").get_text()
    print(title2.strip(), price2.strip())
    round_price = price2[:-3]
    # we take the three last digits out of the variable , which are the '€' one whitespace and the last decimal number (optional)
    list_price = list(round_price)
    final_price = ""
    for i in list_price:
        if i == ",":
           i = "."
        # we change the coma for a dot so the program knows its a float number 
        final_price += i
    print('Precio final: ' + str(final_price) + " €")
    
    if float(final_price) < 80:
        SSD = 1

    if (SSD == 1) or (RTX == 1):
        send_email()
    
def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    # the method ehlo is for establishing connections between two gmail connections (?)
    server.starttls()
    # encrypts our connection
    server.ehlo()

    server.login(sender, password)
    if (SSD == 1) and (RTX == 1):
        subject = 'Han bajado algunos precios!'

        body= 'Compruebalo tu mismo;\nLink RTX: ' + URL + '\n link SSD: ' + URL2
    elif (SSD == 1):
        subject = 'Ha bajado el precio del SSD!'
        body= 'Compruebalo tu mismo;\nLink: ' + URL2 
    else:
        subject = 'Ha bajado el precio de la grafica!'
        body = 'Compruebalo tu mismo ahora; \nLink: ' + URL

    msg = f"Subject: {subject}\n\n{body}"
    # 'f' is for format
    try:
        server.sendmail(sender, receiver, msg)
        # sendmail = from (1) to (2) and the message itself (3)
        print('The email has been sent succesfully!')
    except: 
        print("Couldn't send the email..")

    server.quit()

check_prices()
# if we only want to check once whenever we want we just execute the .exe, if not we uncomment the while True

# while True:
#     check_RTX()
#     time.sleep(60 * 60 * 24)
# we check every day for an update on the price of the product