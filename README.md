# hiv-cusum-demo
local stremlit demo for CUSUM alerts

# CUSUM Surveillance Demo

This is a small demo app for detecting potential disease clusters using a CUSUM approach.

The app runs locally and takes a CSV file with monthly case counts by county. It then generates alerts and simple visualizations.

The goal of this prototype is to show how a health department could quickly upload surveillance data and see possible alerts without sending data to external servers.

---

## What the app demo does 

- Upload a CSV file with monthly case counts
- Run a mock CUSUM calculation (it's fake)
- Detect possible alerts 
- Show two plots:
  - case counts vs baseline
  - CUSUM monitoring statistic
- Display a summary table of alerts by county

Everything runs locally in your browser.

---

## Example data format

The app expects a CSV file with this structure:

```
month,county,cases  
2020-01,King,22  
2020-02,King,21  
2020-03,King,23  
2020-01,Pierce,9  
2020-02,Pierce,8
...
```

Columns:

- **month** → month in `YYYY-MM` format  
- **county** → county name  
- **cases** → case count for that month  

A synthetic dataset is included: ```sample_hiv_2020_2024.csv```

---

## Requirements

Python 3.9 or newer is required.

You can check if Python is installed by running:

python --version

If Python is not installed, download it from:
https://www.python.org/downloads/

---

## How to run the app

### 1. Download the project

Either clone the repo:

```
  git clone https://github.com/tiffani-hao/hiv-cusum-demo.git
  
  cd hiv-cusum-demo
```

or download the ZIP from GitHub.

---

### 2. Create a virtual environment

```python -m venv venv``` Activate it.

Mac / Linux: ```source venv/bin/activate```

windows:
```source venv/bin/activate```

---

### 3. Install required packages

```
pip install -r requirements.txt
```

---

### 4. Run the application

```
python -m streamlit run app.py
```

Then open:
```
http://localhost:8501
```

Upload a dataset and the dashboard will generate alerts and plots.

---

### 5. Quit the application

```
ctrl + c
```

or just close everything

---

## Project structure
```
app.py
mock_algo.py
sample_hiv_2020_2024.csv
requirements.txt
README.md
```

---

## Notes

This is only a simple demo for demonstration purposes.

The setup steps may look a bit complicated right now because this is just a prototype. 
The final application would likely be packaged so users can run it more easily.

The current visualizations and outputs are not final. 
They are only examples to show how the workflow might look. 
More features, outputs, and visualizations can be added if needed.

The diagrams and plots shown in the app are also just a rough draft to illustrate the idea.

---

## Author

Tiffani Hao  