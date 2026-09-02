# SecureCart – Flask Web Application with CI/CD and Security Testing

This project is a secure, full-stack, containerised Flask-based e-commerce web application developed as part of my Cyber Context of Software Engineering module coursework. 

It integrates secure coding practices, automated testing, and CI/CD deployment pipelines, allowing security practices to be incorporated during development rather than after, thereby classifying the work as part of a Secure SDLC.

---
The web application is a simple e-commerce website and is created using both back-end and front-end, along with a connected SQL database.  

The website has been developed using HTML for templates, JavaScript for interactive components, CSS for styling and Python for the back-end.  

The website allows users to sign up or log in, manages inventory correctly and has incorporated role-based access controls to ensure only the admin can access the admin dashboard.  

The website uses sessions and enforces a strong password policy.

---
The CI/CD pipelines integrate SAST and SCA by running Snyk open-source and code tests.
Secrets are managed securely by GitHub secrets.
The CI stage performs checks on code, including a SAST and SCA scan with Snyk.
OWASP ZAP can be used manually for dynamic testing before deployment.
The CD stage deploys a Docker image into Docker Hub for local hosting.

---
The following are needed to test the CI/CD Pipeline and the web application.
- Docker
- GitHub Actions
- Snyk
- OWASP ZAP

---
The Docker image is built and pushed by GitHub Actions. You can run it locally using the following steps.
Before these steps, the GitHub workflow should have been completed and should have a green tick.

1. Pull the Docker image:\
  docker pull sukhpreetsahi5/securecart-app:latest

2. Run the container with the required secret:\
  docker run -d -p 5000:5000 \
    -e SECRET_KEY=############################### \   # Commented out for security purposes.
    --name securecart sukhpreetsahi5/securecart-app:latest
   
3. Open the app using this URL in a browser:\
  http://localhost:5000

4. OWASP ZAP Scan:
   Open ZAP and pass in the URL in step 3 to perform the scan on it.

Note:
This is a sample testing scenario, hence the secret key is provided here. The secret key would be kept hidden otherwise.

## Website Screenshots
<img width="1908" height="751" alt="Login page" src="https://github.com/user-attachments/assets/dbf4b5a7-4045-4c33-8021-d531436a4133" />
<img width="1911" height="701" alt="Viewing cart" src="https://github.com/user-attachments/assets/a31fd0ef-ea6b-4059-9ea4-2965a6b858d3" />
<img width="1334" height="354" alt="Viewing Own Orders" src="https://github.com/user-attachments/assets/152fd12c-16b4-4862-8b04-fc4cdb17c560" />
<img width="1328" height="438" alt="Editing Product Details" src="https://github.com/user-attachments/assets/ccfaf0a5-d8d1-4ae9-a8c1-bc93d30dfe48" />
<img width="640" height="811" alt="Checkout page" src="https://github.com/user-attachments/assets/b1485093-3b0d-477e-aa90-7fcb25bc672a" />
<img width="510" height="351" alt="Editing Password" src="https://github.com/user-attachments/assets/b7d01747-cf0b-4ef3-8cc1-3b587a4574e1" />
<img width="940" height="872" alt="Password requirements being met" src="https://github.com/user-attachments/assets/a5781d02-7f0f-4a98-a3da-652abb6eff1f" />


