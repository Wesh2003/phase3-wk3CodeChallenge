#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Customer, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurant_database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Customer).delete()

    fake = Faker()

    restaurant_names = ['The Grill', 'Local cuisine', 'Simpana',
        'Nyamchom', 'killoma', 'SpicyGrill']

    restaurants = []
    for i in range(50):
        restaurant = Restaurant(
            name=random.choice(restaurant_names),
            price=random.randint(20, 200)
        )

        # add and commit individually to get IDs back
        session.add(restaurant)
        session.commit()

        restaurants.append(restaurant)


    customers = []
    for i in range(50):
        customer = Customer(
            first_name=fake.unique.name(),
            last_name=fake.unique.name()
        )

        # add and commit individually to get IDs back
        session.add(customer)
        session.commit()

        customers.append(customer)
    
    reviews = []
    for restaurant in restaurants:
        for i in range(random.randint(1,4)):
            customer = random.choice(customers)
            if restaurant not in customer.restaurants:
                customer.restaurants.append(restaurant)
                session.add(customer)
                session.commit()
            
            review = Review(
                star_rating=random.randint(0, 5),
                comment=fake.sentence(),
                restaurant_id=restaurant.id,
                customer_id=customer.id,
            )

            reviews.append(review)

    session.bulk_save_objects(reviews)
    session.commit()
    session.close()
