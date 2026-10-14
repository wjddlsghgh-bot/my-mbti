import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered"
)

# 2. 커스텀 CSS (따뜻한 크림/노란색 톤, 큰 글씨, 초보자 친화적 디자인)
st.markdown("""
    <style>
    /* 전체 배경색 - 따뜻한 크림톤 */
    .stApp {
        background-color: #FFFDF0;
        color: #4A3E3D;
        font-family: 'Malgun Gothic', 'Pretendard', sans-serif;
    }
    
    /* 제목 스타일 */
    .main-title {
        color: #D97706;
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #78350F;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 25px;
    }

    /* 포켓몬 카드 박스 */
    .pokemon-card {
        background-color: #FFFFFF;
        border: 3px solid #FFE89C;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 20px rgba(220, 190, 120, 0.2);
        margin-top: 15px;
    }

    /* 포켓몬 이름 */
    .pokemon-name {
        color: #B45309;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 5px;
    }

    /* 영어 이름 및 타입 */
    .pokemon-meta {
        font-size: 1.1rem;
        color: #92400E;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* 어울리는 이유 박스 */
    .reason-box {
        background-color: #FFFBEB;
        border: 2px dashed #FCD34D;
        border-radius: 15px;
        padding: 18px;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #4B5563;
        margin-top: 15px;
        word-break: keep-all;
    }

    /* Selectbox 큰 글씨 적용 */
    div[data-baseweb="select"] {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 16가지 MBTI 데이터 정의 (PokeAPI 정식 이미지 URL 연동)
POKEMON_DATA = {
    "ISTJ": {
        "ko_name": "거북왕",
        "en_name": "Blastoise",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "type": "💧 물 타입",
        "feature": "묵묵하고 단단한 껍질을 지닌 신뢰의 아이콘",
        "reason": "책임감이 강하고 규칙을 철저하게 지키는 원칙주의자입니다.<br>단단한 껍질처럼 어떠한 상황에서도 흔들리지 않는 신뢰감을 주며 팀의 중심을 잡아줍니다."
    },
    "ISFJ": {
        "ko_name": "해피너스",
        "en_name": "Blissey",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "type": "⚪ 노말 타입",
        "feature": "상처받은 마음을 치료해 주는 자상한 간호사",
        "reason": "상대방을 따뜻하게 잘 보살피고 헌신적인 성격입니다.<br>친절한 태도와 넓은 마음으로 주변 사람들의 마음을 치유해 주는 포근한 매력이 있습니다."
    },
    "INFJ": {
        "ko_name": "가디안",
        "en_name": "Gardevoir",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/282.png",
        "type": "🔮 에스퍼 / 🧚 페어리 타입",
        "feature": "트레이너를 지키기 위해 미래까지 예지하는 수호자",
        "reason": "깊은 통찰력과 예민한 감수성을 지니고 있습니다.<br>소중한 이의 마음을 귀신같이 알아차리며 깊은 공감 능력으로 상대를 가만히 수호해 줍니다."
    },
    "INTJ": {
        "ko_name": "뮤츠",
        "en_name": "Mewtwo",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "type": "🔮 에스퍼 타입",
        "feature": "압도적인 지능과 독립성을 지닌 치밀한 전략가",
        "reason": "독창적이고 논리적이며 계산된 전략을 펼치는 완벽주의자입니다.<br>자신만의 기준이 명확하여 철저한 계획을 통해 목표를 반드시 달성해 냅니다."
    },
    "ISTP": {
        "ko_name": "루카리오",
        "en_name": "Lucario",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "type": "🥊 격투 / ⚙️ 강철 타입",
        "feature": "상대의 파동을 감지해 냉철하게 대응하는 만능 해결사",
        "reason": "조용하지만 필요할 때 압도적인 순발력과 행동력을 발휘합니다.<br>상황 판단이 빠르고 도구를 다루는 데 능숙하며, 과묵하게 본인의 일을 뛰어나게 해냅니다."
    },
    "ISFP": {
        "ko_name": "메타몽",
        "en_name": "Ditto",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png",
        "type": "⚪ 노말 타입",
        "feature": "어디든 어떤 모습으로든 맞춰 변신하는 유연함",
        "reason": "온화하고 유연하며 남에게 맞춰주는 적응력이 뛰어납니다.<br>자신만의 평화롭고 자유로운 예술적 감성을 지니고 있어 누구와도 잘 어울립니다."
    },
    "INFP": {
        "ko_name": "이브이",
        "en_name": "Eevee",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "type": "⚪ 노말 타입",
        "feature": "어떤 모습으로든 진화할 수 있는 무한한 가능성의 소유자",
        "reason": "무한한 상상력과 낭만을 품고 있는 열정적인 이상가입니다.<br>내면에 다채로운 가능성을 간직하고 있으며, 사람들에게 따뜻하고 선한 영감을 줍니다."
    },
    "INTP": {
        "ko_name": "후딘",
        "en_name": "Alakazam",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png",
        "type": "🔮 에스퍼 타입",
        "feature": "IQ 5000의 두뇌로 모든 사건을 분석하는 지적 탐구자",
        "reason": "호기심이 풍부하고 지적 탐구욕이 강한 논리적인 학자 스타일입니다.<br>복잡한 문제를 지치지 않고 풀어내며 지식을 습득할 때 깊은 즐거움을 느낍니다."
    },
    "ESTP": {
        "ko_name": "윈디",
        "en_name": "Arcanine",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/59.png",
        "type": "🔥 불꽃 타입",
        "feature": "바람처럼 빠르게 달려나가는 당당하고 당찬 모험가",
        "reason": "에너지가 넘치며 도전을 두려워하지 않는 매력적인 행동파입니다.<br>탁월한 순발력으로 순간적인 기회를 포착해 시원시원하게 해결해 버립니다."
    },
    "ESFP": {
        "ko_name": "푸린",
        "en_name": "Jigglypuff",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "type": "⚪ 노말 / 🧚 페어리 타입",
        "feature": "마이크를 잡으면 주목받는 솔직하고 사랑스러운 연예인",
        "reason": "시선을 즐기고 밝은 흥을 전파하는 분위기 메이커입니다.<br>솔직하고 열정적인 모습으로 주위 사람들에게 웃음과 즐거움을 선사해 줍니다."
    },
    "ENFP": {
        "ko_name": "피카츄",
        "en_name": "Pikachu",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "type": "⚡ 전기 타입",
        "feature": "상대방을 기분 좋게 스파크 시키는 인간 백구 스타일",
        "reason": "밝고 호기심이 많아 주변에 항상 긍정적인 파동을 뿜어냅니다.<br>누구와도 단숨에 친해지는 신비로운 매력을 가지고 있으며 늘 새로운 모험을 꿈꿉니다."
    },
    "ENTP": {
        "ko_name": "팬텀",
        "en_name": "Gengar",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "type": "👻 고스트 / ☠️ 독 타입",
        "feature": "어디서 튈지 모르는 신출귀몰한 장난꾸러기 창의왕",
        "reason": "재치 있고 장난기 넘치며 독창적인 아이디어가 끊임없이 샘솟습니다.<br>틀에 갇히는 것을 안 좋아하며 통통 튀는 사고로 늘 흥미진진한 무대를 만듭니다."
    },
    "ESTJ": {
        "ko_name": "괴력몬",
        "en_name": "Machamp",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/68.png",
        "type": "🥊 격투 타입",
        "feature": "4개의 팔로 모든 과업을 단숨에 끝내는 지도자",
        "reason": "체계적이고 리더십이 뛰어나며 현실적인 문제를 지혜롭게 풀어냅니다.<br>명확한 목적의식과 강력한 실행력으로 자신이 맡은 팀을 확실하게 끌어줍니다."
    },
    "ESFJ": {
        "ko_name": "라이츄",
        "en_name": "Raichu",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png",
        "type": "⚡ 전기 타입",
        "feature": "주변을 화사하게 케어해주는 인싸 포켓몬",
        "reason": "친절하고 사교적이며 주변 이들을 세심하게 살피는 따뜻한 마음씨를 지녔습니다.<br>정이 많아 공동체의 화합을 도모하며 에너지를 공유할 때 가장 빛납니다."
    },
    "ENFJ": {
        "ko_name": "망나뇽",
        "en_name": "Dragonite",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png",
        "type": "🐉 드래곤 / 🕊️ 비행 타입",
        "feature": "바다를 건너 거친 풍랑 속에서도 사람을 구하는 온화한 영웅",
        "reason": "온화하고 다정한 품성으로 다른 사람들의 가능성을 끌어내어 주는 리더입니다.<br>타인의 아픔에 깊이 공감하며 선한 영향력을 펼치는 따뜻한 매력이 있습니다."
    },
    "ENTJ": {
        "ko_name": "리자몽",
        "en_name": "Charizard",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "type": "🔥 불꽃 / 🕊️ 비행 타입",
        "feature": "뜨거운 불꽃으로 장애물을 태워버리는 강력한 사령관",
        "reason": "강렬한 열정과 비전을 품고 담대하게 나아가는 카리스마의 소유자입니다.<br>어려운 장애물도 특유의 결단력과 거침없는 도전 정신으로 가뿐히 파쇄해 버립니다."
    }
}

# 4. 헤더 레이아웃
st.markdown("<div class='main-title'>⚡ MBTI 단짝 포켓몬 찾기 ⚡</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당신의 성격 유형과 꼭 닮은 포켓몬을 만나보세요!</div>", unsafe_allow_html=True)

# 5. MBTI 선택창
selected_mbti = st.selectbox(
    "👇 당신의 MBTI를 선택해 주세요",
    options=list(POKEMON_DATA.keys()),
    index=10 # 기본 선택값: ENFP
)

# 6. 매칭 결과 출력 버튼
if st.button("내 단짝 포켓몬 확인하기 🔍", use_container_width=True, type="primary"):
    # 축하 효과 (풍선 팡팡)
    st.balloons()
    
    data = POKEMON_DATA[selected_mbti]
    
    # 결과 화면 레이아웃
    st.markdown(f"""
        <div class="pokemon-card">
            <div style="text-align: center;">
                <span style="background-color: #FEF3C7; color: #B45309; font-weight: bold; padding: 6px 16px; border-radius: 20px; font-size: 1.1rem;">
                    {selected_mbti} 대표 포켓몬
                </span>
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <div class="pokemon-name">{data['ko_name']}</div>
                <div class="pokemon-meta">{data['en_name']} | {data['type']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2열 컬럼 레이아웃 (이미지 + 특징)
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.image(data['image'], use_container_width=True)
        
    with col2:
        st.markdown(f"### 🌟 주요 특징")
        st.write(f"**{data['feature']}**")
        
        st.markdown(f"""
            <div class="reason-box">
                <b>💡 어울리는 이유</b><br>
                {data['reason']}
            </div>
        """, unsafe_allow_html=True)

# 하단 안내 메시지
st.markdown("<br><hr style='border: 1px dashed #FCD34D;'><p style='text-align: center; color: #9CA3AF;'>제작: MBTI Pokemon Finder</p>", unsafe_allow_html=True)
