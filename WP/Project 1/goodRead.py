import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "AMuriwqLcks7Iin0ZQaS1A", "isbns": "9781632168146"})
print(res.json())