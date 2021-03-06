import numpy as np
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix

from svm_plot import plot_svm_decision_boundary, plot_score_vs_degree, plot_score_vs_gamma, plot_mnist, \
    plot_confusion_matrix

"""
Computational Intelligence TU - Graz
Assignment 3: Support Vector Machine, Kernels & Multiclass classification
Part 1: SVM, Kernels

TODOS are all contained here.
"""

__author__ = 'bellec,subramoney'


def ex_1_a(x, y):
    """
    Solution for exercise 1 a)
    :param x: The x values
    :param y: The y values
    :return:
    """
    ###########
    ## Train an SVM with a linear kernel
    ## and plot the decision boundary and support vectors using 'plot_svm_decision_boundary' function
    ###########

    clf = svm.SVC(kernel='linear')
    clf.fit(x, y)
    plot_svm_decision_boundary(clf, x, y)
    pass


def ex_1_b(x, y):
    """
    Solution for exercise 1 b)
    :param x: The x values
    :param y: The y values
    :return:
    """
    ###########
    ## Add a point (4,0) with label 1 to the data set and then
    ## train an SVM with a linear kernel
    ## and plot the decision boundary and support vectors using 'plot_svm_decision_boundary' function
    ###########
    new_x = np.vstack((x, np.array([4,0])))
    new_y = np.hstack((y, np.array((1))))

    clf = svm.SVC(kernel='linear')
    clf.fit(new_x, new_y)
    plot_svm_decision_boundary(clf, new_x, new_y)
    pass


def ex_1_c(x, y):
    """
    Solution for exercise 1 c)
    :param x: The x values
    :param y: The y values
    :return:
    """
    ###########
    ## Add a point (4,0) with label 1 to the data set and then
    ## train an SVM with a linear kernel with different values of C
    ## and plot the decision boundary and support vectors  for each using 'plot_svm_decision_boundary' function
    ###########
    Cs = [1e6, 1, 0.1, 0.001]
    new_x = np.vstack((x, np.array([4,0])))
    new_y = np.hstack((y, np.array((1))))

    for c in Cs:
        clf = svm.SVC(kernel='linear', C=c)
        clf.fit(new_x, new_y)
        plot_svm_decision_boundary(clf, new_x, new_y)
    return


def ex_2_a(x_train, y_train, x_test, y_test):
    """
    Solution for exercise 2 a)
    :param x_train: Training samples (2-dimensional)
    :param y_train: Training labels
    :param x_test: Testing samples (2-dimensional)
    :param y_test: Testing labels
    :return:
    """
    ###########
    ## TODO:
    ## Train an SVM with a linear kernel for the given dataset
    ## and plot the decision boundary and support vectors  for each using 'plot_svm_decision_boundary' function
    ###########

    machine = svm.SVC(kernel='linear')
    machine.fit(x_train, y_train)
    plot_svm_decision_boundary(machine, x_train, y_train, x_test, y_test)

    print('Linear SVM score: {}'.format(machine.score(x_test, y_test)))


def ex_2_b(x_train, y_train, x_test, y_test):
    """
    Solution for exercise 2 b)
    :param x_train: Training samples (2-dimensional)
    :param y_train: Training labels
    :param x_test: Testing samples (2-dimensional)
    :param y_test: Testing labels
    :return:
    """
    ###########
    ## TODO:
    ## Train SVMs with polynomial kernels for different values of the degree
    ## (Remember to set the 'coef0' parameter to 1)
    ## and plot the variation of the test and training scores with polynomial degree using 'plot_score_vs_degree' func.
    ## Plot the decision boundary and support vectors for the best value of degree
    ## using 'plot_svm_decision_boundary' function
    ###########

    degrees = range(1, 21)
    machines = [svm.SVC(kernel='poly', degree=d, coef0=1.0) for d in degrees]

    for machine in machines:
        machine.fit(x_train, y_train)

    trainScores = [machine.score(x_train, y_train) for machine in machines]
    testScores = [machine.score(x_test, y_test) for machine in machines]

    plot_score_vs_degree(trainScores, testScores, degrees)

    bestDegree = testScores.index(max(testScores))
    print('Score of best polynomial degree ({}): {}'.format(bestDegree + 1, testScores[bestDegree]))
    plot_svm_decision_boundary(machines[bestDegree], x_train, y_train, x_test, y_test)


