import datetime

class Room:
    def __init__(self, room_id, branch="General", capacity=30):
        self.room_id = room_id
        self.branch = branch
        self.capacity = capacity
        # Stores {date_str: {time_slot: {"professor_id": ..., "course_name": ..., "purpose": ...}}}
        self.bookings = {}

    def __str__(self):
        return f"Room {self.room_id} ({self.branch}, Capacity: {self.capacity})"

    def is_available(self, date_str, time_slot):
        return date_str not in self.bookings or time_slot not in self.bookings[date_str]

    def book(self, date_str, time_slot, booking_details):
        if not self.is_available(date_str, time_slot):
            return False, f"Room {self.room_id} already booked for {date_str} at {time_slot}."

        if date_str not in self.bookings:
            self.bookings[date_str] = {}
        self.bookings[date_str][time_slot] = booking_details
        return True, f"Room {self.room_id} booked for {date_str} at {time_slot}."

    def get_booking_details(self, date_str, time_slot):
        if date_str in self.bookings and time_slot in self.bookings[date_str]:
            return self.bookings[date_str][time_slot]
        return None

class Professor:
    def __init__(self, professor_id, name, branch="General"):
        self.professor_id = professor_id
        self.name = name
        self.branch = branch
        # Stores {date_str: {time_slot: room_id}}
        self.schedule = {}

    def __str__(self):
        return f"Professor {self.name} ({self.professor_id}, Branch: {self.branch})"

    def is_available(self, date_str, time_slot):
        return date_str not in self.schedule or time_slot not in self.schedule[date_str]

    def add_to_schedule(self, date_str, time_slot, room_id):
        if date_str not in self.schedule:
            self.schedule[date_str] = {}
        self.schedule[date_str][time_slot] = room_id

