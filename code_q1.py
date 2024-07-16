# solution to q1

# cost per click is the ratio of advertising spend to total no.of clicks

def calculate_cost_per_click_for_each_channel_id():
    # calculate ad_spend per channel id
    ad_spend_df = spend.groupby('channel_id')['spend'].sum().reset_index()

    # calculate no.of clicks for each channel id
    no_of_clicks_df = clicks.groupby('channel_id').size().reset_index(name='clicks')

    # combine the dataframes of ad spend per channel with no.of clicks per channel
    # and further merge that with the dataframe with split channel names
    ad_spend_merged_no_of_clicks_df = pd.merge(no_of_clicks_df, ad_spend_df, on = 'channel_id')

    cost_per_click_for_each_channel_id_df = ad_spend_merged_no_of_clicks_df.groupby('channel_id').agg({'spend': 'sum', 'clicks' : 'sum'}).reset_index()

    cost_per_click_for_each_channel_id_df['cost_per_click'] = cost_per_click_for_each_channel_id_df['spend'] / cost_per_click_for_each_channel_id_df['clicks']

    return cost_per_click_for_each_channel_id_df

def calculate_cost_per_click_for_each_category():
    # create a new df with split channel names by calling a function
    new_ad_channels_df = create_new_columns_ad_channels()

    # call the above function to calculate cost per click for each channel
    cost_per_click_for_each_channel_id_df = calculate_cost_per_click_for_each_channel_id()

    #combine cost per click for each channel_id with the new segregated ad channel names
    cost_per_click_df_merged_new_ad_channels_df = pd.merge(cost_per_click_for_each_channel_id_df, new_ad_channels_df, on = 'channel_id')

    # aggregate and calculate the total ad spend per catergory
    # and also the total no.of clicks per category
    cost_per_click_for_each_category_df = cost_per_click_df_merged_new_ad_channels_df.groupby('category').agg({'spend': 'sum', 'clicks' : 'sum'}).reset_index()

    #calculate the cost per click for each category
    cost_per_click_for_each_category_df['cost_per_click'] = cost_per_click_for_each_category_df['spend'] / cost_per_click_for_each_category_df['clicks']

    return cost_per_click_for_each_category_df

def category_with_least_cpc():
    # call the function to calculate cost per click
    cost_per_click_for_each_category_df = calculate_cost_per_click_for_each_category()

    # find the category with min cost per click
    min_cpc_index = cost_per_click_for_each_category_df['cost_per_click'].idxmin()
    category_with_least_cpc = cost_per_click_for_each_category_df.loc[min_cpc_index, 'category']

    return category_with_least_cpc

##### print solution to q1

print("Category with the least CPC value:", category_with_least_cpc(), "\n\n\n\n\n")

calculate_cost_per_click_for_each_category().sort_values(by = 'cost_per_click')
