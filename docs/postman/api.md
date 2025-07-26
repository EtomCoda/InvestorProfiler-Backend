Invest Guide
These routes define the major data flows in the application.
Collection Information

Name: Invest Guide
Description: These routes define the major data flows in the application
Schema: https://schema.getpostman.com/json/collection/v2.1.0/collection.json
Postman ID: bd0dca4e-becb-4c52-8722-5cfbda986ce5
Exporter ID: 34198340

Routes
1. Post Question Results

Method: POST
URL: 127.0.0.1:8000/core/risk-profile-form/submit/
Description: This sends the option IDs to the server, which are then used to calculate the risk profile. The server processes the request and returns a JSON response containing the risk profile name and description.
Request Body:{
    "option_ids": [3,7,9,15,18,21,25]
}


Response:
Status: OK
Code: 200
Headers:
Date: Sat, 26 Jul 2025 14:38:28 GMT
Server: WSGIServer/0.2 CPython/3.12.10
Content-Type: application/json
X-Frame-Options: DENY
Content-Length: 154
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin


Body:{
    "profile": "Moderately Aggressive",
    "description": "You are willing to accept higher risk and volatility for the potential of higher long-term returns."
}





2. Get Fund Profile

Method: GET
URL: 127.0.0.1:8000/funds/get-fund-profile
Description: This gets the matching funds for the user's risk appetite.
Response:
Status: OK
Code: 200
Headers:
Date: Sat, 26 Jul 2025 14:25:09 GMT
Server: WSGIServer/0.2 CPython/3.12.10
Content-Type: application/json
X-Frame-Options: DENY
Content-Length: 18937
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin


