# Allocation Lab

Multi-asset portfolio construction, walk-forward tested across 23 years and 40 allocation methods.

**Live dashboard:** https://allocation-lab.streamlit.app

![Single run view](docs/img/single_run.png)

Four risk tiers on a 14-sleeve ETF universe, solved monthly by a mean-CVaR linear program under hard concentration caps. One walk-forward pass per method, never re-fitted, with costs. Every configuration counted as a trial, every Sharpe deflated for the number of tries.

## Results

Long test, October 2003 to July 2026, house weights, 60/40 benchmark run through the same loop.

![Findings](docs/img/findings.png)

| | |
| --- | --- |
| **Value sits in the constraint, not the forecast** | Conservative tier: Sharpe 0.83 vs 0.62 for the 60/40, max drawdown -14% vs -36%, alpha +1.8% a year. Alpha falls tier by tier and turns negative on growth and aggressive |
| **Aggressive outperformance is beta** | +713% vs +479% for the 60/40, but beta 1.41 and alpha -0.6%. A 60/40 levered to the same beta ends higher (USD 9.38m vs 8.06m), with a better Sharpe (0.62 vs 0.56) and a smaller drawdown |
| **Overlays win 7 of 8 crises** | Dual momentum: -2.6% in the 2008 crisis vs -35.6%. Trend plus momentum: -5.0% in the 2022 rate shock vs -21.7%, because the filter exits bonds too. In calm blocks the 60/40 wins 2 of 5 |
| **Diversification beats optimisation** | Equal weight on the 14 sleeves, no estimation at all: Sharpe 0.75. Risk-only methods that never see expected returns top the board: max diversification 0.96, risk parity 0.89 |
| **Nothing clears the multiple-testing bar on four years** | 286 configurations, luck threshold Sharpe 0.57, best run 0.57, deflated Sharpe 56% against 95% required. The benchmark fails the same gate. Hence the 23-year tests |

### By tier

| Configuration | CAGR | Vol | Sharpe | Max DD | Beta | Alpha |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 60/40 benchmark | 8.07% | 10.77% | 0.62 | -36.3% | 1.00 | 0.00% |
| Dual momentum, conservative | 4.67% | 3.29% | 0.88 | -7.9% | 0.14 | +1.95% |
| Mean-CVaR, conservative | 5.05% | 3.95% | 0.83 | -14.2% | 0.23 | +1.76% |
| Max return under CVaR cap, conservative | 6.04% | 5.65% | 0.76 | -21.8% | 0.41 | +1.61% |
| Mean-CVaR, balanced | 7.25% | 8.85% | 0.64 | -32.4% | 0.80 | +0.40% |
| Max return under CVaR cap, balanced | 7.91% | 10.30% | 0.63 | -37.4% | 0.93 | +0.27% |
| Mean-CVaR, growth | 8.28% | 12.09% | 0.58 | -42.4% | 1.10 | -0.29% |
| Max return under CVaR cap, growth | 9.01% | 13.30% | 0.59 | -45.8% | 1.21 | -0.19% |
| Mean-CVaR, aggressive | 8.95% | 14.74% | 0.54 | -50.1% | 1.33 | -0.89% |
| Max return under CVaR cap, aggressive | 9.70% | 15.56% | 0.56 | -51.3% | 1.41 | -0.59% |

### Risk-only references, same 14 sleeves

| Method | CAGR | Vol | Sharpe | Max DD | Alpha |
| --- | ---: | ---: | ---: | ---: | ---: |
| Max diversification | 5.58% | 3.97% | 0.96 | -14.6% | +2.18% |
| Risk parity | 5.91% | 4.66% | 0.89 | -19.1% | +1.85% |
| Inverse volatility | 6.14% | 5.24% | 0.84 | -22.7% | +1.56% |
| Hierarchical risk parity | 4.59% | 3.41% | 0.83 | -16.8% | +1.76% |
| Equal weight | 8.35% | 8.98% | 0.75 | -29.6% | +1.44% |
| Min variance | 3.87% | 2.91% | 0.73 | -13.2% | +1.35% |

### Crisis windows, balanced tier