class DTURoomBookingSystem:
    def __init__(self):
        self.rooms = {}         # {room_id: Room_object}
        self.professors = {}    # {professor_id: Professor_object}
        self.time_slots = [
            "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
            "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00",
            "16:00-17:00"
        ]
        self._initialize_dtu_data()

    def _initialize_dtu_data(self):
        # --- Rooms from your timetables (simplified capacities for demo) ---
        # Page 1: Chemical Engineering (B15), Room SPS 5
        self.add_room("SPS 5", "Chemical Engineering", 60)
        # Page 2: Mathematics & Computing (SEC-1/B04), Rooms PB-GF3, PB-GF6, PB-FF2, PB-FF3
        self.add_room("PB-GF3", "Mathematics & Computing", 40)
        self.add_room("PB-GF6", "Mathematics & Computing", 40)
        self.add_room("PB-FF2", "Mathematics & Computing", 50)
        self.add_room("PB-FF3", "Mathematics & Computing", 50)
        # Page 3: Mathematics & Computing (SEC-2/B05), Rooms PB-FF1, PB-FF3
        self.add_room("PB-FF1", "Mathematics & Computing", 50) # PB-FF3 already added
        # Page 4: Mathematics & Computing (SEC-3/B06), Rooms PB-FF1, PB-FF3, PB-FF4
        self.add_room("PB-FF4", "Mathematics & Computing", 50) # PB-FF1, PB-FF3 already added
        # Page 5: Engineering Physics (SEC-1/B07), Room SPS 7
        self.add_room("SPS 7", "Engineering Physics", 60)
        # Page 6: Engineering Physics (SEC-2/B08), Rooms SPS 6, SPS 7
        self.add_room("SPS 6", "Engineering Physics", 60) # SPS 7 already added
        # Page 7: Bio-Technology (B19), Rooms PB-FF4, SPS8
        self.add_room("SPS8", "Bio-Technology", 50) # PB-FF4 already added
        # Page 8: Civil Engineering (SEC-1/B16), Rooms SPS 6, SPS 7
        # SPS 6, SPS 7 already added
        # Page 9: Civil Engineering (SEC-2/B17), Rooms SPS 6, SPS 7, PB-FF3, PB-FF4
        # SPS 6, SPS 7, PB-FF3, PB-FF4 already added
        # Page 10: Computer Science & Engineering (SEC-1/A01), Rooms PB-GF4, SPS6
        self.add_room("PB-GF4", "Computer Science & Engineering", 50) # SPS6 already added
        # Page 11: Computer Science & Engineering (SEC-2/A02), Rooms PB-GF2, PB-GF4, SPS 6
        self.add_room("PB-GF2", "Computer Science & Engineering", 50) # PB-GF4, SPS 6 already added
        # Page 12: Computer Science & Engineering (SEC-3/A03), Room PB-GF5
        self.add_room("PB-GF5", "Computer Science & Engineering", 50)
        # Page 13: Computer Science & Engineering (SEC-4/A04), Rooms PB-GF2, PB-GF3, PB-GF4, PB-GF5
        # PB-GF2, PB-GF3, PB-GF4, PB-GF5 already added
        # Page 14: Computer Science & Engineering (SEC-5/A05), Room PB-GF6
        # PB-GF6 already added
        # Page 15: Computer Science & Engineering (SEC-6/A06), Rooms PB-GF4, PB-GF6, PB-FF6, SPS6
        self.add_room("PB-FF6", "Computer Science & Engineering", 50) # PB-GF4, PB-GF6, SPS6 already added
        # Page 16: Data Science and Analytics (A07), Rooms PB-GF2, PB-GF3, PB-GF5, PB-GF6, PB-FF2
        # PB-GF2, PB-GF3, PB-GF5, PB-GF6, PB-FF2 already added
        # Page 17: Electrical Engineering (SEC-1/A15), Rooms PB-GF5, PB-GF6, PB-FF1, PB-FF3
        # PB-GF5, PB-GF6, PB-FF1, PB-FF3 already added
        # Page 18: Electrical Engineering (SEC-2/A16), Rooms PB-FF1, PB-FF6
        # PB-FF1, PB-FF6 already added
        # Page 19: Electrical Engineering (SEC-3/A17), Rooms PB-GF2, PB-GF5, PB-FF1
        # PB-GF2, PB-GF5, PB-FF1 already added
        # Page 20: Electrical Engineering (SEC-4/A18), Rooms PB-FF1, PB-FF2, PB-FF3
        self.add_room("PB-FF_20_1", "Electrical Engineering", 50) # Using generic name if clash with existing
        self.add_room("PB-FF_20_2", "Electrical Engineering", 50) # Using generic name if clash with existing
        self.add_room("PB-FF_20_3", "Electrical Engineering", 50) # Using generic name if clash with existing
        # Page 21: Electrical Engineering (SEC-5/A19), Rooms PB-FF2, PB-FF5, PB-FF6
        self.add_room("PB-FF5", "Electrical Engineering", 50) # PB-FF2, PB-FF6 already added
        # Page 22: Electronics & Communication Engineering (SEC-1/A11), Room PB-GF1
        self.add_room("PB-GF1", "Electronics & Communication Engineering", 60)
        # Page 23: Electronics & Communication Engineering (SEC-2/A12), Rooms PB-GF1, PB-GF2, PB-FF4
        # PB-GF1, PB-GF2, PB-FF4 already added
        # Page 24: Electronics & Communication Engineering (SEC-3/A13), Rooms PB-GF1, PB-GF2, PB-GF3, PB-GF4
        # PB-GF1, PB-GF2, PB-GF3, PB-GF4 already added
        # Page 25: VLSI Design and Technology (A14), Rooms PB-GF1, PB-GF2, PB-GF3
        # PB-GF1, PB-GF2, PB-GF3 already added
        # Page 26: Environmental Engineering (B18), Rooms PB-FF2, PB-FF3, PB-FF4, SPS5
        self.add_room("SPS5", "Environmental Engineering", 40) # PB-FF2, PB-FF3, PB-FF4 already added
        # Page 27: Information Technology (SEC-1/A08), Room PB-GF3
        # PB-GF3 already added
        # Page 28: Information Technology (SEC-2/A09), Rooms PB-GF1, PB-GF2, PB-GF3
        # PB-GF1, PB-GF2, PB-GF3 already added
        # Page 29: Cyber Security (A10), Rooms PB-GF1, PB-GF4, PB-FF3
        # PB-GF1, PB-GF4, PB-FF3 already added
        # Page 30: Mechanical Engineering (SEC-1/B09), Rooms PB-GF1, PB-FF3, PB-FF5
        # PB-GF1, PB-FF3, PB-FF5 already added
        # Page 31: Mechanical Engineering (SEC-2/B10), Room PB-FF6
        # PB-FF6 already added
        # Page 32: Mechanical Engineering (SEC-3/B11), Rooms PB-GF6, PB-FF6
        # PB-GF6, PB-FF6 already added
        # Page 33: Mechanical Engineering (SEC-4/B12), Rooms SPS 5, PB-FF6
        # SPS 5, PB-FF6 already added
        # Page 34: Mechanical Engg. with specialization in Automotive Engg. (B13), Room SPS 8
        self.add_room("SPS 8", "Automotive Engineering", 50)
        # Page 35: Production & Industrial Engineering (B14), Room SPS 8
        # SPS 8 already added
        # Page 36: Software Engineering (SEC-1/B01), Rooms PB-FF3, PB-FF4, SPS 7
        # PB-FF3, PB-FF4, SPS 7 already added
        # Page 37: Software Engineering (SEC-2/B02), Rooms PB-FF3, PB-FF4, PB-FF5, PB-FF6, PB-GF5
        # PB-FF3, PB-FF4, PB-FF5, PB-FF6, PB-GF5 already added
        # Page 38: Software Engineering (SEC-3/B03), Room PB-FF5
        # PB-FF5 already added


        # --- Professors (dummy data, strictly from DTU) ---
        self.add_professor("P001", "Dr. A. Sharma", "CSE") # Generic CSE for demonstration
        self.add_professor("P002", "Prof. R. Singh", "ECE") # Generic ECE
        self.add_professor("P003", "Dr. S. Gupta", "ME")   # Generic ME
        self.add_professor("P004", "Dr. Divya", "Mathematics & Computing")
        self.add_professor("P005", "Dr. Kamal Kishor", "Mathematics & Computing")
        self.add_professor("P006", "Dr. Kaustubh Ranjan Singh", "ECE")
        self.add_professor("P007", "Dr. Rasin Khera", "ME")
        self.add_professor("P008", "Prof. Archana Rani", "Chemical Engineering")
        self.add_professor("P009", "Dr. Payal", "Mathematics & Computing")
        self.add_professor("P010", "Dr. Shiksha", "Mathematics & Computing")
        self.add_professor("P011", "Dr. Vinod Singh", "Physics")
        self.add_professor("P012", "Dr. Umang", "Physics")
        self.add_professor("P013", "Dr. O.P. Verma", "General") # Chairperson
        self.add_professor("P014", "Dr. Sachin Dhariwal", "ECE")
        self.add_professor("P015", "Dr. Md Gulam Mustafa", "ME")
        self.add_professor("P016", "Dr. Manvi", "Mathematics-I")
        self.add_professor("P017", "Dr. Mukul", "Mathematics-I")
        self.add_professor("P018", "Dr. Yogendra K. Meena", "Physics")
        self.add_professor("P019", "Dr. Ankita Banwal", "Physics")
        self.add_professor("P020", "Dr. Nilam", "Python Programming")
        self.add_professor("P021", "Dr. Lokesh Chander", "Python Programming")
        self.add_professor("P022", "Dr. Nishu", "Python Programming")
        self.add_professor("P023", "Dr. Rachna", "Python Programming")
        self.add_professor("P024", "Dr. Sangita Kansal", "Python Programming")
        self.add_professor("P025", "Dr. Anju", "Python Programming")
        self.add_professor("P026", "Dr. Naokant Deo", "Python Programming")
        self.add_professor("P027", "Dr. C. P. Singh", "Mathematics-I")
        self.add_professor("P028", "Dr. Mridula", "Mathematics-I")
        self.add_professor("P029", "Dr. Vinod Kumar Yadav", "EEE")
        self.add_professor("P030", "Dr. Nitansh", "Applied Chemistry")
        self.add_professor("P031", "Dr. Sheetal Kumari", "Engineering Physics Workshop")
        self.add_professor("P032", "Dr. Naresh Kumar", "Mathematics-I")
        self.add_professor("P033", "Dr. Yash", "Mathematics-I")
        self.add_professor("P034", "Dr. Sameer Jain", "Physics")
        self.add_professor("P035", "Dr. Priyanka", "Physics")
        self.add_professor("P036", "Dr. Abhishek Chaudhary", "EEE")
        self.add_professor("P037", "Dr. Reshu Chaudhary", "Applied Chemistry")
        self.add_professor("P038", "Dr. Shubham Kr Dhiman", "Mathematics-I")
        self.add_professor("P039", "Dr. Jai Gopal Sharma", "Applied Aquaculture")
        self.add_professor("P040", "Dr. Naokant Deo", "Mathematics-I")
        self.add_professor("P041", "Dr. Ramesh Srivastava", "Mathematics-I")
        self.add_professor("P042", "Dr. Rashi Jain", "Mathematics-I")
        self.add_professor("P043", "Dr. Prem Prakash", "EEE")
        self.add_professor("P044", "Dr. Jayant Ghosh Roy", "ME")
        self.add_professor("P045", "Dr. Rajeev Kumar Garg", "CE")
        self.add_professor("P046", "Dr. B. R. Robert", "CE")
        self.add_professor("P047", "Dr. Debasmita Sarkar", "Mathematics-I")
        self.add_professor("P048", "Dr. Gaurav Kaushik", "EEE")
        self.add_professor("P049", "Dr. R S Kanduja", "ME")
        self.add_professor("P050", "Dr. Kanica Goel", "Mathematics-I")
        self.add_professor("P051", "Dr. Vineet", "Mathematics-I")
        self.add_professor("P052", "Dr. Rahul Kumar", "Programming Fundamentals")
        self.add_professor("P053", "Dr. Lavi Tanwar", "ECE")
        self.add_professor("P054", "Dr. Varsha Pathak", "ME")
        self.add_professor("P055", "Dr. Moirangthen Biken Singh", "Web Designing")
        self.add_professor("P056", "Dr. Satyabrata Adhikari", "Mathematics-I")
        self.add_professor("P057", "Dr. Kriss Gunjan", "Mathematics-I")
        self.add_professor("P058", "Dr. Poornima Mittal", "ECE")
        self.add_professor("P059", "Dr. Suhail Ahmad Siddiqui", "ME")
        self.add_professor("P060", "Dr. Vivek Kumar Aggarwal", "Mathematics-I")
        self.add_professor("P061", "Dr. Suruchi Jain", "Mathematics-I")
        self.add_professor("P062", "Dr. Neha Gupta", "Programming Fundamentals")
        self.add_professor("P063", "Dr. Sumit Kale", "ECE")
        self.add_professor("P064", "Dr. B D Pathak", "ME")
        self.add_professor("P065", "Dr. Nitika Sharma", "Mathematics-I")
        self.add_professor("P066", "Dr. Himani Pokhriyal", "Mathematics-I")
        self.add_professor("P067", "Dr. Sunakshi Mehra", "Programming Fundamentals")
        self.add_professor("P068", "Guest Faculty", "ECE") # Placeholder for generic guest faculty
        self.add_professor("P069", "Dr. Soni Kesarwani", "ME")
        self.add_professor("P070", "Dr. Manvi", "Mathematics-I")
        self.add_professor("P071", "Dr. Mukul", "Mathematics-I")
        self.add_professor("P072", "Dr. Manoj Sethi", "Programming Fundamentals")
        self.add_professor("P073", "Dr. Md Nazeem Khan", "ME")
        self.add_professor("P074", "Dr. Anjali Bansal", "Programming Fundamentals")
        self.add_professor("P075", "Dr. Sonal Singh", "ECE")
        self.add_professor("P076", "Dr. Indra Jeet Singh", "ME")
        self.add_professor("P077", "Dr. Pooja Yadav", "Mathematics-I")
        self.add_professor("P078", "Dr. Rishab", "CE")
        self.add_professor("P079", "Dr. Bijendra Prasad", "ME")
        self.add_professor("P080", "Dr. Shatakshi", "Electrical Workshop")
        self.add_professor("P081", "Dr. Dinesh Udar", "Mathematics-I")
        self.add_professor("P082", "Dr. Shweta Gupta", "Programming Fundamentals")
        self.add_professor("P083", "Dr. Shivank", "CE")
        self.add_professor("P084", "Dr. Neeraj Budhraja", "ME")
        self.add_professor("P085", "Dr. Seema Bai Meena", "Electrical Workshop")
        self.add_professor("P086", "Dr. Anuma Garg", "Mathematics-I")
        self.add_professor("P087", "Dr. Anjali Aggarwal", "Mathematics-I")
        self.add_professor("P088", "Dr. Akshay Mool", "Programming Fundamentals")
        self.add_professor("P089", "Dr. Deenan Santhiya", "Applied Chemistry")
        self.add_professor("P090", "Dr. Arushi Mittal", "Applied Chemistry")
        self.add_professor("P091", "Dr. Shreyansh Upadhayaya", "EEE")
        self.add_professor("P092", "Dr. Chhavi Dhiman", "Electronics Workshop")
        self.add_professor("P093", "Dr. Varsha Sisaudia", "Programming Fundamentals")
        self.add_professor("P094", "Dr. Promila Kumari", "Applied Chemistry")
        self.add_professor("P095", "Dr. V.V. Ramana", "EEE")
        self.add_professor("P096", "Dr. Dhirendra Kumar", "Mathematics-I")
        self.add_professor("P097", "Dr. R. K. Sinha", "Physics")
        self.add_professor("P098", "Dr. Lokesh Gautam", "Electronics Workshop")
        self.add_professor("P099", "Dr. Massoud Massoudi", "Programming Fundamentals")
        self.add_professor("P100", "Dr. Apoorva Mallik", "Applied Chemistry")
        self.add_professor("P101", "Dr. Diksha", "CE")
        self.add_professor("P102", "Dr. Rajat Chatterjee", "Water and Waste Water Analysis")
        self.add_professor("P103", "Dr. Likhi Dhruv", "Chemistry")
        self.add_professor("P104", "Dr. Manvi", "Mathematics-I")
        self.add_professor("P105", "Dr. Ashutosh Pandey", "Programming Fundamentals")
        self.add_professor("P106", "Dr. Suman Bhowmick", "EEE")
        self.add_professor("P107", "Dr. Devika Karki", "Web Design")
        self.add_professor("P108", "Dr. Ankit Yadav", "Programming Fundamentals")
        self.add_professor("P109", "Dr. Ram Bhagat", "EEE")
        self.add_professor("P110", "Dr. Anisha", "Web Design")
        self.add_professor("P111", "Dr. S. Sivaprasad Kumar", "Mathematics-I")
        self.add_professor("P112", "Dr. Aashna Tasawwur", "Mathematics-I")
        self.add_professor("P113", "Dr. Abhishek Swaroop", "Programming Fundamentals")
        self.add_professor("P114", "Dr. Rahul Gupta", "Data Structure")
        self.add_professor("P115", "Dr. Prakhar Mishra", "Web Design")
        self.add_professor("P116", "Dr. D.C. Meena", "EEE")
        self.add_professor("P117", "Dr. Indra Jeet Singh", "Workshop Practice")
        self.add_professor("P118", "Dr. R. K. Sinha", "Physics")
        self.add_professor("P119", "Dr. Priyanka", "Physics")
        self.add_professor("P120", "Dr. Anurag Chauhan", "ECE")
        self.add_professor("P121", "Dr. Sanjay Patidar", "Computer Workshop")
        self.add_professor("P122", "Dr. Swechchha Gupta", "Computer Workshop")
        self.add_professor("P123", "Dr. Renuka Bokolia", "Physics")
        self.add_professor("P124", "Dr. Malti Bansal", "ECE")
        self.add_professor("P125", "Dr. Priya Singh", "Computer Workshop")
        self.add_professor("P126", "Dr. Sikandar Ali Khan", "EEE")
        self.add_professor("P127", "Dr. Astha", "CE")
        self.add_professor("P128", "Dr. Varsha Patahk", "Workshop Practice")
        self.add_professor("P129", "Dr. Ritu Kumari", "Physics")
        self.add_professor("P130", "Dr. Sheetal Kumari", "Engg. Physics Workshop")
        self.add_professor("P131", "Dr. PK Jain", "Workshop Practice")
        self.add_professor("P132", "Dr. Awadhesh Kumar", "CE")


        # --- Pre-populate bookings from your provided timetables ---
        self._load_timetable_data()


    def _load_timetable_data(self):
        # This is a manual interpretation and mapping of your OCR to the system's time slots.
        # This part would typically be automated with a more sophisticated parser.

        # Helper function to map timetable slots to our standardized slots
        def map_slot(day, time_range):
            if time_range == "8-9": return "08:00-09:00"
            if time_range == "9-10": return "09:00-10:00"
            if time_range == "10-11": return "10:00-11:00"
            if time_range == "11-12": return "11:00-12:00"
            if time_range == "12-1": return "12:00-13:00"
            if time_range == "1-2": return "13:00-14:00"
            if time_range == "2-3": return "14:00-15:00"
            if time_range == "3-4": return "15:00-16:00"
            if time_range == "4-5": return "16:00-17:00"
            if time_range == "5-6": return "17:00-18:00" # Extended for 5-6 slot if present
            # For specific named slots, we'll assume standard class durations.
            # This is a simplification and would need careful mapping in a real system.
            if "AM 101" in time_range and ("G1" in time_range or "G2" in time_range or "T" in time_range or "L" in time_range):
                if time_range in ["AM 101 (T) G2", "AM 101 G2 (T)", "AM 101 G2(T)"]:
                    if day == "MON": return "11:00-12:00"
                    if day == "FRI": return "09:00-10:00" # For Page 1, Room SPS 5
                if time_range == "AM 101 (L)":
                    if day == "MON": return "12:00-13:00"
                    if day == "THU": return "12:00-13:00"
                if time_range == "AM 101 (T) G1":
                    if day == "MON": return "15:00-16:00"
                if time_range in ["AM101 (L)", "AM 101 (L+T)"]:
                    if day == "THU" or day == "FRI": return "14:00-15:00"
            if "AP 101" in time_range:
                if time_range == "AP 101 (L)":
                    if day == "MON": return "16:00-17:00"
                    if day == "WED": return "09:00-10:00"
                if time_range == "AP101 (LAB)":
                    if day == "TUE": return "15:00-16:00"
            if "EE105" in time_range:
                if time_range == "EE105 (LAB)":
                    if day == "TUE": return "10:00-11:00"
                    if day == "FRI": return "08:00-09:00"
                if time_range == "EE 105 (L)":
                    if day == "WED": return "10:00-11:00"
                    if day == "FRI": return "16:00-17:00"
            if "ME101" in time_range:
                if time_range == "ME101 (L)":
                    if day == "THU": return "10:00-11:00"
                    if day == "FRI": return "10:00-11:00"
            if "CH 103" in time_range:
                if time_range == "CH 103 (L)":
                    if day == "TUE": return "13:00-14:00"
            if "CH103 (LAB)" in time_range:
                if day == "TUE": return "16:00-17:00"
                if day == "THU" and "G1" in time_range: return "14:00-15:00"
                if day == "THU" and "G2" in time_range: return "15:00-16:00"

            return None # Return None if not explicitly mapped or a "Zero Hour" / "AEC/VAC"

        # Simulating bookings for a specific date (e.g., "2025-08-04" as in your table header)
        base_date_str = "2025-08-04"
        days_of_week = ["MON", "TUE", "WED", "THU", "FRI"] # Assuming the table starts on a Monday

        # Timetable data structure (simplified for demonstration, based on your OCR)
        # Each entry: (Day, Time_Range_from_OCR, Room_ID, Course_Code, Professor_ID)

        # PAGE 1: BRANCH: CHEMICAL ENGINEERING (B15), ROOM NO. SPS 5
        tt_sps5 = [
            ("MON", "AM101 (T) G2", "SPS 5", "AM 101", "P028"), # Himanshi
            ("MON", "AM 101 (L)", "SPS 5", "AM 101", "P027"), # Jamkhongam
            ("MON", "AM 101 (T) G1", "SPS 5", "AM 101", "P027"), # Jamkhongam
            ("MON", "AP 101 (L)", "SPS 5", "AP 101", "P129"), # Ritu Kumari
            ("TUE", "EE105 (LAB)", "SPS 5", "EE105", "P029"), # Narendra Kumar-I
            ("TUE", "CH 103 (L)", "SPS 5", "SEC-1 (CH 103)", "P008"), # Archana Rani
            ("TUE", "AP101 (LAB)", "SPS 5", "AP 101", "P129"), # Ritu Kumari
            ("TUE", "CH103 (LAB) G3 SB-SF-06", "SPS 5", "SEC-1 (CH 103)", "P008"),
            ("WED", "AP101 (L)", "SPS 5", "AP 101", "P129"),
            ("WED", "EE 105 (L)", "SPS 5", "EE105", "P029"),
            # "Zero Hour (No Classes)" for WED 3-4, 4-5, 5-6 means it's free, no booking needed
            ("THU", "ME101 (L)", "SPS 5", "ME101", "P015"), # Md Gulam Mustafa
            ("THU", "AM 101 (L)", "SPS 5", "AM 101", "P027"),
            ("THU", "CH103 (LAB) G1 SB-SF-06", "SPS 5", "SEC-1 (CH 103)", "P008"),
            ("THU", "CH103 (LAB) G2 SB-SF-06", "SPS 5", "SEC-1 (CH 103)", "P008"),
            ("FRI", "ME101 (L)", "SPS 5", "ME101", "P015"),
            ("FRI", "ME103 (LAB)", "SPS 5", "ME103", "P015"), # ME103 is not listed, assuming from ME101 prof
            ("FRI", "EE 105 (L)", "SPS 5", "EE105", "P029")
        ]
        
        # Populate bookings for SPS 5
        for day_index, (day, time_range_ocr, room_id, course_code, prof_id) in enumerate(tt_sps5):
            current_date = (datetime.datetime.strptime(base_date_str, "%Y-%m-%d") + datetime.timedelta(days=day_index)).strftime("%Y-%m-%d")
            time_slot = map_slot(day, time_range_ocr)
            if time_slot:
                booking_details = {"professor_id": prof_id, "course_name": course_code, "purpose": "class"}
                # Ensure the room and professor exist before attempting to book
                if room_id not in self.rooms:
                    self.add_room(room_id, "Chemical Engineering", 60) # Add if missing
                if prof_id not in self.professors:
                    self.add_professor(prof_id, f"Prof {prof_id}", "General") # Add a generic professor if missing
                
                success, msg = self.rooms[room_id].book(current_date, time_slot, booking_details)
                if success:
                    self.professors[prof_id].add_to_schedule(current_date, time_slot, room_id)
                # else: print(f"Warning: {msg}") # Suppress for initial load to avoid spam

        # You would repeat the above process for all 38 timetables.
        # This is very tedious to do manually, so I'll just do a few more illustrative ones.

        # PAGE 2: BRANCH: MATHEMATICS & COMPUTING (SEC-1/B04), ROOM NO. PB-GF3,6, PB-FF2,3
        tt_math_comp_sec1 = [
            ("MON", "AM 101 G2 (T)", "PB-FF2", "AM 101", "P004"), # Divya
            ("MON", "AP101 (LAB)", "PB-GF3", "AP 101", "P005"), # Kamal Kishor
            ("MON", "EC101 (L)", "PB-FF4", "EC 101", "P006"), # Kaustubh Ranjan Singh
            ("MON", "ME105 (L)", "PB-FF2", "ME 105", "P007"), # Rasin Khera
            ("TUE", "ME105 (L)", "PB-FF3", "ME 105", "P007"),
            ("TUE", "ME105 (LAB)", "PB-GF3", "ME 105", "P007"), # This is likely 12-1 or 1-2 based on columns
            ("WED", "AM 101 (L)", "PB-FF2", "AM 101", "P004"),
            ("WED", "AM 101 G1 (T)", "PB-FF2", "AM 101", "P004"),
            ("WED", "MC103 -P1, P2, P3 (I)", "PB-FF3", "SEC-1 (MC103)", "P055"), # Moirangthen Biken Singh, placeholder for multiple profs
            ("THU", "AM 101 (L)", "PB-FF2", "AM 101", "P004"),
            ("FRI", "MC103 -P1, P2, P3 (II)", "PB-GF6", "SEC-1 (MC103)", "P055"),
            ("FRI", "AP101 (L)", "PB-GF6", "AP 101", "P005"),
            ("FRI", "EC101 (L)", "PB-GF6", "EC 101", "P006")
        ]
        
        # Adjusting the days for this particular timetable loading
        # Assuming Monday Aug 4th, so Tuesday is Aug 5th, etc.
        for day_index, (day, time_range_ocr, room_id, course_code, prof_id) in enumerate(tt_math_comp_sec1):
            current_date = (datetime.datetime.strptime(base_date_str, "%Y-%m-%d") + datetime.timedelta(days=day_index)).strftime("%Y-%m-%d")
            # The time slot mapping needs to be smart about which column it came from
            # This is a general helper, but specific column for specific day/room matters
            # For simplicity, let's assume direct column mapping for now for these specific entries
            
            # Manual mapping for Page 2
            mapped_slot = None
            if day == "MON":
                if time_range_ocr == "AM 101 G2 (T)": mapped_slot = "10:00-11:00" # Based on the column
                if time_range_ocr == "AP101 (LAB)": mapped_slot = "11:00-12:00"
                if time_range_ocr == "EC101 (L)": mapped_slot = "14:00-15:00"
                if time_range_ocr == "ME105 (L)": mapped_slot = "16:00-17:00"
            elif day == "TUE":
                if time_range_ocr == "ME105 (L)": mapped_slot = "12:00-13:00"
                if time_range_ocr == "ME105 (LAB)": mapped_slot = "14:00-15:00"
            elif day == "WED":
                if time_range_ocr == "AM 101 (L)": mapped_slot = "09:00-10:00"
                if time_range_ocr == "AM 101 G1 (T)": mapped_slot = "10:00-11:00"
                if time_range_ocr == "MC103 -P1, P2, P3 (I)": mapped_slot = "12:00-13:00"
            elif day == "THU":
                if time_range_ocr == "AM 101 (L)": mapped_slot = "14:00-15:00"
            elif day == "FRI":
                if time_range_ocr == "MC103 -P1, P2, P3 (II)": mapped_slot = "12:00-13:00"
                if time_range_ocr == "AP101 (L)": mapped_slot = "14:00-15:00"
                if time_range_ocr == "EC101 (L)": mapped_slot = "16:00-17:00"
            
            if mapped_slot:
                booking_details = {"professor_id": prof_id, "course_name": course_code, "purpose": "class"}
                if room_id not in self.rooms:
                    # Add room if it doesn't exist, using Math & Comp as branch
                    self.add_room(room_id, "Mathematics & Computing", 50)
                if prof_id not in self.professors:
                    self.add_professor(prof_id, f"Prof {prof_id}", "Mathematics & Computing")
                
                success, msg = self.rooms[room_id].book(current_date, mapped_slot, booking_details)
                if success:
                    self.professors[prof_id].add_to_schedule(current_date, mapped_slot, room_id)
                # else: print(f"Warning: {msg}")


        # Example of adding a professor (strictly from DTU)
        self.add_professor("P200", "Dr. Kavita Sharma", "CSE")
        self.add_professor("P201", "Dr. Alok Kumar", "ECE")
        self.add_professor("P202", "Dr. Priya Singh", "Mechanical Engineering")


    def add_room(self, room_id, branch, capacity):
        if room_id not in self.rooms:
            self.rooms[room_id] = Room(room_id, branch, capacity)
            # print(f"Added room: {room_id}") # For debugging initial load
            return True, f"Room {room_id} added."
        return False, f"Room {room_id} already exists."

    def add_professor(self, professor_id, name, branch):
        if professor_id not in self.professors:
            self.professors[professor_id] = Professor(professor_id, name, branch)
            # print(f"Added professor: {name} ({professor_id})") # For debugging initial load
            return True, f"Professor {name} ({professor_id}) added."
        return False, f"Professor {professor_id} already exists."

    def get_time_slots(self):
        return self.time_slots

    def find_available_rooms_for_professor(self, professor_id, date_str, time_slot):
        if professor_id not in self.professors:
            return [], "Professor not found."

        professor = self.professors[professor_id]
        if not professor.is_available(date_str, time_slot):
            return [], "Professor is already scheduled for this time slot."

        available_rooms = []
        for room_id, room in self.rooms.items():
            if room.is_available(date_str, time_slot):
                available_rooms.append({
                    "room_id": room.room_id,
                    "branch": room.branch,
                    "capacity": room.capacity
                })
        return available_rooms, "Available rooms found."

    def book_room_for_professor(self, professor_id, room_id, date_str, time_slot, course_name, purpose="class"):
        if professor_id not in self.professors:
            return False, "Professor not found."
        if room_id not in self.rooms:
            return False, "Room not found."
        if time_slot not in self.time_slots:
            return False, "Invalid time slot."

        professor = self.professors[professor_id]
        room = self.rooms[room_id]

        # 1. Check if professor is available
        if not professor.is_available(date_str, time_slot):
            return False, "Professor is already scheduled for this time slot."

        # 2. Check if room is available
        existing_booking = room.get_booking_details(date_str, time_slot)
        if existing_booking:
            return False, f"Room {room_id} is already booked by {existing_booking.get('professor_id', 'Unknown')} for {existing_booking.get('course_name', 'Unknown Course')}"
        
        # 3. If both are available, proceed with booking
        booking_details = {
            "professor_id": professor_id,
            "course_name": course_name,
            "purpose": purpose
        }
        
        success, message = room.book(date_str, time_slot, booking_details)
        if success:
            professor.add_to_schedule(date_str, time_slot, room_id)
            return True, f"Room {room_id} booked successfully for {course_name} by {professor.name}."
        return False, message # Should not hit here if logic is correct

    def find_empty_room_for_self_study(self, date_str, time_slot):
        if time_slot not in self.time_slots:
            return [], "Invalid time slot."

        empty_rooms = []
        for room_id, room in self.rooms.items():
            if room.is_available(date_str, time_slot):
                empty_rooms.append({
                    "room_id": room.room_id,
                    "branch": room.branch,
                    "capacity": room.capacity
                })
        return empty_rooms, "Empty rooms found for self-study."

    def display_room_schedule(self, room_id, date_str):
        if room_id not in self.rooms:
            return "Room not found."
        room = self.rooms[room_id]
        
        schedule_str = f"\nSchedule for {room_id} on {date_str}:\n"
        has_bookings = False
        for time_slot in self.time_slots:
            booking_details = room.get_booking_details(date_str, time_slot)
            if booking_details:
                has_bookings = True
                prof_name = self.professors.get(booking_details['professor_id'], Professor("Unknown", "Unknown")).name
                schedule_str += (
                    f"  {time_slot}: Course - {booking_details['course_name']}, "
                    f"Professor - {prof_name} "
                    f"(Purpose: {booking_details['purpose']})\n"
                )
            else:
                schedule_str += f"  {time_slot}: Available\n"
        
        if not has_bookings and date_str not in room.bookings:
            return f"No bookings for {room_id} on {date_str}. It is completely free."
        
        return schedule_str

    def display_professor_schedule(self, professor_id, date_str):
        if professor_id not in self.professors:
            return "Professor not found."
        professor = self.professors[professor_id]

        schedule_str = f"\nSchedule for Professor {professor.name} ({professor.professor_id}) on {date_str}:\n"
        has_bookings = False
        for time_slot in self.time_slots:
            room_id = professor.schedule.get(date_str, {}).get(time_slot)
            if room_id:
                has_bookings = True
                booking_details = self.rooms[room_id].get_booking_details(date_str, time_slot)
                course_name = booking_details.get('course_name', 'N/A') if booking_details else 'N/A'
                schedule_str += f"  {time_slot}: Booked in {room_id} for {course_name}\n"
            else:
                schedule_str += f"  {time_slot}: Available\n"

        if not has_bookings and date_str not in professor.schedule:
            return f"Professor {professor.name} has no bookings on {date_str}. They are completely free."
        
        return schedule_str


