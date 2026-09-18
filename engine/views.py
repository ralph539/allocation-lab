import numpy as np

# short key -> funded sleeve name
NAME = {
    "US": "Equity - US", "EU": "Equity - Europe",
    "AP": "Equity - Developed Asia-Pacific / Japan", "EM": "Equity - Emerging / Asia",
    "AI": "Equity - Thematic AI / automation", "GOV": "Fixed income - Govt / core",
    "IG": "Fixed income - IG credit", "IL": "Fixed income - Inflation-linked",
    "HY": "Fixed income - High yield", "EMD": "Fixed income - EM debt",
    "GLD": "Gold", "ALT": "Liquid alternatives / hedge funds",
    "RE": "Real assets / REITs / infrastructure",
}


def momentum_stance(R: np.ndarray, config) -> np.ndarray:
    # point-in-time BL views: cross-sectional 12-1m momentum z-scores, computed only
    # from returns up to T, so no hindsight enters the posterior.
    from engine.overlays import momentum_score
    m = momentum_score(R)
    z = (m - m.mean()) / (m.std() + 1e-9)
    return np.clip(z, -2.0, 2.0)


def build_views(s: np.ndarray, Pi: np.ndarray, Sigma: np.ndarray, config):
    active = np.where(s != 0)[0]
    P = np.eye(len(s))[active]
    kappa, tau = config.params["kappa"], config.params["tau"]
    Q = Pi[active] + np.clip(kappa * s[active], -0.03, 0.03)
    Omega = np.diag([(tau / abs(s[i])) * Sigma[i, i] for i in active])
    return P, Q, Omega


def bl_posterior(Pi, Sigma, P, Q, Omega, tau: float) -> np.ndarray:
    if len(P) == 0:
        return Pi
    tauS = tau * Sigma
    mid = P @ tauS @ P.T + Omega
    return Pi + tauS @ P.T @ np.linalg.solve(mid, Q - P @ Pi)
