########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bb75187fb0e94731ac28db3ddbc45548',
}

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'Categories,Tags',
    'language': 'en',
})

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, "{'url':'https://ylakeland.com/wp-content/uploads/2015/04/blueberry450_221068a_8col.jpg'}", headers)
    response = conn.getresponse()
    data = response.read()
    data=data.decode("utf-8")
    jdata = json.loads(data)
    potentialFoodList = []

    for x in jdata["tags"]:
        if(x["confidence"] > 0.90):
            potentialFoodList.append(x["name"])

    for x in potentialFoodList:
        print(x)
        
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
