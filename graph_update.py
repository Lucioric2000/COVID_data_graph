import pandas as pd, os, glob, datetime
STATE = "Morelos"
COUNTRY = "Mexico"
columns = "FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key,Incident_Rate,Case_Fatality_Ratio".split(",")
def data_gen_for_each_day():
    for filename in glob.iglob(os.path.join("COVID-19", "csse_covid_19_data",
        "csse_covid_19_daily_reports", "*.csv")):
        filenameparts = os.path.split(filename)
        date = datetime.datetime.strptime(filenameparts[1], "%m-%d-%Y.csv").date()
        print("date", date)
        day_df = pd.read_csv(filename)
        if "Country_Region" in day_df.columns:
            q1 = day_df["Country_Region"] == COUNTRY
        else:
            q1 = day_df["Country/Region"] == COUNTRY
        if "Province_State" in day_df.columns:
            q2 = day_df["Province_State"] == STATE
        else:
            q2 = day_df["Province/State"] == STATE
        q = q1 & q2
        of_the_state = day_df[q]
        assert of_the_state.shape[0]<2
        if of_the_state.shape[0]==1:
            of_the_state.at[of_the_state.index[0],"Date"] = date
            if "Case-Fatality_Ratio" in day_df.columns:
                of_the_state.at[of_the_state.index[0],"Case_Fatality_Ratio"] = of_the_state.at[of_the_state.index[0],"Case-Fatality_Ratio"]
            yield of_the_state
state_df = pd.concat(data_gen_for_each_day(), axis=0, join='inner', ignore_index=True)
state_df.sort_values(axis=0, by="Date", inplace=True, ignore_index=True)
for (irow, row) in state_df.iterrows():
    if irow>0:
        state_df.loc[irow, "New_Confirmed"] = state_df.loc[irow, "Confirmed"] - state_df.loc[irow-1, "Confirmed"]
        state_df.loc[irow, "New_Deaths"] = state_df.loc[irow, "Deaths"] - state_df.loc[irow-1, "Deaths"]
        state_df.loc[irow, "New_Recovered"] = state_df.loc[irow, "Recovered"] - state_df.loc[irow-1, "Recovered"]
state_df.to_excel(f"Timeseries_{STATE}_{COUNTRY}.xlsx")
print("state_df", state_df, state_df.shape, type(state_df))