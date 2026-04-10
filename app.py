import streamlit as st
import pandas as pd

file = "data.xlsx"

# -------- LOAD DATA --------
def load_data(sheet):
    return pd.read_excel(file, sheet_name=sheet)

def save_data(df, sheet):
    with pd.ExcelWriter(file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet, index=False)

users = load_data("users")
projects = load_data("projects")
applications = load_data("applications")
reviews = load_data("reviews")
chat = load_data("chat")

# -------- SESSION --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LOGIN --------
if not st.session_state.logged_in:
    st.title("🔐 Student Marketplace Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users[(users["name"] == username) & (users["password"] == password)]

        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.user_id = int(user.iloc[0]["user_id"])
            st.session_state.role = user.iloc[0]["role"]
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")
    st.stop()

# -------- MAIN UI --------
st.title("🎓 Freelancer Marketplace for Students")

menu = st.sidebar.selectbox("Menu", [
    "View Projects",
    "Post Project",
    "Apply",
    "Manage Applications",
    "Reviews",
    "Chat",
    "Dashboard",
    "Logout"
])

# -------- VIEW PROJECTS --------
if menu == "View Projects":
    st.subheader("📋 Available Projects")
    st.dataframe(projects)

# -------- POST PROJECT --------
elif menu == "Post Project":
    st.subheader("📤 Post New Project")

    title = st.text_input("Project Title")
    desc = st.text_area("Description")
    budget = st.number_input("Budget")

    if st.button("Post Project"):
        new_id = len(projects) + 1
        new_data = pd.DataFrame(
            [[new_id, title, desc, budget, st.session_state.user_id]],
            columns=projects.columns
        )

        projects = pd.concat([projects, new_data])
        save_data(projects, "projects")

        st.success("Project Posted Successfully 🎉")

# -------- APPLY --------
elif menu == "Apply":
    st.subheader("📝 Apply for Project")

    st.dataframe(projects)

    project_id = st.number_input("Enter Project ID")

    if st.button("Apply Now"):
        new_id = len(applications) + 1
        new_app = pd.DataFrame(
            [[new_id, project_id, st.session_state.user_id, "Pending"]],
            columns=applications.columns
        )

        applications = pd.concat([applications, new_app])
        save_data(applications, "applications")

        st.success("Application Submitted ✅")

# -------- MANAGE APPLICATIONS --------
elif menu == "Manage Applications":
    st.subheader("✅ Manage Applications")

    st.dataframe(applications)

    app_id = st.number_input("Application ID")
    action = st.selectbox("Select Action", ["Accept", "Reject"])

    if st.button("Update Status"):
        applications.loc[applications["app_id"] == app_id, "status"] = action
        save_data(applications, "applications")

        st.success("Status Updated 🔄")

# -------- REVIEWS --------
elif menu == "Reviews":
    st.subheader("⭐ Reviews & Ratings")

    st.dataframe(reviews)

    project_id = st.number_input("Project ID")
    rating = st.slider("Rating", 1, 5)
    comment = st.text_area("Write Review")

    if st.button("Submit Review"):
        new_id = len(reviews) + 1
        new_review = pd.DataFrame(
            [[new_id, project_id, st.session_state.user_id, rating, comment]],
            columns=reviews.columns
        )

        reviews = pd.concat([reviews, new_review])
        save_data(reviews, "reviews")

        st.success("Review Submitted ⭐")

# -------- CHAT --------
elif menu == "Chat":
    st.subheader("💬 Chat System")

    st.dataframe(chat)

    receiver_id = st.number_input("Send To User ID")
    message = st.text_input("Enter Message")

    if st.button("Send Message"):
        new_id = len(chat) + 1
        new_msg = pd.DataFrame(
            [[new_id, st.session_state.user_id, receiver_id, message]],
            columns=chat.columns
        )

        chat = pd.concat([chat, new_msg])
        save_data(chat, "chat")

        st.success("Message Sent 📩")

# -------- DASHBOARD --------
elif menu == "Dashboard":
    st.subheader("📊 Dashboard")

    st.write("Total Users:", len(users))
    st.write("Total Projects:", len(projects))
    st.write("Total Applications:", len(applications))

    st.subheader("Projects per User")
    st.bar_chart(projects["posted_by"].value_counts())

    st.subheader("Application Status")
    st.bar_chart(applications["status"].value_counts())

# -------- LOGOUT --------
elif menu == "Logout":
    st.session_state.logged_in = False
    st.rerun()