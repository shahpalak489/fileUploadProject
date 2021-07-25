# from sqlalchemy import Column, Date, Integer, Boolean, String, *
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class cCompanyInfo(Base):
# 	__tablename__   = "company_info"
# 	__table_args__ = {'schmema' : 'dbo'}
# 	id = Column(Integer, primery_key = True)
# 	cname = Column(String(64), primery_key = True)
# 	share_price_dt = Column(Date)
# 	share_price = Column(String(64))  # float
# 	comments = Column(String(64))
# 	file_name = Column(String(64))
# 	inserted_by = Column(String(64))
# 	inserted_time = Column(DateTime)
#     canceled_by = Column(String(64))
# 	canceled_time = Column(DateTime)
# 	canceled = Column(Bit)
#     runid = Column(Numeric(20,0))
