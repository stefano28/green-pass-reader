from pyzbar.pyzbar import decode
from PIL import Image
import json
import base45
import cbor2
from cose.messages import CoseMessage
import zlib
import sys

img = Image.open(sys.argv[1])
result = decode(img)
token = ''
for i in result:
    token += i.data.decode("utf-8")
decoded = base45.b45decode(token[4:])
decompressed = zlib.decompress(decoded)
cose = CoseMessage.decode(decompressed)
decoded_json = json.dumps(cbor2.loads(cose.payload), indent=2)
f = open("decoded.txt", "w")
f.write(decoded_json)
f.close()
f = open('decoded.txt', "r+")
data = json.load(f)
iterations = 0
json_index = []

name = ''
surname = ''
vaccine_date = ''
istitute = ''

for i in data:
    iterations += 1
    if iterations == 4:
        json_index.append(i)

iterations = 0
for i in data[json_index[0]]:
    iterations += 1
    if iterations == 1:
        json_index.append(i)

iterations = 0
for i in data[json_index[0]][json_index[1]]:
    iterations += 1
    if iterations == 1:
        json_index.append(i)
        istitute = data[json_index[0]][json_index[1]][json_index[2]][0]["is"]
        vaccine_date = data[json_index[0]][json_index[1]][json_index[2]][0]["dt"]
    if i == 'nam':
       name = data[json_index[0]][json_index[1]]["nam"]["gn"]
       surname = data[json_index[0]][json_index[1]]["nam"]["fn"]
        

print()
print("[*] GREEN PASS READING")
print("> istitution: " + istitute)
print("> vaccine date: " + vaccine_date)
print("> name: " + name)
print("> surname: " + surname)
print()
f.close()
