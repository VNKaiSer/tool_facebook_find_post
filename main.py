from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from urllib.parse import quote
from utils import GetPageIDFacebook
from utils import CheckBlackListPost as checkPost
from utils import CheckBlackListPage as checkPage
from utils import DeletePageCheck as deletePage
# from telegram_bot import bot_handler
def create_driver():
    proxy = {
        'proxy':  
            {
                'https': 'https://NhdwMsiAD:UauahJVDR@185.179.198.213:64296',
                'http': 'http://NhdwMsiAD:UauahJVDR@185.179.198.213:64296',
                'no_proxy': 'localhost,127.0.0.1'
            },
    }
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--log-level=3')
    
    # options.add_argument('--headless')  
    chrome_options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(seleniumwire_options=proxy, options=chrome_options)
    return driver

import telebot
bot = telebot.TeleBot('6950197694:AAFhd_3Q-AdxzswSadSqJ1d6xwi9d_o0VHA')
group = ['-1002019053383', '-1002178883406']
time_reload = 1500
xpath_element = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[5]/div[2]/div[2]/div[4]/div[1]'
time_rety = 0
def send_telegram_message(message):
    for group_id in group:
        bot.send_message(group_id, message)
    
def main(keyword):
    global time_reload
    global xpath_element
    global time_rety
    driver = create_driver()
    encoded_keyword = quote(keyword, safe='')
    url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=VN&q={encoded_keyword}&search_type=keyword_unordered&media_type=all"
    driver.get(url)
    print("Get data")
    actions = ActionChains(driver)
    root_tab = driver.current_window_handle
    
    POST = '//*[contains(@class, "xrvj5dj xdq2opy xexx8yu xbxaen2 x18d9i69 xbbxn1n xdoe023 xbumo9q x143o31f x7sq92a x1crum5w")]'
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, POST))
        )
    except Exception as e:
        driver.refresh()
    
    i = 0
    while True:  # Điều chỉnh phạm vi nếu cần thiết
        time.sleep(1)
        if time_reload == 0:
            driver.quit()
            return
        try:
            i = i + 1
            if i == time_reload:
                deletePage.delete_page_check()
                driver.refresh()
                i = 0
                continue
            try: 
                WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.XPATH, xpath_element + f'/div[{i}]'))
                )
                # Tìm phần tử bài viết
                posts_element = driver.find_element(By.XPATH, xpath_element + f'/div[{i}]')
            except Exception as e:
                if time_rety < 3:
                    time_rety = time_rety + 1
                    driver.refresh()
                    continue
                send_telegram_message('Vui lòng xét lại XPATH')
                driver.quit()
                return
                
            actions.move_to_element(posts_element).perform()
            html_content = posts_element.get_attribute('outerHTML')

            soup = BeautifulSoup(html_content, 'html.parser')
            
            links = soup.find_all('a')
            if links:
                id_page = GetPageIDFacebook.get_id_page_fb(links[0].get('href'))
            else :
                continue
            if checkPage.check_black_list_page(id_page):
                continue
            

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(links[0].get('href'))
            
            # index = 0
            # for span in spans:
            #     index = index + 1
            #     print(f'[{index}]'+span.text)
            time.sleep(5)

            post_selector = "a[href*='/posts/']"
            video_selector = "a[href*='/videos/']"
            permalink_selector = "a[data-sigil='feed-ufi-permalink']"

            posts = driver.find_elements(By.CSS_SELECTOR, post_selector)
            videos = driver.find_elements(By.CSS_SELECTOR, video_selector)
            permalinks = driver.find_elements(By.CSS_SELECTOR, permalink_selector)
            
            links_collected = []

            for element in (posts + videos + permalinks):
                link_collected = element.get_attribute("href")
                if link_collected:
                    links_collected.append(link_collected)
                if len(links_collected) >= 1:
                    break
            print(link_collected)

            for link_collected in enumerate(links_collected):
                id_page = ""
                try:
                    id_page = GetPageIDFacebook.get_id_page_fb(link_collected)
                except Exception as e:
                    send_telegram_message(link_collected)
                if checkPost.check_black_list_post(id_page):
                    continue
                send_telegram_message(id_page)
                
            driver.close()
            driver.switch_to.window(root_tab)
            time.sleep(3)
        except Exception as e:
            driver.close()
            driver.switch_to.window(root_tab)
            continue

try:
    import telebot

    bot = telebot.TeleBot('6950197694:AAFhd_3Q-AdxzswSadSqJ1d6xwi9d_o0VHA')
    command_help = {
        '/start': 'Bắt đầu bot',
        '/help': 'Hiển thị trợ giúp',
        '/groupinfo': 'Thể thay đổi nhóm',
        '/tu_khoa': 'Nhập từ khoá để lấy link',
        '/set_reload': 'Thay đổi số posts để reload',
        '/set_xpath': 'Thay đổi xpath ',
    }
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Xin chào! Tôi là bot Telegram của bạn.")

    @bot.message_handler(commands=['groupinfo'])
    def group_info(message):
        chat_id = message.chat.id
        chat_type = message.chat.type
        chat_title = message.chat.title
        
        bot.reply_to(message, f"ID của nhóm: {chat_id}\nLoại nhóm: {chat_type}\nTên nhóm: {chat_title}")

    @bot.message_handler(commands=['tu_khoa'])
    def tu_khoa(message):
        keyword = message.text.split(maxsplit=1)[1]
        main(keyword)
        
    @bot.message_handler(commands=['help'])
    def help(message):
        help_text = "\n".join([f"{key}: {value}" for key, value in command_help.items()])
        
        bot.reply_to(message, help_text)

    @bot.message_handler(commands=['set_reload'])
    def set_reload(message):
        global time_reload
        time_reload = message.text.split(maxsplit=1)[1]
        time_reload = int(time_reload)

    @bot.message_handler(commands=['set_xpath'])
    def set_xpath(message):
        global xpath_element
        xpath_element = message.text.split(maxsplit=1)[1]
        
        
        
            
    bot.polling()

except:
    print()