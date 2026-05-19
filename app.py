from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), 'progress.json')

# 默认学习数据
DEFAULT_DATA = {
    "stages": [
        {
            "id": 1,
            "name": "第一阶段：基础扫盲（1-2周）",
            "description": "搞懂基本概念，不被术语忽悠",
            "tasks": [
                {"id": "1-1", "name": "学习K线、成交量、均线基本概念", "done": False, "link": "https://www.bilibili.com/video/BV1Wx411c7s8/"},
                {"id": "1-2", "name": "了解A股交易规则（T+1、涨跌停、手续费）", "done": False, "link": ""},
                {"id": "1-3", "name": "理解PE、ROE等基础财务指标", "done": False, "link": ""},
                {"id": "1-4", "name": "开通东方财富/同花顺模拟盘", "done": False, "link": "https://www.eastmoney.com/"},
                {"id": "1-5", "name": "模拟盘操作5次以上", "done": False, "link": ""},
                {"id": "1-6", "name": "阅读《小狗钱钱》建立理财思维", "done": False, "link": ""}
            ]
        },
        {
            "id": 2,
            "name": "第二阶段：建立认知（2-4周）",
            "description": "建立自己的判断逻辑，不跟风",
            "tasks": [
                {"id": "2-1", "name": "学习价值投资基础（好公司判断标准）", "done": False, "link": ""},
                {"id": "2-2", "name": "学习技术分析基础（支撑位、压力位、趋势线）", "done": False, "link": "https://www.bilibili.com/video/BV1nE411d7zG/"},
                {"id": "2-3", "name": "开通A股证券账户", "done": False, "link": ""},
                {"id": "2-4", "name": "入金3000元，购买第一只ETF", "done": False, "link": ""},
                {"id": "2-5", "name": "记录每笔交易的买卖理由", "done": False, "link": ""},
                {"id": "2-6", "name": "阅读《日本蜡烛图技术》", "done": False, "link": ""}
            ]
        },
        {
            "id": 3,
            "name": "第三阶段：形成策略（1-3个月）",
            "description": "找到适合小资金的稳定策略",
            "tasks": [
                {"id": "3-1", "name": "学习ETF定投策略并实践", "done": False, "link": ""},
                {"id": "3-2", "name": "尝试龙头股逢低买入策略", "done": False, "link": ""},
                {"id": "3-3", "name": "学习网格交易策略", "done": False, "link": ""},
                {"id": "3-4", "name": "完成10笔以上真实交易", "done": False, "link": ""},
                {"id": "3-5", "name": "总结适合自己的交易方法", "done": False, "link": ""},
                {"id": "3-6", "name": "逐步加大资金到1-2w", "done": False, "link": ""}
            ]
        }
    ],
    "resources": [
        {"name": "B站 - 李永乐老师股票相关视频", "url": "https://search.bilibili.com/all?keyword=%E6%9D%8E%E6%B0%B8%E4%B9%90%20%E8%82%A1%E7%A5%A8", "desc": "通俗易懂的金融知识科普"},
        {"name": "东方财富网", "url": "https://www.eastmoney.com/", "desc": "行情、资讯、模拟盘"},
        {"name": "雪球", "url": "https://xueqiu.com/", "desc": "投资者交流社区"},
        {"name": "理杏仁", "url": "https://www.lixinger.com/", "desc": "基本面数据查询"},
        {"name": "乌龟量化", "url": "https://wglh.com/", "desc": "量化数据和回测工具"},
        {"name": "AkShare - 开源财经数据接口", "url": "https://github.com/akfamily/akshare", "desc": "Python免费A股数据"},
        {"name": "同花顺官网", "url": "https://www.10jqka.com.cn/", "desc": "行情软件和资讯"}
    ],
    "etf_list": [
        {"code": "510300", "name": "沪深300ETF", "desc": "跟踪大盘蓝筹股"},
        {"code": "159915", "name": "创业板ETF", "desc": "跟踪创业板指数"},
        {"code": "510500", "name": "中证500ETF", "desc": "跟踪中小盘股"},
        {"code": "510180", "name": "上证180ETF", "desc": "跟踪上证180指数"}
    ],
    "portfolio": {
        "total": 30000,
        "etf": 15000,
        "stocks": 5000,
        "learning": 3000,
        "cash": 7000
    }
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data, now=datetime.now().strftime('%Y-%m-%d'))

@app.route('/api/toggle', methods=['POST'])
def toggle_task():
    task_id = request.json.get('task_id')
    data = load_data()
    
    for stage in data['stages']:
        for task in stage['tasks']:
            if task['id'] == task_id:
                task['done'] = not task['done']
                save_data(data)
                return jsonify({'success': True, 'done': task['done']})
    
    return jsonify({'success': False})

@app.route('/api/progress')
def get_progress():
    data = load_data()
    total = 0
    done = 0
    for stage in data['stages']:
        for task in stage['tasks']:
            total += 1
            if task['done']:
                done += 1
    return jsonify({'total': total, 'done': done, 'percent': round(done/total*100, 1) if total > 0 else 0})

@app.route('/api/reset', methods=['POST'])
def reset_progress():
    save_data(DEFAULT_DATA)
    return jsonify({'success': True})

if __name__ == '__main__':
    # 确保目录存在
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    # 初始化数据文件
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    print('🚀 股票学习路线跟踪系统启动中...')
    print('📊 访问地址: http://localhost:8000')
    print('💡 按 Ctrl+C 停止服务')
    app.run(host='0.0.0.0', port=8000, debug=True)
