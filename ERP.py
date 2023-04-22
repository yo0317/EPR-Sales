# ＿＿author＿＿：CHANG,YOU-HSUAN/yo
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
import matplotlib.pyplot as plt         # 匯入 matplotlib 的 pyplot 類別,並設定為 plt
# //注意這裡用的不是'SimHei'
import sys
import pymysql as MySQLdb                # pip install MySQLdb    # MySQL
import datetime as dt
from PIL import ImageTk, Image
import tkinter.messagebox as tkMessageBox
# 連接至資料庫
db = MySQLdb.connect(host="127.0.0.1",   #  連接到RDS
                     user="admin",       #  MySQL/PHPMyAdmin2 新增的 用戶
                     passwd="admin",
                     db="mydatabase")    #  MySQL/PHPMyAdmin2 新增的 資料庫
# -author/yo-定義saleDate和saleDateTree為字串
saleDate = ""
saleDateTree = ""
# 判斷系統
if sys.platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
    print("linux")  # linux
elif sys.platform == "darwin":  # MAC OS X
    from matplotlib.font_manager import FontProperties      # 中文字體
    plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
    plt.rcParams['axes.unicode_minus'] = False      # 解決座標軸負數的負號顯示問題
    font1 = ("Helvetica", 16)       # 字體
    bg1 = "#B0C4DE"                 # background
    bg2 = "#B0C4DE"                 # background
    anchor1 = "center"              # anchor
    # -author/yo-日曆格式修改
    def calender(calenderGet):
        # -author/yo-將XXXX/XX/XX改成符合MySQL的格式XXXX-XX-XX
        global saleDate
        global saleDateTree
        saleDate1 = calenderGet.split("/")
        if int(saleDate1[1]) < 10:
            month = "0" + str(saleDate1[1])
        else:
            month = str(saleDate1[1])
        if int(saleDate1[2]) < 10:
            day = "0" + str(saleDate1[2])
        else:
            day = str(saleDate1[2])
        saleDateTree = saleDate1[0] + "-" + month + "-" + day
        # -author/yo-確認日期後跑出單號
        # -author/yo-設置訂單編號-前8碼為日期
        saleDate = saleDate1[0] + month + day
        return saleDate, saleDateTree
elif sys.platform == "win32":
    # Windows (either 32-bit or 64-bit)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 換成中文的字體
    plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負數的負號顯示問題
    font1 = ("華文行楷", 12)         # 字體
    bg1 = "#B0C4DE"                 # background
    bg2 = "#ececec"                 # background
    anchor1 = "w"                   # anchor
    def calender(calenderGet):
        global saleDate
        global saleDateTree
        saleDate1 = calenderGet.split("/")
        if int(saleDate1[0]) < 10:
            month = "0" + str(saleDate1[0])
        else:
            month = str(saleDate1[0])
        if int(saleDate1[1]) < 10:
            day = "0" + str(saleDate1[1])
        else:
            day = str(saleDate1[1])
        saleDateTree = "20" + saleDate1[2] + "-" + month + "-" + day
        # -author/yo-確認日期後跑出單號
        # -author/yo-設置訂單編號-前8碼為日期
        saleDate = "20" + saleDate1[2] + month + day
        return saleDate, saleDateTree


# -author/yo-暫存訂單資料的物件
class order(object):
    def __init__(self, date, ID1, ID2, store, quantity, name, color, capacity, depot, person, text):
        self.saleDate = date
        self.saleID =ID1
        self.productID = ID2
        self.saleStore = store
        self.saleQuantity = quantity
        self.productName = name
        self.productColor = color
        self.productCapacity = capacity
        self.productDepot = depot
        self.salePerson = person
        # self.Ordercheck = check
        self.text = text
    # 放進treeview格式
    def info(self):
        return (
            self.saleDate,
            self.saleID,
            self.productID,
            self.saleStore,
            self.saleQuantity,
            self.productName,
            self.productColor,
            self.productCapacity,
            self.productDepot,
            self.salePerson,
            # self.Ordercheck,
            self.text
        )



