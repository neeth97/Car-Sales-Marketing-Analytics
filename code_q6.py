# solution to q6

def calculate_avg_clicks_before_lock():

    clicks_time_adjusted_df = clicks.copy()
    locks_time_adjusted_df = locks.copy()

    clicks_time_adjusted_df['click_datetime'] = pd.to_datetime(clicks_time_adjusted_df['click_datetime'])
    locks_time_adjusted_df['lock_datetime'] = pd.to_datetime(locks_time_adjusted_df['lock_datetime'], format = 'mixed', yearfirst = True)

    click_time_merged_lock_time_df = pd.merge(locks_time_adjusted_df, clicks_time_adjusted_df, on = 'user_id', how = 'left')

    # filter rows where 'click_datetime' is less than 'lock_datetime'
    filtered_df = click_time_merged_lock_time_df[click_time_merged_lock_time_df['click_datetime'] < click_time_merged_lock_time_df['lock_datetime']]

    # group by calculate the unique count of 'channel_id'
    result = filtered_df.groupby('lock_id')['channel_id'].nunique()

    # assign the result to the original DataFrame
    click_time_merged_lock_time_df['click_count_before_lock'] = click_time_merged_lock_time_df['lock_id'].map(result)

    # calculate the average clicks for each lock
    # we do not calculate for each user_id because
    # sometimes the users come back for purchase
    interactions_per_lock_id_df = click_time_merged_lock_time_df[['lock_id', 'click_count_before_lock']].drop_duplicates()
    avg_clicks_before_lock_df = interactions_per_lock_id_df['click_count_before_lock'].sum() / len(interactions_per_lock_id_df['lock_id'].unique())

    return avg_clicks_before_lock_df

calculate_avg_clicks_before_lock()
