# server_malaysia.py - 完整马来西亚版
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime

app = FastAPI(
    title="T4U Malaysia",
    version="4.0",
    description="马来西亚补习班搜索平台 API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS设置 - 必须放在前面！
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 数据模型
class CenterCreate(BaseModel):
    name: str
    subject: str
    grade: Optional[str] = "Tingkatan 1-5"
    address: str
    city: str
    state: str
    price: str
    description: Optional[str] = ""
    phone: Optional[str] = ""
    operating_hours: Optional[str] = "Mon-Fri: 4pm-9pm"

# 马来西亚补习班数据库
centers_db = [
    {
        "id": 1,
        "name": "精英数学补习中心",
        "subject": "数学",
        "grade": "Tingkatan 1-5",
        "address": "No. 123, Jalan Bukit Bintang",
        "city": "吉隆坡",
        "state": "WP Kuala Lumpur",
        "price": "RM50/jam",
        "rating": 4.7,
        "distance": "1.2km",
        "subjects": ["数学", "高级数学"],
        "phone": "03-1234 5678",
        "description": "专攻SPM数学，小班教学，经验丰富老师",
        "operating_hours": "Mon-Fri: 4pm-9pm, Sat-Sun: 9am-6pm",
        "created_at": "2024-01-01",
        "added_by_user": False
    },
    {
        "id": 2,
        "name": "牛顿物理补习社",
        "subject": "物理",
        "grade": "Tingkatan 4-5",
        "address": "45-2, Jalan SS2/24, Petaling Jaya",
        "city": "八打灵再也",
        "state": "雪兰莪",
        "price": "RM55/jam",
        "rating": 4.5,
        "distance": "2.5km",
        "subjects": ["物理", "数学"],
        "phone": "03-8765 4321",
        "description": "物理实验与理论结合，SPM历年考题分析",
        "operating_hours": "Mon-Sat: 3pm-8pm",
        "created_at": "2024-01-01",
        "added_by_user": False
    },
    {
        "id": 3,
        "name": "化学实验室补习中心",
        "subject": "化学",
        "grade": "Tingkatan 3-5",
        "address": "78, Jalan Tan Sri Teh Ewe Lim",
        "city": "怡保",
        "state": "霹雳",
        "price": "RM60/jam",
        "rating": 4.8,
        "distance": "3.8km",
        "subjects": ["化学", "生物"],
        "phone": "05-2345 6789",
        "description": "化学方程式教学，实验安全指导",
        "operating_hours": "Mon-Fri: 2pm-7pm, Sat: 9am-1pm",
        "created_at": "2024-01-01",
        "added_by_user": False
    },
    {
        "id": 4,
        "name": "英语大师补习学院",
        "subject": "英文",
        "grade": "Standard 1-Tingkatan 5",
        "address": "12-1, Jalan Tun Razak",
        "city": "新山",
        "state": "柔佛",
        "price": "RM65/jam",
        "rating": 4.6,
        "distance": "0.8km",
        "subjects": ["英文", "英国文学"],
        "phone": "07-3456 7890",
        "description": "英语会话与写作，SPM作文技巧",
        "operating_hours": "Everyday: 10am-8pm",
        "created_at": "2024-01-01",
        "added_by_user": False
    }
]

# 马来西亚数据
MALAYSIA_STATES = [
    "全部地区", "吉隆坡", "雪兰莪", "槟城", "柔佛", "霹雳", "马六甲", 
    "森美兰", "彭亨", "登嘉楼", "吉兰丹", "砂拉越", "沙巴", "玻璃市", "吉打"
]

MALAYSIA_SUBJECTS = [
    "全部科目", "数学", "高级数学", "科学", "物理", "化学", "生物", 
    "英文", "华文", "马来文", "历史", "地理", "会计", "经济", 
    "商业", "道德教育", "全科", "电脑科学", "其他"
]

# ==================== API端点 ====================

@app.get("/")
def home():
    return {
        "service": "T4U Malaysia API",
        "version": "4.0",
        "country": "Malaysia",
        "currency": "RM (Malaysian Ringgit)",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "all_centers": "/api/centers",
            "search": "/api/search?keyword=数学&state=吉隆坡&max_price=100",
            "states": "/api/states",
            "subjects": "/api/subjects",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "T4U Malaysia",
        "timestamp": datetime.now().isoformat(),
        "centers_count": len(centers_db)
    }

@app.get("/api/centers")
def get_all_centers():
    """获取所有补习中心"""
    return JSONResponse(content={
        "success": True,
        "message": "Successfully retrieved tuition centers",
        "currency": "RM",
        "country": "Malaysia",
        "count": len(centers_db),
        "centers": centers_db
    })

@app.get("/api/states")
def get_states():
    """获取马来西亚州属列表"""
    return {
        "success": True,
        "states": MALAYSIA_STATES
    }

@app.get("/api/subjects")
def get_subjects():
    """获取马来西亚科目列表"""
    return {
        "success": True,
        "subjects": MALAYSIA_SUBJECTS
    }

@app.get("/api/search")
def search_centers(
    keyword: str = "",
    subject: str = "",
    state: str = "",
    city: str = "",
    max_price: int = None,
    sort_by: str = "rating"
):
    """搜索补习中心"""
    results = centers_db.copy()
    
    # 关键字搜索
    if keyword and keyword.strip():
        keyword = keyword.lower().strip()
        results = [
            c for c in results 
            if (keyword in c["name"].lower()) or 
               (keyword in c["subject"].lower()) or
               (keyword in c["description"].lower()) or
               (keyword in c["city"].lower())
        ]
    
    # 科目筛选
    if subject and subject != "全部科目":
        subject = subject.lower()
        results = [c for c in results if subject in c["subject"].lower()]
    
    # 州属筛选
    if state and state != "全部地区":
        results = [c for c in results if state == c["state"]]
    
    # 城市筛选
    if city and city.strip():
        city = city.lower().strip()
        results = [c for c in results if city in c["city"].lower()]
    
    # 价格筛选
    if max_price:
        results = [
            c for c in results 
            if extract_price(c["price"]) <= max_price
        ]
    
    # 排序
    if sort_by == "rating":
        results.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "price":
        results.sort(key=lambda x: extract_price(x["price"]))
    elif sort_by == "distance":
        results.sort(key=lambda x: float(x["distance"].replace("km", "")))
    
    return {
        "success": True,
        "message": f"Found {len(results)} centers",
        "currency": "RM",
        "filters": {
            "keyword": keyword,
            "subject": subject,
            "state": state,
            "city": city,
            "max_price": max_price,
            "sort_by": sort_by
        },
        "count": len(results),
        "results": results
    }

@app.get("/api/center/{center_id}")
def get_center(center_id: int):
    """获取单个补习中心详情"""
    for center in centers_db:
        if center["id"] == center_id:
            return {
                "success": True,
                "center": center
            }
    
    raise HTTPException(status_code=404, detail="Center not found")

@app.post("/api/centers")
def create_center(center_data: CenterCreate):
    """创建新补习中心"""
    # 验证价格格式
    if not center_data.price.startswith("RM"):
        raise HTTPException(status_code=400, detail="Price must start with 'RM'")
    
    # 创建新补习中心
    new_id = max([c["id"] for c in centers_db], default=0) + 1
    new_center = {
        "id": new_id,
        **center_data.dict(),
        "rating": 4.0,
        "distance": f"{new_id % 10 + 0.5}km",
        "subjects": [center_data.subject],
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "added_by_user": True
    }
    
    centers_db.append(new_center)
    
    return {
        "success": True,
        "message": "Tuition center created successfully",
        "center_id": new_id,
        "center": new_center
    }

def extract_price(price_str: str) -> int:
    """从价格字符串提取数字"""
    import re
    numbers = re.findall(r'\d+', price_str)
    return int(numbers[0]) if numbers else 999

if __name__ == "__main__":
    print("=" * 70)
    print("🇲🇾 T4U Malaysia - 马来西亚补习班平台")
    print("=" * 70)
    print("💰 货币: RM (马来西亚令吉)")
    print("📍 地区: 马来西亚全境")
    print("📚 科目: 马来西亚教育体系")
    print("=" * 70)
    print("🚀 服务器启动中...")
    print(f"📡 API地址: http://127.0.0.1:8000")
    print(f"📚 文档: http://127.0.0.1:8000/docs")
    print("=" * 70)
    print("📋 测试端点:")
    print("  • 所有补习班: http://127.0.0.1:8000/api/centers")
    print("  • 搜索数学: http://127.0.0.1:8000/api/search?keyword=数学")
    print("  • 吉隆坡补习: http://127.0.0.1:8000/api/search?state=吉隆坡")
    print("  • 价格筛选: http://127.0.0.1:8000/api/search?max_price=60")
    print("=" * 70)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )