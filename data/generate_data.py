import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')
random.seed(42)

# --- CONFIG ---
NUM_CUSTOMERS = 500
NUM_ORDERS = 3000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

CATEGORIES = ['Electronics', 'Fashion', 'Home & Kitchen', 'Beauty', 'Sports']
PRODUCTS = {
    'Electronics': [('Wireless Earbuds', 2499), ('Phone Case', 399), ('USB Hub', 899), ('Webcam', 3499)],
    'Fashion':     [('Cotton Kurta', 699), ('Sneakers', 1999), ('Sunglasses', 1299), ('Watch', 4999)],
    'Home & Kitchen': [('Air Fryer', 5999), ('Water Bottle', 499), ('Bedsheet Set', 1299), ('Mixer', 3299)],
    'Beauty':      [('Face Serum', 899), ('Lipstick Set', 599), ('Moisturizer', 749), ('Hair Oil', 399)],
    'Sports':      [('Yoga Mat', 999), ('Resistance Bands', 599), ('Protein Shaker', 449), ('Skipping Rope', 299)],
}

CITIES = ['Hyderabad', 'Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Pune', 'Kolkata']

# --- CUSTOMERS ---
customers = []
for i in range(NUM_CUSTOMERS):
    customers.append({
        'customer_id': f'CUST{1000+i}',
        'name': fake.name(),
        'email': fake.email(),
        'city': random.choice(CITIES),
        'signup_date': fake.date_between(start_date='-2y', end_date='-6m'),
    })
customers_df = pd.DataFrame(customers)

# --- ORDERS ---
orders = []
for i in range(NUM_ORDERS):
    customer = random.choice(customers)
    category = random.choice(CATEGORIES)
    product_name, base_price = random.choice(PRODUCTS[category])

    # Inject weekly seasonality — weekends sell more
    order_date = START_DATE + timedelta(days=random.randint(0, 364))
    if order_date.weekday() >= 5:
        base_price = int(base_price * 0.95)  # weekend discount

    quantity = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
    revenue = base_price * quantity
    is_returned = random.choices([True, False], weights=[12, 88])[0]
    return_reason = random.choice(['Defective', 'Wrong size', 'Not as described', 'Changed mind']) if is_returned else None

    orders.append({
        'order_id': f'ORD{10000+i}',
        'customer_id': customer['customer_id'],
        'order_date': order_date.strftime('%Y-%m-%d'),
        'product_name': product_name,
        'category': category,
        'quantity': quantity,
        'unit_price': base_price,
        'revenue': revenue,
        'city': customer['city'],
        'is_returned': is_returned,
        'return_reason': return_reason,
        'status': random.choices(
            ['delivered', 'shipped', 'cancelled'],
            weights=[80, 12, 8]
        )[0],
    })

orders_df = pd.DataFrame(orders)

# --- SAVE ---
customers_df.to_csv('data/customers.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)

print(f"✅ Generated {len(customers_df)} customers")
print(f"✅ Generated {len(orders_df)} orders")
print(f"✅ Date range: {orders_df['order_date'].min()} → {orders_df['order_date'].max()}")
print(f"✅ Total revenue: ₹{orders_df['revenue'].sum():,.0f}")
print(f"✅ Return rate: {orders_df['is_returned'].mean()*100:.1f}%")
print("\nFiles saved to data/")