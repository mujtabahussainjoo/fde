# SRE Foundation: Monitoring and Observability (Simple + Descriptive Notes)

## 1) Big Picture
- Monitoring tells you **something is wrong**.
- Observability helps you understand **why it is wrong**.
- SRE needs both to keep services reliable and reduce outage impact.
- Monitoring is the early warning layer; observability is the investigation layer.

## 2) Monitoring vs Observability
### Monitoring
- Tracks known signals with predefined metrics and thresholds.
- Best for detecting known failure patterns quickly.
- Example: Error rate crosses 5% -> alert fires.
- Goal: Fast detection and quick response.

### Observability
- Uses metrics + logs + traces to investigate unknown issues.
- Best for root-cause analysis in distributed systems.
- Example: CPU looks normal, but traces reveal slow DB calls in one downstream service.
- Goal: Deep understanding and long-term reliability improvement.

## 3) Why Monitoring Alone Is Not Enough
- In modern systems, one user request may pass through many services.
- A single alert may not show which dependency caused the problem.
- Observability connects events across services so teams can understand failure chains.

## 4) Three Pillars of Observability
- **Metrics**: numbers over time for quick trend view.
- **Logs**: detailed event records for exact error/context.
- **Traces**: end-to-end request path to find bottlenecks and propagation failures.
- Practical use: metrics detect, logs explain, traces localize.

## 5) Golden Signals (Must Remember)
- **Latency**: how fast the system responds.
- **Errors**: how many requests fail.
- **Traffic/Throughput**: how much load the system handles.
- **Saturation**: how close resources are to limits.

Memory trick: **L-E-T-S**
- L = Latency
- E = Errors
- T = Traffic
- S = Saturation

## 6) Cardinality (Very Important)
### What it is
- Cardinality = number of unique label combinations in metrics.
- More unique labels -> more time series -> more memory/storage/query pressure.

### Why dangerous
- Can crash monitoring during peak traffic.
- Causes slow dashboards, query timeouts, and high observability cost.
- Teams can become blind exactly when incident response is most critical.

### Labels to avoid (usually)
- user_id
- request_id / trace_id
- timestamps in labels
- raw geo coordinates
- session tokens / transaction IDs

### Safe labeling style
- Use bounded labels: env=prod/stage/dev, status=200/500, region=us-east-1.
- Aggregate data before shipping metrics.
- Set cardinality budgets and alerts on growth trends.

## 7) Dashboards and Alerts
### Dashboards
- Give real-time health context and trend visibility.
- Keep layout clear, grouped, and low clutter.
- Put Golden Signals first and business-impact metrics near top.

### Alerts
- Notify only when human action is needed.
- Tune thresholds with historical baseline data.
- Reduce alert fatigue by removing low-value or duplicate alerts.
- Every alert should say what happened, why it matters, and what to check first.

Rule:
- **Dashboards for context**
- **Alerts for action**

## 8) Logs and Traces for Troubleshooting
- Metrics show symptom severity, logs show event details, traces show path and latency hotspots.
- Centralized logging is essential for microservices; scattered logs slow investigations.
- Trace sampling and log retention policies are needed to control data volume and cost.

## 9) Common Tool Categories
- Metrics collection/storage: Prometheus, cloud metric stores.
- Visualization/analysis: Grafana and cloud dashboards.
- Logs/traces stacks: ELK/Loki + Jaeger/Tempo (or cloud-native alternatives).
- Platform suites: CloudWatch, Azure Monitor, Google Cloud Monitoring.

## 10) Best Practices
- Monitor what affects users and business outcomes first.
- Prefer actionable metrics over vanity metrics.
- Keep cardinality controlled from day 1.
- Review alerts monthly and remove noisy ones.
- Use logs/traces for deep debugging, not only metrics.
- Maintain monitoring like any production system: tune, clean up, and evolve.

## 11) Fast Exam Recap
- Monitoring answers: **"Is there a problem?"**
- Observability answers: **"Why did it happen?"**
- Core service health metrics: latency, errors, traffic, saturation.
- Cardinality prevention: bounded labels + aggregation + budgets.
- Strong operations: actionable alerts + clear dashboards + periodic maintenance.

## 12) 30-Second Revision Card
- Monitoring = detect known issues.
- Observability = investigate unknown issues.
- Pillars = metrics, logs, traces.
- Golden signals = L-E-T-S.
- Cardinality can break observability if labels are unbounded.
- Good alerts are actionable, minimal, and user-impact focused.