Body:{
    "Conservative": [
        {
            "category": "Cash/Money Market Funds",
            "percent": "30.00",
            "funds": [
                ["AXA Mansard Money Market Fund", "2.80"],
                ["FBN Money Market Fund", "4.60"],
                ["Stanbic IBTC Money Market Fund", "4.50"],
                ["ValuAlliance Money Market Fund", "4.35"],
                ["EDC Money Market Class B", "4.15"],
                ["Cordros Money Market Fund", "3.95"],
                ["Abacus Money Market Fund", "3.85"],
                ["PACAM Money Market Fund", "3.60"],
                ["Core Investment Money Market Fund", "3.55"],
                ["Coronation Money Market Fund", "3.50"],
                ["NOVA Prime Money Market Fund", "3.50"],
                ["Stanbic IBTC Money Market Fund**", "2.25"],
            ]
        },
        {
            "category": "Fixed Income Funds",
            "percent": "50.00",
            "funds": [
                ["Lead Fixed Income Fund", "3.00"],
                ["Stanbic IBTC Income Fund", "5.00"],
                ["Zenith Income Fund", "4.00"],
                ["Legacy USD Bond Fund", "4.00"],
                ["Nigeria Eurobond Fund", "3.50"],
                ["Coral Income Fund", "3.55"],
                ["Coronation Fixed Income Fund", "3.55"],
                ["EDC Nigeria Fixed Income Fund", "3.50"],
                ["Lead Fixed Income Fund", "3.50"],
                ["Vantage Guaranteed Income Fund", "3.50"],
                ["FBN Nigeria Eurobond (USD) Fund - Institutional", "3.00"],
            ]
        },
        {
            "category": "Large Cap Equity Funds",
            "percent": "20.00",
            "funds": [
                ["United Capital Equity Fund", "4.50"],
                ["Afrinvest Equity Fund", "3.00"],
                ["FBN Nigeria Smart Beta Equity Fund", "3.00"],
                ["Legacy Equity Fund", "3.00"],
                ["Pacam Equity Fund", "3.00"],
                ["Stanbic IBTC Nigerian Equity Fund", "3.00"],
                ["Vantage Equity Income Fund", "3.00"],
                ["AXA Mansard Equity Income Fund", "2.50"],
                ["Anchoria Equity Fund", "2.50"],
                ["Meristem Equity Market Fund", "2.50"],
                ["Paramount Equity Fund", "2.50"],
                ["Zenith Equity Fund", "2.50"]
            ]
        }
    ],
    "Moderately Conservative": [
        {
            "category": "Cash/Money Market Funds",
            "percent": "10.00",
            "funds": [
                ["AXA Mansard Money Market Fund", "2.80"],
                ["FBN Money Market Fund", "4.60"],
                ["Stanbic IBTC Money Market Fund", "4.50"],
                ["ValuAlliance Money Market Fund", "4.35"],
                ["EDC Money Market Class B", "4.15"],
                ["Cordros Money Market Fund", "3.95"],
                ["Abacus Money Market Fund", "3.85"],
                ["PACAM Money Market Fund", "3.60"],
                ["Core Investment Money Market Fund", "3.55"],
                ["Coronation Money Market Fund", "3.50"],
                ["NOVA Prime Money Market Fund", "3.50"],
                ["Stanbic IBTC Money Market Fund**", "2.25"],
            ]
        },
        {
            "category": "Fixed Income Funds",
            "percent": "50.00",
            "funds": [
                ["Lead Fixed Income Fund", "3.00"],
                ["Stanbic IBTC Income Fund", "5.00"],
                ["Zenith Income Fund", "4.00"],
                ["Legacy USD Bond Fund", "4.00"],
                ["Nigeria Eurobond Fund", "3.50"],
                ["Coral Income Fund", "3.55"],
                ["Coronation Fixed Income Fund", "3.55"],
                ["EDC Nigeria Fixed Income Fund", "3.50"],
                ["Lead Fixed Income Fund", "3.50"],
                ["Vantage Guaranteed Income Fund", "3.50"],
                ["FBN Nigeria Eurobond (USD) Fund - Institutional", "3.00"],
            ]
        },
        {
            "category": "Large Cap Equity Funds",
            "percent": "35.00",
            "funds": [
                ["United Capital Equity Fund", "4.50"],
                ["Afrinvest Equity Fund", "3.00"],
                ["FBN Nigeria Smart Beta Equity Fund", "3.00"],
                ["Legacy Equity Fund", "3.00"],
                ["Pacam Equity Fund", "3.00"],
                ["Stanbic IBTC Nigerian Equity Fund", "3.00"],
                ["Vantage Equity Income Fund", "3.00"],
                ["AXA Mansard Equity Income Fund", "2.50"],
                ["Anchoria Equity Fund", "2.50"],
                ["Meristem Equity Market Fund", "2.50"],
                ["Paramount Equity Fund", "2.50"],
                ["Zenith Equity Fund", "2.50"]
            ]
        },
        {
            "category": "Small Cap Equity Funds",
            "percent": "5.00",
            "funds": []
        }
    ],
    "Moderate": [
        {
            "category": "Cash/Money Market Funds",
            "percent": "5.00",
            "funds": [
                ["AXA Mansard Money Market Fund", "2.80"],
                ["FBN Money Market Fund", "4.60"],
                ["Stanbic IBTC Money Market Fund", "4.50"],
                ["ValuAlliance Money Market Fund", "4.35"],
                ["EDC Money Market Class B", "4.15"],
                ["Cordros Money Market Fund", "3.95"],
                ["Abacus Money Market Fund", "3.85"],
                ["PACAM Money Market Fund", "3.60"],
                ["Core Investment Money Market Fund", "3.55"],
                ["Coronation Money Market Fund", "3.50"],
                ["NOVA Prime Money Market Fund", "3.50"],
                ["Stanbic IBTC Money Market Fund**", "2.25"],
            ]
        },
        {
            "category": "Fixed Income Funds",
            "percent": "35.00",
            "funds": [
                ["Lead Fixed Income Fund", "3.00"],
                ["Stanbic IBTC Income Fund", "5.00"],
                ["Zenith Income Fund", "4.00"],
                ["Legacy USD Bond Fund", "4.00"],
                ["Nigeria Eurobond Fund", "3.50"],
                ["Coral Income Fund", "3.55"],
                ["Coronation Fixed Income Fund", "3.55"],
                ["EDC Nigeria Fixed Income Fund", "3.50"],
                ["Lead Fixed Income Fund", "3.50"],
                ["Vantage Guaranteed Income Fund", "3.50"],
                ["FBN Nigeria Eurobond (USD) Fund - Institutional", "3.00"],
            ]
        },
        {
            "category": "Large Cap Equity Funds",
            "percent": "50.00",
            "funds": [
                ["United Capital Equity Fund", "4.50"],
                ["Afrinvest Equity Fund", "3.00"],
                ["FBN Nigeria Smart Beta Equity Fund", "3.00"],
                ["Legacy Equity Fund", "3.00"],
                ["Pacam Equity Fund", "3.00"],
                ["Stanbic IBTC Nigerian Equity Fund", "3.00"],
                ["Vantage Equity Income Fund", "3.00"],
                ["AXA Mansard Equity Income Fund", "2.50"],
                ["Anchoria Equity Fund", "2.50"],
                ["Meristem Equity Market Fund", "2.50"],
                ["Paramount Equity Fund", "2.50"],
                ["Zenith Equity Fund", "2.50"]
            ]
        },
        {
            "category": "Small Cap Equity Funds",
            "percent": "10.00",
            "funds": []
        }
    ],
    "Moderately Aggressive": [
        {
            "category": "Cash/Money Market Funds",
            "percent": "5.00",
            "funds": [
                ["AXA Mansard Money Market Fund", "2.80"],
                ["FBN Money Market Fund", "4.60"],
                ["Stanbic IBTC Money Market Fund", "4.50"],
                ["ValuAlliance Money Market Fund", "4.35"],
                ["EDC Money Market Class B", "4.15"],
                ["Cordros Money Market Fund", "3.95"],
                ["Abacus Money Market Fund", "3.85"],
                ["PACAM Money Market Fund", "3.60"],
                ["Core Investment Money Market Fund", "3.55"],
                ["Coronation Money Market Fund", "3.50"],
                ["NOVA Prime Money Market Fund", "3.50"],
                ["Stanbic IBTC Money Market Fund**", "2.25"],
            ]
        },
        {
            "category": "Fixed Income Funds",
            "percent": "15.00",
            "funds": [
                ["Lead Fixed Income Fund", "3.00"],
                ["Stanbic IBTC Income Fund", "5.00"],
                ["Zenith Income Fund", "4.00"],
                ["Legacy USD Bond Fund", "4.00"],
                ["Nigeria Eurobond Fund", "3.50"],
                ["Coral Income Fund", "3.55"],
                ["Coronation Fixed Income Fund", "3.55"],
                ["EDC Nigeria Fixed Income Fund", "3.50"],
                ["Lead Fixed Income Fund", "3.50"],
                ["Vantage Guaranteed Income Fund", "3.50"],
                ["FBN Nigeria Eurobond (USD) Fund - Institutional", "3.00"],
                ["Legacy Debt(formerly Short Maturity) Fund", "3.00"],
            ]
        },
        {
            "category": "Large Cap Equity Funds",
            "percent": "65.00",
            "funds": [
                ["United Capital Equity Fund", "4.50"],
                ["Afrinvest Equity Fund", "3.00"],
                ["FBN Nigeria Smart Beta Equity Fund", "3.00"],
                ["Legacy Equity Fund", "3.00"],
                ["Pacam Equity Fund", "3.00"],
                ["Stanbic IBTC Nigerian Equity Fund", "3.00"],
                ["Vantage Equity Income Fund", "3.00"],
                ["AXA Mansard Equity Income Fund", "2.50"],
                ["Anchoria Equity Fund", "2.50"],
                ["Meristem Equity Market Fund", "2.50"],
                ["Paramount Equity Fund", "2.50"],
                ["Zenith Equity Fund", "2.50"]
            ]
        },
        {
            "category": "Small Cap Equity Funds",
            "percent": "15.00",
            "funds": []
        }
    ],
    "Aggressive": [
        {
            "category": "Cash/Money Market Funds",
            "percent": "5.00",
            "funds": [
                ["AXA Mansard Money Market Fund", "2.80"],
                ["FBN Money Market Fund", "4.60"],
                ["Stanbic IBTC Money Market Fund", "4.50"],
                ["ValuAlliance Money Market Fund", "4.35"],
                ["EDC Money Market Class B", "4.15"],
                ["Cordros Money Market Fund", "3.95"],
                ["Abacus Money Market Fund", "3.85"],
                ["PACAM Money Market Fund", "3.60"],
                ["Core Investment Money Market Fund", "3.55"],
                ["Coronation Money Market Fund", "3.50"],
            ]
        },
        {
            "category": "Fixed Income Funds",
            "percent": "0.00",
            "funds": [
                ["Lead Fixed Income Fund", "3.00"],
                ["Stanbic IBTC Income Fund", "5.00"],
                ["Zenith Income Fund", "4.00"],
                ["Legacy USD Bond Fund", "4.00"],
                ["Nigeria Eurobond Fund", "3.50"],
                ["Coral Income Fund", "3.55"],
                ["Coronation Fixed Income Fund", "3.55"],
                ["EDC Nigeria Fixed Income Fund", "3.50"],
                ["Lead Fixed Income Fund", "3.50"],
                ["Vantage Guaranteed Income Fund", "3.50"],

            ]
        },
        {
            "category": "Large Cap Equity Funds",
            "percent": "70.00",
            "funds": [
                ["United Capital Equity Fund", "4.50"],
                ["Afrinvest Equity Fund", "3.00"],
                ["FBN Nigeria Smart Beta Equity Fund", "3.00"],
                ["Legacy Equity Fund", "3.00"],
                ["Pacam Equity Fund", "3.00"],
                ["Stanbic IBTC Nigerian Equity Fund", "3.00"],
                ["Vantage Equity Income Fund", "3.00"],
                ["AXA Mansard Equity Income Fund", "2.50"],
                ["Anchoria Equity Fund", "2.50"],
                ["Meristem Equity Market Fund", "2.50"],
                ["Paramount Equity Fund", "2.50"],
                ["Zenith Equity Fund", "2.50"]
            ]
        },
        {
            "category": "Small Cap Equity Funds",
            "percent": "20.00",
            "funds": []
        },
        {
            "category": "REITs and/or Infrastructure Funds",
            "percent": "5.00",
            "funds": [
                ["Lead Balanced Fund", "3.00"],
                ["ARM Aggressive Growth Fund", "4.00"],
                ["ARM Discovery Fund", "4.00"],
                ["Cordros Milestone Fune 2023", "4.00"],
                ["Nigeria Energy Sector Fund", "4.00"],
                ["Vantage Dollar Fund", "4.00"],
                ["United Capital Growthd Fund", "3.50"],
                ["Stanbic IBTC Dollar Fund", "3.50"],
                ["Women Investment Fund", "3.50"],
                ["Coral Growth Fund", "3.85"],
                ["Vantage Growthd Fund", "3.60"],
                ["Cordros Milestone Fune 2028", "3.50"]
            ]
        }
    ]
}





3. Get Ranked Funds

Method: GET
URL: 127.0.0.1:8000/funds/get-fund-profile
Description: This request pulls present funds from the database, ranked in order of most favorable to least favorable and displays them.
Response:
Status: OK
Code: 200
Headers:
Date: Sat, 26 Jul 2025 14:33:25 GMT
Server: WSGIServer/0.2 CPython/3.12.10
Content-Type: application/json
X-Frame-Options: DENY
Content-Length: 18937
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin


Body: (Same as the "Get Fund Profile" response body, as it retrieves the same fund profile data.)


