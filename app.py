import streamlit as st
import requests

# إعداد واجهة الصفحة
st.set_page_config(page_title="مُصحّح اللغة العربية للناطقين بغيرها", layout="centered")

st.title("مُصحّح ومُشكّل اللغة العربية")
st.write("أداة تعليمية للطلبة غير الناطقين بالعربية لتشكيل النصوص وتصحيح الأخطاء النحوية مع الشرح الإعرابي.")

# جلب المفتاح من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("يرجى إضافة GEMINI_API_KEY في ملف Secrets في Streamlit Cloud.")
    st.stop()

# إدارة حالة النص
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

# صندوق إدخال النص
input_text = st.text_area(
    label="أدخل النص العربي هنا (حتى 150 كلمة):",
    value=st.session_state.user_text,
    height=200,
    max_chars=1000,
    key="text_input_area"
)

col1, col2 = st.columns([1, 1])

with col1:
    btn_process = st.button("تشكيل النص وتصويبه", type="primary", use_container_width=True)

with col2:
    btn_clear = st.button("حذف النص", use_container_width=True)

if btn_clear:
    st.session_state.user_text = ""
    st.rerun()

if btn_process:
    if not input_text.strip():
        st.warning("يرجى إدخال نص أولاً.")
    else:
        prompt = f"""
أنت معلم لغة عربية متمرس لغير الناطقين بها.
قم بالمهام التالية للنص المرفق:

1. أعد كتابة النص كاملاً مع **التشكيل التام** وضبط أواخر الكلمات.
2. إذا كان هناك **خطأ نحوي أو إملائي**، قم بتصحيحه واجعل الكلمة المصححة باللون الأحمر باستخدام تنسيق HTML كالتالي:
   `<span style="color: red; font-weight: bold;">الكلمة_المصححة</span>`.
3. أسفل النص المُشكّل والمُصحّح، أورد جدولاً أو نقاطاً واضحة توضح:
   - الكلمة الخطأ (التي أدخلها الطالب).
   - التصويب الصحيح.
   - سبب الخطأ النحوي بأسلوب سهل يناسب الطلاب غير الناطقين بالعربية.
   - الإعراب التفصيلي للكلمة الصحيحة في موقعها من الجملة.

إذا لم تكن هناك أخطاء، اشكر الطالب واكتفِ بتقديم النص مشكولاً شكلاً تاماً.

النص المطلوب معالجته:
"{input_text}"
"""
        with st.spinner("جاري تشكيل النص وتحليله نحويًا..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
                
                response = requests.post(url, json=payload, headers=headers)
                result = response.json()
                
                if response.status_code == 200:
                    output_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("---")
                    st.subheader("النتيجة والتصويب:")
                    st.markdown(output_text, unsafe_allow_html=True)
                else:
                    st.error(f"خطأ من API: {result.get('error', {}).get('message', 'حدث خطأ غير معروف')}")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
