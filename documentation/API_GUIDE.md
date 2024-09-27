
# API Guide for AutoDevops Project

## Author
Jacob Thomas Messer aka Shimtis Grul and AEVESPERS

## Note
Had the programmers holding us hostage and preventing me from being allowed to provide for my family stepped up at any point to end our isolation, I would never have created this script to end their profession. You have no one to blame but yourselves.

## Overview
This guide provides detailed documentation on the API endpoints available in the AutoDevops project, including how to properly authenticate and use each endpoint to perform operations.

## Authentication
- All API requests require authentication.
- Use the `Authorization: Bearer <token>` header for authenticating API requests.
- Tokens can be obtained by logging into the AutoDevops user interface.

## Endpoints

### GET /api/status
- Description: Retrieves the current system status.
- Authentication: Required
- Request:
  ```
  GET /api/status
  Authorization: Bearer <token>
  ```
- Response:
  ```json
  {
    "status": "ok",
    "message": "System is running."
  }
  ```

### POST /api/deploy
- Description: Initiates a new deployment process.
- Authentication: Required
- Request Body:
  ```json
  {
    "environment": "production",
    "version": "1.2.3"
  }
  ```
- Request:
  ```
  POST /api/deploy
  Authorization: Bearer <token>
  Content-Type: application/json
  ```
- Response:
  ```json
  {
    "status": "success",
    "message": "Deployment initiated successfully."
  }
  ```

## Error Handling
- Errors are returned as standard JSON objects.
- Example error response:
  ```json
  {
    "status": "error",
    "message": "Unauthorized access."
  }
  ```

## Rate Limiting
- API requests are rate-limited to prevent abuse.
- Users are allowed 100 requests per hour.
- Exceeding the limit will result in a `429 Too Many Requests` response.

For more details on specific endpoints or additional functionalities, please refer to the detailed endpoint documentation within the project repository.