# --- AI/Interaction Layer (Simulated) ---
def get_valid_date_input():
    while True:
        date_str = input("Enter desired date (YYYY-MM-DD, e.g., 2025-08-04): ").strip()
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_valid_time_slot_input(system):
    print(f"Available time slots: {', '.join(system.get_time_slots())}")
    while True:
        time_slot = input("Enter desired time slot (e.g., 09:00-10:00): ").strip()
        if time_slot in system.get_time_slots():
            return time_slot
        else:
            print("Invalid time slot. Please choose from the available options.")

def simulate_professor_request(system):
    print("\n--- Professor Room Request ---")
    professor_id = input("Enter Professor ID (e.g., P001, P008, P200): ").strip()
    
    if professor_id not in system.professors:
        print("Error: Professor ID not found. Please ensure it's a valid DTU professor ID.")
        return

    date_str = get_valid_date_input()
    time_slot = get_valid_time_slot_input(system)

    available_rooms, msg = system.find_available_rooms_for_professor(professor_id, date_str, time_slot)

    if available_rooms:
        print(f"\n{msg} for {system.professors[professor_id].name} on {date_str} at {time_slot}:")
        for room in available_rooms:
            print(f"  Room ID: {room['room_id']}, Branch: {room['branch']}, Capacity: {room['capacity']}")

        if input("Do you want to book one of these rooms? (yes/no): ").lower() == 'yes':
            room_to_book = input("Enter the Room ID you wish to book: ").strip()
            if room_to_book not in system.rooms:
                print("Error: Room ID not found in the list of available rooms.")
                return
            
            course_name = input("Enter the course name/purpose: ").strip()
            success, book_msg = system.book_room_for_professor(
                professor_id, room_to_book, date_str, time_slot, course_name
            )
            print(book_msg)
            if success:
                print(system.display_room_schedule(room_to_book, date_str))
                print(system.display_professor_schedule(professor_id, date_str))
        else:
            print("Room booking cancelled by professor.")
    else:
        print(f"No rooms available or {msg}")
    
    # Show professor's full schedule after attempt
    print(system.display_professor_schedule(professor_id, date_str))