# -author/yo-視窗設定
win = tk.Tk()
win.wm_title("訂單管理")                          # 視窗標題
win.resizable(width=False, height=False)      # 視窗設為不可拉動大小
win.minsize(width=940, height=510)             # 視窗最小範圍
win.maxsize(width=940, height=510)             # 視窗最大範圍
x = Image.open("B0C4DE.png")                   # 讀取背景圖片
img = ImageTk.PhotoImage(x)                     # 轉換成PhotoImage
labelBackground = tk.Label(win, image=img)      # 建立Label物件 顯示圖片
labelBackground.pack()                          # 置入圖片
# -author/yo-銷貨單號-----label-每按一次儲存就會跳出新的單號
labelNum = tk.Label(win, text="銷貨單號：", fg="black", bg=bg1, bd=0, font=font1)    # 標題：銷貨單號
labelNum.place(x=20, y=60)
labelNum1 = tk.Label(win, text="", bg=bg1, width=12)        # 銷貨單號放置位置
labelNum1.place(x=100, y=57)
# -author/yo-按下日期按鈕 呼叫新視窗選擇日期的function
# -author/yo-用來暫存修改前選取的單號
chooseNum = 0
# -author/yo-跳出新視窗
def createNewWindow():
    global newWindow
    newWindow = Toplevel(win)
    # -author/yo-於新視窗置入日曆工具
    cal = Calendar(newWindow, selectmode='day')
    cal.pack(pady=5)
    # -author/yo-newWindow視窗中的按鈕所連結的function
    def grad_date():
        global newWindow        # -author/yo-newWindow
        global Num              # -author/yo-暫存訂單編號
        # -author/yo-放置修改後日期於視窗（呼叫calender並帶入選取之日期，取得回傳第二項放入labelDateRes）
        labelDateRes['text'] = calender(cal.get_date())[1]
        # -author/yo-設置訂單編號-後4碼流水號
        temp = 0
        # -author/yo-以選取的日期至SQL搜尋該日之銷貨單號
        sqlNum = "SELECT `銷貨單號` FROM `ERP` WHERE `銷貨日期`='" + str(calender(cal.get_date())[1]) + "';"
        cursor.execute(sqlNum)  # 執行新增資料
        db.commit()
        listNumFromSQL = cursor.fetchall()
        if listNumFromSQL == ():
            Num = labelNum1['text'] = str(calender(cal.get_date())[0]) + "0001"
        else:
            for i in listNumFromSQL:
                if int(i[0]) > temp:
                    temp = int(i[0])
            Num = labelNum1['text'] = str(temp + 1)
        newWindow.destroy()
    # -author/yo-於新視窗日曆下方置入按鈕，按下date choose按鈕進入grad_date函式
    Button(newWindow, text="date choose",
           command=grad_date).pack(pady=5)











# -author/yo-當更改品名、數量、規格時，會自動帶入計算，並更新價格在畫面上
def price(event):
    # price
    try:
        if comboboxValueProduct.get() == 'iPhone 13 Pro':
            price = 32900
        elif comboboxValueProduct.get() == 'iPhone 13 Pro Max':
            price = 36900
        if comboboxValueCapacity.get() == '128GB':
            price = (price + 0) * int(entryQuantityString.get())
        elif comboboxValueCapacity.get() == '256GB':
            price = (price + 3500) * int(entryQuantityString.get())
        elif comboboxValueCapacity.get() == '512GB':
            price = (price + 7000) * int(entryQuantityString.get())
        elif comboboxValueCapacity.get() == '1TB':
            price = (price + 7000) * int(entryQuantityString.get())
        label2Price['text'] = price
    except:
        tk.messagebox.showinfo("警告", "請輸入阿拉伯數字！！！")

