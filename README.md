Tenant OSINT.

Description:
This script will pull information associated with a domain from a Microsoft API including but not limited to, banner logo, background image, background color, favicon, and external redirect URL.

Explanation of key data:
Federation Redirect URL - If this value exists, when a user logs into Microsoft it will redirect them to an external page, usually okta.
Banner Logo - Logo of the brand.
Illustration - Background of the tenant's login page.
Boilerplate Text - Text shown below the login box, usually along the lines of - "Unauthorized access is a violation of the law."
Favicon - Link to the sites Favicon.
Assumption - A pre-defined assumption based on the data found, due to the many configurations and uses of a Microsoft tenant this was easiest to hardcode.

Possible Assumption Outcomes:
"Brand does not use Microsoft and never has." - No redirect URL was found, and no branding was found.
"Brand uses Microsoft with no federation redirects." - No redirect URL was found, and branding was found.
"Brand has used Microsoft in the past but migrated to - {{External Redirect URL}}" - Redirect URL was found, and branding was found.

Uses:
Initial investigation to determine the official login page.
Output data can be utilized to create a realistic phishing page using official branding.
more!

Comments:
This script was designed to aid pentests using publicly accessible information, but could also be utilized to output statistical information about what companies use what configurations.
