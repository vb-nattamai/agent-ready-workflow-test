# Order Service

A lightweight REST API for managing customer orders. Built with Flask.

## Features
- Create, read, update, and cancel orders
- Per-customer order history
- Simple in-memory store (swap for a database in production)

## Quick Start

```bash
pip install -r requirements.txt
python -m flask --app src/app run
```

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/orders` | Place a new order |
| GET | `/orders/{id}` | Get an order by ID |
| GET | `/orders?customer=<id>` | List orders for a customer |
| PATCH | `/orders/{id}/cancel` | Cancel an order |

## Testing

```bash
pip install pytest
pytest tests/ -v
```