def ex_2_c(x_train, y_train, x_test, y_test):
    """
    Solution for exercise 2 c)
    :param x_train: Training samples (2-dimensional)
    :param y_train: Training labels
    :param x_test: Testing samples (2-dimensional)
    :param y_test: Testing labels
    :return:
    """
    ###########
    ## TODO:
    ## Train SVMs with RBF kernels for different values of the gamma
    ## and plot the variation of the test and training scores with gamma using 'plot_score_vs_gamma' function.
    ## Plot the decision boundary and support vectors for the best value of gamma
    ## using 'plot_svm_decision_boundary' function
    ###########
    gammas = np.arange(0.01, 2, 0.02)
    machines = [svm.SVC(kernel='rbf', gamma=g, coef0=1.0) for g in gammas]

    for machine in machines:
        machine.fit(x_train, y_train)

    trainScores = [machine.score(x_train, y_train) for machine in machines]
    testScores = [machine.score(x_test, y_test) for machine in machines]

    plot_score_vs_gamma(trainScores, testScores, gammas)

    bestGamma = np.argmax(testScores)
    print('Score of best rbf gamma ({}): {}'.format(gammas[bestGamma], testScores[bestGamma]))
    plot_svm_decision_boundary(machines[bestGamma], x_train, y_train, x_test, y_test)


def ex_3_a(x_train, y_train, x_test, y_test):
    """
    Solution for exercise 3 a)
    :param x_train: Training samples (2-dimensional)
    :param y_train: Training labels
    :param x_test: Testing samples (2-dimensional)
    :param y_test: Testing labels
    :return:
    """
    ###########
    ## Train multi-class SVMs with one-versus-rest strategy with
    ## - linear kernel
    ## - rbf kernel with gamma going from 10**-5 to 10**5
    ## - plot the scores with varying gamma using the function plot_score_versus_gamma
    ## - Mind that the chance level is not .5 anymore and add the score obtained with the linear kernel as optional argument of this function
    ###########
    dfs = 'ovr'
    c = 10

    linear = svm.SVC(kernel='linear', C=c, decision_function_shape=dfs)
    linear.fit(x_train, y_train)
    lin_score_train = linear.score(x_train, y_train)
    lin_score_test = linear.score(x_test, y_test)

    gammas = [pow(10, i) for i in range(-5, 6)]
    rbfs = [svm.SVC(kernel='rbf', gamma=gamma, C=c, decision_function_shape=dfs) for gamma in gammas]
    for rbf in rbfs:
        rbf.fit(x_train, y_train)

    train_scores = [rbf.score(x_train, y_train) for rbf in rbfs]
    test_scores = [rbf.score(x_test, y_test) for rbf in rbfs]

    plot_score_vs_gamma(train_scores, test_scores, gammas, lin_score_train, lin_score_test, .2)




def ex_3_b(x_train, y_train, x_test, y_test):
    """
    Solution for exercise 3 b)
    :param x_train: Training samples (2-dimensional)
    :param y_train: Training labels
    :param x_test: Testing samples (2-dimensional)
    :param y_test: Testing labels
    :return:
    """
    ###########
    ## Train multi-class SVMs with a LINEAR kernel
    ## Use the sklearn.metrics.confusion_matrix to plot the confusion matrix.
    ## Find the index for which you get the highest error rate.
    ## Plot the confusion matrix with plot_confusion_matrix.
    ## Plot the first 10 occurrences of the most misclassified digit using plot_mnist.
    ###########

    labels = range(1, 6)
    linear = svm.SVC(kernel='linear', C=10, decision_function_shape='ovr')
    linear.fit(x_train, y_train)
    y_pred = linear.predict(x_test)
    cm = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(cm, labels)

    errors = np.zeros(5)
    for i in range(5):
        for j in range(5):
            if i != j:
                errors[j] += cm[i][j]
    max_err_label = np.argmax(errors) + 1  # should be the label number corresponding the largest classification error

    indices = np.nonzero(y_pred == max_err_label)[0].astype(int)
    sel_err = np.array([], dtype=int)  # Numpy indices to select images that are misclassified.
    for i in indices:
        if y_test[i] != y_pred[i]:
            sel_err = np.insert(sel_err, sel_err.size, i)

    # Plot with mnist plot
    plot_mnist(x_test[sel_err], y_pred[sel_err], labels=max_err_label, k_plots=10, prefix='Predicted class')
