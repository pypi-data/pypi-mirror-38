 =============================
 ThreatBook Resource Storage SDK for Python
 =============================

 ------------------------
 INTRODUCTION
 -------------------------

 This release provides access to the corresponding functionality through
 both public API_KEY and private API_KEY.


 The public API_KEY can access the file detection function of the cloud
 sandbox. You need to register for a ThreatBook online account and view
 your API Key through the Personal Center, which will be used for all your
 API operations without submitting via the web, uploading the file/URL for
 analysis and extracting the completed analysis. Report data. The
 ThreatBook Online Sandbox API is a free service available for free websites
 and programs. Please do not use the API for any commercial product or
 service, as an alternative to an anti-virus product, or for any project that
 may directly or indirectly damage the anti-virus industry.


The private API_KEY provides an easy way to invoke data from the
Threat Analytics Platform database and its detection and analysis
capabilities from any client. It includes the following functions:
file digital signature identification, new registered domain query,
email registration information query, domain analysis, IOC detection,
IP analysis, IP reputation query, etc. As our business customer or partner,
we will deliver your corresponding apikey by mail.


 ----------------------------
 Directory structure
 ----------------------------
├── LICENSE
├── MANIFEST.in
├── my_api
│   ├── domain_analysis.py
│   ├── domain_query.py
│   ├── email_query.py
│   ├── fetch_file_legal_ca.py
│   ├── file.py
│   ├── __init__.py
│   ├── ioc.py
│   ├── ip_analysis.py
│   └── ip_reputation.py
├── README.rst
└── setup.py

 --------------------------
 Example
 --------------------------
This is an example:

    # import domain analysis
    from my_api import  domain_analysis

    # create Create an instance object
    test = domain_analysis.DomainAnalysis('your private api_key')

    # Get the current whois information of the domain
    info = test.get_cur_whois('domain to be queried  ')
    print(info)





