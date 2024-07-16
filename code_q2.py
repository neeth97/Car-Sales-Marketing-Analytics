# solution to q2

def calculate_top_three_campaigns_no_of_sales_generated_first_touch():

    sales_per_channel_id_df = calculate_sales_per_channel_id()

    # create df with split channel names by calling a function
    new_ad_channels_df = create_new_columns_ad_channels()

    # map the sales per each channel id with the new_ad_channels df
    sales_per_channel_id_merged_ad_channels_df = pd.merge(sales_per_channel_id_df, new_ad_channels_df, on = 'channel_id')

    # calculate the number of sales per campaign
    aggregate_sales_by_campaign_df = pd.DataFrame(sales_per_channel_id_merged_ad_channels_df.groupby('campaign')['no_of_sales'].sum()).reset_index()

    # identify the top three campaigns by no.of sales generated based on first touch attribution
    top_three_campaigns_by_sales_df = aggregate_sales_by_campaign_df.sort_values(by = 'no_of_sales', ascending = False).head(3)

    return top_three_campaigns_by_sales_df#['campaign'].tolist()

##### print solution to q2

# top three campaigns with most sales:
calculate_top_three_campaigns_no_of_sales_generated_first_touch()
