import random
from datetime import datetime, timedelta

inserts = []
for i in range(0, 4000):
    after_days = random.randint(-5_000, 10)
    stages = random.randint(1, 3)

    estimated_date = datetime.now() + timedelta(days=after_days)

    inserts.append(f"INSERT INTO delivery VALUES ({i}, '{estimated_date}');\n")

    for j in range(0, stages):
        if j == 0:
            date = estimated_date - timedelta(hours=random.randint(10,40))
            inserts.append(f"INSERT INTO delivery_update (delivery_status, updated_date, tracking_number) VALUES ('approved', '{date}', {i});\n")
        elif j == 1:
            date += timedelta(hours=random.randint(1, 10))
            inserts.append(f"INSERT INTO delivery_update (delivery_status, updated_date, tracking_number) VALUES ('shipped', '{date}', {i});\n")
        elif j == 2:
            date += timedelta(hours=random.randint(1, 4))
            inserts.append(f"INSERT INTO delivery_update (delivery_status, updated_date, tracking_number) VALUES ('delivered', '{date}', {i});\n")

with open("./inserts.sql", "w", encoding="utf-8") as file:
    for insert in inserts:
        file.write(insert)