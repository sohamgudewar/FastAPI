import streamlit as st
import requests

# Configuration
API_URL = "http://localhost:8000"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# Page Title
st.title("🏥 Hospital Management System")

# Login Section
if not st.session_state.logged_in:
    st.header("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            try:
                response = requests.post(
                    f"{API_URL}/admin/token",
                    data={"username": username, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Login failed. Check your credentials.")
            except:
                st.error("Cannot connect to server. Make sure FastAPI is running.")
    
    with col2:
        if st.button("Create Account"):
            new_username = st.text_input("New Username", key="new_user")
            new_password = st.text_input("New Password", type="password", key="new_pass")
            if st.button("Create", key="create_btn"):
                try:
                    response = requests.post(
                        f"{API_URL}/admin/add",
                        json={"username": new_username, "password": new_password}
                    )
                    if response.status_code == 200:
                        st.success("Account created! You can now login.")
                    else:
                        st.error("Failed to create account.")
                except:
                    st.error("Cannot connect to server.")

# Main Application (After Login)
else:
    # Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.token = None
        st.rerun()
    
    st.success(f"✅ Logged in")
    st.markdown("---")
    
    # Navigation
    page = st.selectbox("Choose a page:", ["Patients", "Doctors", "Insurance Prediction"])
    st.markdown("---")
    
    # PATIENTS PAGE
    if page == "Patients":
        st.header("Patient Management")
        
        action = st.radio("What do you want to do?", ["Create", "View", "Update", "Delete"])
        
        # Create Patient
        if action == "Create":
            st.subheader("Create New Patient")
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0, max_value=120)
            weight = st.number_input("Weight (kg)", min_value=0.0)
            height = st.number_input("Height (m)", min_value=0.0, max_value=2.5)
            
            if st.button("Create Patient"):
                try:
                    response = requests.post(
                        f"{API_URL}/patients/patient/",
                        json={"name": name, "age": int(age), "weight": float(weight), "height": float(height)}
                    )
                    if response.status_code == 200:
                        st.success("Patient created!")
                        st.json(response.json())
                    else:
                        st.error("Failed to create patient.")
                except:
                    st.error("Cannot connect to server.")
        
        # View Patient
        elif action == "View":
            st.subheader("View Patient")
            patient_id = st.number_input("Patient ID", min_value=1, value=1)
            
            if st.button("Get Patient"):
                try:
                    response = requests.get(f"{API_URL}/patients/patient/{int(patient_id)}")
                    if response.status_code == 200:
                        patient = response.json()
                        st.success("Patient found!")
                        st.write(f"**Name:** {patient['name']}")
                        st.write(f"**Age:** {patient['age']}")
                        st.write(f"**Weight:** {patient['weight']} kg")
                        st.write(f"**Height:** {patient['height']} m")
                    else:
                        st.error("Patient not found.")
                except:
                    st.error("Cannot connect to server.")
        
        # Update Patient
        elif action == "Update":
            st.subheader("Update Patient")
            patient_id = st.number_input("Patient ID", min_value=1, value=1, key="update_id")
            name = st.text_input("Name", key="update_name")
            age = st.number_input("Age", min_value=0, max_value=120, key="update_age")
            weight = st.number_input("Weight (kg)", min_value=0.0, key="update_weight")
            height = st.number_input("Height (m)", min_value=0.0, max_value=2.5, key="update_height")
            
            if st.button("Update Patient"):
                try:
                    response = requests.put(
                        f"{API_URL}/patients/patient_id/{int(patient_id)}",
                        json={"name": name, "age": int(age), "weight": float(weight), "height": float(height)}
                    )
                    if response.status_code == 200:
                        st.success("Patient updated!")
                        st.json(response.json())
                    else:
                        st.error("Failed to update patient.")
                except:
                    st.error("Cannot connect to server.")
        
        # Delete Patient
        elif action == "Delete":
            st.subheader("Delete Patient")
            patient_id = st.number_input("Patient ID", min_value=1, value=1, key="delete_id")
            name = st.text_input("Patient Name (for confirmation)", key="delete_name")
            
            if st.button("Delete Patient", type="primary"):
                try:
                    response = requests.delete(
                        f"{API_URL}/patients/patient_id/{int(patient_id)}",
                        params={"name": name}
                    )
                    if response.status_code == 200:
                        st.success("Patient deleted!")
                    else:
                        st.error("Failed to delete patient.")
                except:
                    st.error("Cannot connect to server.")
    
    # DOCTORS PAGE
    elif page == "Doctors":
        st.header("Doctor Management")
        
        action = st.radio("What do you want to do?", ["Create", "View", "Update", "Delete"])
        
        # Create Doctor
        if action == "Create":
            st.subheader("Create New Doctor")
            name = st.text_input("Doctor Name")
            specialty = st.text_input("Specialty")
            
            if st.button("Create Doctor"):
                try:
                    response = requests.post(
                        f"{API_URL}/doctors/doctor/",
                        json={"name": name, "specialty": specialty}
                    )
                    if response.status_code == 200:
                        st.success("Doctor created!")
                        st.json(response.json())
                    else:
                        st.error("Failed to create doctor.")
                except:
                    st.error("Cannot connect to server.")
        
        # View Doctor
        elif action == "View":
            st.subheader("View Doctor")
            doctor_id = st.number_input("Doctor ID", min_value=1, value=1)
            
            if st.button("Get Doctor"):
                try:
                    response = requests.get(f"{API_URL}/doctors/doctor/{int(doctor_id)}")
                    if response.status_code == 200:
                        doctor = response.json()
                        st.success("Doctor found!")
                        st.write(f"**Name:** {doctor['name']}")
                        st.write(f"**Specialty:** {doctor['specialty']}")
                    else:
                        st.error("Doctor not found.")
                except:
                    st.error("Cannot connect to server.")
        
        # Update Doctor
        elif action == "Update":
            st.subheader("Update Doctor")
            doctor_id = st.number_input("Doctor ID", min_value=1, value=1, key="update_doc_id")
            name = st.text_input("Doctor Name", key="update_doc_name")
            specialty = st.text_input("Specialty", key="update_doc_specialty")
            
            if st.button("Update Doctor"):
                try:
                    response = requests.put(
                        f"{API_URL}/doctors/doctor_id/{int(doctor_id)}",
                        json={"name": name, "specialty": specialty}
                    )
                    if response.status_code == 200:
                        st.success("Doctor updated!")
                        st.json(response.json())
                    else:
                        st.error("Failed to update doctor.")
                except:
                    st.error("Cannot connect to server.")
        
        # Delete Doctor
        elif action == "Delete":
            st.subheader("Delete Doctor")
            doctor_id = st.number_input("Doctor ID", min_value=1, value=1, key="delete_doc_id")
            
            if st.button("Delete Doctor", type="primary"):
                try:
                    response = requests.delete(f"{API_URL}/doctors/doctor_id/{int(doctor_id)}")
                    if response.status_code == 200:
                        st.success("Doctor deleted!")
                    else:
                        st.error("Failed to delete doctor.")
                except:
                    st.error("Cannot connect to server.")
    
    # INSURANCE PREDICTION PAGE
    elif page == "Insurance Prediction":
        st.header("Insurance Premium Prediction")
        st.write("Enter your information to predict insurance premium category")
        
        # Input Form
        age = st.number_input("Age", min_value=1, max_value=120, value=35)
        weight = st.number_input("Weight (kg)", min_value=0.0, value=75.0)
        height = st.number_input("Height (m)", min_value=0.0, max_value=2.5, value=1.75, step=0.01)
        income = st.number_input("Annual Income (LPA)", min_value=0.0, value=12.5)
        smoker = st.checkbox("Are you a smoker?")
        city = st.text_input("City", value="Mumbai")
        occupation = st.selectbox(
            "Occupation",
            ["Engineer", "Driver", "Teacher", "Banker", "Sales Manager", "Businessman", "Factory Worker"]
        )
        
        if st.button("Predict Premium", type="primary"):
            try:
                # Calculate BMI
                bmi = weight / (height ** 2) if height > 0 else 0
                st.write(f"**Your BMI:** {bmi:.2f}")
                
                # Make prediction
                response = requests.post(
                    f"{API_URL}/insurance_premium/predict",
                    json={
                        "age": int(age),
                        "weight": float(weight),
                        "height": float(height),
                        "income_lpa": float(income),
                        "smoker": smoker,
                        "city": city,
                        "occupation": occupation
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get("response", {})
                    
                    category = prediction.get("predicted_category", "Unknown")
                    confidence = prediction.get("confidence", 0.0)
                    
                    st.markdown("---")
                    st.subheader("Prediction Result")
                    
                    # Show result with color
                    if category == "High":
                        st.error(f"**Premium Category: {category}**")
                    elif category == "Medium":
                        st.warning(f"**Premium Category: {category}**")
                    else:
                        st.success(f"**Premium Category: {category}**")
                    
                    st.write(f"**Confidence:** {confidence*100:.2f}%")
                    
                    # Show probabilities
                    st.write("**Probabilities:**")
                    probs = prediction.get("class_probabilities", {})
                    for cat, prob in probs.items():
                        st.write(f"- {cat}: {prob*100:.2f}%")
                else:
                    st.error("Prediction failed.")
            except Exception as e:
                st.error(f"Cannot connect to server. Error: {str(e)}")
