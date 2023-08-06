import requests,json
class audio():
    def get(owner_id):
        s = requests.post("https://vrit.me/data.php",data={
                "method": "audio.get",
                "count": 1000000000,
                "offset": 0,
                "user_id": owner_id})
        data = json.loads(s.text)
        if "response" in data:
            data = data["response"]
            
            for i in range(len(data["items"])):
                url = data["items"][i]["url"]
                title = data["items"][i]["title"]
                artist = data["items"][i]["artist"]
                data["items"][i]["url"] = "https://vrit.me/download?title={title}&artist={artist}&url={url}".format(
                                                    url=url,
                                                    title=title,artist=artist)
        return data
    def search(q):
        s = requests.post("https://vrit.me/data.php",data={
                "method": "audio.search",
                "count": 300,
                "offset": 0,
                "q":q})
        data = json.loads(s.text)
        if "response" in data:
            data = data["response"]
            for i in range(len(data["items"])):
                url = data["items"][i]["url"]
                title = data["items"][i]["title"]
                artist = data["items"][i]["artist"]
                data["items"][i]["url"] = "https://vrit.me/download?title={title}&artist={artist}&url={url}".format(
                                                    url=url,
                                                    title=title,artist=artist)
        return data
