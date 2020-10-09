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
    select 
		zillow.properties_2017.parcelid,
		basementsqft,
		bathroomcnt,
		bedroomcnt,
		buildingqualitytypeid,
		calculatedbathnbr,
		decktypeid,
		finishedfloor1squarefeet,
		calculatedfinishedsquarefeet,
		finishedsquarefeet12,
		finishedsquarefeet13,
		finishedsquarefeet15,
		finishedsquarefeet50,
		finishedsquarefeet6,
		fips,
		fireplacecnt,
		fullbathcnt,
		garagecarcnt,
		garagetotalsqft,
		hashottuborspa,
		latitude,
		longitude,
		lotsizesquarefeet,
		poolcnt,
		poolsizesum,
		pooltypeid10,
		pooltypeid2,
		pooltypeid7,
		propertycountylandusecode,
		propertyzoningdesc,
		rawcensustractandblock,
		regionidcity,
		regionidcounty,
		regionidneighborhood,
		regionidzip,
		roomcnt,
		threequarterbathnbr,
		unitcnt,
		yardbuildingsqft17,
		yardbuildingsqft26,
		yearbuilt,
		numberofstories,
		fireplaceflag,
		structuretaxvaluedollarcnt,
		taxvaluedollarcnt,
		assessmentyear,
		landtaxvaluedollarcnt,
		taxamount,
		taxdelinquencyflag,
		taxdelinquencyyear,
		censustractandblock,
		airconditioningdesc,
		architecturalstyledesc,
		buildingclassdesc,
		heatingorsystemdesc,
		propertylandusedesc,
		storydesc,
		typeconstructiondesc
		logerror,
		recent.transactiondate
	from properties_2017
	join (select parcelid, max(transactiondate) as transactiondate from predictions_2017
	group by parcelid) recent
	using(parcelid)
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
	and longitude is not null
	'''
    file = 'zillow.csv'
    
    if os.path.isfile(file):
        return pd.read_csv('zillow.csv')
    else:
        df = pd.read_sql(sql_query, get_connection(db))
        df.to_csv('zillow.csv', index=False)
        return df
