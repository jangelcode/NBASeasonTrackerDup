import pandas as pd
from sqlalchemy import create_engine

# ... (other imports)

class LeagueDashPtStats:
    # ... (existing code)

    def get_request(self):
        self.nba_response = NBAStatsHTTP().send_api_request(
            endpoint=self.endpoint,
            parameters=self.parameters,
            proxy=self.proxy,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self.nba_response.get_data_frames()

# ... (rest of the class)

def insert_data_into_postgres(data_frame, table_name, engine):
    data_frame.to_sql(table_name, engine, if_exists='replace', index=False)

# Modify the parameters according to your needs
api_params = {
    'Season': '2019-20',
    'PerMode': 'Totals',
    'PlayerOrTeam': 'Team',
    'PtMeasureType': 'SpeedDistance',
}

# Instantiate LeagueDashPtStats with the API parameters
api_data = LeagueDashPtStats(**api_params)

# Get the response data frames
response_data_frames = api_data.get_request()

# Connect to the PostgreSQL database (modify the connection string accordingly)
# Make sure to replace 'user', 'password', 'host', and 'port' with your actual PostgreSQL credentials
engine = create_engine('postgresql://postgres:postgres@localhost:5432/defense')

# Define the table name
table_name = 'nba_stats_table'

# Insert data into the PostgreSQL database
for key, value in response_data_frames.items():
    insert_data_into_postgres(value, f"{table_name}_{key}", engine)



