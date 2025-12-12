import pandas as pd
from app.advanced_services.database_manager import DatabaseManager

# Analytical queries for cyber incidents.
def get_incidents_by_type_count(db: DatabaseManager):

    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    rows = db.fetch_all(query)
    df = pd.DataFrame(rows, columns=["category", "count"])
    return df

def get_high_severity_by_status(db: DatabaseManager):

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
def get_datasets_by_uploader(conn):
    
    # Count datasets uploaded by each user.
    
    query = """
    SELECT uploaded_by, COUNT(*) as dataset_count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY dataset_count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_large_datasets(conn, min_rows):
    
 
    
    query = """
    SELECT name, rows, columns, uploaded_by
    FROM datasets_metadata
    WHERE rows > ? 
    ORDER BY rows DESC
    """
    # ? is used to avoid SQL injection.
    df = pd.read_sql_query(query, conn, params=(min_rows,))
    return df   

def get_dataset_upload_trends_monthly(conn):
    
    # Monthly datsets upload trends.
    
    query = """
    SELECT strftime('%Y-%m', upload_date) AS month, COUNT(*) AS upload_count
    FROM datasets_metadata
    GROUP BY month
    ORDER BY month ASC
    """
    df = pd.read_sql_query(query, conn)
    return df

# Analytical queries for IT tickets.

def get_tickets_by_priority(conn):
    
    # Count tickets by priority level.
    
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_high_priority_tickets(conn):
    # Get all high priority tickets

    query = """
        SELECT *
        FROM it_tickets
        WHERE priority = 'High'
        ORDER BY ticket_id ASC
    """
    
    df = pd.read_sql_query(query, conn)
    return df


def get_high_priority_tickets_by_status(conn):
    
    # Count high priority tickets by status.
    
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_slow_resolution_tickets_by_status(conn, min_resolution_time = 24) :
    
    # Find tickets with resolution time greater than min_resolution_time hours by status.
    
    query = """
    SELECT status, AVG(resolution_time_hours) as avg_resolution
    FROM it_tickets
    GROUP BY status
    HAVING AVG(resolution_time_hours) > ?
    ORDER BY avg_resolution DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_resolution_time,))
    return df

def get_avg_resolution_by_staff(conn):
    # Average resolution time by assigned staff member.
    query = """
        SELECT assigned_to, AVG(resolution_time_hours) AS avg_resolution_time
        FROM it_tickets
        WHERE resolution_time_hours IS NOT NULL
        GROUP BY assigned_to
        ORDER BY avg_resolution_time DESC
    """
    
    df = pd.read_sql_query(query, conn)
    return df


def get_slow_resolution_tickets_only(conn, min_resolution_time=24):
    # Find all tickets with resolution time greater than min_resolution_time hours.
    
    query = """
    SELECT *
    FROM it_tickets
    WHERE resolution_time_hours > ?
    ORDER BY resolution_time_hours DESC
    """
    
    df = pd.read_sql_query(query, conn, params=(min_resolution_time,))
    return df
