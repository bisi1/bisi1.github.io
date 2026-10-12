Azure Function: sendEmail

This Azure Function accepts POST requests with JSON { name, email, message } and sends an email to the configured recipient using Mailjet.

Setup

1. Create a Mailjet account and an API key/secret.
2. Set the following Application Settings in your Function App (or local.settings.json for local testing):
   - MAILJET_API_KEY: your Mailjet API key
   - MAILJET_API_SECRET: your Mailjet API secret
   - FROM_EMAIL: verified sender address used by Mailjet
   - TO_EMAIL: private recipient address for website enquiries

Local testing

- Copy `local.settings.json.example` to `local.settings.json` and fill in your values (DO NOT commit `local.settings.json` with secrets).
- Install dependencies and run the function locally with the Azure Functions Core Tools:

  npm install
  func start

Deployment (Azure)

- Deploy the function app using the Azure Functions Core Tools or CI/CD. Example using the Core Tools:

  func azure functionapp publish <APP_NAME>

- Make sure the Function App's Application Settings include the MAILJET_API_KEY and MAILJET_API_SECRET.

Security

- Keep your Mailjet keys secret; use Azure Application Settings (not in repo).
- Consider rate-limiting or spam protections if the site will receive high traffic.

Endpoint

Once deployed, the HTTP endpoint will be:
  https://<YOUR_FUNCTION_APP>.azurewebsites.net/api/sendEmail

From the static site, the contact form posts JSON to `/api/sendEmail` (same origin when hosted together) — ensure CORS is configured if hosting separately.
