import requests

#client_secret = requests.get("http://34.67.212.21/api/v1/register?code=0xfbce434ee3").json()['client_secret']

response1 = requests.get("http://34.67.212.21/api/v1/resetinfo?master_key=0x238746AFB").json()

print(response1)

#response2 = requests.get(f"http://34.67.212.21/api/v1/sendmessage?client_secret={client_secret}&key=TestWashingMachine1&value=1").json()

#print(response2)

#response3 = requests.get(f"http://34.67.212.21/api/v1?client_secret={client_secret}").json()

#print(response3)
