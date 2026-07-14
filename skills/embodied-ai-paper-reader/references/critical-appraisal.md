# Critical Appraisal

Evaluate the dimensions that apply to the paper type. Use `not reported` or `not applicable` when appropriate; never fill gaps with assumptions.

## Method, empirical, and system papers

- Does the design isolate the claimed mechanism?
- Are data, tasks, embodiments, horizons, and evaluation conditions representative of the claimed scope?
- Are baselines current, comparable, and equally resourced?
- Do metrics measure deployment utility or only proxies?
- Are ablations sufficient to attribute the gain?
- Are uncertainty, variance, sample size, and failure cases reported?
- Could implementation details, privileged information, or simulator assumptions explain the result?

## Dataset and benchmark papers

- What population, environment, and behavior distribution is represented?
- How were data selected, filtered, labeled, and quality-controlled?
- What blind spots, leakage, licensing, or governance constraints exist?
- Do benchmark metrics reward behavior that matters outside the benchmark?

## Survey and position papers

- Is the search or selection process explicit?
- Does the taxonomy omit important adjacent or contrary work?
- Which statements summarize primary evidence and which are the authors' synthesis?
- Are field-wide claims proportional to the reviewed corpus?

## Transfer boundary

Write the narrowest defensible applicability statement across:

- data distribution;
- task and environment;
- embodiment and sensor/action interface;
- training and inference resources;
- evaluation horizon and metric;
- deployment constraints.

Keep author-stated limitations separate from reader-inferred boundaries.
