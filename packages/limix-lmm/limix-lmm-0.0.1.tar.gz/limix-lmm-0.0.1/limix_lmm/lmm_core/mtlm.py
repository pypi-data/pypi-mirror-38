import scipy as sp
import scipy.stats as st
import scipy.linalg as la
import pdb
import time

def calc_Ai_beta_s2(yKiy, FF, AKiA, AoFKiY, df):
    Areml_c_inv = la.inv(AKiA)
    Areml_r_inv = la.inv(FF)
    B = sp.dot(sp.dot(Areml_r_inv, AoFKiY), Areml_c_inv.T)
    s2 = (yKiy - sp.einsum('ij,ij->', AoFKiY, B)) / df
    return Ai, beta, s2


class MTLM():
    """
    Parameters
    ----------
    y : (`N`, `P`) ndarray
        phenotype vector
    F : (`N`, `L`) ndarray
        fixed effect design for covariates.
    """
    def __init__(self, Y, F):
        if F is None:   F = sp.ones((y.shape[0],1))
        self.Y = Y
        self.F = F
        self.df = Y.size - (F.shape[1] * Y.shape[1])
        self.Cn_inv = la.inv(la.cov(Y.T) + 1e-4)
        self._fit_null()

    def _fit_null(self):
        """ Internal functon. Fits the null model """
        self.KiY = sp.dot(self.Y, self.Cn_inv.T)
        self.AoFKiY = sp.dot(self.F.T, self.KiY)
        self.FF = sp.dot(self.F.T, self.F)
        self.AKiA = self.Cn_inv
        self.yKiy = sp.dot(self.y[:,0], self.Kiy[:,0])
        # calc beta_F0 and s20
        self.A0i, self.beta_F0, self.s20 = calc_Ai_beta_s2(yKiy, FF, AKiA, AoFKiY, df)

    def process(self, G):
        r"""
        Fit genotypes one-by-one.

        Parameters
        ----------
        G : (`N`, `S`) ndarray
        Inter : (`N`, `M`) ndarray
            Matrix of `M` factors for `N` inds with which
            each variant interact
            By default, Inter is set to a matrix of ones.
        """
        pdb.set_trace()
        t0 = time.time()
        F1F1 = sp.zeros([self.F.shape[1] + 1, self.F.shape[1] + 1])
        F1F1[:F.shape[1], :F.shape[1]] = self.FF
        FG = sp.dot(F.T, G)
        GG = sp.einsum('is,is->s', G, G)
        AoF1KiY = sp.zeros([self.AoFKiY.shape[0]+1, self.AoFKiY.shape[1]])
        AoF1KiY[:-1,:] = self.AoFKiY
        AoGKiY = sp.dot(G.T, self.KiY)
        beta = sp.zeros([G.shape[1], self.Y.shape[1]])
        s2 = sp.zeros(s)
        for s in range(G.shape[1]):
            F1F1[:,-1] = FG[:,s]
            F1F1[-1,:] = FG[:,s]
            F1F1[-1,-1] = GG[s]
            AoF1KiY[-1,:] = AoGKiY[s,:]
            _, _B, _s2 = calc_Ai_beta_s2(yKiy, FF, AKiA, AoFKiY, df)
            beta[s, :] = _B[-1, :]
            s2[s] = _s2

        #dlml and pvs
        self.lrt = -self.df*sp.log(s2/self.s20)
        self.pv = st.chi2(m).sf(self.lrt)
        self.beta_g = beta

        t1 = time.time()
        if verbose:
            print('Tested for %d variants in %.2f s' % (G.shape[1],t1-t0))

        return self.pv, self.lrt

    def getPv(self):
        """
        Get pvalues

        Returns
        -------
        pv : ndarray
        """
        return self.pv

    def getBetaSNP(self):
        """
        get effect size SNPs


        Returns
        -------
        pv : ndarray
        """
        return self.beta_g

    def getBetaCov(self):
        """
        get beta of covariates

        Returns
        -------
        beta : ndarray
        """
        return self.beta_F

    def getLRT(self):
        """
        get lik ratio test statistics

        Returns
        -------
        lrt : ndarray
        """
        return self.lrt

    def getBetaSNPste(self):
        """
        get standard errors on betas

        Returns
        -------
        beta_ste : ndarray
        """
        beta = self.getBetaSNP()
        pv = self.getPv()
        z = sp.sign(beta) * sp.sqrt(st.chi2(1).isf(pv))
        ste = beta / z
        return ste
