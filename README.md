
E-Kart Recommendation System (Flask)
-----------------------------------
Flask-based e-commerce web application with real-time product recommendations using CSV-driven product data. Implemented personalized suggestions based on cart items, categories, and with dynamic cart management and user-friendly interface.



🚀 Features

🔍 Search & Browse – Find products by name or category.

🛍️ Smart Recommendations – Personalized product suggestions based on:

Items in cart

Related products from dataset

Same category items

Popular fallback products

🧾 Dynamic Cart Management – Add or remove items from the shopping cart with instant recommendation updates.

🖼️ Image Handling – Supports local images; generates placeholder images automatically for missing ones.

📂 CSV-Driven Catalog – Product data is stored in a CSV file for easy updates.

💻 User-Friendly Web Interface – Built with Flask, HTML, CSS

Files created:
- app.py                : Flask application
- templates/            : HTML templates (layout, home, cart)
- static/               : static files (currently empty)
- products.csv          : should be placed in the project root or kept at /mnt/data/products.csv


Notes:
- Product images are generated via a placeholder service using the product name.
- Recommendation logic uses the 'related_products' column from products.csv plus same-category fallbacks.
- You can expand product attributes (price, description, real image URL) in products.csv and adjust templates accordingly.
