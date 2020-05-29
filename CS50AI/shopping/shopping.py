import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

# Define string mth format to int format
def mth_str_to_num(mth_str):
    m = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12
        }
    s = mth_str.lower()
    return m[s]

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # open csv file
    with open("shopping.csv", newline='') as f:
        reader = list(csv.DictReader(f))
        data = list(reader)

        evidence = []
        label = []

        # work through rows of imported csv data adjusting variable types as required
        for row in data:
            evidence_row = []
            row["Month"] = mth_str_to_num(row["Month"][:3])
            if row["VisitorType"] == "Returning_Visitor":
                row["VisitorType"] = 1
            else:
                row["VisitorType"] = 0
            for header in ["Revenue", "Weekend"]:
                if row[header] == "TRUE":
                    row[header] = 1
                else:
                    row[header] = 0
            for header in ["Administrative", "Informational", "ProductRelated", "OperatingSystems", "Browser", "Region", "TrafficType"]:
                row[header] = int(row[header])
            for header in ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]:
                row[header] = float(row[header])
            for header in row:
                if header == "Revenue":
                    label.append(row[header])
                else:
                    evidence_row.append(row[header])
            evidence.append(evidence_row)
    return (evidence, label)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence,labels)
    
    return neigh

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # define dicts to capture true positives and true negative actual vs predictions
    true_positives = {
        "labels": 0,
        "predictions": 0
    }

    true_negatives = {
        "labels": 0,
        "predictions": 0
    }

    label_num = range(len(labels))

    for label in label_num:
        if labels[label] == 1:
            true_positives["labels"] += 1
            true_positives["predictions"] += predictions[label]
        else:
            true_negatives["labels"] += 1
            true_negatives["predictions"] += 1 - predictions[label]

    # calc sensitivity and specificity rates
    sensitivity = true_positives["predictions"]/true_positives["labels"]
    specificity = true_negatives["predictions"]/true_negatives["labels"]

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
