# 수정 전
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

TECH_UNITS = [
    {
        "id": "UNIT-01",
        "name": "Boston Dynamics Atlas",
        "category": "HUMANOID",
        "developer": "Boston Dynamics (Hyundai Motor Group)",
        "status": "ALL-ELECTRIC 2024",
        "desc": "기존 유압 방식을 전면 폐기하고 360도 회전 관절 액추에이터를 탑재한 완전 전동식 차세대 휴머노이드 로봇.",
        "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=800&q=80",
        "market_share": "산업 제조용 로보틱스 글로벌 기술 선두",
        "specs": {
            "Actuation": "Full Electric Custom Actuators (360° 무제한 가동)",
            "Sensors": "Real-time Multi-Depth Computer Vision",
            "Autonomy": "Reinforcement Learning Model",
            "Target Field": "현대차 생산 라인 차체 조립 및 부품 운반 자동화"
        },
        "industry_insight": "골드만삭스(Goldman Sachs) 분석 보고서에 따르면 글로벌 휴머노이드 로봇 시장은 2035년까지 380억 달러(약 50조 원) 규모에 도달하며 연간 140만 대 이상 출하될 것으로 전망됩니다.",
        "source": "Goldman Sachs Global Investment Research: Humanoids Report"
    },
    {
        "id": "UNIT-02",
        "name": "Tesla Optimus Gen 2",
        "category": "HUMANOID",
        "developer": "Tesla, Inc.",
        "status": "INTERNAL PILOT DEPLOYED",
        "desc": "테슬라 자율주행(FSD) 신경망과 11자유도 촉각 센서 손가락을 결합하여 공정 부품을 실시간 분류하는 양산형 안드로이드.",
        "image": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?auto=format&fit=crop&w=800&q=80",
        "specs": {
            "Weight": "57kg (이전 세대 대비 10kg 경량화)",
            "Hands": "11 DoF 손가락 + 촉각 햅틱 센서",
            "Neural Net": "Tesla Video Neural Net (End-to-End)",
            "Target Price": "양산 시 20,000 ~ 25,000 USD 목표"
        },
        "industry_insight": "모건 스탠리(Morgan Stanley) 분석에 따르면 테슬라는 기가팩토리 내부 배터리 셀 공정에 실전 투입을 시작했으며, 인건비 절감과 24시간 연속 가동을 목표로 하고 있습니다.",
        "source": "Morgan Stanley Equity Research & Tesla Shareholder Deck"
    },
    {
        "id": "UNIT-03",
        "name": "Apple Vision Pro",
        "category": "XR-SPATIAL",
        "developer": "Apple Inc.",
        "status": "COMMERCIAL PLATFORM",
        "desc": "초고해상도 듀얼 마이크로 OLED와 R1 실시간 센서 프로세서를 탑재하여 공간 자체를 캔버스로 쓰는 공간 컴퓨터.",
        "image": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?auto=format&fit=crop&w=800&q=80",
        "specs": {
            "Display": "2,300만 화소 3D 마이크로 OLED (눈당 4K 이상)",
            "Chipset": "Apple M2 + R1 듀얼 실리콘 (12ms 지연율)",
            "Tracking": "카메라 12개, 센서 5개, 정밀 시선 및 제스처 인식",
            "OS": "visionOS 공간 운영체제"
        },
        "industry_insight": "가트너(Gartner)에 따르면 엔터프라이즈 정밀 수술 시뮬레이션 및 항공/자동차 3D CAD 원격 협업 분야에서 B2B 도입이 급성장하고 있습니다.",
        "source": "Gartner Enterprise Emerging Tech Report"
    },
    {
        "id": "UNIT-04",
        "name": "Meta Quest 3",
        "category": "VR-AR",
        "developer": "Meta Platforms, Inc.",
        "status": "MASS COMMERCIAL",
        "desc": "팬케이크 광학 렌즈와 듀얼 컬러 패스스루 카메라로 선명한 혼합현실(MR)을 구현한 세계 최고 점유율 기기.",
        "image": "https://images.unsplash.com/photo-1592478411213-6153e4ebc07d?auto=format&fit=crop&w=800&q=80",
        "specs": {
            "Optics": "4K+ Infinite Display (눈당 2064x2208)",
            "SoC": "Qualcomm Snapdragon XR2 Gen 2",
            "Pass-through": "듀얼 4MP RGB 컬러 카메라 + 심도 센서",
            "Weight": "515g 경량 헤드셋"
        },
        "industry_insight": "시장조사기관 IDC의 공인 트래커에 따르면 Meta는 전 세계 독립형 VR/MR 헤드셋 시장 점유율 70% 이상을 유지하며 시장 표준을 이끌고 있습니다.",
        "source": "IDC Worldwide Quarterly AR/VR Tracker"
    },
    {
        "id": "UNIT-05",
        "name": "Intuitive Da Vinci 5",
        "category": "SURGICAL",
        "developer": "Intuitive Surgical",
        "status": "FDA 510(k) CLEARED",
        "desc": "10,000배 향상된 컴퓨팅 파워와 촉각 센싱(Force Feedback)을 통해 외과의의 손끝 감각을 재현하는 정밀 수술 로봇.",
        # 안정적인 로봇 수술실 고화질 직결 링크
        "image": "https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=800&q=80",
        "specs": {
            "Force Sensing": "조직 압력 실시간 역각 전달",
            "Console": "3D 4K 고해상도 디지털 뷰어",
            "Computing": "차세대 통합 AI 연산 하드웨어",
            "Track Record": "글로벌 누적 수술 1,400만 건 이상"
        },
        "industry_insight": "IFR(국제로봇연맹) 보고서에 따르면 수술용 로봇은 고령화와 최소침습 시술 보편화로 의료기기 산업군 중 가장 안정적인 고성장세를 기록 중입니다.",
        "source": "International Federation of Robotics (IFR) World Robotics Report"
    }
]

