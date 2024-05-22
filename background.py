import os
import requests
import datetime
import sys
import bs4
from PIL import Image,ImageEnhance



def main(args):
    if len(args) == 0:
        offset = 0
    else:
        offset = abs(int(args[0]))
    date = datetime.datetime.now() - datetime.timedelta(days=offset)
    date = date.strftime("%Y-%m-%d")
    #print(date)
    path = os.path.expanduser("~")
    path = os.path.join(path,"Pictures","picture-of-the-day", date)
    version = sys.version.split(" ")[0]
    user_agent = "Python/" + version + " ( dserver.lukas.pahomovs@gmail.com )"
    headers = {
        "user-agent": user_agent
    }
    url = "https://commons.wikimedia.org/wiki/Template:Potd/" + date
    #print(url)
    response = requests.get(url, headers=headers)    
    site = response.text
    #print(site)
    image_name = bs4.BeautifulSoup(site, "html.parser").find("div", {"class": "mw-content-ltr mw-parser-output"}).find("a")["href"].split("/")[-1]
    #print(image_name)
    image_url = "https://commons.wikimedia.org/wiki/" + image_name
    #print(image_url)
    image_response = requests.get(image_url, headers=headers)
    image_site = image_response.text
    original_image_url = bs4.BeautifulSoup(image_site, "html.parser").find("div", {"class": "mw-content-ltr fullMedia"}).find("a")["href"]
    
    #print(original_image_url)
    original_image_url = original_image_url
    #print(original_image_url)
    image = requests.get(original_image_url, headers=headers)
    image_path = os.path.join(path, image_name).replace("File:", "")
    os.makedirs(path, exist_ok=True)
    with open(image_path, "wb") as file:
        file.write(image.content)
    #print(image_path)
    image=Image.open(image_path)
    enhanser = ImageEnhance.Brightness(image)
    image = enhanser.enhance(0.5)
    image.save(image_path)

    command = "gsettings set org.gnome.desktop.background picture-uri-dark"
    
    command = command + " 'file://" + image_path + "'"
    os.system(command)

if __name__ == "__main__":
    main(sys.argv[1:])
