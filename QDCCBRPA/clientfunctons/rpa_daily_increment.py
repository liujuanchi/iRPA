import tagui as t
import datetime
import pandas as pd



def getdailyincrement(str_to_append):


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
    t.type(element_identifier='//*[@id="fxr"]',text_to_type=str_to_append)
        #再点击，确保日期不会遮住底下的搜索按钮
    t.click(element_identifier='//*[@id="fxr"]')
    t.hover(element_identifier='//*[@class="ipf01"]')
    t.click(element_identifier='//*[@class="ipf01"]')
    #把展示的尺寸设置为50个产品每页：
    t.hover(element_identifier='//*[@data-pagesize="50"]')
    t.click(element_identifier='//*[@data-pagesize="50"]')

    #当下一页没有被disable的时候,有以下超参数
    page_curr = 1 #当前页面index
    value_dict = {} #存放data
    count = 1 #csv 命名用
    #存放列名
    name_list = ['序号', '综合评级', 'url']

    for col_name in name_list:
        value_dict.setdefault(col_name, []) #初始化空数据集


    #当可以翻页，或数据只有一页的时候，进行循环
    while (t.read(element_identifier='//div[@id = "pagefoot"]//a[@class = "cur pf-disabled"]') == str(page_curr)) or (page_curr == 1):

        #每页的数据量大小（row number）
        count_values = int(t.count(element_identifier='//tbody[@id = "content"]//tr')) + 1 # python从0开始
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
        for i in range(1,count_values):
            # 判定条件：如果是今天刚发行的，拿到所有主页面上的数据；
            #如果最下面那条数据都大于今天，就直接翻页
            if str(t.read(
                    element_identifier='//tbody[@id = "content"]//tr[' + str(count_values-1) + ']//td[@class = "px"]')) > str_to_append:
                # print("direct break..")
                break
            else:
                if str(t.read(element_identifier='//tbody[@id = "content"]//tr['+str(i)+']//td[@class = "px"]')) == str_to_append:
                    #序号
                    value_dict[name_list[0]].append(t.read(element_identifier='//tbody[@id = "content"]//tr['+str(i)+']/td[2]'))
                    #综合评级
                    value_dict[name_list[1]].append(t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//td[12]//i/@title'))
                    #url
                    value_dict[name_list[2]].append(t.read(element_identifier='//tbody[@id = "content"]//tr['+ str(i) +']//a/@href'))
                else: #如果不是今天增量，什么都不做
                    pass
        # print("turn the page..")
        # 翻页
        page_curr += 1
        # 鼠标模拟移动，并点击翻页
        t.hover(element_identifier='//*[@href="' + str(page_curr) + '"]')
        t.click(element_identifier='//*[@href="' + str(page_curr) + '"]')

    #关闭tagui流
    t.close()
    #输出格式为："今日日期.csv"
    today_data = pd.DataFrame(value_dict)
    today_data.to_csv(str_to_append+".csv",index=False,encoding='UTF-8')
    return count-1

if __name__ == '__main__':
    # 获取今天（现在时间）
    today = datetime.datetime.today()
    str_to_append = str(today.date()) #得到需要拿到增量的日期，也就是今天
    max_page = getdailyincrement(str_to_append)
    merge_1 = pd.read_csv(str_to_append+".csv")
    merge_list = [pd.DataFrame() for i in range(max_page)]
    for i in range(max_page):  # 到时候换成page number；
        merge_list[i] = pd.read_csv(str(i + 1) + 'daily_data.csv')

    merged = pd.concat(merge_list, axis=0)
    final = pd.merge(merge_1, merged, on='序号', how='inner')
    final.drop_duplicates(inplace=True)

    final = pd.DataFrame(
        final.loc[:, ['序号', '产品名称', '发行银行', '委托货币', '发行日', '停售日', '管理期(天)', '预期收益率', '到期收益率', '与同期储蓄比', '综合评级_x',
                      'url']])
    final.rename(columns={'综合评级_x': '综合评级'}, inplace=True)
    final.to_csv(str_to_append+"final.csv", encoding='UTF-8', index=False)
