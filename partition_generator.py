import calendar
from datetime import datetime, timedelta

def _get_sunday(date):
    '''
    get previous sunday
    '''    
    #monday = 0 Sunday = 6
    week_day = calendar.weekday(date.year, date.month, date.day)
    if week_day == 6:
        return date
    else:
        d = timedelta(days = week_day+1)
        return date-d

def _generate_partitions(date_start, date_end, parent_name, pkey):
    """
    generate create statement from start day until end_day
    """
    sql = ''
    start = _get_sunday(date_start)
    finish = _get_sunday(date_end)
    while start < finish:
        week = timedelta(days = 7)
        end = start + week

        #setup partition name and values
        p_start = datetime.strftime(start,"%Y%m%d")
        p_end = datetime.strftime(end,"%Y%m%d")
        date_from = datetime.strftime(start,"%Y-%m-%d")
        date_to = datetime.strftime(end,"%Y-%m-%d")
        #(primary key ({pkey}))
        create = f"""
        create table {parent_name}_{p_start}_{p_end} partition of {parent_name}
            for values from ('{date_from}') to ('{date_to}');
        """
        sql += create

        #increment for loop 
        start += week
    
    default = f"""\ncreate table {parent_name}_def partition of {parent_name}
            (primary key ({pkey}))
            default;
        """
    sql += default
    return sql

input_start = input('start (dd/mm/yyyy):\n')
input_end = input('end (dd/mm/yyyy):\n')
date_start = datetime.strptime(input_start, "%d/%m/%Y")
date_end = datetime.strptime(input_end, "%d/%m/%Y")
parent_name = 'event_history'
pkey = 'id'

sql_script = _generate_partitions(date_start, date_end, parent_name, pkey)
print(sql_script)