| Window | Best method | Return | 60/40 | Gap |
| --- | --- | ---: | ---: | ---: |
| GFC 2008 | Dual momentum | -2.6% | -35.6% | +33.0 pts |
| Rate shock 2022 | Trend tilt + dual momentum | -5.0% | -21.7% | +16.7 pts |
| Q4 2018 selloff | Regime breaker | -5.3% | -11.3% | +6.0 pts |
| Euro crisis 2011 | Vol target | -5.1% | -10.5% | +5.5 pts |
| China shock 2015 | Trend tilt + regime breaker | -4.1% | -8.2% | +4.1 pts |
| COVID 2020 | Max return under CVaR cap, relaxed caps | -6.3% | -7.0% | +0.7 pts |
| Banking stress 2023 | Max return under CVaR cap | +4.0% | +3.6% | +0.3 pts |
| Taper tantrum 2013 | Max return under CVaR cap, relaxed caps | -2.0% | -1.3% | -0.7 pts |

The winner changes with the window. The full scoreboard's best Sharpe is the maximum over 136 correlated runs, and the dashboard labels it as the luckiest draw as much as the best method.

### What the caps cost

Six constraint layers, from the full policy down to long-only. Fully uncapped, the aggressive tier reaches +2,421% at a Sharpe of 0.89 while holding up to 93% in one sleeve (median 48%). On the four-year ETF universe the same configuration delivers a Sharpe of 0.32, a -32% drawdown and 6.2x annual turnover. The gap between capped and uncapped is the price of the governance, measured.

### Input experiments

One estimator changed at a time, parameters fixed before any result was seen. Scored on 2011 to 2026, balanced tier.

| Experiment | Change | Sharpe | Turnover | Verdict |
| --- | --- | ---: | ---: | --- |
| Base | 3-year window | 0.69 | 1.26x | reference |
| 5-year window | longer lookback | 0.72 | 0.98x | adopted; 0.71 to 0.76 on the second universe |
| 10-year window | longer still | 0.67 | 0.46x | reverses; staleness overtakes sampling error between 5 and 10 years |
| EWMA scenarios | lambda 0.97 | 0.68 | 3.93x | rejected; 66 effective days, tail on three observations |
| Yield-anchored mu | cash rate plus shrunk premia | 0.64 | 0.67x | rejected at 10 bps; halved turnover could flip it at real costs |

Autocorrelation on this data: daily returns -0.075, absolute returns +0.270, monthly turbulence +0.660. Risk is forecastable, direction is not. In 2022 the trailing window still put the stock-bond correlation at -0.38 against a realised +0.14.

## Dashboard

![Which optimizer won](docs/img/which_optimizer_won.png)

Reads a precomputed store, so every control recomputes on the fly.

| Control | Options |
| --- | --- |
| Universe | ETF universe 2022 to 2026, two long tests 2003 to 2026 |
| Period | Full history, five calendar blocks, eight crisis windows; every number and chart follows it |
| Group and config | Baseline, house core, offense, risk-off overlays, combinations, cap regimes, input experiments, risk-only references |
| Tier | Conservative, balanced, growth, aggressive |
| Weight variant | The policy ladder and four stressed versions |

Views: Single run (metrics, growth and drawdown, allocation, P&L by sleeve, every trade), Compare runs, Full scoreboard with deflated Sharpe, Which optimizer won.

## Method

### Universe

| Bucket | Sleeves | ETFs |
| --- | --- | --- |
| Equity | Europe, US, developed Asia-Pacific, emerging, thematic AI | IEUR, IVV, EWJ, IEMG, AIQ |
| Fixed income | Government, IG credit, inflation-linked, high yield, EM debt | GOVT, LQD, TIP, HYG, EMB |
| Alternatives | Gold, liquid alternatives, real assets | GLD, DBMF, IGF |
| Cash | Money market | BIL |

Private markets carries no proxy and sits at zero. The ETF universe is complete from May 2019 (DBMF launch); with 756 days of history required, its backtest starts mid-2022. The long tests rebuild the sleeves from index mutual funds, gold futures and the 13-week T-bill back to 2003, with QQQ or an AAPL, MSFT, AMZN basket for the AI sleeve. Rank correlation between the two long tests is 0.86 to 0.996 across 19 windows, same winner in 17.

Equity band per tier: 0 to 30% conservative, 50 to 55 balanced, 68 to 75 growth, 82 to 92 aggressive.

### Constraints

Hard cvxpy constraints, inside the solver. An infeasible tier reports which cap binds.

```
long-only, fully invested      sum(w) = 1, w >= 0
equity band per tier           lo <= sum(w_equity) <= hi
emerging equity                <= 20% of the equity sleeve
thematic AI                    <= 10% of the equity sleeve
gold                           3% to 5%
high yield + EM debt           <= 8%, 0 on aggressive
tactical band                  |w - w_strategic| <= 10 points
```

### Estimation

Rolling 756-day window, nothing after the decision date.

