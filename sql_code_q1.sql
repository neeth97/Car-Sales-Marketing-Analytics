%%sql

# ad_channels has a column named in the format category-partner_campaign,
# we break this down to three new columns of the names: category, partner and campaign.

CREATE TEMPORARY TABLE IF NOT EXISTS new_ad_channels AS
    SELECT
        channel_id,
        SUBSTRING_INDEX(channel, '-', 1) AS category,
        SUBSTRING_INDEX(SUBSTRING_INDEX(channel, '-', -1), '_', 1) AS partner,
        SUBSTRING_INDEX(channel, '_', -1) AS campaign
    FROM ad_channels;

# calculate ad_spend per channel id
CREATE TEMPORARY TABLE IF NOT EXISTS ad_spend AS
    SELECT channel_id, SUM(spend) AS total_spend
    FROM spend
    GROUP BY channel_id;

# calculate no.of clicks for each channel id
CREATE TEMPORARY TABLE IF NOT EXISTS clicks_per_channel AS
    SELECT channel_id, COUNT(*) AS clicks
    FROM clicks
    GROUP BY channel_id;

# calculate cost per click for each category
SELECT n.category,
       SUM(s.total_spend) / SUM(c.clicks) AS cost_per_click
FROM clicks_per_channel c
JOIN ad_spend s ON c.channel_id = s.channel_id
JOIN new_ad_channels n ON c.channel_id = n.channel_id
GROUP BY n.category
ORDER BY cost_per_click ASC;
