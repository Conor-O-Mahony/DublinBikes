from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from sklearn.ensemble import RandomForestRegressor

def run(target):
    load_dotenv('db.env')

    DB_PASSWORD = os.getenv("DB_PASSWORD")
    URI = 'dublinbikes.clw8uqmac8qf.eu-west-1.rds.amazonaws.com'
    PORT = 3306
    USER = 'admin'
    DB = 'dbikes'

    # Connect to the db
    connection_string = f"mysql+mysqlconnector://{USER}:{DB_PASSWORD}@{URI}:{PORT}/{DB}"
    engine = create_engine(connection_string) #, echo=True

    # Testing
    try:
        connection = engine.connect()
        print("Connection established successfully.")

    except Exception as e:
        print("Failed to establish connection:", e)

    def get_station_data(number):
        query = f"SELECT * FROM availability WHERE number = {number}"
        # Execute the query and fetch results directly into a DataFrame
        df = pd.read_sql(query, engine)
        return df

    def get_weather_data():
        query = "SELECT * FROM currentweather"
        df = pd.read_sql(query, engine)
        return df
    
    def create_weather_df():
        weather_df = get_weather_data()
        weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'], unit='s')
        # Create a merge key that includes up to the minute
        weather_df['merge_key'] = weather_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        return weather_df

    def availability_df(station_number):
        availability_df = get_station_data(station_number)
        availability_df['timestamp'] = pd.to_datetime(availability_df['timestamp'], unit='s')
        # Create a merge key that includes up to the minute
        availability_df['merge_key'] = availability_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        return availability_df


    def merge_dfs(weather_df, station_number):
        availability = availability_df(station_number)
        # Merge on the new merge_key
        merged_df = pd.merge(weather_df, availability, on='merge_key', how='inner')
        # Optionally, convert merge_key back to datetime for further time-based analysis
        merged_df['timestamp'] = pd.to_datetime(merged_df['merge_key'])
        return merged_df
    
    def count_stations():
        query = "SELECT COUNT(DISTINCT number) as Total FROM availability"
        df = pd.read_sql(query, engine)
        return int(df['Total'][0])
    
    def minimised_df(station_number,target,mode=0,dummies=False):
        """Creates a dataframe with only the essential features for predictions"""
        minimised_df = merge_dfs(create_weather_df(), station_number)

        #Create new features
        minimised_df['day_of_week'] = minimised_df['timestamp'].dt.dayofweek+1
        minimised_df['hour'] = minimised_df['timestamp'].dt.hour
        minimised_df['minute'] = minimised_df['timestamp'].dt.minute

        #Drop features redundant for predictions
        unnecessary_features = ['id','timestamp','timestamp_y','lastUpdate','electricalRemovableBatteryBikes','electricalInternalBatteryBikes',
                                'electricalBikes','mechanicalBikes','status','timestamp_x','merge_key','number','availability_id','description']

        #If predicting no. of bikes, we don't need to know no. of stands and vice versa
        if target == 'bikes':
            if mode==1:
                minimised_df.loc[list(minimised_df[minimised_df['bikes']>0].index),'bikes'] = 1
            unnecessary_features.append('stands')
        else:
            if mode==1:
                minimised_df.loc[list(minimised_df[minimised_df['stands']>0].index),'stands'] = 1
            unnecessary_features.append('bikes')

        #If categorical features necessary
        if dummies==True:
            dummie_vals = pd.get_dummies(minimised_df['description'])
            minimised_df = pd.concat([minimised_df, dummie_vals], axis=1)
            with pd.option_context("future.no_silent_downcasting", True):
                minimised_df = minimised_df.replace({True: 1, False: 0}).infer_objects(copy=False)
            
        minimised_df = minimised_df.drop(labels=unnecessary_features, axis=1)

        #Change to correct datatypes
        categorical_columns = ['day_of_week','hour','minute']

        if mode==1:
            categorical_columns.append(target)

        if dummies==True:
            categorical_columns.append(dummie_vals.columns)
        
        for column in categorical_columns:
            minimised_df[column] = minimised_df[column].astype('category') 

        #Try drop duplicates
        if minimised_df.duplicated().sum() > 0:
            minimised_df = minimised_df.drop(minimised_df[minimised_df.duplicated()].index)

        #Return the finalised dataset
        return minimised_df

    def generate_models(target):
        """Options for target: "bikes" or "stands"""""
        number_of_stations = count_stations()

        for i in range(1,number_of_stations+1):
            df = minimised_df(i,target,0,True)

            if not df.empty:
                features = list(df.columns)
                features.remove(target)
        
                X = df[features]
                y = df[target]
            
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
                # Fit the classifier
            
                model = RandomForestRegressor()
                
                model.fit(X_train, y_train)
        
                with open(f'{path}/{target}_{i}.pkl', 'wb') as handle:
                    pickle.dump(model, handle, pickle.HIGHEST_PROTOCOL)

        print(f"{target} have been serialised")

    generate_models(target)

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'pickle_files')
    if not os.path.exists(path):
        os.makedirs(path)
    run("bikes")
    run("stands")