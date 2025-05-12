import json
import time
import yaml
import os
import pickle
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def save_cookies(driver, path):
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path):
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def instagram_login(driver, username, password):
   # Check for saved cookies
   try:
       driver.get("https://www.instagram.com")
       load_cookies(driver, "instagram_cookies.pkl")
       driver.refresh()
       
       # Verify login with cookies
       time.sleep(3)
       try:
        #    WebDriverWait(driver, 5).until(
        #        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/')]"))
        #    )
           print("Logged in using saved cookies!")
           return True
       except:
           print("Cookie login failed, trying manual login...")
   except:
       print("No saved cookies found, proceeding with manual login...")

   # Manual login if cookies fail
   try:
       driver.get("https://www.instagram.com/accounts/login/")
       time.sleep(3)

       username_field = WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.NAME, "username"))
       )
       username_field.send_keys(username)

       password_field = driver.find_element(By.NAME, "password")
       password_field.send_keys(password)
       password_field.send_keys(Keys.RETURN)

       time.sleep(5)

       try:
           save_info_button = WebDriverWait(driver, 5).until(
               EC.element_to_be_clickable((By.XPATH, "//button[text()='Save info']"))
           )
           save_info_button.click()
       except:
           print("No 'Save info' prompt or already handled")

       # Verify login success
       driver.get("https://www.instagram.com")
       time.sleep(3)
       
       try:
        # WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/')]|//a[contains(@href, '/reel/')]"))
        # )
        print("Successfully logged in!")
        # Save cookies after successful login
        save_cookies(driver, "instagram_cookies.pkl")
        return True
       except:
           print("Login verification failed") 
           return False

   except Exception as e:
       print(f"Error during login: {e}")
       return False

def get_post_date(driver):
    try:
        time_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "time"))
        )
        return datetime.strptime(time_element.get_attribute("datetime")[:10], "%Y-%m-%d")
    except:
        return None
    
def scroll_down(driver):
    """Scroll down comments section"""
    try:
        comment_area = driver.find_element(By.XPATH, "//ul[contains(@class, '_a9ym')]")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_area)
        time.sleep(2)
    except Exception as e:
        print(f"Error scrolling: {e}")

def expand_replies(driver):
   while True:
       try:
           # Find first unexpanded replies button
           first_button = driver.find_element(By.XPATH, "//span[contains(text(),'View replies')]")
           if first_button.is_displayed():
               driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
               time.sleep(5)
               first_button.click()
               time.sleep(2)
           else:
               break
       except:
           break

# def scrape_comments(driver, profile_url, start_date=None, end_date=None):
#     print(f"\nScraping comments from: {profile_url}")
#     print(f"Date range: {start_date} to {end_date}")
    
#     driver.get(profile_url)
#     time.sleep(3)
    
#     processed_urls = set()
#     all_comments = []
#     last_height = 0
#     scroll_count = 0
#     max_scrolls = 1000
#     too_old_count = 0  # Counter for too old posts
#     too_old_limit = 4  # Limit for closing on too old posts
    
#     while scroll_count < max_scrolls:
#         posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]|//a[contains(@href, '/reel/')]")
#         total_posts = len(posts)
        
#         for i in range(total_posts):
#             current_posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]|//a[contains(@href, '/reel/')]")
#             if i >= len(current_posts):
#                 break
                
#             post = current_posts[i]
#             post_url = post.get_attribute('href')
            
#             if post_url in processed_urls:
#                 continue
                
#             try:
#                 print(f"\nChecking post: {post_url}")
#                 processed_urls.add(post_url)
                
#                 driver.execute_script("arguments[0].click();", post)
#                 time.sleep(3)
                
#                 post_date = get_post_date(driver)
#                 print(f"Post date: {post_date}")
                
#                 if post_date:
#                     if start_date and post_date < start_date:
#                         too_old_count += 1
#                         print(f"Post too old ({too_old_count}/{too_old_limit})")
#                         if too_old_count >= too_old_limit:
#                             print("Too old limit reached, stopping scraping for this profile.")
#                             driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
#                             return all_comments
#                         else:
#                             driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
#                             continue
                    
