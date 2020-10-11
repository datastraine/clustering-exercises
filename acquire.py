import pandas as pd
import env
import os


def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Returns a formatted url with login credentials to access data on a SQL database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def load_zillow_data():
    '''
    This function acquires the zillow dataset from a SQL Database.
    It returns the zillow dataset as a Pandas DataFrame.
    
    A local copy will be created as a csv file in the current directory for future use.
    '''
    db = 'zillow'
    sql_query = '''
select * from properties_2017
	join (select parcelid, max(transactiondate) as transactiondate from predictions_2017
	group by parcelid) recent
	using(parcelid)
	join (select parcelid, logerror, transactiondate from predictions_2017) est
	on est.parcelid = recent.parcelid
	and est.transactiondate = recent.transactiondate
	left outer join zillow.airconditioningtype
	using(airconditioningtypeid)
	left outer join zillow.architecturalstyletype
	using (architecturalstyletypeid)
	left outer join zillow.heatingorsystemtype
	using(heatingorsystemtypeid)
	left outer join zillow.propertylandusetype
	using (propertylandusetypeid)
	left outer join zillow.storytype
	using(storytypeid)
	left outer join zillow.typeconstructiontype
	using(typeconstructiontypeid)
	left outer join zillow.buildingclasstype
	using(buildingclasstypeid)
	where latitude is not null 
	and longitude is not null;
	'''
    file = 'zillow_full.csv'
    
    if os.path.isfile(file):
        return pd.read_csv('zillow_full.csv')
    else:
        df = pd.read_sql(sql_query, get_connection(db))
        df.to_csv('zillow_full.csv', index=False)
        return df
