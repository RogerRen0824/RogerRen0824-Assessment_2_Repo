# COVID-19 Data Analysis

This project uses the global COVID-19 dataset provided by Johns Hopkins University.

## **Data Source**
The original dataset can be found on GitHub in the [CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19) repository.

### **1. How to Download the Data**

1. **Clone the Johns Hopkins COVID-19 Repository**  
   Run the following command in your terminal to clone the data repository:
   ```bash
   git clone --depth 1 https://github.com/CSSEGISandData/COVID-19.git

2. **Locate the Data Files**  
   Go to the `csse_covid_19_data/csse_covid_19_time_series` folder. 

3. **Move the Files to Your Project**  
   Copy the files to your `data` folder:

4. **Remove the Original Repository** (Optional):
   ```bash
   rm -rf COVID-19
   ```

---

### **2. Directory Structure**
Maintain this structure:
```
covid19_analysis/
│
├── data/                          # COVID-19 data files
├── some_code_file.py              # Python analysis scripts
├── saved_figure/                  # Visualizations and plots
└── README.md                      # Documentation
```

---

### **3. Coding Standards**
- Follow **PEP 8** guidelines for Python.
- Use meaningful variable and function names.
- Add comments and docstrings:
   ```python
   def load_data(file_path):
       """
       Load a CSV file into a pandas DataFrame.

       Args:
           file_path (str): Path to the CSV file.

       Returns:
           pd.DataFrame: DataFrame containing the data.
       """
       return pd.read_csv(file_path)
   ```

---

## **Project Setup**
1. Install required libraries:
   ```bash
   pip install pandas matplotlib plotly tabulate
   ```

2. Run the analysis script:
   ```bash
   python some_code_file.py
   ```

---

