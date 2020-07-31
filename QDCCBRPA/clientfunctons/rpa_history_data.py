import tagui as t
import datetime
import pandas as pd

def gethistorylist (inputyear):
    # 获取xxxx年的数据
    input = inputyear
    date_start = input + '-01-01' #一年开始的日期 （试一试10天的）
    date_end = input + '-12-31' #一年结束的日期

    #初始化页面
    t.init()
    #输入url进入
    t.url("http://bank.jrj.com.cn/bankpro/data.shtml?type=1")
    #鼠标放上去，点击精简选项
    t.hover(element_identifier='//*[@id="fxr"]')
    t.click(element_identifier='//*[@id="zksq"]')
    #鼠标移动到发行日期上，点击文本栏，输入发行日日期为今日，点击搜索
    t.hover(element_identifier='//*[@id="fxr"]')
    t.click(element_identifier='//*[@id="fxr"]')
    t.type(element_identifier='//*[@id="fxr"]',text_to_type=date_start)
        #再点击，确保日期不会遮住底下的搜索按钮
    t.click(element_identifier='//*[@id="fxr"]')
    t.hover(element_identifier='//*[@class="ipf01"]')
    t.click(element_identifier='//*[@class="ipf01"]')
    #把展示的尺寸设置为50个产品每页：
    t.hover(element_identifier='//*[@data-pagesize="50"]')
    t.click(element_identifier='//*[@data-pagesize="50"]')
    #点击以发行日升序排行，等价于"倒过来取"
    t.hover(element_identifier='//*[@data-sort = "sell_org_date"]')
    t.click(element_identifier='//*[@data-sort = "sell_org_date"]')
    #当下一页没有被disable的时候,有以下超参数
    page_curr = 1 #当前页面index
    value_dict = {} #存放data
    #存放列名
    name_list = ['序号', '产品名称', '发行银行', '委托货币', '发行日', '停售日', '管理期(天)', '预期收益率', '到期收益率', '与同期储蓄比', '综合评级','url']
    for col_name in name_list:
        value_dict.setdefault(col_name, []) #初始化空数据集
    #当可以翻页，或数据只有一页的时候，进行循环
    stop_flag = False
    #当当前页面不是最后一页，或只有一页时，都进行如下循环
    while (t.read(element_identifier='//div[@id = "pagefoot"]//a[@class = "cur pf-disabled"]') == str(page_curr)) or (page_curr == 1):
        if stop_flag == True: #如果没有今年的数据，就没必要翻页了
            break
        #每页的数据量大小（row number）
        count_values = int(t.count(element_identifier='//tbody[@id = "content"]//tr')) + 1 # python从0开始
        #爬取当前页面
        for i in range(1, count_values):
            # 判定条件：如果是今年内(小于今年12-31或等于12-31的)，全都要
            if str(t.read(
                    element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//td[@class = "px"]')) <= date_end:
                # 序号
                value_dict[name_list[0]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[2]'))
                # 产品名称
                value_dict[name_list[1]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[3]'))
                # 发行银行
                value_dict[name_list[2]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[4]'))
                # 委托货币
                value_dict[name_list[3]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[5]'))
                # 发行日
                value_dict[name_list[4]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[6]'))
                # 停售日
                value_dict[name_list[5]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[7]'))
                # 管理期（天）
                value_dict[name_list[6]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[8]'))
                # 预期收益率
                value_dict[name_list[7]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[9]'))
                # 到期收益率
                value_dict[name_list[8]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[10]'))
                # 与同期储蓄比
                value_dict[name_list[9]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[11]'))
                # 综合评级
                value_dict[name_list[10]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//td[12]//i/@title'))
                # url
                value_dict[name_list[11]].append(
                    t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//a/@href'))
            else:  # 如果已经超过今年的数据了，此线程结束，flag置true, while循环结束
                stop_flag = True
                print("thread stops here..")
                break
        # 翻页
        page_curr += 1
        print("turn the page..")
        # 鼠标模拟移动，并点击翻页
        t.hover(element_identifier='//*[@href="' + str(page_curr) + '"]')
        t.click(element_identifier='//*[@href="' + str(page_curr) + '"]')
    # #关闭tagui流
    t.close()
    #输出格式为："今年年份.csv"
    hist_data = pd.DataFrame(value_dict)
    #双格式（csv + xlsx 输出）
    hist_data.to_csv(input+".csv",index=False,encoding='UTF-8')
    hist_data.to_excel(input+".xlsx",index=False,encoding='UTF-8')

gethistorylist('2003')