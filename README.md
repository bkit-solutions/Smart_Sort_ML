# Smart Sorting ML – Final Year Project (BKIT)

Smart Sorting ML is an intelligent fruit & vegetable quality detection system built using **Flask**, **Deep Learning (MobileNetV2)**, and an elegant **Blue–White UI**.  
It classifies images as **Healthy** or **Rotten** and provides a complete analytics dashboard.

---

## 🚀 Features

- ⚡ **Fast, lightweight predictions** using MobileNetV2  
- 📊 **Dashboard analytics** for tracking daily prediction stats  
- 📷 **Drag & Drop image upload**  
- 🎯 **High accuracy model** trained on multiple fruit/vegetable categories  
- 🧩 **Clean UI with animated hero section & responsive layout**  
- 📁 **Automatic file cleanup** for uploaded images  

---

## 📦 Project Structure

```
Smart_Sort_ML/
│── app.py
│── healthy_vs_rotten.h5
│── requirements.txt
│── train_model.ipynb
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── uploads/
│
└── templates/
    ├── base.html
    ├── index.html
    ├── predict.html
    ├── result.html
    └── dashboard.html
```

---

## 🧰 Installation & Setup

### 1️⃣ **Create Virtual Environment**
```
python -m venv venv
```

### 2️⃣ **Activate Virtual Environment**

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

---

### 3️⃣ **Install Requirements**
```
pip install -r requirements.txt
```

---

### 4️⃣ **Run the Flask Application**
```
python app.py
```

Your project will start at:  
👉 **http://127.0.0.1:5000**

---

## 🛠 Technologies Used

- **Python Flask** (Backend & Routing)  
- **TensorFlow / Keras** (Model Loading & Prediction)  
- **MobileNetV2** (Feature Extraction)  
- **Chart.js** (Dashboard Visualization)  
- **Bootstrap 5** (UI Styling)  
- **HTML, CSS, JavaScript**  

---

## 👨‍💻 Built By  
**ML Team at BKIT**
Thank you for exploring Smart Sorting ML! 🎉  
For improvements or enhancements, feel free to ask anytime.
