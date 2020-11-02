import tagui as t
import datetime
import pandas as pd
import os
import s3_function
#超参数
try:
    str_to_append = str(datetime.datetime.today().date())
    # 初始化页面
    t.init()
    # 输入url进入
    t.url("http://bank.jrj.com.cn/bankpro/data.shtml?type=1")
    # 等15秒反应
    t.wait(15)
    # 鼠标放上去，点击精简选项
    t.hover(element_identifier='//*[@id="fxr"]')
    t.click(element_identifier='//*[@id="zksq"]')
    # 鼠标移动到发行日期上，点击文本栏，输入发行日日期为今日，点击搜索
    t.hover(element_identifier='//*[@id="fxr"]')
    t.click(element_identifier='//*[@id="fxr"]')
    t.type(element_identifier='//*[@id="fxr"]', text_to_type=str_to_append)
    # 再点击，确保日期不会遮住底下的搜索按钮
    t.click(element_identifier='//*[@id="fxr"]')
    t.hover(element_identifier='//*[@class="ipf01"]')
    t.click(element_identifier='//*[@class="ipf01"]')
    # 把展示的尺寸设置为50个产品每页：
    t.hover(element_identifier='//*[@data-pagesize="50"]')
    t.click(element_identifier='//*[@data-pagesize="50"]')

    # 当下一页没有被disable的时候,有以下超参数
    page_curr = 1  # 当前页面index
    value_dict = {}  # 存放data
    count = 1  # csv 命名用
    # 存放列名
    name_list = ['序号', '综合评级', 'url']

    for col_name in name_list:
        value_dict.setdefault(col_name, [])  # 初始化空数据集

    # 当可以翻页，或数据只有一页的时候，进行循环
    while (t.read(element_identifier='//div[@id = "pagefoot"]//a[@class = "cur pf-disabled"]') == str(page_curr)) or (
            page_curr == 1):

        # 每页的数据量大小（row number）
        count_values = int(t.count(element_identifier='//tbody[@id = "content"]//tr')) + 1  # python从0开始
        # 爬取页面所有一个table里的值
        if str(t.read(
                element_identifier='//tbody[@id = "content"]//tr[' + str(
                    count_values - 1) + ']//td[@class = "px"]')) > str_to_append:
            # print("direct continue..")
            # 翻页
            page_curr += 1
            # 鼠标模拟移动，并点击翻页
            t.hover(element_identifier='//*[@href="' + str(page_curr) + '"]')
            t.click(element_identifier='//*[@href="' + str(page_curr) + '"]')
            continue
        filename = str(count) + "daily_data.csv"
        count += 1
        t.wait(1)  # 等1秒，万一加载错误了
        t.table(element_identifier='//div[@class = "table-s1 tab-s2 w100"]//table', filename_to_save=filename)
        count_values = int(t.count(element_identifier='//tbody[@id = "content"]//tr')) + 1  # python从0开始
        for i in range(1, count_values):
            # 判定条件：如果是今天刚发行的，拿到所有主页面上的数据；
            # 如果最下面那条数据都大于今天，就直接翻页
            if str(t.read(
                    element_identifier='//tbody[@id = "content"]//tr[' + str(
                        count_values - 1) + ']//td[@class = "px"]')) > str_to_append:
                # print("direct break..")
                break
            else:
                if str(t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(
                        i) + ']//td[@class = "px"]')) == str_to_append:
                    # 序号
                    value_dict[name_list[0]].append(
                        t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[2]'))
                    # 综合评级
                    value_dict[name_list[1]].append(
                        t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//td[12]//i/@title'))
                    # url
                    value_dict[name_list[2]].append(
                        t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//a/@href'))
                else:  # 如果不是今天增量，什么都不做
                    pass
            # print("turn the page..")
            # 翻页
        page_curr += 1
        # 鼠标模拟移动，并点击翻页
        t.hover(element_identifier='//*[@href="' + str(page_curr) + '"]')
        t.click(element_identifier='//*[@href="' + str(page_curr) + '"]')

        # 关闭tagui流
    today_data = pd.DataFrame(value_dict)
    t.close()


    # 输出格式为："今日日期.csv"
    url_list = today_data.loc[:,'url'] #里面都是url

    #进入url详情页

    t.init()
    productName = []
    totalRank = []
    returnRank = []
    secureRank = []
    liquidityRank = []
    bankName = []
    issueTarget  = []
    currencyType  = []
    investmentType  = []
    issueDate = []
    discontinuedDate = []
    delegateManagementPeriod = []
    minAmountOfProduct = []
    unitOfAmountIncreasement = []
    flagOfPledgeLoans = []
    flagOfIterminationInAdvance = []
    flagOfRedemption = []
    saleRegion = []
    returnType = []
    predictMaxReturnRate = []
    realMaxReturnRate = []
    comparisonWithDeposit = []
    startDateOfReturn = []
    endDateOfReturn = []
    returnDesc = []
    purchaseCondition = []
    iterminationCondition = []
    redemptionCondition = []
    investmentRisk = []
    for url_now in url_list:
        t.url(url_now)
        t.wait(3) #等待加载
        productName.append(t.read(element_identifier='//div[@class = "jrj-where"]//span'))

        totalRank.append(t.read(element_identifier='//div[@class = "col-01"]//div[@class = "table-s2"]//tr['+str(2)+']//td['+str(2)+']//i/@title'))

        returnRank.append(t.read(element_identifier='//div[@class = "col-01"]//div[@class = "table-s2"]//tr['+str(3)+']//td['+str(2)+']//i/@title'))

        secureRank.append(t.read(element_identifier='//div[@class = "col-01"]//div[@class = "table-s2"]//tr['+str(3)+']//td['+str(4)+']//i/@title'))

        liquidityRank.append(t.read(element_identifier='//div[@class = "col-01"]//div[@class = "table-s2"]//tr['+str(3)+']//td['+str(6)+']//i/@title'))

        bankName.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//td[2]')) #发行银行

        issueTarget.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//td[4]')) #发行对象

        currencyType.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//td[6]')) #货币

        investmentType.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[2]//td[2]')) #投资类型

        issueDate.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[2]//td[4]')) #发行日期

        discontinuedDate.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[2]//td[6]')) #终止日期

        delegateManagementPeriod.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[3]//td[2]')) #委托管理期限

        minAmountOfProduct.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[3]//td[4]')) #委托起始金额

        unitOfAmountIncreasement.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[3]//td[6]')) #起购金额递增单位

        flagOfPledgeLoans.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[4]//td[2]')) #可否质押贷款

        flagOfIterminationInAdvance.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[4]//td[4]')) #银行可否提前终止

        flagOfRedemption.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[4]//td[6]')) #客户是否可赎回

        saleRegion.append(t.read(element_identifier='//div[@class = "md02 mt"][2]//div[@class = "table-s2"]//tr[5]//td[2]')) #销售地区

        returnType.append(t.read(element_identifier='//div[@class = "md02 mt"][3]//div[@class = "table-s2"]//td[2]')) #收益类型

        predictMaxReturnRate.append(t.read(element_identifier='//div[@class = "md02 mt"][3]//div[@class = "table-s2"]//td[4]')) #预期最高收益率

        realMaxReturnRate.append(t.read(element_identifier='//div[@class = "md02 mt"][3]//div[@class = "table-s2"]//td[6]')) #到期最高收益率

        comparisonWithDeposit.append(t.read(element_identifier='//div[@class = "md02 mt"][3]//div[@class = "table-s2"]//tr[2]//td[2]')) #与同期储蓄比

        startDateOfReturn.append(t.read(element_identifier='//div[@class = "md02 mt"][3]//div[@class = "table-s2"]//tr[2]//td[4]')) #收益起始日期

        endDateOfReturn.append(t.read(element_identifier='//div[@class = "md02 mt"][3]//div[@class = "table-s2"]//tr[2]//td[6]')) #收益终止日期

        returnDesc.append(t.read(element_identifier='//div[@class = "md02 mt"][6]//div[@class = "table-s2"]//td[2]')) #收益率说明

        purchaseCondition.append(t.read(element_identifier='//div[@class = "md02 mt"][6]//div[@class = "table-s2"]//tr[2]//td[2]')) #申购条件说明

        iterminationCondition.append(t.read(element_identifier='//div[@class = "md02 mt"][6]//div[@class = "table-s2"]//tr[3]//td[2]')) #银行提前终止条件

        redemptionCondition.append(t.read(element_identifier='//div[@class = "md02 mt"][6]//div[@class = "table-s2"]//tr[4]//td[2]')) #赎回规定说明

        investmentRisk.append(t.read(element_identifier='//div[@class = "md02 mt"][6]//div[@class = "table-s2"]//tr[5]//td[2]')) #投资风险说明


    df = pd.DataFrame({
    'bankName':bankName,
    'productName':productName,
    'totalRank':totalRank,
    'returnRank':returnRank,
    'secureRank':secureRank,
    'liquidityRank':liquidityRank,
    'issueTarget':issueTarget,
    'currencyType':currencyType,
    'investmentType':investmentType,
    'issueDate':issueDate,
    'discontinuedDate':discontinuedDate,
    'delegateManagementPeriod':delegateManagementPeriod,
    'minAmountOfProduct':minAmountOfProduct,
    'unitOfAmountIncreasement':unitOfAmountIncreasement,
    'flagOfPledgeLoans':flagOfPledgeLoans,
    'flagOfIterminationInAdvance':flagOfIterminationInAdvance,
    'flagOfRedemption':flagOfRedemption,
    'saleRegion':saleRegion,
    'returnType':returnType,
    'predictMaxReturnRate':predictMaxReturnRate,
    'realMaxReturnRate':realMaxReturnRate,
    'comparisonWithDeposit':comparisonWithDeposit,
    'startDateOfReturn':startDateOfReturn,
    'endDateOfReturn':endDateOfReturn,
    'returnDesc':returnDesc,
    'purchaseCondition':purchaseCondition,
    'iterminationCondition':iterminationCondition,
    'redemptionCondition':redemptionCondition,
    'investmentRisk':investmentRisk
    })
    df.to_csv(str_to_append+"product_detail.csv",encoding='utf-8',index = False)
    t.close()
except:
    str_to_append = str(datetime.datetime.today().date())
    with open("FAIL_"+str_to_append+"product_detail.txt",'w',encoding='utf-8') as f:
        f.write("今日理财详情页拉取失败")
    s3_function.upload_to_aws_s3("FAIL_"+str_to_append+"product_detail.txt", 's3qingdao',
                                 "FAIL_"+str_to_append+"product_detail.txt")
    os.remove("FAIL_"+str_to_append+"product_detail.txt")
#上传数据
s3_function.upload_to_aws_s3(str_to_append+"product_detail.csv", 's3qingdao',str_to_append+"product_detail.csv")
#删除数据
os.remove(str_to_append+"product_detail.csv")