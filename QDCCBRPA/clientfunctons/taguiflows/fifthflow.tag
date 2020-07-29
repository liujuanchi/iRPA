http://bank.jrj.com.cn/bankpro/data.shtml

wait 15 
table //div[@class="table-s1 tab-s2 w100"]  to bankjrjdata20200721-1.csv

for card from 1 to 20
    read ((//a[@class="will"])[`card`])/@href to uuuuuu   
    
    read ((//i[@class="star"])[`card`])/@title to star   

    dealrow = ['URL:' + uuuuuu + ", score" + star]
    write `csv_row(dealrow)` to bankjrjdata20200721-1.csv

click 下一页>>

table //div[@class="table-s1 tab-s2 w100"]  to bankjrjdata20200721-2.csv

for card from 1 to 20
    read ((//a[@class="will"])[`card`])/@href to uuuuuu   
    
    read ((//i[@class="star"])[`card`])/@title to star   

    dealrow = ['URL:' + uuuuuu + ", score" + star]    
    write `csv_row(dealrow)` to bankjrjdata20200721-2.csv

