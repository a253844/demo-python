from pickle import FALSE, TRUE
import openpyxl 
import os 

hasNumber = lambda stringVal: any(elem.isdigit() for elem in stringVal)

def TranslateData(FillName, year , month):
    # 開啟資料
    Datawb = openpyxl.load_workbook(FillName + '.xlsx')
    # 開啟範本檔
    Samplewb = openpyxl.load_workbook('Sample.xlsx')

    #指定工作表
    DatasheetName = ""
    
    while(DatasheetName == ""):
        DatasheetName = input("要寶貝幫你處理哪一張資料表(Datasheet) : ")

        flag = 0
        for naem in Datawb.sheetnames:
            if naem == DatasheetName:
                flag += 1
                break
        if flag == 0 :
            print(DatasheetName + "資料表，寶貝找不到 (@~@)?，我要哭了喔，再输入一次" )
            DatasheetName = ""
    
    Datasheet = Datawb[DatasheetName]
    Samplesheet = Samplewb['工作表1']

    # 取出欄位
    DataTitleName = Datasheet['1']
    SampleTitleName = Samplesheet['1']
    UserName = any
    UserId = any
    UserIdType = any
    DateRange = any
    DateStart = ''
    DateEnd = ''

    # 找出須處理的資料列位置 
    for cell in DataTitleName:
        if(cell.value == '身分證'):
            UserId = Datasheet[cell.column_letter]
        if(cell.value == '身分別'):
            UserIdType = Datasheet[cell.column_letter]
        if(cell.value == '姓名日期'):
            UserName = Datasheet[cell.column_letter]
        if(cell.value!= None):
            if(type(cell.value) == int):
                if(DateStart == ''):
                    DateStart = cell.column_letter
                else:
                    DateEnd = cell.column_letter
                
    DateRange = Datasheet[DateStart + ":" + DateEnd]

    DataList = []

    for cell in UserId:
        if(cell.value!= None):
            if(hasNumber(cell.value)): 
                rownum = cell.row
                TypeName = UserIdType[rownum -1].value
                TempUserName = UserName[rownum -1].value
                UType = 0
                tempList = []
                if(TypeName.find("低收") != -1) :
                    UType = 1
                if(TypeName.find("一般戶") != -1):
                    UType = 2
                if(UType != 0):
                    for i in DateRange:
                        List = []
                        Data = Datasheet.cell(row = rownum  ,column = i[0].column)
                        if(Data.value == 1):
                            datenum = str(i[0].value) if len(str(i[0].value)) > 1 else  "0" + str(i[0].value)
                            List.append(cell.value)
                            List.append(year + month + datenum)
                            List.append(UType)
                            List.append(TempUserName)
                            tempList.append(List)
                DataList.append(tempList)

    count = 2
    for j in DataList:
        for k in j:
            #身分證字號
            Samplesheet.cell(row = count  ,column = 1, value = k[0])
            #服務日期
            Samplesheet.cell(row = count  ,column = 2, value = k[1])
            #服務類別
            Samplesheet.cell(row = count  ,column = 4, value = k[2])
            #服務類別
            Samplesheet.cell(row = count  ,column = 12, value = k[3])
            count += 1
            
    Samplewb.save("CompleteData.xlsx")
    return print("寶貝幫你把資料成功轉換好了，檔案已另存囉，記住檔案名稱叫 CompleteData.xlsx")
    return print("我是不是很棒，給我一百個抱抱!!!!  (~￣▽￣)~ ")

class AutoExcelDataBuilding:
    check = False
    FillName = ""

    if os.path.isfile("Sample.xlsx") == False:
        print("哭哭，寶貝找不到範本檔(Sample.xlsx) ，幫我檢查一下 ಥ⌣ಥ" )
    else:
        check = True
        while(FillName == ""):
            FillName = input("寶貝幫你處理檔案，輸入你的檔案名稱(限 .xlsx 檔) : ")

            if os.path.isfile(FillName + ".xlsx") == False:
                print(FillName + ".xlsx 檔案，寶貝找不到，哭哭拉，再输入一次 (@~@)?，!!!" )
                FillName = ""
                
    if(check):
        year = input("請輸入年分(民國年) : ")
        month = input("請輸入檔月份 : ")
        TranslateData(FillName, year, month)
        print("寶貝結束任務了，別太想我，掰! ＼(・ω・)/")
    
    os.system('pause') 
    TranslateData(FillName, year , month)
