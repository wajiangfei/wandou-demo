# coding: utf-8
import auth
import wandou

app_key = "xxxxx"
myauth = auth.Auth(app_key)

# 添加白名单
result1 = myauth.update_list(ip='x.x.x.x')
# 自动将本地外网ip加入ip白名单
result11 = myauth.update_list(ip='3.4.5.6', wid='200409')
print(result11)
# 从白名单中删除一条ip,谨慎使用
result2 = myauth._delete_list('xxxx')
print(result2)
# 打印白名单
result3 = myauth.white_list()
print(result3)
# 生成代理鉴权参数
token = auth.authorization(username='xxx', password='xxx')


mywandou = wandou.WandouManager(myauth)

# 获取区域列表
area_list = mywandou.area_list()
# print(area_list)

# 获取ip
ip_list = mywandou.ip_list(num=3)
ip_list_sim = mywandou.ip_list_simple()
# print(ip_list)
# print(next(ip_list_sim))