# -author/yo-銷貨日期-----日曆小工具連結至函式createNewWindow
labelDate = tk.Label(win, text="銷貨日期：", fg="black", bg=bg1, bd=0, font=font1)
labelDate.place(x=20, y=20)
dateCheckButton = Button(win, text="🗓️", command=createNewWindow, bg=bg2, bd=0, fg="black", font=font1,width=2,anchor=anchor1)
dateCheckButton.place(x=240, y=15)
labelDateRes = Label(win, text=dt.datetime.today().strftime("%Y-%m-%d"), bg=bg1, fg="black", bd=0, font=font1)
labelDateRes.place(x=120, y=20)
# -author/yo-銷售金額-----label
labelPrice = tk.Label(win, text="銷售金額：", fg="black", bg=bg1, bd=0, font=font1)
labelPrice.place(x=280, y=60)
label2Price = tk.Label(win, text=32900, width=12, anchor='e', bg=bg1)
label2Price.place(x=360, y=57)
# -author/yo-出售門市------下拉式選單
labelProductionUnit = tk.Label(win, text="出售門市：", fg="black", bg=bg1, bd=0, font=font1)
labelProductionUnit.place(x=20, y=100)
comboboxValueUnit = tk.StringVar()
comboboxValueUnit.set('台北總店')
productionUnit = ttk.Combobox(win, width=10, textvariable=comboboxValueUnit)
productionUnit['values'] = ('台北總店', '台北二店', '網路銷售')
productionUnit.place(x=100, y=97)                                  # 放置位置
# -author/yo-出售數量------entry
labelQuantity = tk.Label(win, text="出售數量：", fg="black", bg=bg1, bd=0, font=font1)
labelQuantity.place(x=280, y=100)
entryQuantityString = tk.StringVar()
entryQuantityString.set(1)
entryQuantity = tk.Entry(win, textvariable=entryQuantityString, width=12, justify=RIGHT)
entryQuantity.place(x=360, y=97)
# -author/yo-當更改數量時，會連結至price函式自動帶入計算，並更新價格在畫面上
entryQuantity.bind("<KeyRelease>", price)
# -author/yo-品名-----下拉式選單
labelProduct = tk.Label(win, text="品名：", fg="black", bg=bg1, bd=0, font=font1)
labelProduct.place(x=20, y=140)
comboboxValueProduct = tk.StringVar()
comboboxValueProduct.set('iPhone 13 Pro')
product = ttk.Combobox(win, width=39, textvariable=comboboxValueProduct)
product['values'] = ('iPhone 13 Pro', 'iPhone 13 Pro Max')
product.place(x=100, y=137)                                  # 放置位置
# -author/yo-當更改品名時，會連結至price函式自動帶入計算，並更新價格在畫面上
product.bind('<<ComboboxSelected>>', price)
# -author/yo-顏色------下拉式選單
labelColor = tk.Label(win, text="產品顏色：", fg="black", bg=bg1, bd=0, font=font1)
labelColor.place(x=20, y=180)
comboboxValueColor = tk.StringVar()
comboboxValueColor.set('天峰藍色')
color = ttk.Combobox(win, width=10, textvariable=comboboxValueColor)
color['values'] = ('天峰藍色', '石墨色', '金色', '銀色', '松嶺青色')
color.place(x=100, y=177)                                  # 放置位置
# -author/yo-容量------下拉式選單
labelCapacity = tk.Label(win, text="產品容量：", fg="black", bg=bg1, bd=0, font=font1)
labelCapacity.place(x=280, y=180)
comboboxValueCapacity = tk.StringVar()
comboboxValueCapacity.set('128GB')
capacity = ttk.Combobox(win, width=10, textvariable=comboboxValueCapacity)
capacity['values'] = ('128GB', '256GB', '512GB', '1TB')
capacity.place(x=360, y=177)                                  # 放置位置
# -author/yo-當更改規格時，會連結至price函式自動帶入計算，並更新價格在畫面上
capacity.bind('<<ComboboxSelected>>', price)
# -author/yo-倉儲位置-----多選一的元件 Radiobutton
labelDepot = tk.Label(win, text="倉儲位置：", fg="black", bg=bg1, bd=0, font=font1)
labelDepot.place(x=20, y=220)
radioDepot = tk.IntVar()                               # 元件的變數 int
radioDepot.set(1)
rdioDepot1 = tk.Radiobutton(win, text='台北總店倉庫', variable=radioDepot, value=1, bg=bg1)
rdioDepot2 = tk.Radiobutton(win, text='台北二店倉庫', variable=radioDepot, value=2, bg=bg1)
rdioDepot3 = tk.Radiobutton(win, text='境外倉儲轉入', variable=radioDepot, value=3, bg=bg1)
rdioDepot1.place(x=100, y=220)
rdioDepot2.place(x=220, y=220)
rdioDepot3.place(x=340, y=220)
# -author/yo-銷售人員-----下拉式選單
labelSalePerson = tk.Label(win, text="銷售人員：", fg="black", bg=bg1, bd=0, font=font1)
labelSalePerson.place(x=20, y=260)
comboboxValueSalePerson = tk.StringVar()
comboboxValueSalePerson.set('王小美')
salePerson = ttk.Combobox(win, width=10, textvariable=comboboxValueSalePerson)
salePerson['values'] = ('王小美', '陳阿明', '林店長', '吳店長')
salePerson.place(x=100, y=257)

