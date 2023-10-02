from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import decl_api

Base: decl_api.DeclarativeMeta = declarative_base()
