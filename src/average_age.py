import pandas as pd
age_user_data = "user_by_age.csv"
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
age_user_df = pd.read_csv(age_user_data, na_values=idntfrs)

print(age_user_df['age'].mean())