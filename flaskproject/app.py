from flask import Flask, render_template, request
from self_api import SpiderZOL, Chart

# 创建app实例
app = Flask(__name__)

# 用于缓存闲聊信息
result_chat = []


# 首页路由
@app.route('/')
def index():
    return render_template("index.html")


# 查询商品搜索页路由
@app.route('/search_product')
def search_product():
    return render_template("search_product/search_product.html")


# 查询商品结果页路由
@app.route('/search_product_result', methods=["POST"])
def search_product_result():
    if request.method == "POST":
        # 创建中关村爬虫对象
        spider_obj = SpiderZOL(request.form["product_name"])
        # 启动爬虫得到信息
        products = spider_obj.product_info()
        return render_template("search_product/search_product_result.html", products=products)


# 闲聊首页路由
@app.route('/chat')
def chat():
    # 重新提问时清空聊天记录
    result_chat.clear()
    return render_template("chat_robot/chart.html")

# 闲聊连续会话页路由
@app.route('/chat_result', methods=["POST"])
def chat_result():
    if request.method == "POST":
        # 创建Chat对象
        chart_obj = Chart()
        # 添加提问信息缓存到result_chat列表中
        result_chat.append(request.form["question"])
        # 获取回答信息
        result = chart_obj.smart_chat(request.form["question"])
        # 添加回答信息缓存到result_chat列表中
        result_chat.append(result)
        return render_template("chat_robot/chart_result.html", result_chat=result_chat)


if __name__ == '__main__':
    app.run()
