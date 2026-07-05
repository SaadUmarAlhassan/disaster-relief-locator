**🚨 Disaster Relief Resource Locator**  
A serverless, event-driven web application designed to provide real-time tracking of critical life-saving resources (shelters, food, medical) during natural disasters. Built with a decoupled architecture to ensure high availability and automatic scaling when communities need it most.  
 
**📖 Business Problem & Solution**  
**The Problem:** During sudden disasters (hurricanes, earthquakes), traditional centralized servers often crash under the sudden spike in traffic from citizens seeking help. Furthermore, emergency responders need a way to dynamically register new resource points (e.g., a tent city erected overnight) without waiting for IT deployments.  
   
 **The Solution:** A 100% serverless application that scales to zero during "peace time" (costing fractions of a cent) but can instantly scale to handle millions of requests during a crisis.  
- **Admin Dashboard:** Allows responders to dynamically drop pins on a map, geocode addresses, and define custom resource types on the fly.  
- **Citizen Portal:** A mobile-first, lightweight interface that uses HTML5 Geolocation to show citizens nearby open shelters and provides one-click Google Maps navigation.  
   
**🏛️ Architecture Diagram**  
   
                      👤 Citizen / Admin Browser**  
                       /                     \  
                  HTTPS                  REST API/WebSocket  
                     |                           |  
           ☁️ CloudFront CDN         🔗 Amazon API Gateway  
                      |                           |  
        Origin Access Control                  |  
                      |                           |  
           🪣 Amazon S3 (Frontend)        ⚡ AWS Lambda (Python) 
                                                  |  
                                           PutItem / Scan  
                                                  |  
                                           🗄️ Amazon DynamoDB  
  
  
**🛠️ Technology Stack**  
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript (ES6+), Leaflet.js (OpenStreetMap)  
- **Backend:** Python 3.9 (AWS Lambda)  
- **Database:** Amazon DynamoDB (NoSQL, Single-Table Design)  
- **API:** Amazon API Gateway (REST API with CORS MOCK integration)  
- **Content Delivery:** Amazon CloudFront (CDN with Edge Functions for clean URLs)  
- **Infrastructure as Code:** Terraform (AWS Provider - 100% from scratch)
  
**☁️ AWS Well-Architected Framework Alignment**  
This project was designed with the five pillars of the AWS Well-Architected Framework in mind:  
**1. Operational Excellence**  
- **Infrastructure as Code:** 100% of the cloud resources are provisioned using Terraform, allowing for repeatable, version-controlled deployments.  
- **Observability:** AWS CloudWatch logs are enabled via Lambda execution roles for debugging and monitoring.  
**2. Security**  
- **Least Privilege Access:** The Lambda execution role is scoped strictly to only the specific DynamoDB table actions required (PutItem, Scan, etc.).  
- **S3 Security:** The frontend S3 bucket has public access fully blocked. Access is granted exclusively to CloudFront via Origin Access Control (OAC).  
- **No Root Credentials:** Local deployment utilizes a dedicated IAM user with programmatic access, rather than root account keys.
- 
**3. Reliability**  
- **Multi-AZ by Default:** By utilizing managed services (Lambda, DynamoDB, API Gateway), the application automatically benefits from AWS's multi-AZ redundancy.
- 
- **Decoupled Architecture:** The frontend (S3) is completely decoupled from the backend (API Gateway/Lambda). If the backend experiences issues, the frontend UI remains available.
- 
**4. Performance Efficiency**  
- **Edge Computing:** Utilized CloudFront Functions to execute URL rewriting (/citizen -> /citizen.html) at the edge location, reducing origin latency.  
- **Serverless Compute:** Lambda functions only spin up when an API request is made, ensuring zero idle compute resources.  
- **CDN Caching:** Static assets are cached globally at CloudFront edge locations for sub-millisecond load times.  
**5. Cost Optimization**  
- **Pay-Per-Use:** 100% Serverless architecture. DynamoDB uses On-Demand capacity. The application scales to zero, costing approximately $0.00 when not in use, making it highly viable for disaster scenarios where budget is a concern.
  
**🚀 Deployment Guide**  
**Prerequisites**  
- AWS CLI installed and configured with an IAM user's Access Keys.  
- Terraform CLI installed.  
- Python 3.9+ installed.  
**Step 1: Deploy Infrastructure (Terraform)**  
1. Navigate to the terraform/ directory.  
2. Update variables.tf to ensure frontend_bucket_name is globally unique.  
3. Initialize and apply the Terraform configuration:  
4. bash  
5. terraform init  
6. terraform apply -auto-approve  
7. Note the cloudfront_url and rest_api_url from the Terraform outputs.  
**Step 2: Configure & Deploy Frontend**  
1. Open frontend/index.html and frontend/citizen.html.  
2. Replace YOUR_REST_API_URL_HERE with the rest_api_url from Terraform.  
3. Upload the files to your newly created S3 bucket:  
4. bash  
5. aws s3 sync frontend/ s3:///  
**Step 3: Access the Application**  
- **Admin Dashboard:** Navigate to https://<cloudfront_url>/  
- **Citizen Portal:** Navigate to https://<cloudfront_url>/citizen (Edge function handles the routing).  
**🧠 Key Architectural Decisions & Troubleshooting**  
- **Dynamic Resource Types (Schemaless Design):** Instead of hardcoding resource types in a SQL database, I leveraged DynamoDB's schemaless design. The frontend uses an HTML   
- , allowing responders to invent new resource categories (e.g., "Animal Rescue") on the fly without backend migrations.  
- **CORS MOCK Integration:** To solve browser preflight 403 errors, I configured an OPTIONS method in API Gateway with a MOCK integration and strict request templates, returning the necessary CORS headers without invoking the Lambda function.  
- **DynamoDB Float Casting:** Resolved a 502 Bad Gateway error by identifying that boto3 requires explicit type casting for geospatial coordinates. Lat/Lng values are cast to strings before PutItem and reverted to floats during the Scan response for the frontend map.  
   
    