# -author/yo-核對結果-----Checkbutton
# labelCheck = tk.Label(win, text="核對結果：", fg="black", bg=bg1, bd=0, font=font1)
# labelCheck.place(x=280, y=260)
# chkValue = tk.BooleanVar()                                         # 變數值
# chkValue.set(True)                                                   # 內定值
# chkExample1 = tk.Checkbutton(win, text='確認無誤', var=chkValue, bg=bg1)         # 打勾
# chkExample1.place(x=360, y=260)
# chkValue2 = tk.BooleanVar()
# chkValue2.set(False)
# chkExample2 = tk.Checkbutton(win, text='帳目有誤', var=chkValue2, bg=bg1)
# chkExample2.place(x=440, y=260)
# -author/yo-備註-text
def delelt(event):
    text.delete('1.0', "end")
labelText = tk.Label(win, text="備註", fg="black", bg=bg1, bd=0, font=font1, anchor="center", width=35)
labelText.place(x=550, y=160)
text = tk.StringVar()
text.set("")
text = tk.Text(win, height=6, width=45)
text.place(x=550, y=180)
text.bind("<<TextModified>>", delelt)

# -author/yo-製作tree
columns = ('銷貨日期', '銷貨單號', '銷售金額', '出售門市', '出售數量', '品名', '產品顏色', '產品容量', '倉儲位置', '銷售人員', '備註')   # 欄位名稱
saleTree = ttk.Treeview(win, columns=columns, show='headings')          # 設定Treeview欄位名稱
saleTree.column('銷貨日期', width=90, anchor=tk.W)
saleTree.column('銷貨單號', width=105, anchor=tk.E)
saleTree.column('銷售金額', width=80, anchor=tk.E)
saleTree.column('出售門市', width=80, anchor=tk.E)
saleTree.column('出售數量', width=60, anchor=tk.E)
saleTree.column('品名', width=120, anchor=tk.E)
saleTree.column('產品顏色', width=80, anchor=tk.E)
saleTree.column('產品容量', width=80, anchor=tk.E)
saleTree.column('倉儲位置', width=100, anchor=tk.E)
saleTree.column('銷售人員', width=80, anchor=tk.E)
# saleTree.column('核對結果', width=60, anchor=tk.E)
saleTree.place(x=0, y=300)


saleTree.heading('銷貨日期', text='銷貨日期')           # 欄位文字設定
saleTree.heading('銷貨單號', text='銷貨單號')           # 欄位文字設定
saleTree.heading('銷售金額', text='銷售金額')           # 欄位文字設定
saleTree.heading('出售門市', text='出售門市')           # 欄位文字設定
saleTree.heading('出售數量', text='出售數量')           # 欄位文字設定
saleTree.heading('品名', text='品名')                  # 欄位文字設定
saleTree.heading('產品顏色', text='產品顏色')           # 欄位文字設定
saleTree.heading('產品容量', text='產品容量')           # 欄位文字設定
saleTree.heading('倉儲位置', text='倉儲位置')           # 欄位文字設定
saleTree.heading('銷售人員', text='銷售人員')           # 欄位文字設定
# saleTree.heading('核對結果', text='核對結果')           # 欄位文字設定





