from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import requests
from hashlib import new
import requests
import json
import time
def sendu(url112):
        import mysql.connector
        import time    

        # host="localhost",
        # user="root",
        # password="",
        # database="coursefolder_main"
        from bs4 import BeautifulSoup
        from bs4 import BeautifulSoup
        import requests
        header_new = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        v=url112.split('/?', 5)
        url1=v[0]
        html_text=requests.get(url1,headers=header_new).text
        soup=BeautifulSoup(html_text,'lxml')
        slugurl= url1[29:]
        try:

          title=soup.find('h1', class_='clp-lead__title--small').text
          headline=soup.find('div', class_='clp-lead__headline').text
          article_whatyoulearn=soup.find('div', class_='ud-component--course-landing-page-udlite--whatwillyoulearn')
          article_requirements=soup.find('div', class_='ud-component--course-landing-page-udlite--requirements')
          article_descp=soup.find('div', attrs={'data-purpose':'safely-set-inner-html:description:description'})
          current_date=time.strftime('%Y-%m-%d %H:%M:%S')
        except:
          print("ppp")
          return
        for item in soup.find_all('img', limit=2):
            if item['src'][0:5] == 'https':
                imgURL = item['src']
        
        #new code
        headers1={
                "Accept": "application/json, text/plain, */*",
                "Authorization": "Basic Nk1SRVBHTXYwdTRsUk9WTFhpTXdsN2RBeDJRc2hmd2JmRHBGbXZsRDptT1hhZnpITUpmY1JPRnNPa2cyOWJBOXAxUXp2cjBSVUV2WjJscHBRdnBYV3ZDcGx2ZVlLdUg4NGVRYzgzc1JMcnozZGpKUFo5MHNiNXhQNTNvdzJPajJhVXI4NmtqNGhBRlpvQ2YyOWJWTldKWkphSjlQNHZUVzFXaFVCb1FLZg==",
                "Content-Type": "application/json;charset=utf-8"
              }
        fetchonly_coupon=url112.split('couponCode=')
        html_text7=requests.get(url112,headers=header_new).text
        soup7=BeautifulSoup(html_text7,'lxml')
        try:
          course_id=soup7.find('body', {'class':"ud-app-loader ud-component--course-landing-page-udlite udemy"})['data-clp-course-id']
        except:
          tempcourse=imgURL.split('/',5)
          tempcourse1=tempcourse[5].split('_')
          course_id=tempcourse1[0]
        check_url="https://www.udemy.com/api-2.0/course-landing-components/{}/me/?couponCode={}&components=price_text".format(course_id,fetchonly_coupon[1])
        check_url_response=requests.get(check_url,headers=headers1)
        b=check_url_response.text
        y = json.loads(b)
        try:
          user_remain=y['price_text']['data']['pricing_result']['campaign']['uses_remaining']
          total_user=y['price_text']['data']['pricing_result']['campaign']['maximum_uses']
        except:
          user_remain='None'
        if str(user_remain) == 'None':
            print("Coupon Not Working")
            return
        else:
            print(user_remain)
        url11=url1+"/?couponCode="+fetchonly_coupon[1]
        print(url11)
        #new code end

        # print(imgURL)
        # catg=soup.find('a', class_='udlite-heading-sm').text
        mydb = mysql.connector.connect(
        host="192.185.62.74",
        user="preptght_coulder",
        password="A7GR;-~b#F3&",
        database="preptght_coursefo"
        )
        mycursor = mydb.cursor()
        search_article="SELECT count(*) FROM course_details WHERE articleSlug=%s"
        l1 = (slugurl,)
        mycursor.execute(search_article, l1)
        myresult1 = mycursor.fetchall()
        # mycursor.close()
        # mycursor = mydb.cursor()
        if myresult1 == [(0,)]:
          sql = "INSERT INTO course_details (articleSlug,articleTitle,articleHeadline,articleWhat,articleReq,articleDescription,articleDate,articlePhoto,couponlink,total_enroll,total_enroll_pending,coupon_live_status,courseid,coursecoupon) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
          val = (slugurl,title,headline,'str(article_whatyoulearn)',str(article_requirements),str(article_descp),current_date,imgURL,url11,total_user,user_remain,'1',course_id,fetchonly_coupon[1])
          mycursor.execute(sql, val)
          laststoredid=mycursor.lastrowid
          mydb.commit()
          print('Record inserted course_details successfully...')
          mycursor.close()

        else:
          mycursor = mydb.cursor()
          sql_update_query = "Update course_details set articleDescription = %s,articleDate = %s,couponlink = %s,total_enroll=%s,total_enroll_pending=%s,coupon_live_status=%s,coursecoupon=%s,courseid=%s where articleSlug = %s"
          input_data = (str(article_descp),current_date,url11,total_user,user_remain,'1',fetchonly_coupon[1],course_id,slugurl)
          mycursor.execute(sql_update_query, input_data)
          mydb.commit()
          print('Record updated in course_details successfully...')
          laststoredid=0
          mycursor.close()

        category = []
        try:
          # topic-menu topic-menu-condensed ud-breadcrumb udlite-breadcrumb
          # topic-menu ud-breadcrumb udlite-breadcrumb
          cats = soup.find('div',{'class':'topic-menu udlite-breadcrumb'}).findAll('a')
        except:
          try:
            cats = soup.find('div',{'class':'topic-menu topic-menu-condensed udlite-breadcrumb'}).findAll('a')
          except:
            try:
              cats = soup.find('div',{'class':'topic-menu topic-menu-condensed ud-breadcrumb udlite-breadcrumb'}).findAll('a')
            except:
              cats = soup.find('div',{'class':'topic-menu ud-breadcrumb udlite-breadcrumb'}).findAll('a')
        for cat in cats:
            category.append(cat.text)
        if len(category)<3:
            category.append(' ')
            if len(category)<3:
              category.append(' ')
        elif len(category)<2:
            category.append(' ')
        else:
            pass
        
        c1=category[0]
        c2=category[1]
        c3=category[2]
        d1=c1.replace('&','and')
        slug1=d1.replace(' ','-')
        d2=c2.replace('&','and')
        slug2=d2.replace(' ','-')
        d3=c3.replace('&','and')
        slug3=d3.replace(' ','-')

        def check_cat1():
          mycursor = mydb.cursor()
          search_cat1 = "SELECT count(*) FROM category WHERE categorySlug = %s"
          cat1 = (slug1, )
          mycursor.execute(search_cat1, cat1)
          myresult1 = mycursor.fetchall()
          if myresult1 == [(0,)]:
            sql = "INSERT INTO category (categoryName,categorySlug) VALUES (%s, %s)"
            val = (c1,slug1)
            mycursor.execute(sql, val)
            mydb.commit()
            print('Record inserted category 1 successfully...')
            mycursor.close()
        def check_cat2():
          mycursor = mydb.cursor()
          search_cat2 = "SELECT count(*) FROM category WHERE categorySlug = %s"
          cat2 = (slug2, )
          mycursor.execute(search_cat2, cat2)
          myresult2 = mycursor.fetchall()
          if myresult2 == [(0,)]:
            sql = "INSERT INTO category (categoryName,categorySlug) VALUES (%s, %s)"
            val = (c2,slug2)
            mycursor.execute(sql, val)
            mydb.commit()
            print('Record inserted category 2 successfully...')
            mycursor.close()            
        def check_cat3():
          mycursor = mydb.cursor()
          search_cat3 = "SELECT count(*) FROM category WHERE categorySlug = %s"
          cat3 = (slug3, )
          mycursor.execute(search_cat3, cat3)
          myresult3 = mycursor.fetchall()
          if myresult3 == [(0,)]:
            sql = "INSERT INTO category (categoryName,categorySlug) VALUES (%s, %s)"
            val = (c3,slug3)
            mycursor.execute(sql, val)
            mydb.commit()
            print('Record inserted category 3 successfully...')
            mycursor.close()        
        check_cat1()
        check_cat2()
        check_cat3()

        def enter_data_in_cat_link1():
          mycursor = mydb.cursor()
          sql = "SELECT * FROM category WHERE categoryName = %s"
          adr = (c1, )
          mycursor.execute(sql, adr)
          myresult = mycursor.fetchall()
          mycursor.close()
          for x in myresult:
            pass
          mycursor = mydb.cursor()
          search_cat_l1="SELECT count(*) FROM cat_links WHERE articleId=%s and categoryId=%s"
          li1 = (laststoredid,x[0] )
          mycursor.execute(search_cat_l1, li1)
          myresult1 = mycursor.fetchall()
          mycursor.close()
          if myresult1 == [(0,)]:
            mycursor = mydb.cursor()
            insert_cat_link1 = "INSERT INTO cat_links (articleId,categoryId) VALUES (%s, %s)"
            vals = (laststoredid,x[0])
            mycursor.execute(insert_cat_link1, vals)
            mydb.commit()
            print('Record inserted link1 successfully...')
            mycursor.close()
        def enter_data_in_cat_link2():
          mycursor = mydb.cursor()
          sql = "SELECT * FROM category WHERE categoryName = %s"
          adr = (c2, )
          mycursor.execute(sql, adr)
          myresult = mycursor.fetchall()
          for x in myresult:
            pass
          mycursor.close()
          mycursor = mydb.cursor()
          search_cat_l1="SELECT count(*) FROM cat_links WHERE articleId=%s and categoryId=%s"
          li2 = (laststoredid,x[0] )
          mycursor.execute(search_cat_l1, li2)
          myresult2 = mycursor.fetchall()
          mycursor.close()
          if myresult2 == [(0,)]:
            mycursor = mydb.cursor()
            insert_cat_link2 = "INSERT INTO cat_links (articleId,categoryId) VALUES (%s, %s)"
            vals = (laststoredid,x[0])
            mycursor.execute(insert_cat_link2, vals)  
            mydb.commit()
            print('Record inserted link2 successfully...')
            mycursor.close()
        def enter_data_in_cat_link3():
          mycursor = mydb.cursor()
          sql = "SELECT * FROM category WHERE categoryName = %s"
          adr = (c3, )
          mycursor.execute(sql, adr)
          myresult = mycursor.fetchall()
          mycursor.close()
          for x in myresult:
            pass
          mycursor = mydb.cursor()
          search_cat_l3="SELECT count(*) FROM cat_links WHERE articleId=%s and categoryId=%s"
          li3 = (laststoredid,x[0] )
          mycursor.execute(search_cat_l3, li3)
          myresult1 = mycursor.fetchall()
          mycursor.close()
          if myresult1 == [(0,)]:
            mycursor = mydb.cursor()
            insert_cat_link3 = "INSERT INTO cat_links (articleId,categoryId) VALUES (%s, %s)"
            vals = (laststoredid,x[0])
            mycursor.execute(insert_cat_link3, vals)
            mydb.commit()
            print('Record inserted link3 successfully...')
            mycursor.close()
        if laststoredid==0:
          pass
        else:
          enter_data_in_cat_link1()
          enter_data_in_cat_link2()
          enter_data_in_cat_link3()
        # mydb.commit()
        # mycursor.close()
        print("data inserted in database now sending to all telegram channel and facebook page")


        import requests
        import urllib.request
        from urllib.parse import quote_plus
        customurl='https://coursefolder.net/'+slugurl
        urllib.request.urlretrieve(
          imgURL,
          "udemy.png")
        title=title.replace('&','and')
        title=title.replace('#',' ')
        title=title.replace('+',' ')
        title=title.replace('|',' ')
        headline=headline.replace('&','and')
        headline=headline.replace('#',' ')
        headline=headline.replace('+',' ')
        headline=headline.replace('|',' ')
        token='1855081152:AAEouaWih_34yB1bPu5a38iAtN_byXQUZsk'
        # today = datetime.now()
        # chatid="-1001495874688"
        chatid=["-1001122021184","-1001441778319","-1001373611822","-1001290287887","-1001605364144","-1001208383456","-1001311090027","-1001260176831","-1001211072152",'-1001476902406','-1001784609524','-1001745341573','-1001472582296','-1001605611990']
        # if(chatid=="-1001495874688"):
        #   cusername='@mr_vabs'
        for chat in chatid:
          # print(chat)
          if chat=="-1001122021184":
            m="@coursefolder"
          # elif chat=="-1001441778319": 
          #   m="@abtechyzone"
          elif chat=="-1001373611822": 
            m="@elearninglinks" 
          elif chat=="-1001605364144": 
            m="@freeudemybest"
          elif chat=="-1001208383456": 
            m="@udemy_coupon_4_u"
          elif chat=="-1001311090027": 
            m="@HackCoders"
          elif chat=="-1001260176831": 
            m="@bestfreecourses"
          elif chat=="-1001211072152": 
            m="@rahulsha_com_np"
          elif chat=="-1001476902406": 
            m="@loootersworld" 
          elif chat=="-1001784609524": 
            m="@udemycourse123"
          elif chat=="-1001745341573": 
            m="@freeudemycourses4us"
          elif chat=="-1001472582296": 
            m="@knowledgetre"
          elif chat=="-1001605611990": 
            m="@tklnd"
          else:
            m="@getstudyfevers"
          mee='''
<b>{}</b>

<i>{}</i>

Only {} Enrolls Left.

<u>Enroll Now:</u>
{}

<b> <i>Live Tracker:</i> </b> <a href="https://coursefolder.net/live-free-udemy-coupon.php"> Track More Udemy Free Live Coupons. Enroll Now ASAP</a>

<u>Keep learning and keep exploring.</u>
ID: {}
        '''.format(title,headline,user_remain,customurl,m)

          files={'photo':open('udemy.png','rb')}
          print(m)
          a=requests.post("https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption={}&parse_mode={}&disable_notification=1".format(token,chat,mee,"HTML"),files=files)
       
        #fb start
        print("telegram done")
        import facebook as fb
        access_token="EAAHNX7Tqn98BAHBdAyLSsvsHZAfmR1YJZBGmINqIEsSac6EFAv6TZCoAIhi7icN3f0clZC7el79596Jauhlum2Fok1DSn3HklZBXT26YB7UXF14dFBNfuMThHfcK5dXnK74eUCpavBtrRBMTMI3THxmZAwiT2NGaZB6ZBVKTzAEF2o7uP46LZBKbK"
        po=fb.GraphAPI(access_token)
        msg='''
{}
Enroll Now:
{}        
{}
Free for first 1000 Enrolls 

Enroll Now:
{}
#udemyfree #udemycoupon #freecourse #freecoupon #coursefolder
'''.format(title,customurl,headline,customurl)

        try: 
          # pass
          po.put_object("me","feed",message = msg,link=customurl)
        except:
          pass
        print('done sleep for 5 minutes')

