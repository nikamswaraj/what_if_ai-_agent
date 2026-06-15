# ❓ What If Scenario Analyzer

## 📌 Overview

**What If Scenario Analyzer** is an AI-powered application that helps users explore hypothetical situations and predict possible outcomes. Using multiple AI agents powered by **CrewAI** and **Google Gemini**, the system analyzes scenarios from different perspectives and provides strategic recommendations.

Users can enter any "What If" scenario, and the AI agents collaboratively generate structured insights, risk assessments, opportunities, and actionable recommendations.

---

## 🚀 Features

* ✅ AI-powered scenario analysis
* ✅ Multi-agent collaboration using CrewAI
* ✅ Strategic outcome prediction
* ✅ Risk and opportunity assessment
* ✅ Actionable recommendations
* ✅ Interactive Streamlit interface
* ✅ Google Gemini integration
* ✅ Real-time analysis results
* ✅ Clean and user-friendly dashboard

---

## 🛠️ Technologies Used

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Core Programming Language       |
| Streamlit         | Frontend Web Application        |
| CrewAI            | Multi-Agent Framework           |
| Google Gemini API | Large Language Model            |
| dotenv            | Environment Variable Management |
| HTML/CSS          | User Interface Styling          |

---

## 🏗️ System Architecture

```text
User Input
     │
     ▼
What If Scenario
     │
     ▼
───────────────────────
CrewAI Multi-Agent Team
───────────────────────
     │
     ├── Research Analyst Agent
     │       ↓
     │  Scenario Breakdown
     │
     ├── Strategic Advisor Agent
     │       ↓
     │  Outcome Evaluation
     │
     └── Decision Advisor Agent
             ↓
      Recommendations
     │
     ▼
Final Comprehensive Report
```

---

## 🤖 AI Agents

### 1. Senior Research Analyst

**Role:**

* Analyze the scenario
* Identify key components
* Determine major stakeholders
* Recognize important variables

**Output:**

* Structured scenario breakdown

---

### 2. Strategic Advisor

**Role:**

* Evaluate possible outcomes
* Analyze risks and opportunities
* Consider short-term and long-term impacts

**Output:**

* Outcome and implication assessment

---

### 3. Decision Advisor

**Role:**

* Generate actionable recommendations
* Suggest strategies
* Provide practical guidance

**Output:**

* Decision-making recommendations

---

## 🔄 Workflow

### Step 1: User Input

User enters a hypothetical scenario:

```text
What if renewable energy became 80% of global energy production by 2030?
```

### Step 2: Scenario Analysis

The Research Analyst identifies:

* Main actors
* Key factors
* Timeline
* Dependencies

### Step 3: Outcome Evaluation

The Strategic Advisor predicts:

* Economic impact
* Environmental impact
* Social impact
* Potential risks

### Step 4: Recommendations

The Decision Advisor provides:

* Short-term strategies
* Long-term planning
* Risk mitigation techniques

### Step 5: Final Report

A comprehensive AI-generated analysis is displayed.

---

## 📂 Project Structure

```text
What-If-Scenario-Analyzer/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
│
└── assets/
    ├── screenshots/
    └── diagrams/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/what-if-scenario-analyzer.git

cd what-if-scenario-analyzer
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure API Key

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch in your browser.

---

## 📋 Requirements

```text
streamlit
crewai
google-generativeai
python-dotenv
```

Install manually:

```bash
pip install streamlit crewai google-generativeai python-dotenv
```

---

## 🎯 Example Scenarios

### Technology

```text
What if Artificial General Intelligence becomes available by 2035?
```

### Business

```text
What if remote work becomes mandatory worldwide?
```

### Environment

```text
What if renewable energy supplies 80% of global electricity?
```

### Education

```text
What if AI tutors replace traditional classrooms?
```

### Healthcare

```text
What if personalized medicine becomes affordable for everyone?
```

---

## 📊 Key Benefits

* Faster strategic planning
* Better decision-making
* Risk identification
* Opportunity discovery
* Multi-perspective analysis
* Improved scenario forecasting

---

## 🔮 Future Enhancements

* Web search integration
* PDF report generation
* Scenario comparison mode
* Data visualization dashboards
* Historical trend analysis
* Multi-language support
* Voice-based interaction
* Agent memory and learning

---

## 👨‍💻 Author

**Swaraj Nikam**

B.Tech Student | AI & Data Science

Interested in:

* Artificial Intelligence
* Multi-Agent Systems
* Data Analytics
* Strategic Decision Support Systems

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you found this project useful:

* Star ⭐ the repository
* Fork 🍴 the project
* Share 📢 with others
* Contribute 🚀 improvements

---

## 🏆 Conclusion

The What If Scenario Analyzer demonstrates the power of Multi-Agent AI systems by combining CrewAI and Google Gemini to provide intelligent scenario analysis. By leveraging specialized agents, the application helps users understand complex situations, evaluate possible outcomes, and make informed strategic decisions.
