# solution to q5


def calculate_profit():

    # make sure all the time values are consistent in the sales df
    sales_time_adjusted_df = sales.copy()
    sales_time_adjusted_df['sale_datetime'] = pd.to_datetime(sales_time_adjusted_df['sale_datetime'])

    # make and model make the unique identifier
    combined_df = pd.merge(sales_time_adjusted_df, vehicles, on=['make', 'model'], how='left')

    ##### step 1
    ##### starting value of the profit is avg margin for each vehicle
    combined_df['profit'] = combined_df['avg_margin']

    ##### step 2
    ##### calculate monthly avg apr value

    # filter the DataFrame where 'is_financed' is not equal to 0
    filtered_df = combined_df[combined_df['is_financed'] != 0]

    # group by month and calculate average APR
    avg_apr_per_month = filtered_df.groupby(filtered_df['sale_datetime'].dt.to_period('M'))['apr'].mean()

    # merge the calculated average APR values back into the original DataFrame based on the month
    combined_df['avg_monthly_apr'] = combined_df['sale_datetime'].dt.to_period('M').map(avg_apr_per_month)

    ##### step 3
    ##### calculate apr modifier value for each sale
    combined_df['apr_modifier'] = -0.1  # default value if financed = 0
    mask_financed = (combined_df['is_financed'] != 0)  # mask for financed != 0
    combined_df.loc[mask_financed, 'apr_modifier'] = (combined_df['apr'] - combined_df['avg_monthly_apr']) / combined_df['avg_monthly_apr']

    ##### step 4
    ##### update the profit based on the above calculated apr modifier
    # note that combined_df['profit] initially holds the starting value i.e. avg_margin. we update that in this step
    combined_df['profit'] = combined_df['profit'] * (1 + combined_df['apr_modifier'])

    ##### step 5
    ##### update the profit based on the bodystyle of the vehicle
    mask_trade_in = (combined_df['has_trade_in'] != 0)

    # Sedan or Hatchback
    mask_sedan_hatchback = combined_df['bodystyle'].isin(['Sedan', 'Hatchback'])
    combined_df.loc[mask_sedan_hatchback, 'profit'] += (200 - (combined_df['delivery_distance'] / 2))
    #combined_df.loc[mask_sedan_hatchback, 'profit'] -= combined_df['delivery_distance'] / 2
    combined_df.loc[mask_sedan_hatchback & mask_trade_in, 'profit'] += 400

    # Coupe or SUV
    mask_coupe_suv = combined_df['bodystyle'].isin(['Coupe', 'SUV'])
    combined_df.loc[mask_coupe_suv, 'profit'] -= 0.8 * combined_df['delivery_distance']
    combined_df.loc[mask_coupe_suv & mask_trade_in, 'profit'] += 300  # Trade-in

    # Truck
    mask_truck = combined_df['bodystyle'] == 'Truck'
    combined_df.loc[mask_truck & mask_financed, 'profit'] -= 200 + combined_df['delivery_distance']
    combined_df.loc[mask_truck, 'profit'] -= combined_df['delivery_distance']
    combined_df.loc[mask_truck & mask_trade_in, 'profit'] += 200  # Trade-in

    return combined_df

def calculate_roi_per_channel_id():
    # create first touch df by calling a function
    first_touch_df = create_first_touch_df()

    # map the profit from sales for each user_id and attribute that to a channel based on the first touch
    profit_merged_first_touch_df = pd.merge(calculate_profit(), first_touch_df, on = 'user_id')

    # sum up the profit from sales for each channel id
    profit_per_channel_id_df = pd.DataFrame(profit_merged_first_touch_df.groupby('channel_id')['profit'].sum()).reset_index()

    # calculate ad_spend per channel id
    ad_spend_df = spend.groupby('channel_id')['spend'].sum().reset_index()

    # we merge profit from sales for each channel_id with the ad spend
    profit_per_channel_id_merged_ad_spend_df = pd.merge(profit_per_channel_id_df, ad_spend_df, on = 'channel_id')

    # aggregate and calculate the total ad spend per catergory
    # and also the total profit from sales per category
    roi_per_channel_id_df = profit_per_channel_id_merged_ad_spend_df.groupby('channel_id').agg({'spend': 'sum', 'profit' : 'sum'}).reset_index()

    #calculate the cost per click for each category
    roi_per_channel_id_df['roi'] = roi_per_channel_id_df['profit'] / roi_per_channel_id_df['spend']

    return roi_per_channel_id_df

def roi_per_category():

    # create a new df with split channel names
    new_ad_channels_df = create_new_columns_ad_channels()

    # call the above function calculate roi for each channel
    roi_per_channel_id_df = calculate_roi_per_channel_id()

    # map the profit from sales and ad spend per each channel id with the new_ad_channels df
    roi_variables_merged_ad_channels_df = pd.merge(roi_per_channel_id_df, new_ad_channels_df, on = 'channel_id')

    # aggregate and calculate the total ad spend per catergory
    # and also the total profit from sales per category
    roi_per_category_df = roi_variables_merged_ad_channels_df.groupby('category').agg({'spend': 'sum', 'profit' : 'sum'}).reset_index()

    #calculate the cost per click for each category
    roi_per_category_df['roi'] = roi_per_category_df['profit'] / roi_per_category_df['spend']

    return roi_per_category_df

roi_per_category()
