# Flask_Advanced

# Install Psycopg2
-> pip install psycopg2

# How to use .env file

-> pip install python-dotenv

-> checl .env file then follow the procedure from app.py file

`
from dotenv import load_dotenv

load_dotenv()
`

# Install Flask CORS

-> pip install flask-cors

# JSON Schema

-> pip install jsonschema

# JWT
 
pip uninstall jwt==1.0.0

And then I uninstalled pyJWT using:

pip uninstall PyJWT

And then install it again:

pip install PyJWT

And my code:
open python console and verify it:

>>> import jwt
>>> encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
>>> encoded
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U'
>>> decoded = jwt.decode
>>> decoded
<bound method PyJWT.decode of <jwt.api_jwt.PyJWT object at 0x0000019273531E20>>
>>> decoded = jwt.decode(encoded,'secret',algorithms="HS256")
>>> decoded
{'some': 'payload'}
>>>

