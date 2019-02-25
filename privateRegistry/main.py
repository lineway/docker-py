import requests
import json


url = 'http://192.168.254.56:5000'

# res = requests.get(url + "/v2/_catalog")
# print(json.loads(res.text))


class Registry:

    def __init__(self, protocol="http", url="localhost", port="5000"):
        self.protocol = protocol
        self.url = url
        self.port = port

    def list_image(self):
        URL = self.protocol + "://" + self.url + ":" + str(self.port) + "/v2/_catalog"
        image_list = requests.get(URL).text
        image_list = json.loads(image_list)['repositories']
        return image_list
    
    def list_tag(self, image_name:str):
        URL = self.protocol + "://" + self.url + ":" + str(self.port) + "/v2/" + \
            image_name + "/tags/list"
        tags_list = requests.get(URL).text
        try:
            tags_list = json.loads(tags_list)['tags']
        except KeyError:
            return "Image not found."
        else:
            return tags_list

    def pull_image(self, image_name:str,  tag_name:str):
        URL = self.protocol + "://" + self.url + ":" + str(self.port) + "/v2/" + \
            str(image_name) + "/manifests/" + str(tag_name)
        
        res_code = requests.head(URL).status_code
        if res_code == 200:
            res = json.dumps({"info": [{"code": "EXISTS", "message": "The image already exists"}]})
            return res
        else:
            res = requests.get(URL).text
            res = json.loads(res)
            return res

    def push_image(self, image_name, tag_name):

        URL = self.protocol + "://" + self.url + ":" + str(self.port) + "/v2/" + \
            str(image_name) + "/blobs/" + str(tag_name)

        res = requests.head(URL)
        return res
        # URL = self.protocol + "://" + self.url + ":" + str(self.port) + "/v2/" + \
        #     str(image_name) + "/blobs/uploads/"
        
        # res = requests.post(URL).headers['Location']
        # return res 
        

if __name__ == "__main__":
    print(Registry().push_image(image_name="redis", tag_name="4.0"))
    print(Registry().list_image())

