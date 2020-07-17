import rpa as r

r.init()
r.url('https://cn.bing.com/')
r.type('//*[@name="q"]', 'decentralization[enter]')
print(r.read('result-stats'))
r.snap('page', 'results.png')
r.close()
