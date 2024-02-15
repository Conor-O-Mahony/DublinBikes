CREATE TABLE IF NOT EXISTS Bikes.v3station (
number INTEGER NOT NUll,
address VARCHAR(128),
banking INTEGER,
bike_stands INTEGER,
name VARCHAR(128),
position_lat FLOAT,
position_lng FLOAT,
bonus INTEGER,
overflow INTEGER,
PRIMARY KEY (number)
);