INDUSTRY_METRICS = {
    "robotics_cagr": "38.5%",
    "cagr_source": "Goldman Sachs Research (2024-2035)",
    "spatial_computing_market": "$120B+",
    "spatial_source": "IDC & MarketsandMarkets Worldwide XR Report",
    "smart_factory_automation": "64.2%",
    "factory_source": "IFR World Robotics Statistics"
}

@app.route('/')
def index():
    return render_template('index.html', units=TECH_UNITS, metrics=INDUSTRY_METRICS)

@app.route('/unit/<unit_id>')
def detail(unit_id):
    unit = next((item for item in TECH_UNITS if item["id"] == unit_id), None)
    if not unit:
        abort(404)
    return render_template('detail.html', unit=unit)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip().lower()

    if not message:
        return jsonify({"reply": "[SYS:ERR] 입력된 명령어가 없습니다."})

    if "골드만" in message or "전망" in message or "성장" in message or "시장" in message:
        reply = "골드만삭스(Goldman Sachs) 분석 보고서에 따르면 휴머노이드 로봇 시장은 2035년까지 380억 달러 규모로 성장할 것으로 전망됩니다."
    elif "퀘스트" in message or "메타" in message or "점유율" in message:
        reply = "IDC 공인 리포트에 따르면 Meta는 글로벌 독립형 VR/MR 헤드셋 시장 점유율 약 70%를 점유하고 있습니다."
    elif "아틀라스" in message or "보스턴" in message:
        reply = "보스턴 다이내믹스의 All-Electric Atlas는 전동 액추에이터를 통해 360도 관절 회전이 가능하며 현대차 공장에 실전 투입됩니다."
    elif "출처" in message:
        reply = "본 사이트의 데이터는 Goldman Sachs, IDC, IFR, Morgan Stanley 공시 보고서에 기반합니다."
    else:
        reply = f"명령어 '{message}' 수신: '출처', '골드만삭스', '퀘스트 점유율', '아틀라스' 등을 입력하시면 핵심 시장 지표를 전달합니다."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)