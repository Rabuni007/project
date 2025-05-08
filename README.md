# Distributor Onboarding and Payment Confirmation Backend Service

## Assumptions
- The service is designed for a single organization managing multiple distributors.
- SQLite is used for simplicity; can be replaced with other databases for production.
- Payment confirmation is done via API call; integration with payment gateway is explained but not implemented.
- SAP integration is described conceptually.

## Setup Instructions
1. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Create a superuser (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```
6. Use the API endpoints with JWT authentication.

## API Endpoints
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/distributors/` - List distributors
- `POST /api/distributors/` - Onboard new distributor
- `GET /api/distributors/{id}/` - Get distributor details
- `PUT /api/distributors/{id}/` - Update distributor details
- `GET /api/payments/` - List payment records
- `POST /api/payments/` - Record a new payment
- `GET /api/payments/{id}/` - Get payment details
- `POST /api/payments/{id}/confirm/` - Confirm a payment

## Architecture / Design Decisions
- Django REST Framework for rapid API development.
- JWT authentication for secure API access.
- Models designed to capture distributor and payment details with metadata.
- Payment confirmation as a separate action on payment resource.
- SQLite for simplicity; can be replaced with PostgreSQL or others.
- Modular app structure for scalability.

## Integration Points

### SAP Integration
- Use SAP APIs or middleware to sync distributor and payment data.
- Implement periodic batch jobs or event-driven sync using SAP connectors.
- Ensure data consistency and error handling during sync.

### Cashfree (Payment Gateway) Integration
- Use Cashfree webhook callbacks to confirm payment status.
- Validate webhook signatures for security.
- Update payment records based on webhook data.
- Alternatively, poll Cashfree APIs for payment status.

## Scaling, Logging, and Maintenance
- Use a production-grade database like PostgreSQL.
- Deploy with WSGI servers like Gunicorn behind a reverse proxy.
- Use centralized logging (e.g., ELK stack) for monitoring.
- Implement caching for frequently accessed data.
- Use CI/CD pipelines for automated testing and deployment.
- Monitor API usage and performance metrics.
