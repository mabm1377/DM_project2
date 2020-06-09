from pre_process.utils import read_file2
from pre_process import utils
from sklearn import ensemble
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import BernoulliNB, GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import os
from core.vars import VARS
from tabulate import tabulate


def run_gaussian(x_train, x_test, y_train, y_test):
    gaussian = GaussianNB()
    gaussian.fit(x_train, y_train)
    y_pred = gaussian.predict(x_test)

    return accuracy_score(y_test, y_pred), f1_score(y_test, y_pred, average="macro")


def run_bernoulli(x_train, x_test, y_train, y_test):
    bernoulli = BernoulliNB()
    bernoulli.fit(x_train, y_train)
    y_pred = bernoulli.predict(x_test)
    return accuracy_score(y_test, y_pred), f1_score(y_test, y_pred, average="macro")


def run_decision_tree_classifier(x_train, x_test, y_train, y_test):
    accuracy_score_result = 0
    f1_score_result = 0
    for i in range(1, 16):
        decision_tree_classifier = DecisionTreeClassifier(max_depth=i)
        decision_tree_classifier.fit(x_train, y_train)
        y_pred = decision_tree_classifier.predict(x_test)
        if accuracy_score(y_test, y_pred) >= accuracy_score_result and f1_score(y_test, y_pred,
                                                                                average="macro") >= f1_score_result:
            accuracy_score_result = accuracy_score(y_test, y_pred)
            f1_score_result = f1_score(y_test, y_pred, average="macro")
    return accuracy_score_result, f1_score_result


def run_svm(x_train, x_test, y_train, y_test):
    svc = SVC()
    svc.fit(x_train, y_train)
    y_pred = svc.predict(x_test)
    return accuracy_score(y_test, y_pred), f1_score(y_test, y_pred, average="macro")


def run_random_forest(x_train, x_test, y_train, y_test):
    rn = ensemble.RandomForestClassifier()
    rn.fit(x_train, y_train)
    y_pred = rn.predict(x_test)
    return accuracy_score(y_test, y_pred), f1_score(y_test, y_pred, average="macro")


def run_algorithms(project_directory):
    df = read_file2(os.path.join(project_directory, "pre_process", "removed_outliers_qualitative_data.csv"))
    df = utils.convert_qualitative_data_to_quantitative(df, list(set(VARS.NAMES) - {"wealth"}), "te")
    data_without_target = df.drop(['wealth'], axis=1)
    target = df['wealth']
    x_train, x_test, y_train, y_test = train_test_split(data_without_target, target, test_size=0.3, random_state=0)
    table = []
    score, f1 = run_gaussian(x_train, x_test, y_train, y_test)
    table.append(["gaussian", score, f1])
    score, f1 = run_bernoulli(x_train, x_test, y_train, y_test)
    table.append(["bernoulli", score, f1])
    score, f1 = run_svm(x_train, x_test, y_train, y_test)
    table.append(["svm", score, f1])
    score, f1 = run_random_forest(x_train, x_test, y_train, y_test)
    table.append(["random_forest", score, f1])
    result_table = tabulate(table, headers=["algorithms", "accuracy_score", "f1_score"])
    with open(os.path.join(project_directory, "algorithms", "algorithms_results.txt"), "w") as algorithms_results:
        algorithms_results.write(result_table)
