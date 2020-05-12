from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 


# sqlalchemy need a primary key
# database setup
conn_str  = 'sqlite:///Resources/hawaii.sqlite'
conn = create_engine(conn_str)

# create base class for reflection
Base = automap_base()

# reflect tables in database
Base.prepare(conn,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind=conn)
first10= session.query(Measurement).limit(10).all()

for measurement in first10:
    print(measurement.id, measurement.station,measurement.tobs)

session = Session(bind=conn)
firststation10= session.query(Station).limit(10).all()

for station in firststation10:
    print(station.id, station.name,station.elevation)


# # returns all purchasing data
# all_purchases = session.query(Purchases).all()
# print('all purchases',len(all_purchases))

# # returns all purchasing for a year
# user_purchases = session.query(Purchases)\
#     .filter((Purchases.SN=='Lisim78') | (Purchases.SN=='Lisim78'))

# #
# item_purchases = session.query(Purchases)\
#     .filter(Purchases.ItemID== 108)\
#         .all()
# print('item purchase count',len(item_purchases))

# # particular purchase by id 
# mypurchase_list = session.query(Purchases)\
#     .filter(Purchases.PurchaseID == 1)\
#         .all()

# mypurchase = session.query(Purchases)\
#     .filter(Purchases.PurchaseID == 0)\
#         .first()

# # shows the actual records 
# print(mypurchase.__dict__)