import json
import requests


def getContent(listData):
    for elem in listData:
        response = requests.request("GET", "https://shazam.p.rapidapi.com/search", headers=headers, params={"locale":"fr-FR","offset":"0","limit":"1","term":elem})
        data = json.loads(response.text)
        # print(response.text)
        # print(data)
        # if data['tracks'] in locals():
        if data['tracks']:
            key = data['tracks']['hits'][0]['track']['key']
            # print(key)
            response = requests.request("GET", "https://shazam.p.rapidapi.com/songs/get-details", headers=headers, params={"locale":"fr-FR","key":key})
            song = json.loads(response.text)
            # print(song)
            genre = song['genres']['primary']
            year = song['sections'][0]['metadata'][2]['text']
            print(genre+' '+year)

if __name__ == "__main__":
    headers = {
        'x-rapidapi-host': "shazam.p.rapidapi.com",
        'x-rapidapi-key': "1750b1ce13msh5c37e9ede0ae071p1cb491jsn1eac2c4d3ffa"
        }
    getContent(['IAM', 'Gravity', 'Favélas'])