#                     if end_date and post_date > end_date:
#                         print("Post too recent, skipping")
#                         driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
#                         continue
                    
#                     too_old_count = 0  # Reset the too old counter for valid posts
#                     print("Post within date range, collecting comments")
                    
#                     load_more_count = 0
                    
#                     # Load all comments
#                     while True:
#                         print("Attempting to load more comments...")
#                         try:
#                             load_more_button = WebDriverWait(driver, 5).until(
#                                 EC.element_to_be_clickable((By.XPATH, "//button//*[contains(text(), 'Load more comments') or contains(text(), 'View more comments')]/.."))
#                             )
#                             load_more_button.click()
#                             load_more_count += 1
#                             time.sleep(2)
#                         except TimeoutException:
#                             print("No more comments to load.")
#                             break
                        
#                         scroll_down(driver)
                    
#                     print("Finished loading comments. Now collecting comment data...")
                    
#                     # Collect comments
#                     comment_elements = driver.find_elements(By.XPATH, "//ul[contains(@class, '_a9ym')]//li[contains(@class, '_a9zj')]")
#                     print(f"Found {len(comment_elements)} comments")
                    
#                     # First get normal comments
#                     for comment in comment_elements:
#                         try:
#                             username = comment.find_element(By.XPATH, ".//h3[contains(@class, '_a9zc')]//a").text
#                             comment_text = comment.find_element(By.XPATH, ".//div[contains(@class, '_a9zs')]//span").text
#                             timestamp = comment.find_element(By.XPATH, ".//time").get_attribute("datetime") 
                            
#                             comment_data = {
#                                 "post_url": post_url,
#                                 "post_date": post_date.strftime("%Y-%m-%d"), 
#                                 "username": username,
#                                 "comment": comment_text,
#                                 "comment_timestamp": timestamp,
#                                 "replies": []
#                             }
#                             all_comments.append(comment_data)
#                         except:
#                             continue

#                     # Then get all replies as separate comments
#                     try:
#                         expand_replies(driver)
#                         reply_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'a9ye')]")
                        
#                         for reply in reply_elements:
#                             reply_text = reply.find_element(By.XPATH, ".//div[contains(@class, '_a9zs')]//span").text
#                             reply_user = reply.find_element(By.XPATH, ".//h3[contains(@class, '_a9zc')]//a").text
#                             timestamp = reply.find_element(By.XPATH, ".//time").get_attribute("datetime")
                            
#                             reply_data = {
#                                 "post_url": post_url,
#                                 "post_date": post_date.strftime("%Y-%m-%d"),
#                                 "username": reply_user,
#                                 "comment": reply_text, 
#                                 "comment_timestamp": timestamp,
#                                 "replies": []
#                             }
#                             all_comments.append(reply_data)
#                     except Exception as e:
#                         print(f"No replies found: {e}")

#                 # Close post
#                 close_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']"))
#                 )
#                 close_button.click()
#                 time.sleep(2)

#             except Exception as e:
#                 print(f"Error processing post: {e}")
#                 try:
#                     driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
#                 except:
#                     pass
#                 continue

#         # Scroll to load more posts
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
        
#         if new_height == last_height:
#             print("Reached end of page")
#             break
        
#         last_height = new_height
#         scroll_count += 1
#         print(f"Collected total of {len(all_comments)} comments from {len(processed_urls)} posts")

#     return all_comments

