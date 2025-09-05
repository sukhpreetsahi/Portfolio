## SecureCart – Flask Web Application with CI/CD and Security Testing.

This project is a secure, full-stack, containerised Flask-based e-commerce web application developed as part of my Cyber Context of Software Engineering module coursework. 

It integrates secure coding practices, automated testing, and CI/CD deployment pipelines, allowing security practices to be incorporated during development rather than after, thereby classifying the project as DevSecOps.

---
The web application is a simple e-commerce website and is created using both a back-end and a front-end, along with a connected SQL database.  

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
    -e SECRET_KEY=90c519ae5f6939826bb52e0a678ef0f03ca54b8417152857 \
    --name securecart sukhpreetsahi5/securecart-app:latest
   
3. Open the app using this URL in a browser:\
  http://localhost:5000

4. OWASP ZAP Scan:
   Open ZAP and pass in the URL in step 3 to perform the scan on it.

Note:
This is a sample testing scenario, hence the secret key is provided here. The secret key would be kept hidden otherwise.

## Website Screenshot

<img width="1913" height="949" alt="image" src="https://github.com/user-attachments/assets/d6da70e2-2e87-4d86-9c4f-0ac9444d67ff" />
