# 豆瓣二创文备份项目

## 爬虫

1. 将asoul_article.sql及asoul_paper.sql导入至mysql数据库
2. 修改dbcrawler.py，填入用户名、密码、数据库名
3. 后台运行dbcrawler.py

## 网站

1. 修改main.go，填入数据库用户名、密码、数据库名
2. 编译
3. 后台运行

## Tips

1. 特别感谢心亦向晚提供的豆瓣客户端api
2. 定期将asoul_article中textdata字段的write.as替换为writeas.xyz可解决前者在中国大陆无法访问的问题
