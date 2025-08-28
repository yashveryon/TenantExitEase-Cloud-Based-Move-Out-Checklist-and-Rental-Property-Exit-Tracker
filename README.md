# TenantExitEase-Cloud-Based-Move-Out-Checklist-and-Rental-Property-Exit-Tracker

TenantExitEase is a **cloud-powered, automated tenant exit management system** designed to streamline the process of **tenant move-outs** for landlords, property managers, and real estate companies. The platform eliminates the manual paperwork, delays, and communication gaps involved in tenant exits by offering **digital request submission, real-time status tracking, document handling, and automated notifications**.  

With its **interactive admin dashboard** and **AWS-backed serverless architecture**, TenantExitEase ensures **faster, more transparent, and error-free move-out processes**, benefiting both tenants and property managers.  

---

## 🌟 Key Features  

### For Tenants  
- **Digital Move-Out Requests:** Tenants can request a move-out online without physical visits.  
- **Document Uploads:** All required exit documents can be uploaded in one place.  
- **Real-Time Status Tracking:** Tenants can check the status of their request anytime.  
- **Automated Notifications:** Get instant updates on approvals, inspections, and final settlements.  

### For Admins & Property Managers  
- **Interactive Admin Dashboard:**  
  - View all tenant exit requests in one place.  
  - Filter, sort, and search for quick access.  
  - Approve/reject requests with a single click.  
  - Visualize request statistics using charts & graphs.  
- **Automated Workflows:** Notifications and updates are triggered automatically.  
- **Centralized Data Management:** All requests and documents stored securely in the cloud.  

---

## 🏢 Business Use Case  

- **Property Management Companies:** Streamline operations, reduce manual errors, and improve tenant satisfaction.  
- **Individual Landlords:** Manage multiple properties and tenant exits efficiently without additional staff.  
- **Real Estate Firms:** Integrate with existing property portals to offer end-to-end property lifecycle management.  

TenantExitEase saves **time**, **reduces costs**, and ensures **transparency** by replacing manual, paper-based exit processes with an **automated digital solution**.  

---

## ⚙️ Tech Stack  

- **Frontend:** HTML, CSS, JavaScript (Interactive UI with `admin.html` & `admin.js`)  
- **Backend:** AWS Lambda (Serverless Functions)  
- **Database:** AWS DynamoDB (NoSQL)  
- **API Management:** AWS API Gateway  
- **Authentication:** AWS Cognito (optional)  
- **Notifications:** AWS SNS (SMS/Email)  
- **Hosting:** AWS S3 for frontend hosting, AWS Amplify (optional) for CI/CD  

---

## 🏗️ System Architecture  

1. **Tenant Portal:** For move-out requests & document uploads.  
2. **Admin Dashboard:** For reviewing, approving, and managing requests.  
3. **Serverless Backend:** APIs via AWS Lambda & API Gateway handle all requests.  
4. **Database Layer:** DynamoDB stores tenant details, requests, and documents.  
5. **Notification Service:** AWS SNS sends real-time updates.  

---

