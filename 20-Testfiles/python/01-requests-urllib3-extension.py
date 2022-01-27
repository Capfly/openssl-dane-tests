import requests.exceptions

import requests as req
import OpenSSL
import urllib3
import certifi
import urllib3.util.ssl_ as isl

if not False:
    try:
        import urllib3.contrib.pyopenssl
        urllib3.contrib.pyopenssl.inject_into_urllib3()

        print("Using pyopenssl backend now...")
    except ImportError:
        print("IE")
        pass

try:
    print("1. Without dane check: ", end="")
    r = req.get("https://stangew.de")
    print("passed!")
    print(r.content[:200])
except requests.exceptions.SSLError as e:
    print("SSL VERIFY FAILED")

try:
    print("2. With dane check [dnssec not ok]: ", end="")
    r = req.get("https://stangew.de", check_dane=True)
    print("passed!")
    print(r.content[:200])
except requests.exceptions.SSLError as e:
    print("SSL VERIFY FAILED")

try:
    print("2. With dane check [dnssec ok]: ", end="")
    r = req.get("https://fedoraproject.org", check_dane=True)
    print("passed!")
    print(r.content[:200])
except requests.exceptions.SSLError as e:
    print("SSL VERIFY FAILED")


#http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

#r = http.request("GET", "https://stangew.de")

#print(r.data)

#print(isl.IS_PYOPENSSL)
