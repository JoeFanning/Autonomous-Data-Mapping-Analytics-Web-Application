# 🌐 Autonomous Data Mapping & Analytics Web Application


An easy to use, interactive data analytics platform built with Streamlit and a Deep Learning Transformer Model. Upload your business spreadsheets, instantly preview key financial metrics, and automatically dispatch summary reports to your email.

## 🧠 The Motivation: Exploring Data Drift

I am interested in how data changes over time and how software reacts to those unexpected changes. In the real world, data is rarely perfect or consistent; software must learn to adapt to these shifts rather than crashing. This curiosity is what led me to explore the concept of **Data Drift**.

---

## 🌊 What is Data Drift?

Data Drift happens when the structure or statistical properties of data shifts over time. A common and frustrating type is **Schema Drift**, which occurs when file headers or column names suddenly change without warning. 

For example, if a traditional program expects an Excel column to be named exactly `"Total Price", but a user or automated system updates the file column names to `"Total Amount"`, `"Invoice Total"`, or `"Net Cost"`, the pipeline will break and the software will crash.

---

## 🛠️ The Solution: Adaptive Pipeline

To tackle this problem, this software is a simple but effective solution to handle shifting column names automatically.

### 🤖 Intelligent Column Detection with a Deep Learning Transformer Model
* **Powered by AI:** Uses the `all-MiniLM-L6-v2` Deep Learning Transformer model to dynamically map and identify the 'Total Price or 'Total Amount Due' column in the data Schema. It is a mini Neural Network (a MiniLM Transformer) trained on over one billion sentences.
* **Context-Aware:** Understands the actual meaning of column headers rather than relying on rigid keyword matching.
* **Fuzzy & Multi-lingual Support:** Automatically handles variations in spelling, shorthand (e.g., `Amt`, `Prc`), snake_case, camelCase, and multiple languages (such as Spanish, French, and German).
* **Zero Training Required:** Works entirely local and out-of-the-box using pre-trained sentence embeddings.
  Pre-trained sentence embeddings are whole sentences converted into a list of mathematical numbers (called a vector) that capture the exact meaning of the text.
 
---

### 🔮 The Ultimate Goal: Total Autonomous Data Mapping

Looking ahead, the ultimate achievement for an engineering pipeline like this would be expanding autonomous classification to the entire dataset. Instead of just targeting a single price field, a mature system would evaluate every text and numeric column simultaneously—instantly identifying exactly *what* the column represents, classifying the specific type of data it holds, and dynamically applying the correct analytical process without any human intervention.

---

## 🚀 Live Application
You can access and interact with the live software directly in your web browser:

👉 **[Launch Autonomous-Data-Mapping-Analytics-Web-Application](https://joefanning.streamlit.app/)** 

---

## 📂 How to Use the App
1. Open the application using the link above.
2. Enter your **Email Address** to receive the final summary.
3. Drag and drop or upload your **CSV (.csv)** or **Excel (.xlsx)** spreadsheets.
4. The spreadsheet must have a numeric type, for example 'Invoice Total' for Summary Statistics. 
5. Click **Run Analytics & Email Report** to process your files and dispatch your email report.

---

## 📈 Auto-Detected Price Metrics
The app automatically scans your dataset columns for financial markers (such as Price, Cost, Rate, MSRP, or Precio) and instantly displays these **8 core metrics**:

* **Total Revenue Sum:** The aggregate total financial revenue accumulation calculated across all line items combined.
* **Highest Price Found:** The maximum financial value identified in your target data vector.
* **Lowest Price Found:** The absolute minimum price tag recorded inside your file.
* **Average Price (Mean):** The standard calculated average across all transaction prices.
* **Median Price (Middle Point):** The exact middle-tier price point, completely unaffected by extreme luxury or discount anomalies.
* **Price Range Spread:** The total numeric dollar gap spanning between your cheapest and most expensive items.
* **Standard Deviation:** A measurement showing how spread out or tightly clustered your data's price points are.
* **Total Record Count:** The total number of valid transaction rows currently processed by the dataset engine.

## 📄 License
This project is open-source software created by **Joe Fanning** and is licensed under the [MIT License](LICENSE).
