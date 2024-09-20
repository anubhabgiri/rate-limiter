# Rate Limiter

Configurable rate limiter for notifications

This is meant to be a standalone service

! Future scope - use Redis

## Run with Docker
``` docker compose up ```

## Sample Request

```
    {
        "user_id": "36049",
        "timestamp": 1278403827,
        "limit": 3
    }
```