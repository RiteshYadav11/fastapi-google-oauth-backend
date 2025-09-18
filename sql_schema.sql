-- SQL schema for PostgreSQL
CREATE TYPE area_enum AS ENUM ('Mumbai', 'Bangalore');
CREATE TYPE payment_status_enum AS ENUM ('pass', 'fail');


CREATE TYPE payment_type_enum AS ENUM ('UPI', 'card');
CREATE TYPE food_item_enum AS ENUM ('veg_manchurian', 'chicken_manchurian',
'veg_fried_rice', 'chicken_noodles');


CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    google_id VARCHAR UNIQUE NOT NULL,
    age INTEGER
);


CREATE TABLE restaurants (
    restaurant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_name VARCHAR NOT NULL,
    area area_enum NOT NULL
);


CREATE TABLE payments (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status payment_status_enum NOT NULL,
    payment_type payment_type_enum NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);


CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_item food_item_enum NOT NULL,
    transaction_id UUID REFERENCES payments(transaction_id) NOT NULL,
    restaurant_id UUID REFERENCES restaurants(restaurant_id) NOT NULL,
    customer_id UUID REFERENCES customers(id) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);


CREATE INDEX idx_customers_google_id ON customers (google_id);
CREATE INDEX idx_restaurants_area ON restaurants (area);
CREATE INDEX idx_payments_status ON payments (status);