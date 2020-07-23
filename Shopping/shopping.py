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



def load_data(filename):
    """p_predict = p_predict + 1
            if y is 1:
                p_identified = p_identified + 1
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
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        Month = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}
        VisitorType = {"Returning_Visitor": 1, "New_Visitor": 0}
        Labels = {"TRUE": 1, "FALSE": 0}
        Weekend = {"TRUE": 1, "FALSE": 0}
        evidence = []
        labels = []
        for x in reader:
            tmp = x[::]
            arr1 = [0,2,4,11,12,13,14]
            arr2 = [1,3,5,6,7,8,9]
            for p in arr1:
                tmp[p] = int(tmp[p])
            for p in arr2:
                tmp[p] = float(tmp[p])

            tmp[10] = Month[tmp[10]]
            tmp[16] = Weekend[tmp[16]]
            if tmp[15] not in VisitorType.keys():
                tmp[15] = 0
            else:
                tmp[15] = VisitorType[tmp[15]]
            tmp[17] = Labels[tmp[17]]
            evidence.append(tmp[:17])
            labels.append(tmp[17])
        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    Kmodel = KNeighborsClassifier(n_neighbors = 1)
    return Kmodel.fit(evidence, labels)


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
    p_predict = 0
    n_predict = 0
    p_identified = 0
    n_identified = 0
    for label, prediction in zip(labels, predictions):
        if label == 0:
            n_predict = n_predict + 1
            if prediction == 0:
                n_identified = n_identified + 1

        elif label == 1:
            p_predict = p_predict + 1
            if prediction == 1:
                p_identified = p_identified + 1

        else:
            raise ValueError
    sensitivity = float(p_identified /p_predict)
    specificity = float(n_identified/n_predict)

    return (sensitivity, specificity)



if __name__ == "__main__":
    main()
