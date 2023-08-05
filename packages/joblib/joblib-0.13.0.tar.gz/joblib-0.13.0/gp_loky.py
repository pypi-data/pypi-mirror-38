import numpy as np




def evaluateModel(C, gamma):
    clf = SVC(C=10**C, gamma=10**gamma)
    return np.average(cross_val_score(clf, X, y))

if __name__ == "__main__":
    import joblib
    import multiprocessing as mp
    mp.set_start_method('loky_init_main')
    
    from sklearn.datasets import make_moons
    from sklearn.svm import SVC
    from sklearn.model_selection import cross_val_score

    np.random.seed(20)
    X, y = make_moons(n_samples = 200, noise = 0.3) # Data and target


    params = {'C':      ('cont', (-4, 5)),
            'gamma':  ('cont', (-4, 5))
            }

    from pyGPGO.surrogates.GaussianProcess import GaussianProcess
    from pyGPGO.covfunc import squaredExponential
    sexp = squaredExponential()
    gp = GaussianProcess(sexp)

    from pyGPGO.acquisition import Acquisition
    acq = Acquisition(mode = 'ExpectedImprovement')

    from pyGPGO.GPGO import GPGO



    with joblib.parallel_backend("loky"):
        gpgo = GPGO(gp, acq, evaluateModel, params, n_jobs=2)
        gpgo.run(max_iter = 20)
