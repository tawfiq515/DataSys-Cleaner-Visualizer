# DataSys – Smart Data Cleaner & Visualizer

📊 **DataSys** is a powerful and user-friendly web application built with **Streamlit** that helps you clean your datasets and visualize relationships between numerical features quickly and efficiently.

---

## Features

- Upload CSV files with ease.
- Automatically detect and drop columns with excessive missing values (default > 70%).
- Fill missing categorical data with mode.
- Fill missing numeric data with mean.
- Remove outliers based on the IQR method.
- Interactive scatter plots and regression plots for numerical column pairs.
- Preview cleaned data before downloading.
- Download the cleaned dataset as a CSV file.

---

## How to Use

1. Upload your CSV file.
2. Choose to visualize raw data or clean & visualize.
3. When cleaning, the system automatically processes missing values and removes outliers.
4. Explore the generated plots to understand your data better.
5. Download the cleaned CSV file.

---

## Installation

Make sure you have Python 3.7+ installed. Then install required packages:

```bash
pip install streamlit pandas seaborn matplotlib
```

## Contributing
Contributions are welcome! Feel free to fork the repo, make changes, and submit a pull request.

## Authors
Tawfiq Tahineh - [GitHub Profile] (https://github.com/tawfiq515)

Rama AlJada - [GitHub Profile] (https://github.com/RamaAljada)

## License
This project is licensed under the MIT License. See the LICENSE file for details.


