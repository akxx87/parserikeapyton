def run_forever():
 try:
  import mysql.connector
  cnx = mysql.connector.connect(user='ikeaik', password='ikeaik',
                              host='51.75.53.71',
                              database='factory') 
  if __name__ == "__main__":
   from katclass import Test1, webdriver
   test1 = Test1() 
   PATH = "C:\katowiceR\chromedriver.exe"
   options = webdriver.ChromeOptions()
 #options.add_argument("no-sandbox")
 #options.add_argument("start-maximized")
 #options.page_load_strategy = ("none")
   options.add_argument("user-data-dir=C:/User Data/Profile2")
 #options.add_argument("disable-gpu")
   options.add_argument("headless")
   options.add_argument('blink-settings=imagesEnabled=false')
   options.add_argument("log-level=3")
   driver = webdriver.Chrome(PATH,options=options)
   mycursor = cnx.cursor()
   mycursor.execute("select * from `ikeamagazyn` where `urli` IS NOT NULL AND `up` = 0 AND `chk` = 1 ORDER BY id DESC")
   myresult = mycursor.fetchall() 
   for row in myresult:
    print(row[0])
    test1.setDriver(row[13], row[2], driver, row[1])

   sql = "UPDATE ikeamagazyn SET up = 0  WHERE chk = 1"
   mycursor.execute(sql)
   cnx.commit()    
 except:
  handle_exception(driver)

def handle_exception(driver):
    driver.quit();
    run_forever()
    pass
    
run_forever()