def scrape_comments(driver, profile_url, start_date=None, end_date=None):
   driver.get(profile_url)
   time.sleep(3)
   
   processed_urls = set()
   all_comments = []
   last_height = 0
   scroll_count = 0
   max_scrolls = 1000
   too_old_count = 0
   too_old_limit = 4
   
   while scroll_count < max_scrolls:
       posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]|//a[contains(@href, '/reel/')]")
       total_posts = len(posts)
       
       for i in range(total_posts):
           current_posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]|//a[contains(@href, '/reel/')]")
           if i >= len(current_posts):
               break
               
           post = current_posts[i]
           post_url = post.get_attribute('href')
           
           if post_url in processed_urls:
               continue
               
           try:
               print(f"\nChecking post: {post_url}")
               processed_urls.add(post_url)
               
               driver.execute_script("arguments[0].click();", post)
               time.sleep(3)
               
               post_date = get_post_date(driver)
               print(f"Post date: {post_date}")
               
               if post_date:
                   if start_date and post_date < start_date:
                       too_old_count += 1
                       print(f"Post too old ({too_old_count}/{too_old_limit})")
                       if too_old_count >= too_old_limit:
                           print("Too old limit reached, stopping scraping for this profile.")
                           driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
                           return all_comments
                       else:
                           driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
                           continue
                   
                   if end_date and post_date > end_date:
                       print("Post too recent, skipping")
                       driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
                       continue
                   
                   too_old_count = 0
                   print("Post within date range, collecting comments")
                   
                   while True:
                       print("Attempting to load more comments...")
                       try:
                           load_more_button = WebDriverWait(driver, 5).until(
                               EC.element_to_be_clickable((By.XPATH, "//button//*[contains(text(), 'Load more comments') or contains(text(), 'View more comments')]/.."))
                           )
                           load_more_button.click()
                           time.sleep(2)
                       except TimeoutException:
                           print("No more comments to load.")
                           break
                       
                       scroll_down(driver)
                   
                   print("Finished loading comments. Now collecting comment data...")
                   
                   comment_elements = driver.find_elements(By.XPATH, "//ul[contains(@class, '_a9ym')]//li[contains(@class, '_a9zj')] | //ul[contains(@class, '_a9ym')]//li[contains(@class, '_a9ye')]")
                   print(f"Found {len(comment_elements)} comments")
                   
                   for comment in comment_elements:
                       try:
                           username = comment.find_element(By.XPATH, ".//h3[contains(@class, 'x3nfvp2')]//a").text
                           comment_text = comment.find_element(By.XPATH, ".//div[contains(@class, 'xt0psk2')]//span").text
                           timestamp = comment.find_element(By.XPATH, ".//time").get_attribute("datetime") 
                           
                           comment_data = {
                               "post_url": post_url,
                               "post_date": post_date.strftime("%Y-%m-%d"), 
                               "username": username,
                               "comment": comment_text,
                               "comment_timestamp": timestamp,
                           }
                           all_comments.append(comment_data)
                       except:
                           continue

               close_button = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']"))
               )
               close_button.click()
               time.sleep(2)

           except Exception as e:
               print(f"Error processing post: {e}")
               try:
                   driver.find_element(By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']//*[name()='svg']").click()
               except:
                   pass
               continue

       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       time.sleep(5)
       new_height = driver.execute_script("return document.body.scrollHeight")
       
       if new_height == last_height:
           print("Reached end of page")
           break
       
       last_height = new_height
       scroll_count += 1
       print(f"Collected {len(all_comments)} comments from {len(processed_urls)} posts")

   return all_comments

def main():
    config = read_config("config.yml")
    username = config['username']
    password = config['password']
    influencers = config['influencers']

    # Get date range from user
    print("\nEnter date range (format: YYYY-MM-DD):")
    start_date_input = input("Start date (format: YYYY-MM-DD): ")
    end_date_input = input("End date (format: YYYY-MM-DD): ")

    # Convert to datetime objects
    try:
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d")

        if start_date > end_date:
            raise ValueError("Start date cannot be after End date. Please enter a valid date range.")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        return

    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        if not instagram_login(driver, username, password):
            print("Login failed! Exiting...")
            return

        # Create output directory
        output_dir = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(output_dir, exist_ok=True)

        # Process each influencer
        for influencer in influencers:
            profile_url = influencer['profile_url']
            comments = scrape_comments(driver, profile_url, start_date, end_date)

            # Save comments
            influencer_name = profile_url.rstrip('/').split('/')[-1]
            output_file = os.path.join(output_dir, f"{influencer_name}_comments.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=4)
            
            print(f"\nSaved {len(comments)} comments for {influencer_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    main()