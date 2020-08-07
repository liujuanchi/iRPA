import tagui as t
import datetime
import pandas as pd
import os

def getblanklist():
    #初始化页面
    t.init()
    #输入url进入
    t.url("http://bank.jrj.com.cn/bankpro/data.shtml?type=1")
    t.wait(15)
	#直接开始搜索，不需要任何筛选条件
    t.click(element_identifier='//*[@id="fxr"]')
    t.hover(element_identifier='//*[@class="ipf01"]')
    t.click(element_identifier='//*[@class="ipf01"]')
    #把展示的尺寸设置为50个产品每页：
    t.hover(element_identifier='//*[@data-pagesize="50"]')
    t.click(element_identifier='//*[@data-pagesize="50"]')
    #点击以发行日升序排行，等价于"倒过来取"，这样发行日为空的会在最前面
    t.hover(element_identifier='//*[@data-sort = "sell_org_date"]')
    t.click(element_identifier='//*[@data-sort = "sell_org_date"]')
    
    #当下一页没有被disable的时候,有以下超参数
    page_curr = 1 #当前页面index
    max_page = 1  # 最大的页面数记录
    
    # 存放列名
    value_dict = {}  # 存放data
    name_list = ['序号', '综合评级', 'url']
    
    for col_name in name_list:
        value_dict.setdefault(col_name, [])  # 初始化空数据集

    #当可以翻页，或数据只有一页的时候，进行循环
    stop_flag = False # 初始化一个flag，flag = true代表我们需要的数据已经取完了，没必要再翻页了
    while (t.read(element_identifier='//div[@id = "pagefoot"]//a[@class = "cur pf-disabled"]') == str(page_curr)) or (page_curr == 1):
        
        if stop_flag == True: #如果没有空白数据了，就没必要翻页了
            break
        max_page = page_curr
        #每页的数据量大小（row number）
        count_values = int(t.count(element_identifier='//tbody[@id = "content"]//tr')) + 1 # python从0开始
        # 爬取页面所有一个table里的值
        filename = str(page_curr) + "blank_date.csv"
        t.wait(1)  # 等1秒，万一加载错误了
        t.table(element_identifier='//div[@class = "table-s1 tab-s2 w100"]//table', filename_to_save=filename)
        
        #爬取当前页面 (只有title和href）
        for i in range(1, count_values):
            # 判定条件：如果发行日是空(--)，进入此if
            if str(t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//td[@class = "px"]')) == '--':
                # print("number {} is running".format(str(i)))
                # 序号
                value_dict[name_list[0]].append(
                                                t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']/td[2]'))
                # 综合评级
                value_dict[name_list[1]].append(
                                                t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//td[12]//i/@title'))
                # url
                value_dict[name_list[2]].append(
                                                t.read(element_identifier='//tbody[@id = "content"]//tr[' + str(i) + ']//a/@href'))
        
            else:  # 如果不再是空值-- ，此线程结束，flag置true, while循环结束
                stop_flag = True
                # print("thread stops here..")
                break
        # 翻页
        page_curr += 1
        # print("turn the page..")
        # 鼠标模拟移动，并点击翻页
        t.hover(element_identifier='//*[@href="' + str(page_curr) + '"]')
        t.click(element_identifier='//*[@href="' + str(page_curr) + '"]')
    
    
    
    # #关闭tagui流
    t.close()
    #
    # 输出格式为："blank_date.csv"
    hist_data = pd.DataFrame(value_dict)
    hist_data.to_csv("blank_date.csv", index=False, encoding='UTF-8')
    return max_page


def main():
    max_page = getblanklist()
    merge_1 = pd.read_csv('blank_date.csv')
    os.remove('blank_date.csv')
    merge_list = [pd.DataFrame() for i in range(max_page)]
    for i in range(max_page):  # 到时候换成page number；
        merge_list[i] = pd.read_csv(str(i + 1) + 'blank_date.csv')
        os.remove(str(i + 1) + 'blank_date.csv')

    merged = pd.concat(merge_list, axis=0)
    final = pd.merge(merge_1, merged, on='序号',how = 'inner')
    final.drop_duplicates(inplace=True)
    final = pd.DataFrame(final.loc[:, ['序号','产品名称', '发行银行', '委托货币', '发行日', '停售日', '管理期(天)', '预期收益率', '到期收益率', '与同期储蓄比', '综合评级_x',
                                       'url']])
    final.rename(columns={'综合评级_x':'综合评级'},inplace=True)
    final.to_csv('blank_date_final.csv', encoding='UTF-8', index=False)
    return 'blank_date_final.csv'
