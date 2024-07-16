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
