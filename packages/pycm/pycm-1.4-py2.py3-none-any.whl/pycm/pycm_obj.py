# -*- coding: utf-8 -*-

from .pycm_func import *
from .pycm_output import *
import os
import json
import types
import numpy


class pycmVectorError(Exception):
    pass


class pycmMatrixError(Exception):
    pass


class ConfusionMatrix():
    '''
    Main Class Of ConfusionMatrix
    >>> y_actu = [2, 0, 2, 2, 0, 1, 1, 2, 2, 0, 1, 2]
    >>> y_pred = [0, 0, 2, 1, 0, 2, 1, 0, 2, 0, 2, 2]
    >>> cm = ConfusionMatrix(y_actu, y_pred)
    >>> cm.classes
    [0, 1, 2]
    >>> cm.table
    {0: {0: 3, 1: 0, 2: 0}, 1: {0: 0, 1: 1, 2: 2}, 2: {0: 2, 1: 1, 2: 3}}
    >>> cm2 = ConfusionMatrix(matrix={"Class1": {"Class1": 1, "Class2":2},"Class2": {"Class1": 0, "Class2": 5}})
    >>> cm2
    pycm.ConfusionMatrix(classes: ['Class1', 'Class2'])
    '''

    def __init__(
            self,
            actual_vector=None,
            predict_vector=None,
            matrix=None,
            digit=5, threshold=None, file=None,
            sample_weight=None, transpose=False):
        '''
        :param actual_vector: Actual Vector
        :type actual_vector: python list or numpy array of any stringable objects
        :param predict_vector: Predicted Vector
        :type predict_vector: python list or numpy array of any stringable objects
        :param matrix: direct matrix
        :type matrix: dictionary
        :type matrix: dict
        :param digit: precision digit (default value : 5)
        :type digit : int
        :param threshold : activation threshold function
        :type threshold : FunctionType (function or lambda)
        :param file : saved confusion matrix file object
        :type file : (io.IOBase & file)
        :param sample_weight : sample weights list
        :type sample_weight : list
        :param transpose : transpose flag
        :type transpose : bool
        '''
        self.actual_vector = actual_vector
        self.predict_vector = predict_vector
        self.digit = digit
        self.weights = None
        if isfile(file):
            obj_data = json.load(file)
            if obj_data["Actual-Vector"] is not None and obj_data[
                    "Predict-Vector"] is not None:
                try:
                    loaded_weights = obj_data["Sample-Weight"]
                except Exception:
                    loaded_weights = None
                matrix_param = matrix_params_calc(obj_data[
                    "Actual-Vector"],
                    obj_data[
                    "Predict-Vector"], loaded_weights)
                self.actual_vector = obj_data["Actual-Vector"]
                self.predict_vector = obj_data["Predict-Vector"]
                self.weights = loaded_weights
            else:
                try:
                    loaded_transpose = obj_data["Transpose"]
                except Exception:
                    loaded_transpose = False
                self.transpose = loaded_transpose
                matrix_param = matrix_params_from_table(obj_data[
                    "Matrix"], loaded_transpose)
            self.digit = obj_data["Digit"]
        elif isinstance(matrix, dict):
            if matrix_check(matrix):
                if class_check(list(matrix.keys())) == False:
                    raise pycmMatrixError(
                        "Input Matrix Classes Must Be Same Type")
                else:
                    matrix_param = matrix_params_from_table(matrix, transpose)
            else:
                raise pycmMatrixError("Input Confusion Matrix Format Error")
        else:
            if isinstance(threshold, types.FunctionType):
                predict_vector = list(map(threshold, predict_vector))
                self.predict_vector = predict_vector
            if not isinstance(actual_vector, (list, numpy.ndarray)) or not\
                    isinstance(predict_vector, (list, numpy.ndarray)):
                raise pycmVectorError("Input Vectors Must Be List")
            if len(actual_vector) != len(predict_vector):
                raise pycmVectorError("Input Vectors Must Be The Same Length")
            if len(actual_vector) == 0 or len(predict_vector) == 0:
                raise pycmVectorError("Input Vectors Are Empty")
            [actual_vector, predict_vector] = vector_filter(
                actual_vector, predict_vector)
            matrix_param = matrix_params_calc(
                actual_vector, predict_vector, sample_weight)
            if isinstance(sample_weight, list):
                self.weights = sample_weight
            if isinstance(sample_weight, numpy.ndarray):
                self.weights = sample_weight.tolist()
        if isinstance(transpose, bool):
            self.transpose = transpose
        else:
            self.transpose = False
        if len(matrix_param[0]) < 2:
            raise pycmVectorError("Number Of Classes < 2")
        self.classes = matrix_param[0]
        self.table = matrix_param[1]
        self.TP = matrix_param[2]
        self.TN = matrix_param[3]
        self.FP = matrix_param[4]
        self.FN = matrix_param[5]
        statistic_result = class_statistics(
            TP=matrix_param[2],
            TN=matrix_param[3],
            FP=matrix_param[4],
            FN=matrix_param[5],
            classes=matrix_param[0],
            table=matrix_param[1])
        self.class_stat = statistic_result
        self.overall_stat = overall_statistics(
            RACC=statistic_result["RACC"],
            RACCU=statistic_result["RACCU"],
            TPR=statistic_result["TPR"],
            PPV=statistic_result["PPV"],
            TP=statistic_result["TP"],
            FN=statistic_result["FN"],
            FP=statistic_result["FP"],
            POP=statistic_result["POP"],
            P=statistic_result["P"],
            TOP=statistic_result["TOP"],
            jaccard_list=statistic_result["J"],
            classes=self.classes,
            table=self.table,
            CEN_dict=statistic_result["CEN"],
            MCEN_dict=statistic_result["MCEN"],
            AUC_dict=statistic_result["AUC"])
        self.TPR = statistic_result["TPR"]
        self.TNR = statistic_result["TNR"]
        self.PPV = statistic_result["PPV"]
        self.NPV = statistic_result["NPV"]
        self.FNR = statistic_result["FNR"]
        self.FPR = statistic_result["FPR"]
        self.FDR = statistic_result["FDR"]
        self.FOR = statistic_result["FOR"]
        self.ACC = statistic_result["ACC"]
        self.F1 = statistic_result["F1"]
        self.MCC = statistic_result["MCC"]
        self.BM = statistic_result["BM"]
        self.MK = statistic_result["MK"]
        self.DOR = statistic_result["DOR"]
        self.PLR = statistic_result["LR+"]
        self.NLR = statistic_result["LR-"]
        self.POP = statistic_result["POP"]
        self.P = statistic_result["P"]
        self.N = statistic_result["N"]
        self.TOP = statistic_result["TOP"]
        self.TON = statistic_result["TON"]
        self.PRE = statistic_result["PRE"]
        self.G = statistic_result["G"]
        self.RACC = statistic_result["RACC"]
        self.RACCU = statistic_result["RACCU"]
        self.F2 = statistic_result["F2"]
        self.F05 = statistic_result["F0.5"]
        self.ERR = statistic_result["ERR"]
        self.J = statistic_result["J"]
        self.IS = statistic_result["IS"]
        self.CEN = statistic_result["CEN"]
        self.MCEN = statistic_result["MCEN"]
        self.AUC = statistic_result["AUC"]
        self.dInd = statistic_result["dInd"]
        self.sInd = statistic_result["sInd"]
        self.Overall_J = self.overall_stat["Overall_J"]
        self.SOA1 = self.overall_stat["Strength_Of_Agreement(Landis and Koch)"]
        self.SOA2 = self.overall_stat["Strength_Of_Agreement(Fleiss)"]
        self.SOA3 = self.overall_stat["Strength_Of_Agreement(Altman)"]
        self.SOA4 = self.overall_stat["Strength_Of_Agreement(Cicchetti)"]
        self.Kappa = self.overall_stat["Kappa"]
        self.Overall_ACC = self.overall_stat["Overall_ACC"]
        self.TPR_Macro = self.overall_stat["TPR_Macro"]
        self.PPV_Macro = self.overall_stat["PPV_Macro"]
        self.TPR_Micro = self.overall_stat["TPR_Micro"]
        self.PPV_Micro = self.overall_stat["PPV_Micro"]
        self.Overall_RACC = self.overall_stat["Overall_RACC"]
        self.Overall_RACCU = self.overall_stat["Overall_RACCU"]
        self.PI = self.overall_stat["Scott_PI"]
        self.AC1 = self.overall_stat["Gwet_AC1"]
        self.S = self.overall_stat["Bennett_S"]
        self.Kappa_SE = self.overall_stat["Kappa Standard Error"]
        self.Kappa_CI = self.overall_stat["Kappa 95% CI"]
        self.Chi_Squared = self.overall_stat["Chi-Squared"]
        self.Phi_Squared = self.overall_stat["Phi-Squared"]
        self.KappaUnbiased = self.overall_stat["Kappa Unbiased"]
        self.KappaNoPrevalence = self.overall_stat["Kappa No Prevalence"]
        self.V = self.overall_stat["Cramer_V"]
        self.DF = self.overall_stat["Chi-Squared DF"]
        self.CI = self.overall_stat["95% CI"]
        self.SE = self.overall_stat["Standard Error"]
        self.ReferenceEntropy = self.overall_stat["Reference Entropy"]
        self.ResponseEntropy = self.overall_stat["Response Entropy"]
        self.CrossEntropy = self.overall_stat["Cross Entropy"]
        self.JointEntropy = self.overall_stat["Joint Entropy"]
        self.ConditionalEntropy = self.overall_stat["Conditional Entropy"]
        self.MutualInformation = self.overall_stat["Mutual Information"]
        self.KL = self.overall_stat["KL Divergence"]
        self.LambdaB = self.overall_stat["Lambda B"]
        self.LambdaA = self.overall_stat["Lambda A"]
        self.HammingLoss = self.overall_stat["Hamming Loss"]
        self.ZeroOneLoss = self.overall_stat["Zero-one Loss"]
        self.NIR = self.overall_stat["NIR"]
        self.PValue = self.overall_stat["P-Value"]
        self.Overall_CEN = self.overall_stat["Overall_CEN"]
        self.Overall_MCEN = self.overall_stat["Overall_MCEN"]
        self.Overall_MCC = self.overall_stat["Overall_MCC"]
        self.RR = self.overall_stat["RR"]
        self.CBA = self.overall_stat["CBA"]
        self.AUNU = self.overall_stat["AUNU"]
        self.AUNP = self.overall_stat["AUNP"]

    def matrix(self, one_vs_all=False, class_name=None):
        '''
        This method print confusion matrix
        :param one_vs_all : One-Vs-All mode flag
        :type one_vs_all : bool
        :param class_name : target class name for One-Vs-All mode
        :type class_name : any valid type
        :return: None
        '''
        classes = self.classes
        table = self.table
        if one_vs_all:
            [classes, table] = one_vs_all_func(
                classes, table, self.TP, self.TN, self.FP, self.FN, class_name)
        print(table_print(classes, table))

    def normalized_matrix(self, one_vs_all=False, class_name=None):
        '''
        This method print normalized confusion matrix
        :param one_vs_all : One-Vs-All mode flag
        :type one_vs_all : bool
        :param class_name : target class name for One-Vs-All mode
        :type class_name : any valid type
        :return: None
        '''
        classes = self.classes
        table = self.table
        if one_vs_all:
            [classes, table] = one_vs_all_func(
                classes, table, self.TP, self.TN, self.FP, self.FN, class_name)
        print(normalized_table_print(classes, table))

    def stat(self):
        '''
        This method print statistical measures table
        :return: None
        '''
        print(
            stat_print(
                self.classes,
                self.class_stat,
                self.overall_stat,
                self.digit))

    def __str__(self):
        '''
        ConfusionMatrix object string representation method
        :return: representation as str (matrix + params)
        '''
        result = table_print(self.classes, self.table)
        result += "\n" * 4
        result += stat_print(self.classes, self.class_stat,
                             self.overall_stat, self.digit)
        return result

    def save_stat(self, name, address=True):
        try:
            message = None
            file = open(name + ".pycm", "w")
            matrix = "Matrix : \n\n" + table_print(self.classes,
                                                   self.table) + "\n\n"
            normalized_matrix = "Normalized Matrix : \n\n" + \
                                normalized_table_print(self.classes,
                                                       self.table) + "\n\n"
            one_vs_all = "\nOne-Vs-All : \n\n"
            for class_name in self.classes:
                one_vs_all += str(class_name) + "-Vs-All : \n\n"
                [classes, table] = one_vs_all_func(self.classes, self.table,
                                                   self.TP, self.TN, self.FP,
                                                   self.FN, class_name)
                one_vs_all += table_print(classes, table) + "\n\n"
            stat = stat_print(
                self.classes,
                self.class_stat,
                self.overall_stat,
                self.digit)
            file.write(matrix + normalized_matrix + stat + one_vs_all)
            file.close()
            if address:
                message = os.path.join(os.getcwd(), name + ".pycm")
            return {"Status": True, "Message": message}
        except Exception as e:
            return {"Status": False, "Message": str(e)}

    def save_html(self, name, address=True):
        try:
            message = None
            html_file = open(name + ".html", "w")
            html_maker(
                html_file,
                name,
                self.classes,
                self.table,
                self.overall_stat,
                self.class_stat,
                self.digit)
            html_file.close()
            if address:
                message = os.path.join(os.getcwd(), name + ".html")
            return {"Status": True, "Message": message}
        except Exception as e:
            return {"Status": False, "Message": str(e)}

    def save_csv(self, name, address=True):
        try:
            message = None
            csv_file = open(name + ".csv", "w")
            csv_data = csv_print(self.classes, self.class_stat, self.digit)
            csv_file.write(csv_data)
            if address:
                message = os.path.join(os.getcwd(), name + ".csv")
            return {"Status": True, "Message": message}
        except Exception as e:
            return {"Status": False, "Message": str(e)}

    def save_obj(self, name, address=True):
        try:
            message = None
            obj_file = open(name + ".obj", "w")
            actual_vector_temp = self.actual_vector
            predict_vector_temp = self.predict_vector
            if isinstance(actual_vector_temp, numpy.ndarray):
                actual_vector_temp = actual_vector_temp.tolist()
            if isinstance(predict_vector_temp, numpy.ndarray):
                predict_vector_temp = predict_vector_temp.tolist()
            json.dump({"Actual-Vector": actual_vector_temp,
                       "Predict-Vector": predict_vector_temp,
                       "Matrix": self.table,
                       "Digit": self.digit,
                       "Sample-Weight": self.weights,
                       "Transpose": self.transpose}, obj_file)
            if address:
                message = os.path.join(os.getcwd(), name + ".obj")
            return {"Status": True, "Message": message}
        except Exception as e:
            return {"Status": False, "Message": str(e)}

    def F_beta(self, Beta):
        try:
            F_Dict = {}
            for i in self.TP.keys():
                F_Dict[i] = F_calc(
                    TP=self.TP[i],
                    FP=self.FP[i],
                    FN=self.FN[i],
                    Beta=Beta)
            return F_Dict
        except Exception:
            return {}

    def __repr__(self):
        '''
        ConfusionMatrix object representation method
        :return: representation as str
        '''
        return "pycm.ConfusionMatrix(classes: " + str(self.classes) + ")"
