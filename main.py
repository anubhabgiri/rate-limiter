from flask import Flask, request
import time
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Rate limit settings
TOTAL_LIMIT= int(os.getenv("TOTAL"))  # Maximum number of requests 
WINDOW = int(os.getenv("WINDOW"))
PARTITION_KEY = os.getenv("PARTITION_KEY")
PARTITION_KEY_ACTIVE = (int(os.getenv("PARTITION_KEY_ACTIVE")) == 1)
PARTITION_LIMIT = int(os.getenv("PARTITION_LIMIT"))

# In-memory storage for request timestamps
requests = {}
total = []

def rate_limit_check(partition_key: str=None):
    now = int(time.time())
    global total
    global requests
    
    total = list(filter(lambda x: now - x <= WINDOW, total))
    if len(total) >= TOTAL_LIMIT:
        return False

    elif PARTITION_KEY_ACTIVE and partition_key != None:
        
        r = requests.get(partition_key, [])
        r = list(filter( lambda x: now - x <= WINDOW, r ))
        if len(r) >= PARTITION_LIMIT:
            return False
        else:
            total.append(now)
            r.append(now)
            requests[partition_key] = r
            return True  
    else:
        return True  

@app.route('/')
def check():
    """
    
    """
    req = request.json
    # print("request", req)
    if not rate_limit_check(req.get(PARTITION_KEY, None)):
        return 'Rejected', 400
    return 'Accepted', 200


if __name__ == '__main__':
    app.run()