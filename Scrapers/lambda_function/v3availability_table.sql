CREATE TABLE IF NOT EXISTS Bikes.v3availability
(number INTEGER NOT NULL,
last_update DATETIME NOT NULL,
connected varchar(128),
available_bikes INTEGER,
available_bike_stands INTEGER,
mechanical_bikes INTEGER,
electrical_bikes INTEGER,
electric_internal_bikes INTEGER,
electric_removeable_battery INTEGER,
status VARCHAR(128),
overflow_stands VARCHAR(128),
PRIMARY KEY (number, last_update)
);