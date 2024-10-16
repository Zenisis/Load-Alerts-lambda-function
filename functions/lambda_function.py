import urllib3
import json
import time

def lambda_handler(event, context):
    WEBHOOK = "https://hooks.slack.com/services/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"
    
    # List of URLs to monitor
    URLs = [
        "https://estatenvy.com",
        "https://1851dev.com",
        "https://1851franchise.com",
        "https://room1903.com"
    ]
    
    http = urllib3.PoolManager()
    responses = []

    for URL in URLs:
        try:
            start = time.time()
            response = http.request('GET', URL)
            load_time = time.time() - start
            
            if load_time > 3:
                msg = {
                    "text": f"Alert: {URL} took {load_time:.2f} seconds to load"
                }
                
                # Send alert to Slack
                http.request(
                    'POST',
                    WEBHOOK,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(msg)
                )

            # Collecting responses
            responses.append({
                "url": URL,
                "load_time": f"{load_time:.2f} seconds",
                "status_code": response.status
            })

        except Exception as e:
            error_msg = {
                "text": f"Error monitoring {URL}: {str(e)}"
            }
            
            # Send error message to Slack
            try:
                http.request(
                    'POST',
                    WEBHOOK,
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(error_msg)
                )
            except:
                pass
            
            responses.append({
                "url": URL,
                "error": str(e)
            })

    return {
        "statusCode": 200,
        "body": json.dumps(responses)
    }
