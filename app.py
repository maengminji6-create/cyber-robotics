from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

ESCAPE_ROOMS = [
    {
        "id": "ROOM-01",
        "name": "AI 메인프레임 제어실",
        "codename": "CORE_BREACH",
        "type": "freq-tuner",
        "difficulty": "★★☆☆☆",
        "time_limit": "15분",
        "clear_rate": "84%",
        "status": "LOCKED [LEVEL 1]",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
        "story": "폭주한 AI 코어가 이상 음파 록을 걸었습니다. 주파수 슬라이더를 조작해 공진 파형을 잡고 동기화하십시오.",
        "clues": [
            {"title": "단서 1: 스펙트럼 분석기", "text": "화면에 '80MHz와 90MHz 사이, 소수점 첫째 자리가 5인 지점'이라는 로그가 깜빡입니다."},
            {"title": "단서 2: 다이얼 매뉴얼", "text": "슬라이더를 정확한 수치로 이동시킨 뒤 [SYNC FREQUENCY] 버튼을 누르세요."},
            {"title": "단서 3: 보안 쪽지", "text": "AI의 핵심 공진 주파수는 88.X MHz 대역입니다."}
        ],
        "answer_keyword": "88.5",
        "reward_item": "음파 암호화 코어 칩"
    },
    {
        "id": "ROOM-02",
        "name": "바이오 사이보그 실험실",
        "codename": "CYBER_LAB",
        "type": "chem-lab",
        "difficulty": "★★★☆☆",
        "time_limit": "20분",
        "clear_rate": "68%",
        "status": "LOCKED [BIOHAZARD]",
        "image": "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=800&q=80",
        "story": "신경 가스가 살포되고 있습니다! 시약 A와 B를 조합하여 정확히 100% 중화 농도를 완성하고 배기구를 여십시오.",
        "clues": [
            {"title": "단서 1: 배합 레시피", "text": "신경독 중화 배합: A시약과 B시약은 각각 1회당 20%의 농도를 지닙니다."},
            {"title": "단서 2: 화학적 균형", "text": "A시약의 주입 횟수가 B시약보다 정확히 1번 더 많아야 중화가 일어납니다. (총합 5회)"},
            {"title": "단서 3: 안전 주의사항", "text": "100%를 단 1%라도 초과하면 폭발하므로 정확히 5번(100%)을 채우십시오."}
        ],
        "answer_keyword": "A3-B2",
        "reward_item": "나노 중화제 해독 키"
    },
    {
        "id": "ROOM-03",
        "name": "메가코프 블랙볼트 금고",
        "codename": "BLACK_VAULT",
        "type": "laser-matrix",
        "difficulty": "★★★☆☆",
        "time_limit": "20분",
        "clear_rate": "55%",
        "status": "LOCKED [LASER GRID]",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
        "story": "양자 레이저망이 금고를 둘러싸고 있습니다. 올바른 순서로 센서 노드를 바이패스하여 레이저를 무력화하십시오.",
        "clues": [
            {"title": "단서 1: 청사진 로그", "text": "첫 시작은 항상 첫 번째 그리스 문자 'ALPHA' 노드입니다."},
            {"title": "단서 2: 배선 간섭계", "text": "'BETA' 노드는 가장 마지막에 차단해야 과부하를 막을 수 있습니다."},
            {"title": "단서 3: 우회 프로토콜", "text": "중간 다리 역할을 하는 노드는 'GAMMA'입니다."}
        ],
        "answer_keyword": "ALPHA-GAMMA-BETA",
        "reward_item": "시온 마스터 큐브"
    }
]

@app.route('/')
def index():
    return render_template('index.html', rooms=ESCAPE_ROOMS)

@app.route('/room/<room_id>')
def detail(room_id):
    room = next((item for item in ESCAPE_ROOMS if item["id"] == room_id), None)
    if not room:
        abort(404)
    return render_template('detail.html', room=room)

