import requests,shutil,os
from random import randint
from bs4 import BeautifulSoup
from lxml import html
class hfox():
    def __init__(self):
        self.hfoxTerm = ""
    def printout(self):
        print (self.hfoxTerm)
    def get_data(self,pc,tree,xpath):
        tree = html.fromstring(pc.content)
        caption = tree.xpath(xpath)
        pagenum = ''.join(caption)
        return pagenum
    def Search(self):
        #20 results per page
        #get number of pages
        url = "https://hentaifox.com/search/{0}/pag/1/".format(self.hfoxTerm)
        print (url)
        pageContent=requests.get(url, headers = {'User-agent': 'fox-bot'})
        html.fromstring(pageContent.content)
        tree = html.fromstring(pageContent.content) #get the content of the supplied url
        page_xpath = '//*[@id="content"]/div[1]/div[2]/div/h2//text()'
        caption = tree.xpath(page_xpath)
        pagenum = ''.join(caption)
        
        #some numbers so that we can properly truncuate no matter what search it is
        truncfront = 24 + len(self.hfoxTerm) + 16
        #more number singular
        truncend = 15

        manga_num = pagenum[truncfront:-truncend]
        page_num = int(manga_num)/20
        page_num = int(page_num)
        print ("{0} Pages in total".format(str(page_num)))
        print ("There are {0} manga from your searched term '{1}'".format(manga_num,self.hfoxTerm))

        #getting the unique manga ids, 20 per page, all href as well.
        base_id_list = tree.xpath('//a/@href')
        base_id_list = base_id_list[17:-5]
        parse_id_list = []
        for i in base_id_list:
            if not i.startswith("/gallery/"):
                pass
            else:
                parse_id_list.append(i)
        #there are twenty extra from the right hand side so we truncuate those
        parse_id_list = parse_id_list[:-20]
        
        manga_name_list = []
        #get manga names from page
        for i in range (1,21):
            name_xpath = '//*[@id="content"]/div[1]/div[3]/div[{0}]/a/div[2]//text()'.format(i)
            nm = tree.xpath(name_xpath)
            manga_name = ''.join(nm)
            manga_name_list.append(" " + manga_name.strip())

        #merge manga_name_list and parse_id_list together in order to have one list
        merged_list = [a + b for a, b in zip(parse_id_list, manga_name_list)]

        for i in merged_list:
            print ("[*] - " + i)
        user_choice_id = input ("Pick gallery link from the list above ex: /gallery/1/:")
        return user_choice_id
    def Download(self,hId,st):
        #sec_id = id[9:-1]

        url = "https://hentaifox.com{0}".format(hId)
        page_number_xpath = '//*[@id="content"]/div[1]/div[2]/div[2]/span[8]//text()'

        pageContent=requests.get(url, headers = {'User-agent': 'fox-bot'})
        tree = html.fromstring(pageContent.content) #get the content of the supplied url
        caption = tree.xpath(page_number_xpath)
        pagenum = ''.join(caption)

        #hentaifox gives the page number a different span number in some cases so we do this.
        num = 0
        while not pagenum.startswith("Pages"):
            pagenum = self.get_data(pageContent,tree,'//*[@id="content"]/div[1]/div[2]/div[2]/span[{0}]//text()'.format(str(num)))
            num+=1

        pagenum = pagenum[7:]
        pagenum = int(pagenum)
        print ("Pages: {0}".format(str(pagenum)))

        manga_name_xpath = '//*[@id="content"]/div[1]/div[2]/div[2]/h1//text()'
        caption = tree.xpath(manga_name_xpath)
        mgname = ''.join(caption)

        data = pageContent.text
        soup = BeautifulSoup(data, "lxml")

        img_link_list = []
        for i in soup.find_all('img'):
            img_link_list.append(i)
        this_one = img_link_list.pop(1)
        this_one = str(this_one)

        t_len = len (mgname)
        truncbeg = 10 + t_len + 7 + 4
        this_one = this_one[truncbeg:-12]
        print (this_one)
        if this_one.startswith("."):
            this_one = this_one [1:]
        this_one = "https://i." + this_one
        random = randint(1,2893579823759) #generate a random integer to make a folder that is random
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') #get desktop path
        if os.path.exists(desktop + "\\HentaiFox"):
            pass
        else:
            os.mkdir(desktop + "\\HentaiFox")
        os.mkdir(desktop + "\\HentaiFox\\" +str(random)) #make the folder with a random number name
        pagenum += 1
        os.chdir(desktop + "\\HentaiFox\\" + str(random) + "\\")
        for i in range (1,pagenum):
            x = this_one + "{0}".format(str(i) + ".jpg")
            name = "{0}.jpg".format(str(i))
            print (x)
            user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36"
            response = requests.get(x, stream=True,headers={'User-agent': user_agent})
            with open (name, 'wb') as outfile:
                shutil.copyfileobj(response.raw,outfile)