dateRes = ""
data1 = ()
orderName = []


# -author/yo-匯入SQL原始資料-按照單號放入tree-僅匯入本日往前推一週的資料
cursor = db.cursor()
sql = "SELECT `銷貨日期`,`銷貨單號`,`銷售金額`,`出售門市`,`出售數量`,`品名`,`產品顏色`,`產品容量`,`倉儲位置`,`銷售人員`," \
      "`備註` FROM `ERP` WHERE `銷貨日期`>'"+str(dt.date.today() + dt.timedelta(days=-7))+\
      "' AND `銷貨日期`<'"+str(dt.date.today() + dt.timedelta(days=+7))+"'ORDER BY `銷貨單號`;"
cursor.execute(sql)          # 執行新增資料
db.commit()                  # 送出
listDataFromSQL = cursor.fetchall()     # 將資料轉換成陣列
for row in listDataFromSQL:
    data2 = order(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
    saleTree.insert('', tk.END, values=data2.info())
    orderName.append(data2)


# -author/yo-初始單號-
temp = 0
sqlNum = "SELECT `銷貨單號` FROM `ERP` WHERE `銷貨日期`='" + str(dt.datetime.today().strftime("%Y-%m-%d")) + "';"
sqlNum1 = "SELECT `銷貨單號` FROM `ERP` WHERE `銷貨日期`='2022-08-11'"
cursor.execute(sqlNum)          # 執行新增資料
db.commit()
listNumFromSQL = cursor.fetchall()
if listNumFromSQL == ():
    Num = labelNum1['text'] = str(dt.datetime.today().strftime("%Y%m%d")) + "0001"
else:
    for i in listNumFromSQL:
        if int(i[0]) > temp:
            temp = int(i[0])
    Num = labelNum1['text'] = str(temp + 1)


# -author/yo-新增
def addButtonFunc():
    global data1
    global saleDate
    global saleDateTree
    global Num
    # -author/yo-將radioButton取得的值先轉換為文字再放入tree、My SQL
    if radioDepot.get() == 1:
        depot = "台北總店倉庫"
    elif radioDepot.get() == 2:
        depot = "台北二店倉庫"
    elif radioDepot.get() == 3:
        depot = "境外倉儲轉入"
    # -author/yo-加入SQL
    loc_dt = dt.datetime.today()
    time_del = dt.timedelta()
    new_dt = loc_dt + time_del
    time1 = new_dt.strftime("%Y-%m-%d %H:%M:%S")
    sqlCheck = "INSERT INTO `ERP`(`id`, `更新日期`, `銷貨日期`, `銷貨單號`, `銷售金額`, `出售門市`, `出售數量`, `品名`," \
               "`產品顏色`, `產品容量`, `倉儲位置`, `銷售人員`, `備註`) VALUES (null, '" + str(time1) + "',"\
               " '" + str(labelDateRes['text']) + "', '" + str(labelNum1['text']) + "','" + str(label2Price['text']) + "', " \
               " '" + str(comboboxValueUnit.get()) + "', '" + str(entryQuantityString.get()) + "'," \
               " '" + str(comboboxValueProduct.get()) + "', '" + str(comboboxValueColor.get()) + "', '" + str(comboboxValueCapacity.get()) + "', " \
               " '" + str(depot) + "','" + str(comboboxValueSalePerson.get()) + "', '"+str(text.get('1.0', 'end'))+"');"
    cursor.execute(sqlCheck)        # 執行新增資料
    db.commit()
    # 先把tree刪掉再從資料庫匯入
    saleTree.delete(*saleTree.get_children())
    # cursor = db.cursor()
    sql = "SELECT `銷貨日期`,`銷貨單號`,`銷售金額`,`出售門市`,`出售數量`,`品名`,`產品顏色`,`產品容量`,`倉儲位置`,`銷售人員`," \
          "`備註` FROM `ERP` WHERE `銷貨日期`>'" + str(dt.date.today() + dt.timedelta(days=-7)) + \
          "' AND `銷貨日期`<'" + str(dt.date.today() + dt.timedelta(days=+7)) + "'ORDER BY `銷貨單號`;"
    cursor.execute(sql)  # 執行新增資料
    db.commit()  # 送出
    listDataFromSQL = cursor.fetchall()  # 將資料轉換成陣列
    for row in listDataFromSQL:
        data2 = order(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        saleTree.insert('', tk.END, values=data2.info())
        orderName.append(data2)
    # -author/yo-單號
    # -author/yo-設置訂單編號-前8碼為日期
    saleDate = labelDateRes['text'].split("-")[0] + labelDateRes['text'].split("-")[1] + labelDateRes['text'].split("-")[2]
    # -author/yo-設置訂單編號-後4碼流水號
    temp = 0
    sqlNum = "SELECT `銷貨單號` FROM `ERP` WHERE `銷貨日期`='" + str(labelDateRes['text']) + "';"
    cursor.execute(sqlNum)  # 執行新增資料
    db.commit()
    listNumFromSQL = cursor.fetchall()
    if listNumFromSQL == ():
        Num = labelNum1['text'] = str(saleDate) + "0001"
    else:
        for i in listNumFromSQL:
            if int(i[0]) > temp:
                temp = int(i[0])
        Num = labelNum1['text'] = str(temp + 1)

# -author/yo-刪除
def delSelected():
    global chooseNum
    for selected_item in saleTree.selection():
        saleTree.delete(selected_item)
        # -author/yo-至SQL搜尋欲更改之單號的id
        sqlNumber = "SELECT `id` FROM `ERP` WHERE `銷貨單號`='" + str(chooseNum) + "';"
        cursor.execute(sqlNumber)  # 執行新增資料
        db.commit()
        listNum = cursor.fetchall()  # 將資料轉換成陣列
        sqlDel = "DELETE FROM `ERP` WHERE `id`='" + str(listNum[0][0]) + "';"
        cursor.execute(sqlDel)  # 執行新增資料
        db.commit()
    # 先把tree刪掉再從資料庫匯入
    saleTree.delete(*saleTree.get_children())
    # cursor = db.cursor()
    sql = "SELECT `銷貨日期`,`銷貨單號`,`銷售金額`,`出售門市`,`出售數量`,`品名`,`產品顏色`,`產品容量`,`倉儲位置`,`銷售人員`," \
          "`備註` FROM `ERP` WHERE `銷貨日期`>'" + str(dt.date.today() + dt.timedelta(days=-7)) + \
          "' AND `銷貨日期`<'" + str(dt.date.today() + dt.timedelta(days=+7)) + "'ORDER BY `銷貨單號`;"
    cursor.execute(sql)  # 執行新增資料
    db.commit()  # 送出
    listDataFromSQL = cursor.fetchall()  # 將資料轉換成陣列
    for row in listDataFromSQL:
        data2 = order(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        saleTree.insert('', tk.END, values=data2.info())
        orderName.append(data2)


# -author/yo-修改
def modifySelected():
    global saleDate
    global saleDateTree
    global Num
    global chooseNum
    for selected_item in saleTree.selection():
        if radioDepot.get() == 1:
            depot = "台北總店倉庫"
        elif radioDepot.get() == 2:
            depot = "台北二店倉庫"
        elif radioDepot.get() == 3:
            depot = "境外倉儲轉入"
        saleTree.item(selected_item, text="", values=(labelDateRes['text'], labelNum1['text'], label2Price['text'],
                                                      comboboxValueUnit.get(), entryQuantityString.get(),
                                                      comboboxValueProduct.get(), comboboxValueColor.get(),
                                                      comboboxValueCapacity.get(), depot,
                                                      comboboxValueSalePerson.get(), text.get('1.0', 'end')))
        loc_dt = dt.datetime.today()
        time_del = dt.timedelta()
        new_dt = loc_dt + time_del
        time1 = new_dt.strftime("%Y-%m-%d %H:%M:%S")
        # -author/yo-用暫存的chooseNum至SQL搜尋欲更改之單號的id
        sqlNumber = "SELECT `id` FROM `ERP` WHERE `銷貨單號`='" + str(chooseNum) + "';"
        cursor.execute(sqlNumber)  # 執行新增資料
        db.commit()
        listNum = cursor.fetchall()     # 將資料轉換成陣列
        # -author/yo-至SQL以id搜尋該筆資料並更新
        sqlModi = "UPDATE `ERP` SET `更新日期`='" + str(time1) + "',`銷貨日期`='" + str(labelDateRes['text']) + "'," + \
                  "`銷貨單號`='" + str(labelNum1['text']) + "',`銷售金額`='" + str(label2Price['text']) + "'," + \
                  "`出售門市`='" + str(comboboxValueUnit.get()) + "',`出售數量`='" + str(entryQuantityString.get()) + "'," + \
                  "`品名`='" + str(comboboxValueProduct.get()) + "',`產品顏色`='" + str(comboboxValueColor.get()) + "'," + \
                  "`產品容量`='" + str(comboboxValueCapacity.get()) + "',`倉儲位置`='" + str(depot) + "'," + \
                  "`銷售人員`='" + str(comboboxValueSalePerson.get()) + "',`備註`='" + str(text.get('1.0', 'end')) + "'" + \
                  " WHERE `id`='" + str(listNum[0][0]) + "';"
        cursor.execute(sqlModi)         # 執行新增資料
        db.commit()
    # 先把tree刪掉再從資料庫匯入
    saleTree.delete(*saleTree.get_children())
    # cursor = db.cursor()
    sql = "SELECT `銷貨日期`,`銷貨單號`,`銷售金額`,`出售門市`,`出售數量`,`品名`,`產品顏色`,`產品容量`,`倉儲位置`,`銷售人員`," \
          "`備註` FROM `ERP` WHERE `銷貨日期`>'" + str(dt.date.today() + dt.timedelta(days=-7)) + \
          "' AND `銷貨日期`<'" + str(dt.date.today() + dt.timedelta(days=+7)) + "'ORDER BY `銷貨單號`;"
    cursor.execute(sql)  # 執行新增資料
    db.commit()  # 送出
    listDataFromSQL = cursor.fetchall()  # 將資料轉換成陣列
    for row in listDataFromSQL:
        data2 = order(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        saleTree.insert('', tk.END, values=data2.info())
        orderName.append(data2)

# -author/yo-放置新增按鈕
addButton = tk.Button(win, text="新增", command=addButtonFunc, fg="black", bg=bg2, bd=0, font=font1)
addButton.place(x=550, y=20)
# -author/yo-放置刪除按鈕
delButton = tk.Button(win, text="刪除", command=delSelected, fg="black", bg=bg2, bd=0, font=font1)
delButton.place(x=550, y=60)
# -author/yo-放置修改按鈕
changeButton = tk.Button(win, text="修改", command=modifySelected, fg="black", bg=bg2, bd=0, font=font1)
changeButton.place(x=550, y=100)

# -author/yo-查詢
def GoodSelected(event):
    global saleTree
    global data1
    global chooseNum
    for sale_item in saleTree.selection():   # 被選的項目
        item = saleTree.item(sale_item)      # 被選的項目資料 Dict
        record = item['values']
        # -author/yo-用chooseNum暫存選取的單號
        chooseNum = record[1]
        labelDateRes["text"] = record[0]
        labelNum1['text'] = record[1]
        label2Price['text'] = record[2]
        comboboxValueUnit.set(record[3])
        entryQuantityString.set(record[4])
        comboboxValueProduct.set(record[5])
        comboboxValueColor.set(record[6])
        comboboxValueCapacity.set(record[7])
        if record[8] == "台北總店倉庫":
            radioDepot.set(1)
        elif record[8] == "台北二店倉庫":
            radioDepot.set(2)
        elif record[8] == "境外倉儲轉入":
            radioDepot.set(3)
        comboboxValueSalePerson.set(record[9])
        # if record[10] == "True":
        #     chkValue.set(1)
        #     chkValue2.set(0)
        # elif record[10] == "False":
        #     chkValue.set(0)
        #     chkValue2.set(1)
        # else:
        #     chkValue.set(0)
        #     chkValue2.set(0)
        text.delete('1.0', "end")
        text.insert('1.0', record[10])




# -author/yo-按下查看本週銷售額表時進入open_ImageFile_file
def open_ImageFile_file():
    taipeiOne = []
    taipeiTwo = []
    web = []
    storeTotal = []
    # -author/yo-取得今天+往前推一週的日期'台北總店', '台北二店', '網路銷售'
    week = []
    for day in range(0, 7):
        week.append(dt.date.today() + dt.timedelta(days=-day))
    # -author/yo-取得今天+往前推一週的日期的銷售量
    for day in week:
        # -author/yo-至資料庫搜尋 將台北總店的日銷售量加入串列中
        cursor = db.cursor()
        sqlImage = "SELECT `銷售金額` FROM `ERP` WHERE (`出售門市`='台北總店') AND `銷貨日期`='"+str(day)+"';"
        cursor.execute(sqlImage)  # 執行新增資料
        db.commit()  # 送出
        listTotal = cursor.fetchall()  # 將資料轉換成陣列
        taipeiOneTotal = 0
        for i in listTotal:
            taipeiOneTotal = taipeiOneTotal + int(i[0])
        taipeiOne.append(taipeiOneTotal)
        # -author/yo-至資料庫搜尋 將台北二店的日銷售量加入串列中
        cursor = db.cursor()
        sqlImage = "SELECT `銷售金額` FROM `ERP` WHERE (`出售門市`='台北二店') AND `銷貨日期`='" + str(day) + "';"
        cursor.execute(sqlImage)  # 執行新增資料
        db.commit()  # 送出
        listTotal = cursor.fetchall()  # 將資料轉換成陣列
        taipeiTwoTotal = 0
        for i in listTotal:
            taipeiTwoTotal = taipeiTwoTotal + int(i[0])
        taipeiTwo.append(taipeiTwoTotal)
        # -author/yo-至資料庫搜尋 將網路銷售的日銷售量加入串列中
        cursor = db.cursor()
        sqlImage = "SELECT `銷售金額` FROM `ERP` WHERE (`出售門市`='網路銷售') AND `銷貨日期`='" + str(day) + "';"
        cursor.execute(sqlImage)  # 執行新增資料
        db.commit()  # 送出
        listTotal = cursor.fetchall()  # 將資料轉換成陣列
        webTotal = 0
        for i in listTotal:
            webTotal = webTotal + int(i[0])
        web.append(webTotal)
        # -author/yo-至資料庫搜尋 將總日銷售量加入串列中
        cursor = db.cursor()
        sqlImage = "SELECT `銷售金額` FROM `ERP` WHERE `銷貨日期`='" + str(day) + "';"
        cursor.execute(sqlImage)  # 執行新增資料
        db.commit()  # 送出
        listTotal = cursor.fetchall()  # 將資料轉換成陣列
        total = 0
        for i in listTotal:
            total = total + int(i[0])
        storeTotal.append(total)

    plt.plot(week, taipeiOne, 'b^-', label='台北總店')      # 繪製藍色直槓
    plt.plot(week, taipeiTwo, 'c*-', label='台北二店')      # 繪製青色直槓
    plt.plot(week, web, 'gd-', label='網路銷售')            # 繪製粉色直槓
    plt.plot(week, storeTotal, 'ro-', label='日總銷售額')            # 繪製粉色直槓
    plt.xlabel("日期")
    plt.ylabel("銷售額")
    plt.legend(loc='upper left')  # 在左下角顯示標籤
    plt.title('本週銷售額')
    plt.show()                  # 顯示



# -author/yo-放置查看每週銷售量報表按鈕
imageButton = tk.Button(win, text="查看本週銷售額報表", command=lambda: open_ImageFile_file(), fg="black", bg=bg2, bd=0, font=font1).place(x=700, y=100)
# -author/yo-選取tree中的資料時會連結到GoodSelected
saleTree.bind('<<TreeviewSelect>>', GoodSelected)             # 綁定事件 選取時
win.mainloop()