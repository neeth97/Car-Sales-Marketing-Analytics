# solution to q7

def calculate_time_diff_between_sale_and_last_click():
    # make sure all the time values are consistent in the sales df
    sales_time_adjusted_df = sales.copy()
    sales_time_adjusted_df['sale_datetime'] = pd.to_datetime(sales_time_adjusted_df['sale_datetime'])

    sales_time_adjusted_filtered_df = sales_time_adjusted_df[['user_id','sale_id', 'sale_datetime']].copy()

    # create a df with the last interaction of a customer with the marketing channel
    last_touch_df = create_last_touch_df()

    # in this df we capture the last time a customer interacted with
    # one of the marketing channels
    merged_sales_last_touch_df = pd.merge(sales_time_adjusted_filtered_df, last_touch_df, on = 'user_id', how = 'left')
    merged_sales_last_touch_df = merged_sales_last_touch_df.fillna(0)

    # make sure all the time values are consistent in the sales df
    merged_sales_last_touch_df['click_datetime'] = pd.to_datetime(merged_sales_last_touch_df['click_datetime'], format = 'mixed', yearfirst = True)
    merged_sales_last_touch_df['sale_datetime'] = pd.to_datetime(merged_sales_last_touch_df['sale_datetime'])

    # calculate time difference in days using vectorized operations
    merged_sales_last_touch_df['time_diff_in_days'] = (merged_sales_last_touch_df['sale_datetime'] - merged_sales_last_touch_df['click_datetime']).dt.days

    return merged_sales_last_touch_df

def calculate_percent_of_sales_with_no_click_for_90_days():
    merged_sales_last_touch_df = calculate_time_diff_between_sale_and_last_click()
    # filter rows where time difference is greater than 90 days
    rows_greater_than_90_days = merged_sales_last_touch_df[merged_sales_last_touch_df['time_diff_in_days'] > 90]
    return (len(rows_greater_than_90_days) / len(merged_sales_last_touch_df))*100

calculate_percent_of_sales_with_no_click_for_90_days()
