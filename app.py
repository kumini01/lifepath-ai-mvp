import datetime as dt
import streamlit as st
import db
from ai_service import ask_life_coach

db.init_db()
st.set_page_config(page_title='LifePath AI', page_icon='🧭', layout='wide')
st.title('🧭 LifePath AI')
st.caption('AI 기반 개인 생애주기 통합관리 플랫폼 · MVP v0.1')

menu = st.sidebar.radio('메뉴', ['Dashboard','My Life','To-Do','가족','AI Life Coach','설정'])
profile = db.get_profile(); events = db.get_events(); todos = db.get_todos()

if menu == 'Dashboard':
    st.header('Life Dashboard')
    c1,c2,c3 = st.columns(3)
    c1.metric('생애 이벤트', len(events)); c2.metric('미완료 To-Do', sum(not x['done'] for x in todos)); c3.metric('가족 구성원', len(db.get_family()))
    if profile: st.info(f"{profile['name']}님의 현재 직업 상태: {profile['job_status']} · 관심영역: {profile['interests']}")
    else: st.warning('설정에서 프로필을 먼저 등록해 주세요.')
    st.subheader('최근 생애 이벤트')
    for x in events[:5]: st.write(f"**{x['event_date'] or '-'} · {x['category']}** — {x['title']}")
    st.subheader('지금 해야 할 일')
    for x in [t for t in todos if not t['done']][:5]: st.write(f"☐ {x['title']} · {x['due_date'] or '기한 없음'}")

elif menu == 'My Life':
    st.header('My Life Timeline')
    with st.form('event'):
        category=st.selectbox('영역',['교육','경력','가족','주거','자산','건강','노후','기타']); title=st.text_input('이벤트'); date=st.date_input('날짜'); memo=st.text_area('메모')
        if st.form_submit_button('등록') and title: db.add_event(category,title,str(date),memo); st.rerun()
    for x in events:
        with st.expander(f"{x['event_date'] or '-'} | {x['category']} | {x['title']}"):
            st.write(x['memo'] or '메모 없음')
            if st.button('삭제', key=f"e{x['id']}"): db.delete_event(x['id']); st.rerun()

elif menu == 'To-Do':
    st.header('일정 · To-Do')
    with st.form('todo'):
        title=st.text_input('할 일'); due=st.date_input('마감일', value=dt.date.today())
        if st.form_submit_button('추가') and title: db.add_todo(title,str(due)); st.rerun()
    for x in todos:
        checked=st.checkbox(f"{x['title']} · {x['due_date'] or '-'}", value=bool(x['done']), key=f"t{x['id']}")
        if checked != bool(x['done']): db.set_todo(x['id'],checked); st.rerun()

elif menu == '가족':
    st.header('가족 관리')
    with st.form('family'):
        name=st.text_input('이름'); relation=st.text_input('관계'); birth=st.number_input('출생연도',1900,2100,2000)
        if st.form_submit_button('등록') and name: db.add_family(name,relation,birth); st.rerun()
    for x in db.get_family(): st.write(f"👤 **{x['name']}** · {x['relation'] or '-'} · {x['birth_year']}년")

elif menu == 'AI Life Coach':
    st.header('🤖 AI Life Coach')
    api_key=st.text_input('OpenAI API Key', type='password', help='키는 DB에 저장하지 않습니다.')
    question=st.text_area('무엇을 준비해야 할지 AI에게 물어보세요.')
    if st.button('상담하기'):
        if not api_key or not question: st.warning('API Key와 질문을 입력해 주세요.')
        else:
            try:
                with st.spinner('생애 정보를 분석하고 있습니다...'): st.write(ask_life_coach(api_key,question,profile,events,todos))
            except Exception as e: st.error(f'AI 호출 중 오류가 발생했습니다: {e}')

else:
    st.header('설정 · 프로필')
    p=profile or {'name':'','birth_year':1980,'job_status':'','interests':''}
    with st.form('profile'):
        name=st.text_input('이름',p['name'] or ''); birth=st.number_input('출생연도',1900,2100,int(p['birth_year'] or 1980)); job=st.text_input('직업/상태',p['job_status'] or ''); interests=st.text_input('관심 생애영역',p['interests'] or '', placeholder='예: 경력, 자산, 노후')
        if st.form_submit_button('저장'): db.save_profile(name,birth,job,interests); st.success('저장했습니다.'); st.rerun()
