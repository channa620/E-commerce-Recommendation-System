
E-Kart Recommendation System (Flask)
-----------------------------------

Files created:
- app.py                : Flask application
- templates/            : HTML templates (layout, home, cart)
- static/               : static files (currently empty)
- products.csv          : should be placed in the project root or kept at /mnt/data/products.csv

How to run:
1. Copy the provided products.csv (already in /mnt/data/products.csv) into the project folder if you want local copy:
   cp /mnt/data/products.csv /mnt/data/e_kart_app/

2. Create a virtual environment and install Flask and pandas:
   python -m venv venv
   source venv/bin/activate   (on Windows: venv\\Scripts\\activate)
   pip install flask pandas

3. Run the app:
   python app.py

4. Open http://127.0.0.1:5000 in your browser.

Notes:
- Product images are generated via a placeholder service using the product name.
- Recommendation logic uses the 'related_products' column from products.csv plus same-category fallbacks.
- You can expand product attributes (price, description, real image URL) in products.csv and adjust templates accordingly.
