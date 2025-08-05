# -*- coding: utf-8 -*-

"""
Data Storytelling Automator

This script automates data analysis and report generation from a CSV file.
It identifies correlations and anomalies, generates visualizations, and
compiles everything into a narrative report in Markdown format.
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Loads data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    print(f"Loading data from '{file_path}'...")
    return pd.read_csv(file_path)

def analyze_correlations(df, numerical_cols):
    """
    Analyzes and finds the most significant correlations in the dataframe.

    Args:
        df (pandas.DataFrame): The input dataframe.
        numerical_cols (list): List of numerical column names.

    Returns:
        pandas.DataFrame: The correlation matrix.
        tuple: A tuple containing the most correlated pair and their value.
    """
    print("Analyzing correlations...")
    if len(numerical_cols) < 2:
        return None, None

    corr_matrix = df[numerical_cols].corr()

    # Unstack the matrix to easily find the max correlation
    corr_unstacked = corr_matrix.unstack()

    # Sort by value
    sorted_corr = corr_unstacked.sort_values(kind="quicksort", ascending=False)

    # Find the most significant correlation (not 1.0)
    most_correlated_pair = None
    for (col1, col2), value in sorted_corr.items():
        if col1 != col2:
            most_correlated_pair = (col1, col2, value)
            break

    return corr_matrix, most_correlated_pair

def detect_anomalies(df, col):
    """
    Detects anomalies in a specific column using the IQR method.

    Args:
        df (pandas.DataFrame): The input dataframe.
        col (str): The column to analyze for anomalies.

    Returns:
        pandas.Series: A series of anomalous data points.
    """
    print(f"Detecting anomalies in column '{col}'...")
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    anomalies = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    return anomalies

def create_visualizations(df, corr_matrix, most_correlated_pair, anomaly_col, output_dir):
    """
    Generates and saves data visualizations.

    Args:
        df (pandas.DataFrame): The input dataframe.
        corr_matrix (pandas.DataFrame): The correlation matrix.
        most_correlated_pair (tuple): The most correlated pair of variables.
        anomaly_col (str): The column selected for anomaly detection visualization.
        output_dir (str): The directory to save visualizations.

    Returns:
        dict: A dictionary of paths to the saved visualization files.
    """
    print("Creating visualizations...")
    paths = {}

    # 1. Correlation Heatmap
    if corr_matrix is not None:
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        path = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(path)
        plt.close()
        paths['heatmap'] = path

    # 2. Scatter Plot for the most correlated pair
    if most_correlated_pair:
        col1, col2, _ = most_correlated_pair
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=col1, y=col2)
        plt.title(f'Scatter Plot: {col1} vs {col2}')
        path = os.path.join(output_dir, 'correlation_scatter_plot.png')
        plt.savefig(path)
        plt.close()
        paths['scatter'] = path

    # 3. Box Plot for anomaly detection
    if anomaly_col:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, y=anomaly_col)
        plt.title(f'Anomaly Detection in {anomaly_col}')
        path = os.path.join(output_dir, 'anomaly_boxplot.png')
        plt.savefig(path)
        plt.close()
        paths['boxplot'] = path

    return paths

def generate_report(findings, viz_paths, output_dir):
    """
    Generates a Markdown report from the analysis findings.

    Args:
        findings (dict): A dictionary containing analysis results.
        viz_paths (dict): A dictionary of paths to visualization files.
        output_dir (str): The directory to save the report.
    """
    print("Generating report...")
    report_path = os.path.join(output_dir, 'report.md')

    with open(report_path, 'w') as f:
        f.write("# Automated Data Analysis Report\n\n")
        f.write("## 1. Introduction\n")
        f.write("This report provides an automated analysis of the provided dataset. It highlights key correlations and identifies potential anomalies.\n\n")

        # Correlation Section
        f.write("## 2. Correlation Analysis\n")
        if findings.get('most_correlated_pair'):
            col1, col2, val = findings['most_correlated_pair']
            f.write(f"The analysis identified a strong relationship between variables. The most significant correlation is between **{col1}** and **{col2}** with a correlation coefficient of **{val:.2f}**.\n\n")
            if 'heatmap' in viz_paths:
                f.write("### Correlation Matrix Heatmap\n")
                f.write(f"![Correlation Heatmap](correlation_heatmap.png)\n\n")
            if 'scatter' in viz_paths:
                f.write(f"### Scatter Plot: {col1} vs {col2}\n")
                f.write(f"![Scatter Plot](correlation_scatter_plot.png)\n\n")
        else:
            f.write("No significant correlations were found among the numerical variables.\n\n")

        # Anomaly Section
        f.write("## 3. Anomaly Detection\n")
        if findings.get('anomalies') is not None and not findings['anomalies'].empty:
            anomaly_col = findings['anomaly_col']
            f.write(f"Anomaly detection was performed on the **'{anomaly_col}'** column. The following outliers were identified:\n\n")
            f.write(findings['anomalies'].to_markdown(index=False))
            f.write("\n\n")
            if 'boxplot' in viz_paths:
                f.write(f"### Box Plot for {anomaly_col}\n")
                f.write(f"This box plot visualizes the distribution and highlights the outliers.\n\n")
                f.write(f"![Anomaly Boxplot](anomaly_boxplot.png)\n\n")
        else:
            f.write("No significant anomalies were detected in the analyzed column.\n\n")

        f.write("## 4. Conclusion\n")
        f.write("This automated report is intended to provide a high-level overview of the data. Further investigation is recommended to understand the context behind these findings.\n")

    print(f"Report successfully generated at '{report_path}'")

def main():
    """
    Main function to run the data analysis and report generation pipeline.
    """
    parser = argparse.ArgumentParser(description="Data Storytelling Automator")
    parser.add_argument("file_path", type=str, help="Path to the input CSV file.")
    args = parser.parse_args()

    try:
        # Define output directory
        output_dir = 'reports'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. Load Data
        df = load_data(args.file_path)

        # Identify numerical columns for analysis
        numerical_cols = df.select_dtypes(include=np.number).columns.tolist()

        if not numerical_cols:
            print("Error: No numerical columns found for analysis.")
            return

        # 2. Analyze Data
        corr_matrix, most_correlated_pair = analyze_correlations(df, numerical_cols)

        # For simplicity, we'll detect anomalies in the first numerical column
        anomaly_col = numerical_cols[0]
        anomalies = detect_anomalies(df, anomaly_col)

        findings = {
            'most_correlated_pair': most_correlated_pair,
            'anomalies': anomalies,
            'anomaly_col': anomaly_col
        }

        # 3. Create Visualizations
        viz_paths = create_visualizations(
            df,
            corr_matrix,
            most_correlated_pair,
            anomaly_col,
            output_dir
        )

        # 4. Generate Report
        generate_report(findings, viz_paths, output_dir)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
