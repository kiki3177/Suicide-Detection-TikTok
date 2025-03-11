from TikTokApi import TikTokApi
import asyncio
import os
import json
import re

from secret import ms_token

async def get_hashtag_videos(hashtag_name):
    videos_info = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False, browser=os.getenv("TIKTOK_BROWSER", "chromium"))
        tag = api.hashtag(name=hashtag_name)
        async for video in tag.videos(count=30):
            try:
                pattern = r"TikTokApi\.video\(id='(\d+)'\)"
                match = re.search(pattern, str(video))
                video_id = ''
                if match:
                    video_id = match.group(1)
                video_data = video.as_dict
                all_hashtags = video_data.get("textExtra")
                hashtag_lst =[]
                for hashtag in all_hashtags:
                    hashtag_string = hashtag.get("hashtagName")
                    normal_string = hashtag_string.encode().decode("unicode_escape")
                    hashtag_lst.append(normal_string)


                formatted_data = {
                    "id": video_id,
                    "hashtags": hashtag_lst,
                    "video": video_data.get("video").get("bitrateInfo")[0].get("PlayAddr").get("UrlList")[2]
                }

                print(json.dumps(formatted_data, indent=4))
                videos_info.append(formatted_data)

            except Exception as e:
                pass

    # Writing all video data to a JSON file after fetching is complete
    os.makedirs("experiment", exist_ok=True)
    file_path = f'experiment/{hashtag_name}_videos_data.json'

    with open(file_path, 'w') as file:
        json.dump(videos_info, file, indent=4)

    print("All video data has been written to 'videos_data.json'.")


if __name__ == "__main__":
    hashtag_name = "depression"
    asyncio.run(get_hashtag_videos(hashtag_name))
