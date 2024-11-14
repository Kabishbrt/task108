from fastapi import FastAPI, HTTPException
import httpx
import json
from urllib.parse import quote_plus
from datetime import datetime
from botManager import BotManager

# initialize BotManager
bot_manager = BotManager()

#initialize FastAPI app
app = FastAPI()


http_client = httpx.AsyncClient(timeout=10.0)

bearer_token = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
features = {
    "hidden_profile_subscriptions_enabled": True,
    "rweb_tipjar_consumption_enabled": True,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "subscriptions_verification_info_is_identity_verified_enabled": True,
    "subscriptions_verification_info_verified_since_enabled": True,
    "highlights_tweets_tab_ui_enabled": True,
    "responsive_web_twitter_article_notes_tab_enabled": True,
    "subscriptions_feature_can_gift_premium": True,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True
}
field_toggles = {"withAuxiliaryUserLabels": False}

@app.get("/api/{username}")
async def get_user_data(username: str):
    """
    Fetches user data from Twitter API for the provided username.
    Returns the user data or an error message if something goes wrong.
    """

    # Define the query parameters
    variables = {
        "screen_name": username
    }


    # URL-encode the parameters
    encoded_variables = quote_plus(json.dumps(variables))
    encoded_features = quote_plus(json.dumps(features))
    encoded_field_toggles = quote_plus(json.dumps(field_toggles))

    # Construct the full API URL with encoded query parameters
    url = f"https://twitter.com/i/api/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName?variables={encoded_variables}&features={encoded_features}&fieldToggles={encoded_field_toggles}"

    try:
        bot_name, csrf_token, cookie, useragent = bot_manager.get_next_bot()

        # If no bot is available, return an error
        if not bot_name:
            raise HTTPException(status_code=500, detail="No bots available to make the request.")
        
        # Make async GET request to the Twitter API
        response = await http_client.get(url, headers={
            "Authorization": f"Bearer {bearer_token}",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent" : useragent,
            "Cookie": cookie,
            "X-CSRF-Token": csrf_token,
            "X-Twitter-Auth-Type": "OAuth2Session"
        })
        response.raise_for_status()  # Check if request was successful

        # Parse JSON response
        response_data = response.json()

        # Extract 'legacy' data
        legacy_data = response_data.get("data", {}).get("user", {}).get("result", {}).get("legacy", {})

        # Check if legacy data is present
        if not legacy_data:
            raise HTTPException(status_code=404, detail="Legacy data not found")

        parsed_time = datetime.strptime(legacy_data["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
        formatted_time = parsed_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        legacy_data["created_at"] = formatted_time

        # Filter out specific keys
        legacy_data = {k: v for k, v in legacy_data.items() if k not in ['entities', 'following', 'can_media_tag']}

        return legacy_data

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

# Start the server when this script is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
