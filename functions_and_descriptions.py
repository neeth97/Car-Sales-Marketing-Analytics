# ad_channels has a column named in the format category-partner_campaign,
# we break this down to three new columns of the names: category, partner and campaign.

def create_new_columns_ad_channels():

    # create a new ad_channels dataframe with split column names
    new_ad_channels_df = ad_channels.copy()

    # Splitting the 'channel_name' column into 'category', 'partner', and 'campaign'
    new_ad_channels_df[['category', 'partner', 'campaign']] = new_ad_channels_df['channel'].str.split(r'[-_]', expand=True)

    # Handling the case when there's no campaign
    new_ad_channels_df['campaign'].fillna(new_ad_channels_df['partner'], inplace=True)

    return new_ad_channels_df
    
# we identify the first touch for every user_id and store that in this dataframe.
# first touch attribution a marketing technique where we care a lot about the
# first channel an user interacts with first.

def create_first_touch_df():
    # sort all the clicks by the datetime in asc order
    sorted_clicks_df = clicks.sort_values(by='click_datetime')
    first_touch_df = sorted_clicks_df.drop_duplicates(subset=['user_id'], keep='first')

    return first_touch_df

# we identify the last touch (last interaction with a marketing channel)
# for every user_id and store that in this dataframe.
def create_last_touch_df():
    # sort all the clicks by the datetime in asc order
    sorted_clicks_df = clicks.sort_values(by='click_datetime')
    last_touch_df = sorted_clicks_df.drop_duplicates(subset=['user_id'], keep='last')

    return last_touch_df

def calculate_sales_per_channel_id():
    # CHANGE THE CODE TO USE A DIFF DF FROM sales BY DROPPING SOME NULL USER_IDs
    sales_per_user_id_df = sales.groupby('user_id').size().reset_index(name='no_of_sales')

    # create first touch df by calling a function
    first_touch_df = create_first_touch_df()

    # map the sales for each user_id and attribute that to a channel based on the first touch
    sales_per_user_id_merged_first_touch_df = pd.merge(sales_per_user_id_df, first_touch_df, on = 'user_id')

    # count the sales for each channel id
    sales_per_channel_id_df = pd.DataFrame(sales_per_user_id_merged_first_touch_df.groupby('channel_id')['no_of_sales'].sum())

    return sales_per_channel_id_df

