-- Sample data
INSERT INTO categories (id, name) VALUES
  (1, 'Electronics'),
  (2, 'Books'),
  (3, 'Clothing'),
  (4, 'Home');

INSERT INTO products (name, description, price, image_url, stock, category_id) VALUES
  ('Wireless Headphones', 'Over-ear Bluetooth headphones with noise isolation and 30-hour battery life.', 2499.00, '/images/headphones.svg', 25, 1),
  ('Mechanical Keyboard', 'Compact 75% mechanical keyboard with tactile switches and RGB backlight.', 3299.00, '/images/keyboard.svg', 15, 1),
  ('Smart Watch', 'Fitness tracker with heart-rate monitor, sleep tracking and 7-day battery.', 4599.00, '/images/smartwatch.svg', 10, 1),
  ('Portable Power Bank', '20000 mAh power bank with fast charging and dual USB output.', 1799.00, '/images/powerbank.svg', 40, 1),
  ('Clean Code', 'A handbook of agile software craftsmanship by Robert C. Martin.', 699.00, '/images/cleancode.svg', 30, 2),
  ('Introduction to Algorithms', 'The classic algorithms textbook covering sorting, graphs and dynamic programming.', 1250.00, '/images/algorithms.svg', 12, 2),
  ('Python Crash Course', 'A hands-on, project-based introduction to programming with Python.', 549.00, '/images/python.svg', 50, 2),
  ('Cotton T-Shirt', 'Soft 100% cotton round-neck t-shirt available in everyday colours.', 499.00, '/images/tshirt.svg', 100, 3),
  ('Denim Jacket', 'Classic regular-fit denim jacket with button closure and two chest pockets.', 1999.00, '/images/jacket.svg', 18, 3),
  ('Running Shoes', 'Lightweight breathable running shoes with cushioned sole.', 2799.00, '/images/shoes.svg', 22, 3),
  ('Ceramic Coffee Mug', 'Set of two 300 ml ceramic mugs, microwave and dishwasher safe.', 399.00, '/images/mug.svg', 60, 4),
  ('LED Desk Lamp', 'Adjustable LED desk lamp with three brightness levels and USB charging port.', 899.00, '/images/lamp.svg', 35, 4);