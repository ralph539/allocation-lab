import os
from dataclasses import dataclass, field
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = Path(os.environ.get("ALLOC_DB", ROOT / "data" / "store.duckdb"))
CONFIG = Path(os.environ.get("ALLOC_CONFIG", ROOT / "config" / "universe.yaml"))
TIERS = ["conservative", "balanced", "growth", "aggressive"]

EM_NAME = "Equity - Emerging / Asia"
AI_NAME = "Equity - Thematic AI / automation"
GOLD_NAME = "Gold"
HY_NAME = "Fixed income - High yield"
EMD_NAME = "Fixed income - EM debt"
CASH_NAME = "Cash / money market"


@dataclass(frozen=True)
class EngineConfig:
    sleeves: list          # full 15, for reporting
    funded: list           # 14 funded names, column order
    tier_w: dict           # tier -> np.array over funded (fractions)
    caps: dict
    eq_idx: np.ndarray
    em_idx: int
    ai_idx: int
    gold_idx: int
    hyemd_idx: np.ndarray
    params: dict = field(default_factory=dict)
    variant: str = "house"

    def idx(self, name: str) -> int:
        return self.funded.index(name)


def load_config(path: Path = CONFIG, variant: str = "house", **params) -> EngineConfig:
    u = yaml.safe_load(open(path))
    funded = [s["name"] for s in u["sleeves"] if s["proxy"]]
    v = u["variants"][variant]
    tier_w = {t: np.array([v["weights"][t][n] for n in funded], float) / 100 for t in TIERS}
    caps = {**u["caps"], "equity_band": v["equity_band"]}
    eq_idx = np.array([i for i, s in enumerate(_funded_sleeves(u))
                       if s["bucket"] == "Equity"])
    p = dict(window=756, cvar_alpha=0.95, delta=2.5, tau=0.05, kappa=0.005,
             band=0.10, rf=0.0)
    p.update(params)
    return EngineConfig(
        sleeves=u["sleeves"], funded=funded, tier_w=tier_w, caps=caps,
        eq_idx=eq_idx, em_idx=funded.index(EM_NAME), ai_idx=funded.index(AI_NAME),
        gold_idx=funded.index(GOLD_NAME),
        hyemd_idx=np.array([funded.index(HY_NAME), funded.index(EMD_NAME)]),
        params=p, variant=variant)


def load_returns(config: EngineConfig, db: Path = DB) -> pd.DataFrame:
    con = duckdb.connect(str(db), read_only=True)
    try:
        df = con.execute("select date, sleeve, ret from sleeve_returns").df()
    finally:
        con.close()
    wide = df.pivot(index="date", columns="sleeve", values="ret")
    return wide.reindex(columns=config.funded).sort_index()


def _funded_sleeves(u: dict) -> list:
    return [s for s in u["sleeves"] if s["proxy"]]
