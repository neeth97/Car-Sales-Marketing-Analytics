# solution to q3

def calculate_monthly_sales_oct_to_dec_per_campaign():
    # make sure all the time values are consistent in the sales df
    sales_time_adjusted_df = sales
    sales_time_adjusted_df['sale_datetime'] = pd.to_datetime(sales_time_adjusted_df['sale_datetime'])

    # filter only sales from oct to dec
    # and assign month value of 10, 11 or 12
    # based on the sale month for each sale
    month_filtered_sales_df = sales_time_adjusted_df[sales_time_adjusted_df['sale_datetime'].dt.month.isin([10, 11, 12])]
    month_filtered_sales_df = month_filtered_sales_df[['user_id','sale_id', 'sale_datetime']].copy()
    month_filtered_sales_df['month'] = month_filtered_sales_df['sale_datetime'].dt.month

    # create first touch df by calling a function
    first_touch_df = create_first_touch_df()

    # map filtered sales with channel_id based on first touch attribution
    first_touch_merged_month_filtered_sales_df = pd.merge(month_filtered_sales_df, first_touch_df, on = 'user_id', how = 'left')

    # drop rows where channel_id is NULL
    merged_month_filtered_sales_cleaned_df = first_touch_merged_month_filtered_sales_df.dropna(subset=['channel_id'])
    merged_month_filtered_sales_cleaned_df = merged_month_filtered_sales_cleaned_df[['sale_id','month','channel_id']].copy()

    # create a pivot table to get counts of sales per month and channel_id
    pivot_table = merged_month_filtered_sales_cleaned_df.pivot_table(index='channel_id', columns='month', aggfunc='size', fill_value=0)

    # rename columns for clarity
    pivot_table.columns = ['sales_in_oct', 'sales_in_nov', 'sales_in_dec']

    # reset index to make channel_id a column instead of index
    oct_to_dec_monthly_sales_per_channel_id_df = pivot_table.reset_index()

    # create a new df with split channel names
    new_ad_channels_df = create_new_columns_ad_channels()

    # map the monthly sales per channel with the campaign, category, and partner.
    final_sales_merged_new_ad_channels_df = pd.merge(oct_to_dec_monthly_sales_per_channel_id_df, new_ad_channels_df, on = 'channel_id')

    #calculate monthly (oct - dec) sales per each campaign
    oct_to_dec_monthly_sales_per_campaign_df = pd.DataFrame(final_sales_merged_new_ad_channels_df.groupby('campaign').agg({'sales_in_oct': 'sum', 'sales_in_nov': 'sum', 'sales_in_dec': 'sum'})).reset_index()

    return oct_to_dec_monthly_sales_per_campaign_df

calculate_monthly_sales_oct_to_dec_per_campaign()
