import requests
import time
import json
import argparse

#Proxy config, remove proxies=proxies from main request to run proxyless.
proxies = {
    "http": "http://user:pass@hostname:port",
    "https": "http://user:pass@hostname:port"
}

#Parsing function to safely format the response json.
def get_branding(data):
    try:
        branding_list = data.get("EstsProperties", {}).get("UserTenantBranding")
        if branding_list and isinstance(branding_list, list) and len(branding_list) > 0:
            print("Branding Found, Progressing.")
            branding = branding_list[0]
            return {
                "bannerlogo": branding.get("BannerLogo"),
                "illustration": branding.get("Illustration"),
                "boilerplatetext": branding.get("BoilerPlateText", "").strip(),
                "tilelogo": branding.get("TileLogo"),
                "tiledarklogo": branding.get("TileDarkLogo"),
                "backgroundcolor": branding.get("BackgroundColor"),
                "useridlabel": branding.get("UserIdLabel"),
                "favicon": branding.get("Favicon"),
            }
        else:
            print("Branding Not Found.")
            return None
    except Exception as e:
        print(f"Error in get_branding: {e}")
        return None

#Second parsing function to grab federation redirect url.
def federation_redirect_url(data):
    fed_url = data.get("Credentials", {}).get("FederationRedirectUrl")
    if fed_url:
        print("Federation Detected.")
        return fed_url
    else:
        print("Federation Not Detected.")
        return None

#Slasher, removes protocol formatting.
def slasher(url):
    if url and "/" in url:
        return url.split("/")[2]
    return url

#Main function to pull, sort, save, and print data.
def main_func(orgname):
    payload = {
        'username': f'thisvaluedoesntmatter@{orgname}',
        'isOtherIdpSupported': True,
        'checkPhones': False,
        'isRemoteNGCSupported': True,
        'isCookieBannerShown': False,
        'isFidoSupported': True,
        'country': 'GB',
        'forceotclogin': False,
        'isExternalFederationDisallowed': False,
        'isRemoteConnectSupported': False,
        'federationFlags': 0,
        'isSignup': False,
        'isAccessPassSupported': True,
        'isQrCodePinSupported': True,
    }

    response = requests.get("https://login.microsoftonline.com/common/GetCredentialType", json=payload, proxies=proxies)
    response_data = response.json()

    if response_data:
        fed_url = federation_redirect_url(response_data)
        branding_data = get_branding(response_data)
        if not fed_url and not branding_data:
            assumption = "Brand does not use Microsoft and never has."
        elif not fed_url and branding_data:
            assumption = "Brand uses Microsoft with no federation redirects."
        elif fed_url and branding_data:
            assumption = f"Brand has used Microsoft in the past but migrated to - {slasher(fed_url)}"
        else:
            assumption = "Unknown brand status."

        final_data = {
            "federationredirecturl": fed_url,
            "federationredirecturlformatted": slasher(fed_url),
            "bannerlogo": branding_data.get("bannerlogo") if branding_data else None,  # Full URL
            "illustration": branding_data.get("illustration") if branding_data else None,  # Full URL
            "boilerplatetext": branding_data.get("boilerplatetext") if branding_data else None,
            "tilelogo": branding_data.get("tilelogo") if branding_data else None,  # Full URL
            "tiledarklogo": branding_data.get("tiledarklogo") if branding_data else None,  # Full URL
            "backgroundcolor": branding_data.get("backgroundcolor") if branding_data else None,
            "useridlabel": branding_data.get("useridlabel") if branding_data else None,
            "favicon": branding_data.get("favicon") if branding_data else None,  # Full URL
            "assumption": assumption
        }
        filename = f"{orgname}-{time.time()}.json"
        with open(filename, "w", encoding="utf8") as file:
            json.dump(final_data, file, indent=4)
        print(f"""
        Report for                    - {orgname}
        Federation Redirect Url       - {slasher(fed_url)}
        Banner Logo                   - {slasher(final_data['bannerlogo'])}
        Illustration                  - {slasher(final_data['illustration'])}
        Boilerplate Text              - {final_data["boilerplatetext"][:75] if final_data["boilerplatetext"] else 'N/A'}
        Tile Logo                     - {slasher(final_data['tilelogo'])}
        Tile Dark Logo                - {slasher(final_data['tiledarklogo'])}
        Background Color              - {final_data["backgroundcolor"]}
        User ID Label                 - {final_data["useridlabel"]}
        Favicon                       - {slasher(final_data['favicon'])}
        Final Assessment              - {assumption}
        """)

parser = argparse.ArgumentParser()
parser.add_argument("--domain",dest="domain", help="Pass in a domain using --domain to see the proxied tenant information, also saves to file", type=str)
args = parser.parse_args()
main_func(args.domain)
