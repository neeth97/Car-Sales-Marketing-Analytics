%%sql

# create a temporary table to store sorted clicks to get first touch
CREATE TEMP TABLE IF NOT EXISTS ranked_clicks AS
    SELECT user_id,
           click_datetime,
           channel_id,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY click_datetime) AS row_num
    FROM clicks;

# create a temporary table to store first touch for each user
CREATE TEMP TABLE IF NOT EXISTS first_touch AS
    SELECT user_id,
            click_datetime,
            channel_id
    FROM ranked_clicks
    WHERE row_num =1;

# ad_channels has a column named in the format category-partner_campaign,
# we break this down to three new columns of the names: category, partner and campaign.
CREATE TEMPORARY TABLE IF NOT EXISTS new_ad_channels AS
    SELECT
        channel_id,
        SUBSTRING_INDEX(channel, '-', 1) AS category,
        SUBSTRING_INDEX(SUBSTRING_INDEX(channel, '-', -1), '_', 1) AS partner,
        SUBSTRING_INDEX(channel, '_', -1) AS campaign
    FROM ad_channels;

# print top 3 campaigns with most sales generated by first touch attribution
SELECT campaign, count(*) num_sales
FROM sales
JOIN first_touch ft ON sales.user_id = ft.user_id
JOIN new_ad_channels nac ON nac.channel_id = ft.channel_id
GROUP BY campaign
ORDER BY num_sales DESC
LIMIT 3
