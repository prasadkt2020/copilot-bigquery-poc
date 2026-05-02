# Identity‑Driven, Zero‑Trust Data Access via Copilot, Entra ID, Cloud Run, and BigQuery

**1. Overview**

This project demonstrates a fully secure, identity‑driven architecture that enables a Sales Rep to retrieve business data from BigQuery directly from Microsoft Teams, without exposing databases, credentials, or backend systems. The solution uses Teams, a custom Copilot Agent, Entra ID OAuth2, a Cloud Run API, and BigQuery to create a zero‑trust, least‑privilege data access pipeline. All components run on free‑tier cloud services, making this an accessible yet enterprise‑grade reference implementation.

**2. Scope**

This demo showcases the complete, secure journey of a Sales Rep asking a question in Teams and receiving data from BigQuery through a hardened, identity‑validated API. When the user interacts with Teams, the message is routed to a Copilot Agent, which obtains an Entra ID–issued JWT token and securely calls a Cloud Run API. Cloud Run validates the token, uses its own service account identity to query BigQuery, and returns only authorized data back to Copilot, which formats the response for the user. The scope includes the end‑to‑end flow, identity enforcement, secure API mediation, BigQuery access via service accounts, and auditability, all implemented using free‑tier cloud components.

**3. Architecture Summary**

Code
Sales Rep (Teams)
        │
        ▼
Teams App (Copilot Entry Point)
        │
        ▼
Copilot Agent (Copilot Studio)
        │  Entra ID OAuth2 Token Request
        ▼
Entra ID (JWT Issuance)
        │  Authorization: Bearer <token>
        ▼
Cloud Run API (Token Validation)
        │  Service Account Identity
        ▼
BigQuery (Dataset + Table)
        │
        ▼
Cloud Run → Copilot → Teams (Response)

**4. Security Model**

**Zero‑Trust Principles
Identity is the boundary — Entra ID issues and Cloud Run validates all tokens.

Least privilege — Only the Cloud Run service account can access BigQuery.

No direct database access — Teams, Copilot, and users never touch BigQuery.

No secrets in clients — All credentials remain server‑side.

Auditability — Cloud Run and BigQuery logs capture all activity.

Key Security Components
Layer	Security Function
Teams	UI only; no data access
Copilot Agent	Authenticated client; obtains Entra ID token
Entra ID	Issues signed JWT access tokens
Cloud Run	Validates tokens; enforces zero‑trust boundary
Service Account	Server‑side identity for BigQuery access
BigQuery IAM	Dataset/table access restricted to service account


**5. End‑to‑End User Journey (Sales Rep Experience)**
1. Sales Rep asks a question in Teams
Example:

“Show me my customer orders for today.”

2. Teams routes the message to the Copilot Agent
Teams acts only as the UI surface.

3. Copilot Agent interprets the request
It determines that it must call the backend API.

4. Copilot obtains an Entra ID access token
It requests a JWT for the Cloud Run API scope.

5. Copilot calls the Cloud Run API
It sends:

Code
Authorization: Bearer <JWT>
GET /list

6. Cloud Run validates the token
Signature

Issuer

Audience

Expiry

If valid → proceed.

7. Cloud Run queries BigQuery using its service account
BigQuery trusts only this identity.

8. Cloud Run returns results to Copilot
Example data:

Code
Alice – 100
Bob – 200
Charlie – 300
9. Copilot formats the response for Teams
The Sales Rep sees a clean, conversational answer.

**6. Components Implemented**
Component	Status
Cloud Run API	✔ Done
BigQuery Dataset + Table	✔ Done
Sample Data	✔ Done
/test Endpoint	✔ Done
/list Endpoint	✔ Done
Copilot Agent	Pending
Teams App Manifest	Pending
Entra ID App Registration	Pending
Audit Logging Review	Pending


**7. What This Demo Proves**
Teams can securely access enterprise data without direct database connectivity.

Copilot can act as a secure, identity‑aware client.

Entra ID tokens can protect APIs hosted on Cloud Run.

Cloud Run can securely access BigQuery using service accounts.

Zero‑trust, least‑privilege patterns can be implemented using only free‑tier cloud components.

**8. Ideal Use Cases**
Secure enterprise data access from Teams

Copilot‑powered business insights

Zero‑trust API architectures

Identity‑driven data access patterns

Cloud Run + BigQuery integration demos

Internal POCs for AI‑assisted workflows