# 개별 힌트 및 정답 분리 처리 챗봇
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    msg = data.get('message', '').strip().lower()

    if not msg:
        return jsonify({"reply": "[SYS:ERR] 명령어를 입력하십시오."})

    # --- 1. 개별 방 힌트 요청 ---
    if any(k in msg for k in ["1번 힌트", "1번방 힌트", "1번힌트"]):
        reply = (
            "💡 <b>[1번방 (제어실) 전술 힌트]</b><br>"
            "• 스펙트럼 분석기 로그를 보면 88MHz 근처에서 녹색 파형이 잡힙니다.<br>"
            "• 소수점 한 자리 숫자는 <b>.5</b>입니다. 슬라이더를 88.0과 89.0의 정중앙에 맞춰보세요!"
        )
    elif any(k in msg for k in ["2번 힌트", "2번방 힌트", "2번힌트"]):
        reply = (
            "💡 <b>[2번방 (실험실) 전술 힌트]</b><br>"
            "• A와 B 시약은 각각 1번 누를 때마다 +20%씩 증가합니다.<br>"
            "• 총 5번 눌러서 100%를 채워야 하며, A를 B보다 1번 더 많이 눌러야 합니다. (A는 3번, B는 2번!)"
        )
    elif any(k in msg for k in ["3번 힌트", "3번방 힌트", "3번힌트"]):
        reply = (
            "💡 <b>[3번방 (금고) 전술 힌트]</b><br>"
            "• 첫 번째는 1번 알파(ALPHA), 마지막은 2번 베타(BETA)입니다.<br>"
            "• 즉, 가운데에 감마(GAMMA)를 넣어 순서대로 터치해보십시오!"
        )
    elif any(k in msg for k in ["힌트", "도움"]):
        reply = (
            "💡 <b>어느 구역의 힌트가 필요하십니까?</b><br>"
            "원하시는 방 번호를 붙여 질문하십시오:<br>"
            "👉 <b>'1번 힌트'</b>, <b>'2번 힌트'</b>, <b>'3번 힌트'</b><br>"
            "※ 바로 해답을 원하시면 <b>'1번 정답'</b>처럼 입력하십시오."
        )

    # --- 2. 개별 방 정답 요청 ---
    elif any(k in msg for k in ["1번 정답", "1번방 정답", "1번답", "1번방 답"]):
        reply = (
            "🔓 <b>[1번방 (AI 제어실) 솔루션]</b><br>"
            "• <b>목표 주파수:</b> <b>88.5 MHz</b><br>"
            "• <b>해결법:</b> 슬라이더를 드래그하여 정확히 <b>88.5</b>에 맞춘 뒤 [SYNC FREQUENCY] 버튼을 클릭하십시오."
        )
    elif any(k in msg for k in ["2번 정답", "2번방 정답", "2번답", "2번방 답"]):
        reply = (
            "🔓 <b>[2번방 (생체 실험실) 솔루션]</b><br>"
            "• <b>배합 공식:</b> <b>A 3회 + B 2회 = 100%</b><br>"
            "• <b>해결법:</b> [INJECT REAGENT A]를 3번, [INJECT REAGENT B]를 2번 눌러 100%를 만든 후 [PURGE & VENT]를 누르십시오."
        )
    elif any(k in msg for k in ["3번 정답", "3번방 정답", "3번답", "3번방 답"]):
        reply = (
            "🔓 <b>[3번방 (비밀 금고) 솔루션]</b><br>"
            "• <b>안전 노드 순서:</b> <b>ALPHA &rarr; GAMMA &rarr; BETA</b><br>"
            "• <b>해결법:</b> 우측 3개의 노드 버튼을 ALPHA -> GAMMA -> BETA 순서로 클릭하십시오."
        )
    elif any(k in msg for k in ["정답", "답", "솔루션", "해답"]):
        reply = (
            "⚠️ 스포일러 방지를 위해 방 번호를 함께 입력해 주십시오:<br>"
            "👉 <b>'1번 정답'</b>, <b>'2번 정답'</b>, <b>'3번 정답'</b>"
        )

    elif any(k in msg for k in ["안녕", "누구", "하이"]):
        reply = "시스템 온라인. 전술 해킹 AI 'AEGIS'입니다. <b>'1번 힌트'</b> 또는 <b>'1번 정답'</b>처럼 명령을 내려주십시오."

    else:
        reply = f"명령어 '{msg}' 수신 완료. 힌트나 정답이 필요하시면 <b>'1번 힌트'</b>, <b>'1번 정답'</b> 형식으로 입력해 주십시오."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)