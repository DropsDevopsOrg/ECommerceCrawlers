from flask import Flask, render_template, request
from pyecharts import Page, Bar

import config
from exts import db
from models import Poet, Poem


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app


app = create_app()


# 获得作诗前十的诗人图表
def get_bar():
    poets = Poet.query.order_by(Poet.num.desc()).limit(10)
    attr_poet = []
    num_poet = []
    for poet in poets:
        attr_poet.append(poet.name)
        num_poet.append(poet.num)
    bar = Bar("作诗数前十名诗人")
    bar.add("", attr_poet, num_poet, is_label_show=True, center=[50,50])
    return bar



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    page = Page()
    bar = get_bar()
    page.add(bar)
    keyword = request.args.get('keyword').replace(' ', '')  # 获得前端传回的keyword
    print(keyword)
    if '：' in keyword:  # 判断是否是高级搜索
        key = keyword.split('：')[0]  # 获取传回的高级搜索关键字，如"诗人：李白"，此时获取‘诗人’
        value = keyword.split('：')[1]  # 获取‘李白’
        if key == '诗人' and value:  # 判断高级搜索为‘诗人’，并且搜索内容不为空
            poet = Poet.query.filter_by(name=value).first()  # 在数据库中查询姓名为”李白“的诗人数据
            if poet:  # 如果查询到
                context = {
                    'poet': poet,  # 诗人字段信息
                    'poem': poet.poems  # 诗人的是诗的字段信息
                }
                return render_template('search.html', **context, chart=page.render_embed())
            else:  # 如果没有查询到
                context = {
                    'message': '没有找到相关内容'  # 返回信息
                }
                return render_template('search.html', **context)  # 渲染页面
        elif key == '诗句' and value:  # 判断高级搜索为‘诗句’，并且搜索内容不为空 如”诗句：清明“
            poem = Poem.query.filter(Poem.content.contains(value)).all()  # 获取全部诗句内容中包含”清明“诗句
            if poem:  # 如果查询到
                context = {
                    'poem': poem  # 诗的字段信息
                }
                return render_template('search.html', **context, chart=page.render_embed(), host='/static/js',
                                       script_list=page.get_js_dependencies())  # 渲染页面
            else:  # 如果没有查询到
                context = {
                    'message': '没有找到相关内容'
                }
                return render_template('search.html', **context)  # 渲染页面
    else:  # 普通搜索，直接搜索诗的名字 如：‘江南’
        poem = Poem.query.filter_by(title=keyword).all()  # 获取所有诗的名字为‘江南’的数据
        if poem:  # 如果查询的到
            context = {
                'poem': poem  # 所有诗的名字为‘江南’字段信息
            }
            return render_template('search.html', **context, chart=page.render_embed(), host='/static/js',
                                   script_list=page.get_js_dependencies())  # 渲染页面
        else:  # 如果没有查询的到
            context = {
                'message': '没有找到相关内容'
            }
            return render_template('search.html', **context)  #渲染页面

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
