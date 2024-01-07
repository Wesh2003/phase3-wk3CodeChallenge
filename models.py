from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///restaurant_database.db')

Base = declarative_base()

restaurant_customer = Table(
    'restaurant_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    reviews = relationship('Review', backref=backref('restaurant'))
    customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')

    def __repr__(self):
        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    import Review
    import Customer
    def reviews():
        """Returns a list of the restaurant's reviews."""
        return [review for review in Reviews.session.query(Review).filter_by
        (restaurant=self)]
    
    def customers():
        """Returns a list of the customer IDs that have reviewed this
        restaurant."""
        return [customer for customer in Customers.session.query(Customer).filter_by
        (restaurant=self)]

    def fanciest():
        """Returns the restaurant with the highest price"""
        highest_price = [restaurant for restaurant in session.query(
            Restaurant.price).order_by(
            desc(Restaurant.price)).limit(1)]
        return (highest_price)
    
    def all_reviews(restaurant):
        """Returns all reviews for a resturant with a specific format"""
        query = session.query(Review).filter(Review.restaurant_id == restaurant)
        for review in query:
            return f'Review for {restaurant.name} by {customer.first_name}: {review.star_rating} stars.'



class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())
    comment = Column(String())

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'star_rating={self.star_rating}, ' + \
            f'comment={self.comment}, ' + \
            f'customer_id={self.customer_id}, ' + \
            f'restaurant_id={self.restaurant_id})'
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    import Customer
    import Restaurant

    def customer():
        query = session.query(Review,Customer).filter(Review.customer_id == Customer.id)
        for item in query:
            return (item.first_name, item.last_name)

    
    def restaurant():
        query = session.query(Review,Restaurant).filter(Review.restaurant_id == Restaurant.id)
        for item in query:
            return (item.name, item.price)
    
    def full_reviews():
        all_reviews = session.query(Review).order_by(Review.
        id).all()
        for review in all_reviews:
            return (f"Review for {Restaurant.name}  by {Customer.first_name}: {review.star_rating} stars.")



class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')
    
    def __repr__(self):
        return f'Customer(id={self.id}, ' + \
            f'first_name={self.name}' +\
            f'last_name={self.last_name})'
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    import Review
    import Restaurant

    def reviews():
        """Return a list of the customer's reviews."""
        return [review for review in Reviews.session.query(Review).filter_by
        (review=self)]
    
    def restaurants():
        """Return a list of the customer's reviewed restaurants."""
        query = session.query(Review).filter(Review.customer_id == customer_id)
        for item in query:
            return(item.name, item.price)

    def full_name():
        return f"{Customer.first_name}+{Customer.last_name}"
    
    def favorite_restaurant():
        # Return the restaurant that has been rated most highly by this customer.
        favourite = [restaurant for restaurant in session.query(
            Restaurant.name, Review.price).order_by(
            desc(Review.star_rating)).limit(1)]
        return (favourite)
    
    def delete_reviews(resturant):
        query = session.query(Review, Restaurant).filter(restaurant.name == restaurant)        
        session.delete(query)
        session.commit()