#fetch from group
# def g():
while True:
    bot_token1="5666955251:AAHrAZ-6BWu0KVeuug9-pl430t55go7d7Cs"
    with open("upid.txt",'r') as up1:
        line_1 = up1.read()
        ost=int(line_1)
    resp7=requests.get("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_token1,ost))
    res7= resp7.text
    # print(res7)
    y = json.loads(res7)
    if (str(y) == "{'ok': True, 'result': []}"):
        print("id not found")
    else:
        newupdateid=y['result'][0]['update_id']
        if (ost == newupdateid):
            try:
              newmsg= y['result'][0]['message']['text']
            except:
              newmsg=" "
            try:
              msgcap= y['result'][0]['message']['caption']
            except:
              msgcap=" "
            #real.discount website
            if 'bit.ly' in newmsg or 'ift.tt' in newmsg:
                st=newmsg.split("https://")
                newst="https://"+st[1]
                url17=newst
                html_text7=requests.get(url17).text
                soup7=BeautifulSoup(html_text7,'lxml')
                title7=soup7.find('div', class_='col-xs-12 col-md-12 col-sm-12 text-center')
                y7=str(title7)
                # print(title7)
                v7=y7.split('<a href="')
                try:
                  aa7=v7[1].split('"')
                  am2=aa7[0]
                except:
                  am2="asd"
                if 'udemy.com' in am2:
                  am3= am2.split('/?', 5)
                  am4=am2.split('couponCode=')
                  am1=am3[0]+"/?couponCode="+am4[1]
                  with open("udemylink.txt",'r') as fp1:
                      Lines1 = fp1.read()
                      if am1 in Lines1:
                          pass
                      else:
                          with open('udemylink.txt', 'a') as outle:
                              outle.write("\n"+ am1)
                          sendu(am1)
            #tutorialbar website
            # print(newmsg)
            if 'tutorialbar.com' in msgcap:
                print("tutorialswala")
                try:
                  splitUlink1=msgcap.split('https://www.tutorialbar.com/')
                  splitUlink2=splitUlink1[1].split('/')
                  completeComLink='https://www.tutorialbar.com/'+ splitUlink2[0] + '/'
                  html_text7=requests.get(completeComLink).text
                  soup7=BeautifulSoup(html_text7,'lxml')
                  title7=soup7.find('a', class_='btn_offer_block re_track_btn')
                  y71=str(title7)
                  v71=y71.split('href="')
                  aa71=v71[1].split('"')
                  am11=aa71[0]
                  if ('couponCode' in am11):
                      am2=am11
                  else:
                    am2='am2'
                  if 'udemy.com' in am2:
                    am3= am2.split('/?', 5)
                    am4=am2.split('couponCode=')
                    am1=am3[0]+"/?couponCode="+am4[1]
                    with open("udemylink.txt",'r') as fp1:
                        Lines1 = fp1.read()
                        if am1 in Lines1:
                            pass
                        else:
                            with open('udemylink.txt', 'a') as outle:
                                outle.write("\n"+ am1)
                            sendu(am1)
                except:
                  pass
            # comidoc
            elif 'comidoc.net/udemy/' in msgcap:
              print("================================")           
              splitUlink1=msgcap.split('https://comidoc.net/udemy/')
              splitUlink2=splitUlink1[1].split('/')
              completeComLink='https://comidoc.net/udemy/'+ splitUlink2[0] + '/'
              html_text=requests.get(completeComLink).text
              soup=BeautifulSoup(html_text,'lxml')
              # searchForCourseIdFull=soup.select('section[class="mx-8 pt-3 pb-6 sm:pt-12 sm:pb-12"] div[class="mx-auto max-w-5xl items-center rounded border-2 border-th-primary-medium bg-white text-th-accent-medium sm:flex sm:space-x-5"] div[class="flex w-full flex-col justify-center border-b-2 border-th-primary-medium p-4 text-center sm:h-36 sm:w-1/4 sm:border-b-0 sm:border-r-2"] div[class="text-2xl font-medium"]')
              try:
                couponDoc1=soup.find('meta', property='og:image') 
                couponDoc12=str(couponDoc1).split('/')
                couponDoc13=couponDoc12[4].split('_')
                finalCourseID=couponDoc13[0]
                # finalCourseID=searchForCourseIdFull[0].text
              except:
                finalCourseID=1
              course_id=finalCourseID
              headers1={
                          "Accept": "application/json, text/plain, */*",
                          "Authorization": "Basic Nk1SRVBHTXYwdTRsUk9WTFhpTXdsN2RBeDJRc2hmd2JmRHBGbXZsRDptT1hhZnpITUpmY1JPRnNPa2cyOWJBOXAxUXp2cjBSVUV2WjJscHBRdnBYV3ZDcGx2ZVlLdUg4NGVRYzgzc1JMcnozZGpKUFo5MHNiNXhQNTNvdzJPajJhVXI4NmtqNGhBRlpvQ2YyOWJWTldKWkphSjlQNHZUVzFXaFVCb1FLZg==",
                          "Content-Type": "application/json;charset=utf-8"
                          }
              check_url1="https://www.udemy.com/api-2.0/courses/{}/".format(course_id)
              check_url_response1=requests.get(check_url1,headers=headers1)
              b1=check_url_response1.text
              y1 = json.loads(b1)
              try:
                # couponDoc=soup.find('table',{'class':'mt-8 w-full table-auto cursor-auto select-none'}).findAll('td')[-4].text
                a1=soup.findAll('script')
                str(a1).split('code')
                b=a1[15].text
                json_object = json.loads(b)
                couponDoc=json_object['props']['pageProps']['course']['coupon'][0]['code']
                findalUrlToSend='https://www.udemy.com'+ y1['url'] +'?couponCode=' + couponDoc
              except:
                findalUrlToSend='pass'
                print("here")
              if 'udemy.com' in findalUrlToSend:
                am3= findalUrlToSend.split('/?', 5)
                am4=findalUrlToSend.split('couponCode=')
                am1=am3[0]+"/?couponCode="+am4[1]
                with open("udemylink.txt",'r') as fp1:
                    Lines1 = fp1.read()
                    if am1 in Lines1:
                      print("pasing")
                      pass
                    else:
                        with open('udemylink.txt', 'a') as outle:
                            outle.write("\n"+ am1)
                        sendu(am1)
            #direct link
            elif 'couponCode='in newmsg and 'udemy.com' in newmsg:
              um2=newmsg
              um3= um2.split('/?', 5)
              um4=um2.split('couponCode=')
              um1=um3[0]+"/?couponCode="+um4[1]
              with open("udemylink.txt",'r') as fp1:
                  Lines1 = fp1.read()
                  if um1 in Lines1:
                      pass
                  else:
                      with open('udemylink.txt', 'a') as outle:
                          outle.write("\n"+ um1)
                      sendu(um1)
            with open('upid.txt', 'w') as outfile:
                outfile.write(str(newupdateid+1))
    print("sleeep time")
    time.sleep(15)
    print("sleeep up")
# am1="https://www.udemy.com/course/viralnomics-creating-youtube-video-ideas-that-go-viral/?awc=6554_1643724281_aefb5b5c1809841a6704b25380dcf08e&utm_source=Growth-Affiliate&utm_medium=Affiliate-Window&utm_campaign=Campaign-Name&utm_term=330563&utm_content=Placement&couponCode=E808F5F0A6EF94369A16"
# sendu(am1)