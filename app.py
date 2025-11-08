import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DB Setup
conn = sqlite3.connect("room_bookings.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    room TEXT,
    date TEXT,
    timeslot TEXT
)
""")
conn.commit()

# Room list from your timetable PDF
ROOMS = [
    "PB-FF1","PB-FF2","PB-FF3","PB-FF4","PB-FF5","PB-FF6",
    "PB-GF1","PB-GF2","PB-GF3","PB-GF4","PB-GF5","PB-GF6",
    "SPS5","SPS6","SPS7","SPS8","CS LAB","DBMS LAB","ML LAB","WATER LAB"
]

st.title("🎓 AI Room Booking System")

name = st.text_input("Enter Name")
role = st.selectbox("Role", ["Professor", "Student"])
date = st.date_input("Select Date")
timeslot = st.selectbox("Select Time Slot", 
            ["8-9","9-10","10-11","11-12","12-1","1-2","2-3","3-4","4-5","5-6"])

if st.button("Check Available Rooms"):

    c.execute("SELECT room FROM bookings WHERE date=? AND timeslot=?", (str(date), timeslot))
    booked_rooms = [r[0] for r in c.fetchall()]

    free_rooms = [room for room in ROOMS if room not in booked_rooms]

    if not free_rooms:
        st.error("❌ No rooms available at this time!")
    else:
        st.success(f"✅ Available Rooms: {', '.join(free_rooms)}")

        # AI Suggestion
        prompt = f"Suggest the best classroom from this list based on availability: {free_rooms}"

        ai_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.info("🤖 AI Suggestion: " + ai_response.choices[0].message.content)

        selected_room = st.selectbox("Select Room to Book", free_rooms)

        if st.button("Confirm Booking"):
            c.execute("INSERT INTO bookings(name, role, room, date, timeslot) VALUES(?,?,?,?,?)",
                      (name, role, selected_room, str(date), timeslot))
            conn.commit()
            st.balloons()
            st.success(f"🎉 Room {selected_room} successfully booked!")
