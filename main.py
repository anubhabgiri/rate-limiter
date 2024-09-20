from flask import Flask, request
import time

app = Flask(__name__)

# Rate limit settings
TOTAL_LIMIT= 10  # Maximum number of requests 
WINDOW = 86400

# In-memory storage for request timestamps
requests = {}
total = []

def rate_limit_check(user_id: str, limit: int):
    # update logic here
    now = int(time.time())
    global total
    global requests
    total = list(filter(lambda x: now - x <= WINDOW, total))
    if len(total) >= TOTAL_LIMIT:
        return False

    else:
        
        r = requests.get(user_id, [])
        r = list(filter( lambda x: now - x <= WINDOW, r ))
        if len(r) >= limit:
            return False
        else:
            total.append(now)
            r.append(now)
            requests[user_id] = r
            return True    

@app.route('/')
def check():
    """
    
    """
    req = request.json
    # TODO : basic request validation
    if not req.get("user_id"):
        return 'user ID is required', 400
    if not rate_limit_check(req.get("user_id"), req.get("limit")):
        return 'Rejected', 400
    return 'Accepted', 200


if __name__ == '__main__':
    app.run()