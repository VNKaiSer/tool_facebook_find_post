import requests
def get_id_page_fb(url_page):
    url = "https://id.traodoisub.com/api.php"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "vi,vi-VN;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://id.traodoisub.com",
        "priority": "u=1, i",
        "referer": "https://id.traodoisub.com/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        "link": url_page
    }
    response = requests.post(url, headers=headers, data=data)
    json_data = response.json()
    try:
        id = json_data['id']
        if json_data['success'] == 200 and json_data['code'] == 200:
            return f"https://facebook.com/{id}"
        else:
            return url_page
    except:
        return url_page
