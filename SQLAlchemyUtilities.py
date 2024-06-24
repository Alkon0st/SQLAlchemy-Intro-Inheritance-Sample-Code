from sqlalchemy import inspect
from db_connection import engine
from db_connection import Session
from orm_base import schema

"""
This file contains assorted utilities that will prove useful when working in SQLAlchemy.
I plan to add to this as we go along.  These utilities could be merged into main.py, but
it makes it easier to maintain them as a separate module.
"""


def check_unique_constraint(session: Session, constraint, instance):
    """Perform a search to see if there are any rows in the table the corresponds to
    the supplied class name that match the corresponding attributes in the supplied
    instance of the input class.  The match has to be across all the columns
    in the supplied constraint.
    :param  session :       The database session that we will use for the search.
    :param  constraint:     A dictionary, with just two fields: the name of the
                            uniqueness constraint, and the list of columns in the
                            constraint.  The constraint could be a primary key or
                            a uniqueness constraint.
    :param instance:        The instance that you want to test to see whether it is
                            a duplicate of an existing row in the corresponding
                            table.
    :return:                If there is already an instance of this class in the table
                            that matches the supplied instance across the columns of
                            the uniqueness constraint, return that instance.  Else
                            return None."""
    # use reflection to get the class from the class_name.  This will throw an exception
    # if the class_name is invalid.
    python_class = instance.__class__
    # __table__.name is the name of the corresponding table.  Remember, we use CamelCase for our
    # class names and snake_case for the table names.  The class name != the table name.
    # Introspect the table corresponding to the class that we are going to search.
    mapper = inspect(python_class)
    columns = mapper.c.keys()  # get a list of column names for this table
    keys = mapper.attrs.keys()  # get list of attribute names for the class
    # Use a list comprehension to get a list of the columns in the table's primary key.
    uk_cols = constraint['column_names']
    filters = []  # The list of column=value pairs that we'll search by
    """Remember that the primary key column names in the table will not necessarily == the 
    name of the corresponding attributes in the OO class.  For each column name, we loop
    through the list of columns until we get a match, and then get the attribute name."""
    for key in uk_cols:  # for each column, find the matching attribute.
        attr_name = ''  # The attribute name of the next column in this uniqueness constraint
        # Look at each attribute in the class and see if the column name matches the column
        # name of the uniqueness constraint that we are looking for.
        for attribute_name in keys:
            # There could be ATTRIBUTE names that have no corresponding columns.  One example of this
            # is the list of children in a parent, or the OO reference from the child up to the parent.
            # We need to skip those.
            if attribute_name in columns:
                if mapper.c[attribute_name].name == key:
                    # if mapper.attrs[attribute_name].columns[0].name == key:
                    attr_name = attribute_name
                    break
        # Add the next column name = value pair to the filter.  getattr on the class returns
        # the class attribute (not the value, but the attribute of the class itself).
        # getattr on the instance returns the value of that attribute in that instance of
        # the class.  Is that cool or what???
        filters.append(getattr(python_class, attr_name) == getattr(instance, attr_name))
    count = session.query(python_class).filter(*filters).count()  # See if we have any matches
    if count == 1:  # This uniqueness constraint is violated.
        result = session.query(python_class).filter(*filters).first()
        return result
    else:  # No duplicate rows found for THIS uniqueness constraint.
        return None


def check_unique(sess: Session, class_instance) -> [str]:
    """Check all the uniqueness constraints (PK as well as candidate keys)
    to make sure that the class_instance is not redundant to any rows already
    in the table.  This assumes that none of the key fields of any
    uniqueness constraint is null in the class_instance, and that there is a
    one for one correspondence between class and table.
    :param sess:            The session that we are connected to.
    :param class_instance:  The new instance that you are about to insert into the database.
    :return:                A list of 0 or more uniqueness constraint names that were
                            violated by the class_instance.  If this list is empty, then
                            you know that you can insert the instance without worrying
                            about any of the uniqueness constraints."""
    results = []  # The list of violated uniqueness constraints
    python_class = class_instance.__class__  # get the class that this is a member of
    table_name = python_class.__table__.name  # get the corresponding table name
    inspector = inspect(engine)  # Need to find a way to pass the engine in
    # use the constructed inspector to get the uniqueness constraints and the primary keys of the table.
    # The schema name is imported from orm_base.
    unique_constraints = inspector.get_unique_constraints(table_name=table_name, schema=schema)
    primary_key = inspector.get_pk_constraint(table_name=table_name, schema=schema)
    # Put all the uniqueness constraints together into one dictionary.
    # Assume that every table at least has a primary key.  Other candidate keys are optional.
    constraints = [{'name': primary_key['name'], 'column_names': primary_key['constrained_columns']}]
    for uk in unique_constraints:
        constraints.append({'name': uk['name'], 'column_names': uk['column_names']})
    for constraint in constraints:
        # If a duplicate row is found, check_unique_constraint returns that row & we know that
        # the uniqueness constraint was violated.
        if check_unique_constraint(sess, constraint, class_instance):
            results.append(constraint)
    return results
