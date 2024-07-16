# solution to q4

# customer acquisition cost is the ratio of advertising spend to the no.of sales

def calculate_customer_acquisition_cost_for_each_channel_id():

    sales_per_channel_id_df = calculate_sales_per_channel_id()

    # calculate ad_spend for each channel
    ad_spend_df = spend.groupby('channel_id')['spend'].sum().reset_index()

    # we merge sales for each channel_id with the ad spend
    sales_per_channel_id_merged_ad_spend_df = pd.merge(sales_per_channel_id_df, ad_spend_df, on = 'channel_id')

    customer_acquisition_cost_for_each_channel_id_df = sales_per_channel_id_merged_ad_spend_df.groupby('channel_id').agg({'no_of_sales': 'sum', 'spend' : 'sum'}).reset_index()

    #calculate the customer acquisition cost for each partner
    customer_acquisition_cost_for_each_channel_id_df['customer_acquisition_cost'] = customer_acquisition_cost_for_each_channel_id_df['spend'] / customer_acquisition_cost_for_each_channel_id_df['no_of_sales']

    return customer_acquisition_cost_for_each_channel_id_df

def calculate_customer_acquisition_cost_for_each_partner():
    # create a new df with split channel names
    new_ad_channels_df = create_new_columns_ad_channels()

    # call the above function to calculate customer acquisition cost for each channel
    customer_acquisition_cost_for_each_channel_id_df = calculate_customer_acquisition_cost_for_each_channel_id()

    # map the above per channel_id data with the campaign, category, and partner.
    sales_per_channel_id_merged_ad_spend_df = pd.merge(customer_acquisition_cost_for_each_channel_id_df, new_ad_channels_df, on = 'channel_id')

    # aggregate and calculate the total ad spend per partner
    # and also the total no.of sales per partner
    customer_acquisition_cost_df = sales_per_channel_id_merged_ad_spend_df.groupby('partner').agg({'no_of_sales': 'sum', 'spend' : 'sum'}).reset_index()

    #calculate the customer acquisition cost for each partner
    customer_acquisition_cost_df['customer_acquisition_cost'] = customer_acquisition_cost_df['spend'] / customer_acquisition_cost_df['no_of_sales']

    return customer_acquisition_cost_df

def partner_with_least_cac():
    # call the function to calculate cost per click
    customer_acquisition_cost_for_each_partner_df = calculate_customer_acquisition_cost_for_each_partner()

    # find the category with min cost per click
    min_cpc_index = customer_acquisition_cost_for_each_partner_df['customer_acquisition_cost'].idxmin()
    partner_with_least_cac = customer_acquisition_cost_for_each_partner_df.loc[min_cpc_index, 'partner']

    return partner_with_least_cac

##### print solution to q4

print("Partner with the least Customer Acquisition Cost value:", partner_with_least_cac(), "\n\n\n\n\n\n")

calculate_customer_acquisition_cost_for_each_partner().sort_values(by = 'customer_acquisition_cost')