- Covariance: Ledoit-Wolf shrinkage. The sample matrix is ill-conditioned with 14 assets and the optimiser inverts it.
- Expected returns: Bayes-Stein shrinkage toward a grand mean. The standard error of a three-year mean is about 11 points; shrinkage moves the balanced return target from 5.60% to 3.89%.
- Tail: the 756 daily return vectors are the scenarios. No summary matrix in between.

### Optimisers

| Family | Method | Program |
| --- | --- | --- |
| Baseline | Buy and hold | Strategic weights, rebalanced on drift |
| House core | Mean-CVaR | min CVaR95 subject to return >= strategic return, all caps. Rockafellar-Uryasev LP |
| Offense | Max return under CVaR cap | max return subject to CVaR95 <= strategic CVaR95. The dual, a risk budget |
| Offense | Mean-variance | Markowitz twin, same caps |
| Offense | Trend tilt | mu nudged toward 12-1 momentum, z-scored, capped at 2 sigma, then solved |
| Offense | Black-Litterman, momentum views | Point-in-time momentum views on the equilibrium prior |
| Offense | Mean-CVaR, anchored | Ridge pull toward strategic weights, lower turnover |
| Overlay | Vol target | Scale to 10% ex-ante vol, remainder in cash; only de-risks |
| Overlay | Regime breaker | Equity composite under its 200-day average: half of equity to cash and gold |
| Overlay | Dual momentum | Any sleeve with 12-1 momentum below cash goes entirely to cash |
| Combinations | Offense + overlay | Tilt, then de-risk |
| References | Risk parity, HRP, min variance, max Sharpe, max diversification, equal weight, inverse vol | Tier-free |

```
minimise    zeta + 1 / ((1 - beta) S) * sum(z_s)
subject to  z_s >= -(w . r_s) - zeta,   z_s >= 0
            mu . w >= mu . w_strategic
            tier constraints
```

At the optimum zeta is the VaR and the objective is the CVaR. Linear throughout, solved exactly.

### Walk-forward

```
wait 756 trading days
first trading day of each month:
    estimate mu, Sigma on returns to date
    solve for target weights
    if max |current - target| > 5 points: trade all sleeves to target, 10 bps on volume
    else: let the book drift
```

One pass per universe, tier and method. Calendar blocks and crisis windows are cut from the finished curve. The benchmark runs the same loop with a constant target.

### Validation

- Deflated Sharpe (Bailey and Lopez de Prado): probability the true Sharpe exceeds zero given trials, their dispersion, track length, skew and kurtosis. Shown on full history only.
- Exposure-matched comparison: a run 43% invested is compared to a passive book at 43%, or the benchmark levered to the same beta.
- Attribution: sleeve P&L minus costs equals the curve, every run.

## Limitations

- Four years on the actual ETFs cannot separate skill from luck after 286 trials.
- Long tests use proxies; checked, not assumed.
- Flat 10 bps per unit traded, optimistic for the least liquid sleeves.
- Overlays act after the solver and can move a weight past a cap; the regime breaker pushes gold over 5% when it fires.
- Concentration is enforced per sleeve; overlapping holdings across sleeves are not netted.
- No derivatives. Overlays are implemented by moving weights.

## Repository

```
engine/         estimators, constraints, optimisers, overlays, allocate()
backtest/       walk-forward loop, benchmark, metrics with deflated Sharpe, robustness lab
data_layer/     price download, returns, quality checks, store build
reporting/      dashboard, periods, charts, tearsheets
config/         universe.yaml: sleeves, proxies, tiers, caps, weight variants
data/           store.duckdb, long-history prices
```

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

```
pip install -r requirements-engine.txt
python -m data_layer.build
ALLOC_LAB=1 python -m backtest.run
python -m backtest.robustness
```

## References

- Rockafellar and Uryasev (2000). Optimization of conditional value-at-risk. *Journal of Risk*.
- Ledoit and Wolf (2004). A well-conditioned estimator for large-dimensional covariance matrices. *Journal of Multivariate Analysis*.
- Jorion (1986). Bayes-Stein estimation for portfolio analysis. *JFQA*.
- Black and Litterman (1992). Global portfolio optimization. *Financial Analysts Journal*.
- Bailey and Lopez de Prado (2014). The deflated Sharpe ratio. *Journal of Portfolio Management*.
- DeMiguel, Garlappi and Uppal (2009). Optimal versus naive diversification. *Review of Financial Studies*.
- Lopez de Prado (2016). Building diversified portfolios that outperform out of sample. *Journal of Portfolio Management*.
- Antonacci (2014). *Dual Momentum Investing*.
- Moreira and Muir (2017). Volatility-managed portfolios. *Journal of Finance*.
