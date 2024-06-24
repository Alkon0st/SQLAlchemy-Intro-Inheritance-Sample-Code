from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Note - The "connect string" shown in db_connection only goes so far as to specify the
# database name, which defaults to 'postgres' if you just hit enter.   in this case.
# Be sure to create the proper schema in the postgresql database BEFORE trying to run
# this code, SQLAlchemy will not do that for you.

# If nothing is entered when input prompts the user for the schema, then the or gets a
# null string for the first argument which evaluates to false, which means that the
# boolean expression takes the right-hand argument as its output and passes that in to the
# MetaData constructor.
schema=(input('Schema name [introduction]-->') or "introduction")
Base = declarative_base(metadata=MetaData(schema))
metadata = Base.metadata
