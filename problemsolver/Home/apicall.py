import requests
import time
def data(id):
    url=f"https://c9aede1d.compilers.sphere-engine.com/api/v4/submissions/{id}?access_token=6ca0d8ef2707a6869ad9ba4098a94fbe"
    data=requests.get(url)
    print(data.json())
    check=type(data.json()['executing'])

    while(check):
        print("*")
        check=requests.get(url).json()['executing']
    time.sleep(1)
    data=requests.get(url)
    print(data.json())
    status=data.json()['result']['status']['name']
    dict={}
    if(status == "accepted"):
        url=data.json()['result']['streams']['output']['uri']
        data=requests.get(url).text

        dict["status"] = "sucess"
        dict["output"] = data
    elif(status == "compilation error"):
        url=data.json()['result']['streams']['cmpinfo']['uri']
        data=requests.get(url).text

        dict["status"] = "compilation error"
        dict["output"] = data
    else:
        url=data.json()['result']['streams']['error']['uri']
        data=requests.get(url).text

        dict["status"] = "runtime error"
        dict["output"] = data
    return dict
if __name__ == "__main__":
    id=24234234
    data(id)