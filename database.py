
def initialise_database():
    with open('bus_stops.json') as f:
        bus_stops = json.load(f)
    with open('bus_services.json') as f:
        bus_services = json.load(f)
    with open('bus_routes.json') as f:
        bus_routes = json.load(f)

    def insert_bus_stop(row,c):
        '''Takes a row from bus_stops as an input and inserts relevant data into database '''
        c.execute(
            """
            INSERT INTO bus_stops
            VALUES(?,?)
            ;"""
        ,
        (row['BusStopCode'],row['Description'])
        )

    def insert_bus_service(row,c):
        c.execute(
            """
            INSERT INTO bus_services
            VALUES(?,?)
            ;"""
        ,
        (row['ServiceNo'],row['Category'])
        )

    def insert_bus_route(row,c):
        c.execute(
            """
            INSERT INTO bus_routes
            VALUES(?,?,?,?,?)
            ;"""
        ,
        (row['ServiceNo'],row['Direction'],row['StopSequence'],row['BusStopCode'],row['Distance'])
        )


    conn = sqlite3.connect('bus_data.db')
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS bus_stops(
            BusStopCode INTEGER PRIMARY KEY,
            Description TEXT)
        ;"""
    )
    for row in bus_stops:
        insert_bus_stop(row,c)


    c.execute(
        """
        CREATE TABLE IF NOT EXISTS bus_services(
            ServiceNo TEXT PRIMARY KEY,
            Category TEXT)
        ;"""
    )
    servicenos = []
    for row in bus_services:
        if row['ServiceNo'] not in servicenos:
            #This is to remove duplicate rows
            servicenos.append(row['ServiceNo'])
            insert_bus_service(row,c)

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS bus_routes(
            ServiceNo TEXT,
            Direction INTEGER,
            StopSequence INTEGER,
            BusStopCode INTEGER,
            Distance INTEGER,
            PRIMARY KEY(ServiceNo,Direction,StopSequence),
            FOREIGN KEY(ServiceNo) REFERENCES bus_service(ServiceNo),
            FOREIGN KEY(BusStopCode) REFERENCES bus_stops(BusStopCode)
            )
        ;"""
    )
    for row in bus_routes:
        if row['BusStopCode'].isnumeric():
            insert_bus_route(row,c)
    conn.commit()
    conn.close()