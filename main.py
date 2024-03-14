import pandas as pd

def data_cleaning():
    # Load the dataset
    data = pd.read_csv('banking_data_assignment.csv')
    # Correct OCR-like errors in account numbers
    data['Account Number'] = data['Account Number'].str.replace('O', '0')
    # Remove currency symbols and handle negative values
    data['Amount'] = data['Amount'].replace('[\$,]', '', regex=True).astype(float)
    # Normalize negative values for withdrawals
    data['Amount'] = pd.to_numeric(data['Amount'])
    # Save cleaned data
    data.to_csv('cleaned_banking_data.csv', index=False)

def read_correctData():
    data = pd.read_csv('cleaned_banking_data.csv')
    return data


def data_analysis():
    # Load cleaned dataset
    data = read_correctData()

    # Separate individual transactions from aggregated data
    individual_transactions = data[data['Transaction Type'].notnull()]

    # Extract aggregated data (subtotals/yearly totals)
    aggregated_data = data[data['Transaction Type'].isnull()]

    # Reconcile transactions by ensuring the consistency of aggregated data with individual transactions
    reconciliation = aggregated_data['Amount'].sum() - individual_transactions['Amount'].sum()

    # Report reconciliation result
    # print(f'Reconciliation Result: {"Matches" if reconciliation == 0 else "Does not match"}')
    reconciliation = "Matches" if reconciliation==0 else "Does not match"
    return reconciliation


def anomaly_detection():
    # Detect anomalies based on unusually high transaction amounts
    data=read_correctData()
    mean_amount = data['Amount'].mean()
    std_amount = data['Amount'].std()
    threshold = mean_amount + 1 * std_amount

    anomalies = data[data['Amount'] > threshold]

    return(anomalies)

def create_report():
    # Call data_analysis function to get reconciliation result
    reconciliation_result = data_analysis()
    
    # Call anomaly_detection function to get detected anomalies
    detected_anomalies = anomaly_detection()

    
    # Save the report to a file or print it
    with open("report.txt", "w") as file:
        # Write reconciliation result
        file.write("Reconciliation Result: {}\n".format(reconciliation_result))
        
        # Write detected anomalies
        file.write("Detected Anomalies:\n")
        file.write(str(detected_anomalies) + "\n")

def main():
    data_cleaning()
    create_report()
