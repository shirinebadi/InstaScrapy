from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
 

def login(): 
 driver = webdriver.Chrome(executable_path='C:/Users/Shirin/chromedriver.exe')
 driver.get('https://www.instagram.com/accounts/login/')
 time.sleep(10)
 
 dom = driver.find_element_by_xpath('//*')
 username = dom.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input')
 password = dom.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input')
 login_button = dom.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button')
 
 username.send_keys('shirin__ebadi')
 password.send_keys('password')
 
 login_button.click()
 time.sleep(5)
 
 return driver

def request(driver, requestList): 
 reqCount = 0
 BasicInfos =[]
 PostInfos = []
 totalInfo = []
 
 for req in requestList:
  html = driver.get("https://www.instagram.com/" + req + "/?__a=1") 
  soup = BeautifulSoup(driver.page_source, "html.parser").get_text()
  jsondata = json.loads(soup)
  
  Info,numberOfPosts = parseBasicInfo(jsondata)
  BasicInfos.append(Info)
  if numberOfPosts != 0 and numberOfPosts > 11 :
      numberOfPosts = 11
      PostInfos = parsePostInfo(jsondata,numberOfPosts)
      
  totalInfo += BasicInfos[reqCount],PostInfos[:numberOfPosts]
  
  reqCount = reqCount + 1
  
 return totalInfo
 
   
def parseBasicInfo(jsondata):
  typeP = "None-Business"
  public = "public"
    
  full_name = jsondata['graphql']['user']['full_name']
  biography = jsondata["graphql"]["user"]["biography"]
  website = jsondata["graphql"]["user"]["external_url"]
  numberOfollowers = jsondata["graphql"]["user"]["edge_followed_by"]["count"]
  numberOfollowing = jsondata["graphql"]["user"]["edge_follow"]["count"]
  businessacount = jsondata["graphql"]["user"]["is_business_account"]
  if businessacount:
      typeP = "Business"
  isprivate = jsondata['graphql']['user']['is_private']
  if isprivate:
      public = "private"
  numberOfPosts = jsondata['graphql']['user']['edge_owner_to_timeline_media']['count']
  
  BasicInfo = [{"full_name": full_name,
                "biography": biography,
                "Website": website,
                "No. followers": numberOfollowers,
                "No. following": numberOfollowing,
                "Type of Account": typeP,
                "Public/Private": public,
                "No. posts": numberOfPosts}]
 
  return BasicInfo,numberOfPosts

def parsePostInfo(jsondata,num):
    PostInfo = []
      
    for n in range (num):
        typeOfPost = jsondata['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['__typename']
        dimensions =  jsondata['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['dimensions']
        urlDisplay =  jsondata['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['display_url']
        caption =  jsondata['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['edge_media_to_caption']['edges'][0]['node']['text']
        comments = jsondata['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['edge_media_to_comment']['count']
        likes = jsondata['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['edge_liked_by']['count']
        
        PostInfo.append([{"typeOfPost": typeOfPost,
                          "dimension":dimensions,
                          "url": urlDisplay,
                          "caption": caption,
                          "No. comments": comments,
                          "No. likes": likes}])
        
    return PostInfo

if __name__ == "__main__":
 requestList = {"saman2000hoseini","shirin__ebadi","instagram"}
 
 driver = login()

 Info = request(driver, requestList)
 for n in range(len(Info)):
    if Info[n] is not None:
     json.dumps(Info[n])
 
 file = open("beautifulSoap.txt", "w", encoding='utf-8')
 file.write(repr(Info))
 file.close() 

 driver.quit()
