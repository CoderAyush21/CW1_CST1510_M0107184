import pandas as pd
from app.advanced_services.database_manager import DatabaseManager

# Analytical queries for cyber incidents.
def get_incidents_by_type_count(db: DatabaseManager):

    '''
    Retrieve incidents by their category and count the sum of each type

    '''
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    rows = db.fetch_all(query) # Use the method from the class DatabaseManager to execute the query 
    df = pd.DataFrame(rows, columns=["category", "count"]) # create pandas dataframe to be returned which will be used for anlayitics 
    return df

def get_high_severity_by_status(db: DatabaseManager):
    '''
    Retrieves the count of HIGH severity cyber incidents grouped by status.
    
    '''

    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    rows = db.fetch_all(query)
    df = pd.DataFrame(rows, columns=["status", "count"])
    return df

def get_high_severity_incidents(db: DatabaseManager):

    '''
    Retreives high severity incidents from the database

    '''

    query = """
    SELECT *
    FROM cyber_incidents
    WHERE severity = 'High'
    ORDER BY incident_id ASC
    """
    rows = db.fetch_all(query)
    df = pd.DataFrame(rows, columns=["incident_id","category","severity","status","description","timestamp","reported_by"])
    return df

def get_incident_types_with_many_cases(db: DatabaseManager, min_count=5):

    '''
    Retrieves incident categories that exceed a minimum number of cases.

    '''

    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    rows = db.fetch_all(query, (min_count,))
    df = pd.DataFrame(rows, columns=["category", "count"])
    return df


# Analytical queries for datasets.
def get_datasets_by_uploader(db: DatabaseManager):

    '''
    Retrieves the number of datasets uploaded by each user.

    '''
    query = """
    SELECT uploaded_by, COUNT(*) as dataset_count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY dataset_count DESC
    """
    rows = db.fetch_all(query)
    df_datasets= pd.DataFrame(rows, columns=["uploaded_by", "dataset_count"])
    return df_datasets

def get_large_datasets(db: DatabaseManager, min_rows: int):

    '''
    Retrieves datasets that contain more than a specified number of rows.

    '''

    query = """
    SELECT name, rows, columns, uploaded_by
    FROM datasets_metadata
    WHERE rows > ?
    ORDER BY rows DESC
    """
    rows = db.fetch_all(query, (min_rows,))
    df_datasets= pd.DataFrame(rows, columns=[
        "name", "rows", "columns", "uploaded_by"
    ])
    return df_datasets


def get_dataset_upload_trends_monthly(db: DatabaseManager):

    '''
    Retrieves monthly dataset upload trends.

    '''

    query = """
    SELECT strftime('%Y-%m', upload_date) AS month, COUNT(*) AS upload_count
    FROM datasets_metadata
    GROUP BY month
    ORDER BY month ASC
    """
    rows = db.fetch_all(query)
    df_datasets= pd.DataFrame(rows, columns=["month", "upload_count"])
    return df_datasets


# Analytical queries for IT tickets.

def get_tickets_by_priority(db: DatabaseManager):

    '''
    Retrieves the number of IT tickets grouped by priority level.

    '''

    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    rows = db.fetch_all(query)
    df_tickets= pd.DataFrame(rows, columns=["priority", "count"])
    return df_tickets

def get_high_priority_tickets(db: DatabaseManager):

    '''
    Retrieves all IT tickets marked as HIGH priority.

    '''

    query = """
    SELECT *
    FROM it_tickets
    WHERE priority = 'High'
    ORDER BY ticket_id ASC
    """
    rows = db.fetch_all(query)
    df_tickets= pd.DataFrame(rows, columns=[
        "ticket_id", "title", "priority", "status",
        "assigned_to", "resolution_time_hours", "timestamp"
    ])
    return df_tickets

def get_high_priority_tickets_by_status(db: DatabaseManager):

    '''
    Retrieves HIGH priority IT tickets grouped by status

    '''
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    rows = db.fetch_all(query)
    df_tickets= pd.DataFrame(rows, columns=["status", "count"])
    return df_tickets

def get_slow_resolution_tickets_by_status(db: DatabaseManager, min_resolution_time=24):

    '''
    Retrieves ticket statuses where the average resolution time
    exceeds a specified value.

    '''
    query = """
    SELECT status, AVG(resolution_time_hours) as avg_resolution
    FROM it_tickets
    GROUP BY status
    HAVING AVG(resolution_time_hours) > ?
    ORDER BY avg_resolution DESC
    """
    rows = db.fetch_all(query, (min_resolution_time,))
    df_tickets= pd.DataFrame(rows, columns=["status", "avg_resolution"])
    return df_tickets

def get_avg_resolution_by_staff(db: DatabaseManager):

    '''
    Retrieves the average resolution time per staff member.

    '''

    query = """
        SELECT assigned_to, AVG(resolution_time_hours) AS avg_resolution_time
        FROM it_tickets
        WHERE resolution_time_hours IS NOT NULL
        GROUP BY assigned_to
        ORDER BY avg_resolution_time DESC
    """
    rows = db.fetch_all(query)
    df_tickets= pd.DataFrame(rows, columns=["assigned_to", "avg_resolution_time"])
    return df_tickets

def get_slow_resolution_tickets_only(db: DatabaseManager, min_resolution_time=24):

    '''
    Retrieves all IT tickets whose resolution time exceeds
    a given value which is 24hrs here.

    '''
    
    query = """
    SELECT *
    FROM it_tickets
    WHERE resolution_time_hours > ?
    ORDER BY resolution_time_hours DESC
    """
    rows = db.fetch_all(query, (min_resolution_time,))
    df_tickets= pd.DataFrame(rows, columns=[
        "ticket_id", "title", "priority", "status",
        "assigned_to", "resolution_time_hours", "timestamp"
    ]) 
    return df_tickets