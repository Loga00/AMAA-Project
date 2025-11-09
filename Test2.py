
import streamlit as st
import pandas as pd
import bcrypt
import os

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="Tableau Login", page_icon="📊", layout="wide")

# ---------- إعداد مسار ملف المستخدمين ----------
FILE_PATH = "users.xlsx"

# ---------- بيانات المستخدم الافتراضي ----------
DEFAULT_USER = {
    "username": "asmaa25899@gmail.com",
    "password": "asmaa25899"
}

# ---------- دالة لتشفير الباسورد ----------
def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# ---------- إنشاء الملف لو مش موجود ----------
if not os.path.exists(FILE_PATH):
    hashed = hash_password(DEFAULT_USER["password"])
    df = pd.DataFrame({
        "username": [DEFAULT_USER["username"]],
        "password": [hashed]
    })
    df.to_excel(FILE_PATH, index=False)

# ---------- تحميل بيانات المستخدمين ----------
users_df = pd.read_excel(FILE_PATH)

# ---------- دالة حفظ المستخدمين ----------
def save_users(df):
    df.to_excel(FILE_PATH, index=False)

# ---------- دالة التحقق ----------
def verify_user(username, password):
    global users_df
    user = users_df[users_df["username"] == username]

    if not user.empty:
        stored_hash = user["password"].values[0]

        # معالجة أي قيمة غير نصية أو NaN
        if not isinstance(stored_hash, str) or stored_hash.strip() == "" or str(stored_hash).lower() == "nan":
            st.error("⚠️ كلمة المرور المخزنة غير صالحة. أعد إنشاء الحساب.")
            return False

        try:
            stored_hash = stored_hash.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception as e:
            st.error(f"حدث خطأ أثناء التحقق من كلمة المرور: {e}")
            return False

    return False

# ---------- دالة إضافة مستخدم ----------
def add_user(username, password):
    global users_df
    hashed = hash_password(password)
    new_user = pd.DataFrame({"username": [username], "password": [hashed]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)

# ---------- حالة الجلسة ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

# ---------- واجهة تسجيل الدخول ----------
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول إلى لوحة Tableau")

    option = st.sidebar.selectbox("اختر الإجراء", ["تسجيل الدخول", "إنشاء حساب جديد"])

    if option == "تسجيل الدخول":
        username = st.text_input("👤 اسم المستخدم أو الإيميل")
        password = st.text_input("🔑 كلمة المرور", type="password")
        if st.button("تسجيل الدخول"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ تم تسجيل الدخول بنجاح")
                st.rerun()

            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

    elif option == "إنشاء حساب جديد":
        new_user = st.text_input("👤 اسم المستخدم الجديد (أو الإيميل)")
        new_pass = st.text_input("🔑 كلمة المرور الجديدة", type="password")
        if st.button("إنشاء الحساب"):
            if new_user in users_df["username"].values:
                st.error("⚠️ هذا الاسم مستخدم بالفعل. اختر اسمًا آخر.")
            else:
                add_user(new_user, new_pass)
                st.success("🎉 تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")

# ---------- واجهة Tableau بعد الدخول ----------
else:
    st.sidebar.success(f"مرحبًا {st.session_state.username} 👋")
    if st.sidebar.button("🔓 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.show_dashboard = False
        st.rerun()


    st.title("📊 Tableau Dashboard")

    if not st.session_state.show_dashboard:
        st.markdown("""
        <div style="text-align:center; font-size:18px; margin-bottom:20px;">
            ✅ تم تسجيل الدخول بنجاح<br>
            اضغط على الزر أدناه لعرض لوحة Tableau الخاصة بك.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 عرض الداشبورد"):
            st.session_state.show_dashboard = True
            st.rerun()


    else:
        # tableau_url = "https://public.tableau.com/views/FinalPoject_3/Dashboard2?:language=en-US&:display_count=n&:origin=viz_share_link"
        # st.components.v1.iframe(tableau_url, width=1200, height=750)

        # st.info("🔹 يمكنك التمرير أو التكبير داخل لوحة Tableau.")

    #    tableau_url = "https://public.tableau.com/views/task2Tableau/Dashboard1"
    #    st.components.v1.iframe(tableau_url, width=1200, height=750)
    #    st.info("🔹 يمكنك التمرير أو التكبير داخل لوحة Tableau.")

        tableau_embed_url = "https://public.tableau.com/views/task2Tableau/TotalSalesToEachRegion?:showVizHome=no&:embed=true"
        st.components.v1.iframe(tableau_embed_url, width=1200, height=750)
        st.info("🔹 يمكنك التمرير أو التكبير داخل لوحة Tableau.")
