import streamlit as st
import requests

# إعداد واجهة الصفحة
st.set_page_config(
    page_title="مُصحّح اللغة العربية للناطقين بغيرها",
    layout="centered"
)
import streamlit as st

# 1. ضبط إعدادات الصفحة
st.set_page_config(
    page_title="تطبيق اللسانيات الذكي",
    page_icon="📖",
    layout="centered"
)

# 2. حقن التنسيقات (CSS Custom Styling)
custom_css = """
<style>
    /* خلفية التطبيق العامة */
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* جعل حاوية المحتوى الرئيسية تشبه البطاقة البيضاء (Card) */
    .main .block-container {
        background-color: #ffffff;
        padding: 40px 30px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        max-width: 550px;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    
    /* تنسيق العناوين */
    h1 {
        color: #1e293b !important;
        text-align: center;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* تنسيق أزرار Streamlit لتشبه أزرار الواجهة */
    div.stButton > button {
        width: 100%;
        background-color: #f8fafc;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 20px;
        font-size: 1.05rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    /* تأثير التحويم عند مرور الماوس على الأزرار */
    div.stButton > button:hover {
        background-color: #ff4b4b;
        color: #ffffff;
        border-color: #ff4b4b;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25);
    }
    
    /* تنسيق مربع إدخال النصوص (Text Area / Text Input) */
    div.stTextArea textarea, div.stTextInput input {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background-color: #f8fafc;
    }
    
    /* إخفاء شريط Streamlit المزدحم في الأعلى والأسفل لمظهر أنظف */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# تطبيق الـ CSS
st.markdown(custom_css, unsafe_allow_html=True)


# --- يمكنك الآن كتابة منطق تطبيقك كالمعتاد ---
st.title("تطبيق التشكيل اللغوي")
text_input = st.text_area("أدخل النص المراد معالجته:")

if st.button("بدء المعالجة"):
    st.success("تمت المعالجة بنجاح!")

st.title("مُصحّح ومُشكّل اللغة العربية")

st.write(
    "أداة تعليمية للطلبة الناطقين بغير العربية لتشكيل النصوص "
    "وتصحيح الأخطاء النحوية مع الشرح الإعرابي."
)

# جلب المفتاح من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "يرجى إضافة GEMINI_API_KEY في ملف Secrets في Streamlit Cloud."
    )
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


# الأزرار
col1, col2 = st.columns([1, 1])

with col1:
    btn_process = st.button(
        "تشكيل النص وتصويبه",
        type="primary",
        use_container_width=True
    )

with col2:
    btn_clear = st.button(
        "حذف النص",
        use_container_width=True
    )


# زر حذف النص
if btn_clear:
    st.session_state.user_text = ""
    st.rerun()


# زر تشكيل وتصحيح النص
if btn_process:

    if not input_text.strip():

        st.warning("يرجى إدخال نص أولاً.")

    else:

        prompt = f"""
أنت معلم لغة عربية متمرس ومتخصص في تعليم اللغة العربية
للناطقين بغيرها.

قم بتحليل النص العربي المرفق وتنفيذ المهام التالية بدقة:

1. أعد كتابة النص كاملاً مع التشكيل التام، بما في ذلك ضبط
   أواخر الكلمات ضبطًا نحويًا صحيحًا.

2. صحح الأخطاء النحوية والإملائية الموجودة في النص.

3. عند وجود كلمة خاطئة، اعرض الكلمة الصحيحة باللون الأحمر
   باستخدام HTML بهذا الشكل تمامًا:

<span style="color: red; font-weight: bold;">الكلمة الصحيحة</span>

4. بعد النص المصحح والمشكل، أنشئ قسمًا بعنوان:

"الأخطاء والتصويبات"

واذكر فيه لكل خطأ:

- الكلمة أو العبارة التي كتبها الطالب.
- التصويب الصحيح.
- نوع الخطأ: نحوي أو إملائي أو صرفي أو غير ذلك.
- سبب الخطأ بأسلوب بسيط وواضح يناسب الطالب غير الناطق بالعربية.
- الإعراب التفصيلي للكلمة الصحيحة في سياق الجملة.

5. إذا كان النص صحيحًا نحويًا وإملائيًا، فلا تخترع أخطاء.
   اذكر أن النص صحيح، ثم قدم النص مشكولًا تشكيلًا تامًا.

6. حافظ على معنى النص الأصلي ولا تضف جملًا أو أفكارًا جديدة.

7. لا تحذف أي جزء من النص الأصلي إلا إذا كان الحذف ضروريًا
   لتصحيح خطأ واضح.

النص المطلوب معالجته:

{input_text}
"""

        with st.spinner("جاري تشكيل النص وتحليله نحويًا..."):

            try:

                # نموذج Gemini الحالي
                url = (
                    "https://generativelanguage.googleapis.com/"
                    "v1beta/models/gemini-3.6-flash:generateContent"
                    f"?key={api_key}"
                )

                headers = {
                    "Content-Type": "application/json"
                }

                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                }

                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=120
                )

                result = response.json()

                # نجاح الطلب
                if response.status_code == 200:

                    try:
                        output_text = (
                            result["candidates"][0]
                            ["content"]["parts"][0]["text"]
                        )

                        st.markdown("---")

                        st.subheader("النتيجة والتصويب:")

                        st.markdown(
                            output_text,
                            unsafe_allow_html=True
                        )

                    except (KeyError, IndexError, TypeError):

                        st.error(
                            "تم الاتصال بـ Gemini بنجاح، "
                            "لكن لم يتم العثور على نص في الاستجابة."
                        )

                        st.code(
                            str(result),
                            language="text"
                        )

                # خطأ من API
                else:

                    error_message = (
                        result
                        .get("error", {})
                        .get(
                            "message",
                            "حدث خطأ غير معروف من Gemini API."
                        )
                    )

                    st.error(
                        f"خطأ من Gemini API:\n\n{error_message}"
                    )

            except requests.exceptions.Timeout:

                st.error(
                    "انتهت مهلة الاتصال بالخدمة. "
                    "يرجى المحاولة مرة أخرى."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"حدث خطأ أثناء الاتصال بالخدمة:\n\n{e}"
                )

            except Exception as e:

                st.error(
                    f"حدث خطأ غير متوقع:\n\n{e}"
             )
# الفوتر في أسفل الصفحة
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666666; font-size: 14px; padding: 10px;">
        تطوير د. عمر الرواجفة © مختبر اللسانيات الحاسوبية وتحليل الخطاب
    </div>
    """,
    unsafe_allow_html=True
)
