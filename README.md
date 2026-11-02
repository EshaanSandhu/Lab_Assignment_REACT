# ShopEasy - Product Listing Website (Part 1)

A simple full-stack e-commerce product listing app.

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | HTML, CSS, vanilla JavaScript       |
| Backend  | Python 3 + Flask (REST API)         |
| Database | SQLite (relational, single file)    |

## Features
- Product listing page showing name, description, price and image
- Product details page
- Search by keyword and filter by category
- REST API with request validation and proper HTTP status codes
- Frontend never touches the database - all data comes through the backend API

## Prerequisites
- Python 3.9 or newer (`python --version`)
- pip (comes with Python)
- No separate database server needed (SQLite is built into Python)

## Project structure
```
ecommerce-app/
├── backend/
│   ├── app.py            # Flask app: API endpoints + serves the frontend
│   ├── init_db.py        # Creates the database from the SQL scripts
│   └── db/
│       ├── schema.sql    # Table definitions
│       └── seed.sql      # Sample categories and products
├── frontend/
│   ├── index.html        # Product listing page
│   ├── product.html      # Product details page
│   ├── css/style.css
│   ├── js/app.js         # Listing, search and filter logic
│   ├── js/product.js     # Details page logic
│   └── images/           # Product images
├── docs/screenshots/     # Screenshots for submission
├── requirements.txt
└── README.md
```

## Setup and run

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd ecommerce-app

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database and load the sample products
python backend/init_db.py

# 5. Start the application
python backend/app.py
```

Open **http://127.0.0.1:5000** in your browser.

Re-running step 4 resets the database to the original sample data.

### Configuration (optional)
| Variable        | Default                  | Purpose                  |
|-----------------|--------------------------|--------------------------|
| `DATABASE_PATH` | `backend/ecommerce.db`   | Location of SQLite file  |

The server runs on port 5000. To change it, edit the last line of `backend/app.py`.

## Architecture

```
 Browser (HTML/CSS/JS)
        │  fetch() JSON over HTTP
        ▼
 Flask backend (backend/app.py)
   - validates requests
   - serves static frontend files
        │  parameterised SQL queries
        ▼
 SQLite database (backend/ecommerce.db)
   categories ──< products
```

- The browser loads static pages from Flask, then calls `/api/...` endpoints to get data as JSON.
- Only the backend talks to the database. All SQL uses parameterised queries (protects against SQL injection), and the frontend inserts data using `textContent` (protects against XSS).
- Frontend and backend are served from the same origin, so no CORS setup is needed.

### Database schema
- `categories(id, name)`
- `products(id, name, description, price, image_url, stock, category_id → categories.id)`

Full definitions are in `backend/db/schema.sql`; sample data is in `backend/db/seed.sql`.

## API endpoints

| Method | Endpoint              | Description                          | Status codes |
|--------|-----------------------|--------------------------------------|--------------|
| GET    | `/api/products`       | List products (supports filters)     | 200, 400     |
| GET    | `/api/products/<id>`  | Get one product                      | 200, 400, 404 |
| GET    | `/api/categories`     | List categories                      | 200          |

`GET /api/products` optional query parameters:

| Parameter   | Description                                   |
|-------------|-----------------------------------------------|
| `search`    | Text matched against name and description (max 100 chars) |
| `category`  | Category id (integer)                         |
| `min_price` | Minimum price (non-negative number)           |
| `max_price` | Maximum price (non-negative number)           |

Examples:
```bash
curl http://127.0.0.1:5000/api/products
curl "http://127.0.0.1:5000/api/products?search=python&category=2"
curl http://127.0.0.1:5000/api/products/3
curl http://127.0.0.1:5000/api/products/999     # 404 {"error": "Product not found"}
curl http://127.0.0.1:5000/api/products/abc     # 400 {"error": "Product id must be a positive integer"}
```

Sample response (`/api/products/3`):
```json
{
  "id": 3, "name": "Smart Watch",
  "description": "Fitness tracker with heart-rate monitor, sleep tracking and 7-day battery.",
  "price": 4599.0, "image_url": "/images/smartwatch.svg", "stock": 10,
  "category_id": 1, "category": "Electronics"
}
```

## Screenshots
Located in `docs/screenshots/`:
- `product-listing.png` - product listing page
- `product-details.png` - product details view
