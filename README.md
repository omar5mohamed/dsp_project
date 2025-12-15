## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit**: For the interactive web interface.
- **NumPy & SciPy**: For high-performance numerical processing and DSP algorithms.
- **Plotly**: For interactive, high-quality visualizations.
- **SoundFile**: For robust audio file handling.

---

## 📦 Installation

1. **Unzip the Project Folder**

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the application locally:

```bash
streamlit run dsp_studio_app.py
```

The app will open in your default web browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
dsp-project/
├── core/
│   ├── frequency_analysis.py # FFT algorithms
│   ├── signal_digitization.py# Sampling and quantization logic
│   └── signal_filters.py     # Filter design and application
├── interface/
│   ├── modules/              # UI logic for each tab
│   └── common.py             # Helper functions and custom CSS
├── dsp_studio_app.py         # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

