import random
import csv
from datetime import datetime, timedelta

# Define lists of dummy values
first_names = [
    "John",
    "Maria",
    "David",
    "Laura",
    "Karen",
    "James",
    "Sarah",
    "Daniel",
    "Nicole",
    "Eric",
    "Michael",
    "Paul",
    "Olivia",
    "Linda",
    "Mike",
    "Jessica",
    "Robert",
    "Emily",
    "Mark",
    "Anna",
    "Anthony",
    "Diana",
]
last_names = [
    "Smith",
    "Gonzalez",
    "Johnson",
    "Chen",
    "Lee",
    "White",
    "Martinez",
    "Watson",
    "Rivera",
    "Anderson",
    "Brown",
    "Singh",
    "Carter",
    "Frank",
    "Davis",
    "Adams",
    "Hall",
    "Evans",
    "King",
    "Perez",
    "Turner",
    "Green",
]

segments = ["Consumer", "Small Business", "Business", "Enterprise"]
cities_states = [
    ("New York", "NY"),
    ("Los Angeles", "CA"),
    ("Chicago", "IL"),
    ("Houston", "TX"),
    ("Phoenix", "AZ"),
    ("San Francisco", "CA"),
    ("Denver", "CO"),
    ("Seattle", "WA"),
    ("Miami", "FL"),
    ("Boston", "MA"),
    ("Atlanta", "GA"),
    ("New Orleans", "LA"),
    ("Dallas", "TX"),
    ("San Diego", "CA"),
    ("Portland", "OR"),
    ("Philadelphia", "PA"),
    ("Charlotte", "NC"),
    ("Detroit", "MI"),
    ("Minneapolis", "MN"),
    ("Salt Lake City", "UT"),
    ("Cleveland", "OH"),
    ("Columbus", "OH"),
    ("Nashville", "TN"),
    ("Kansas City", "MO"),
    ("Indianapolis", "IN"),
]

categories = {
    "Furniture": [
        "Chairs",
        "Desks",
        "Tables",
        "Lamps",
        "Sofas",
        "Cabinets",
        "Office Chairs",
    ],
    "Electronics": [
        "Smartphones",
        "Laptops",
        "Monitors",
        "Headphones",
        "Smartwatches",
        "Printers",
    ],
    "Office Supplies": [
        "Paper",
        "Binders",
        "Notebooks",
        "Envelopes",
        "Markers",
        "Pens",
        "Staplers",
    ],
}


# Function to generate a random date in 2024
def random_date_2024():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")


num_rows = 1000
order_id_start = 1001

with open("dummy_sales_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write header
    writer.writerow(
        [
            "Date",
            "Order ID",
            "Customer Name",
            "Customer Segment",
            "City",
            "State",
            "Product Category",
            "Product Sub-Category",
            "Units Sold",
            "Unit Cost",
            "Unit Price",
            "Total Cost",
            "Total Sales",
            "Margin",
            "Margin %",
        ]
    )

    for i in range(num_rows):
        order_id = f"ORD-{order_id_start + i}"
        date = random_date_2024()
        customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        segment = random.choice(segments)
        city, state = random.choice(cities_states)

        category = random.choice(list(categories.keys()))
        sub_category = random.choice(categories[category])

        units_sold = random.randint(1, 100)
        unit_cost = round(random.uniform(1.0, 600.0), 2)
        # Ensure unit price is always higher than unit cost
        unit_price = round(unit_cost + random.uniform(0.1, unit_cost), 2)

        total_cost = units_sold * unit_cost
        total_sales = units_sold * unit_price
        margin = total_sales - total_cost
        margin_percent = (margin / total_sales) * 100 if total_sales != 0 else 0

        writer.writerow(
            [
                date,
                order_id,
                customer_name,
                segment,
                city,
                state,
                category,
                sub_category,
                units_sold,
                unit_cost,
                unit_price,
                round(total_cost, 2),
                round(total_sales, 2),
                round(margin, 2),
                f"{round(margin_percent,2)}%",
            ]
        )