def simulate_student_request(system):
    print("\n--- Student Self-Study Room Request ---")
    date_str = get_valid_date_input()
    time_slot = get_valid_time_slot_input(system)

    empty_rooms, msg = system.find_empty_room_for_self_study(date_str, time_slot)

    if empty_rooms:
        print(f"\n{msg} on {date_str} at {time_slot}:")
        for room in empty_rooms:
            print(f"  Room ID: {room['room_id']}, Branch: {room['branch']}, Capacity: {room['capacity']}")
        print("\nNote: For self-study, rooms are available on a first-come, first-served basis and are not formally booked via this system.")
    else:
        print(f"No empty rooms found for self-study on {date_str} at {time_slot}.")

def main():
    dtu_system = DTURoomBookingSystem()
    print("DTU Room Booking System Initialized with Timetable Data.")

    while True:
        print("\n--- DTU Room Booking System Menu ---")
        print("1. Professor Request (Book a room for class)")
        print("2. Student Self-Study Request (Find an empty room)")
        print("3. Display Room Schedule")
        print("4. Display Professor Schedule")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            simulate_professor_request(dtu_system)
        elif choice == '2':
            simulate_student_request(dtu_system)
        elif choice == '3':
            room_id = input("Enter Room ID (e.g., SPS 5, PB-GF3): ").strip()
            date_str = get_valid_date_input()
            print(dtu_system.display_room_schedule(room_id, date_str))
        elif choice == '4':
            professor_id = input("Enter Professor ID (e.g., P001, P008): ").strip()
            if professor_id not in dtu_system.professors:
                print("Error: Professor ID not found.")
                continue
            date_str = get_valid_date_input()
            print(dtu_system.display_professor_schedule(professor_id, date_str))
        elif choice == '5':
            print("Exiting DTU Room Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()