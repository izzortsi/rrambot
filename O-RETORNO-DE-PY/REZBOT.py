##
from binance.client import Client
from grabber import *

API_KEY = "XQbT3UoAVCqSr72ivWA2gBnDHAaGuNfaYdfduBMCW3VxHol4rmOCF2w8M3vr0u37"
API_SECRET = "iJ05eftlARzIcR9CHYKU81qkM21MIgvgmk5pZNvJWYLdYUgB6cS9bRLjwqBVXrQ9"
##

client = Client(api_key=API_KEY, api_secret=API_SECRET)
grab = Grabber(client)
##

grab.compute_indicators()
##
