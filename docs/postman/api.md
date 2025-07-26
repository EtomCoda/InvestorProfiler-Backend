
#  InvestProfiler – API Documentation

These routes define the major data flows in the **Invest Guide** application.

---

###  Collection Information

- **Name**: InvestProfiler  
- **Description**: These routes define the major data flows in the application  
- **Schema**: [Postman Schema v2.1.0](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)  
- **Postman ID**: `bd0dca4e-becb-4c52-8722-5cfbda986ce5`  
- **Exporter ID**: `34198340`

---

##  Routes

### 1. **Submit Question Results**

- **Method**: `POST`  
- **URL**: `http://127.0.0.1:8000/core/risk-profile-form/submit/`  
- **Description**: Sends selected option IDs to the server to calculate the user's investment risk profile. Returns a profile name and description.

####  Request Body
```json
{
  "option_ids": [3, 7, 9, 15, 18, 21, 25]
}
```

####  Response
- **Status**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "profile": "Moderately Aggressive",
  "description": "You are willing to accept higher risk and volatility for the potential of higher long-term returns."
}
```

---

### 2. **Get Fund Profile**

- **Method**: `GET`  
- **URL**: `http://127.0.0.1:8000/funds/get-fund-profile`  
- **Description**: Fetches recommended funds based on the user's risk appetite.

####  Response
- **Status**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "Moderately Aggressive": [
    {
      "category": "Large Cap Equity Funds",
      "percent": "65.00",
      "funds": [
      ["United Capital Equity Fund", "4.50"],
      ["Afrinvest Equity Fund", "3.00"],
      ["ValuAlliance Money Market Fund", "4.35"],
      ["EDC Money Market Class B", "4.15"],
      ["Cordros Money Market Fund", "3.95"],
      ["Abacus Money Market Fund", "3.85"],
      ["PACAM Money Market Fund", "3.60"],
      ["Core Investment Money Market Fund", "3.55"],
      ["Coronation Money Market Fund", "3.50"],
      ["NOVA Prime Money Market Fund", "3.50"],
      ["Stanbic IBTC Money Market Fund", "2.25"],
  ]
}
```

> **Note**: The full response includes detailed fund breakdowns for all risk profiles.

---

### 3. **Get Ranked Funds**

- **Method**: `GET`  
- **URL**: `http://127.0.0.1:8000/funds/get-fund-profile`  
- **Description**: Returns all present funds, ranked from most favorable to least favorable based on custom scoring logic.

####  Response
- **Status**: `200 OK`
- **Content-Type**: `application/json`

```json
{
    "Conservative": [
        {
            "category": "Cash/Money Market Funds",
            "percent": "30.00",
            "funds": [
                [
                    " AXA Mansard Money Market Fund ",
                    "2.80"
                ],
                [
                    "FBN Money Market Fund",
                    "4.60"
                ],
                [
                    "Stanbic IBTC Money Market Fund",
                    "4.50"
                ],
                [
                    "ValuAlliance Money Market Fund",
                    "4.35"
                ],
                [
                    "EDC Money Market Class B",
                    "4.15"
                ],
                [
                    "Cordros Money Market Fund",
                    "3.95"
                ],
                [
                    "Abacus Money Market Fund",
                    "3.85"
                ],
                [
                    "PACAM Money Market Fund",
                    "3.60"
                ],
                [
                    "Core Investment Money Market Fund",
                    "3.55"
                ],
                [
                    "Coronation Money Market Fund",
                    "3.50"
                ],
                [
                    "NOVA Prime Money Market Fund",
                    "3.50"
                ],
                [
                    "Stanbic IBTC Money Market Fund**",
                    "2.25"
                ],
                [
                    "AIICO Money Market Fund",
                    "2.25"
                ],
                [
                    "AIICO money market fund",
                    "2.15"
                ],
                [
                    "United Capital Money Market Fund",
                    "2.05"
                ],
                [
                    "GDL Money Market Fund",
                    "2.00"
                ],
                [
                    "ARM Money Market Fund",
                    "1.65"
                ],
                [
                    "Coral Money Market Fund",
                    "1.55"
                ],
                [
                    "Trustbanc Money Market Fund",
                    "2.90"
                ],
                [
                    "Greenwich Plus Money Market",
                    "2.85"
                ],
                [
                    "Norrenberger Money Market Fund",
                    "2.85"
                ],
                [
                    "AXA Mansard Money Market Fund",
                    "2.80"
                ],
                [
                    "AIICO Money market fund",
                    "2.80"
                ],
                [
                    "Legacy Money Market Fund",
                    "2.80"
                ],
                [
                    "Zenith Money Market Fund",
                    "2.80"
                ],
                [
                    "Coral Money Market Fund (FSDH Treasury Bill Fund)",
                    "2.75"
                ],
                [
                    "Coral Money Market Fund(FSDH Treasury Bill Fund)",
                    "2.75"
                ],
                [
                    "Emerging Africa Money Market Fund",
                    "2.65"
                ],
                [
                    "Chapel Hill Denham Money Market Fund(Frml NGIF)",
                    "2.60"
                ],
                [
                    "Vetiva Money Market Fund",
                    "2.55"
                ],
                [
                    "First Allay Asset Management Money Market Fund",
                    "2.50"
                ],
                [
                    "Meristem Money Market Fund",
                    "2.40"
                ],
                [
                    "Chapel Hill Denham Money Market Fund",
                    "2.25"
                ],
                [
                    "Greenwich PLUS (Money Market FUND)",
                    "2.25"
                ],
                [
                    "FAAM Money Market Fund",
                    "2.15"
                ],
                [
                    "EDC Money Market ClassA",
                    "2.05"
                ],
                [
                    "Anchoria Money Market Fund",
                    "1.65"
                ],
                [
                    "UBA Money Market Fund",
                    "1.55"
                ]
            ]
```

---

###  Headers (For All Routes)

These headers are generally included in responses:

```
Date: [Timestamp]
Server: WSGIServer/0.2 CPython/3.12.10
Content-Type: application/json
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
```
