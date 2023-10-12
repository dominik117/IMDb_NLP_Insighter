def find_latest_fetch(*args):
    highest_id = 0
    for data in args:
        latest_id = max(map(int, data.keys())) if data else 0
        if latest_id > highest_id:
            highest_id = latest_id 
    return highest_id