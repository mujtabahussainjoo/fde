# Microservices Fundamentals: Observability, Monitoring, and Security (Simple Notes)

## 1) Big Picture
- Microservices are powerful but complex.
- To keep them healthy, use three areas together:
- Observability helps you understand internal behavior from system outputs.
- Monitoring gives quick warning when system health moves outside normal limits.
- Security protects data, communication, and access across many services.

## 2) Observability Basics
- Observability helps answer: **Why is this happening?**
- Monitoring helps answer: **Is something wrong?**
- In microservices, observability is critical because requests pass through many services.
- It is hard to debug microservices by checking one service at a time.
- Observability connects data across services so teams can find root causes faster.

### Three Pillars (Must Know)
- **Metrics**: numeric signals (CPU, latency, request count).
- **Logs**: detailed event records (errors, actions, context).
- **Traces**: end-to-end request path across services.
- Use metrics for trend view, logs for details, and traces for cross-service flow.

Memory trick: **M-L-T**
- M = Metrics
- L = Logs
- T = Traces

## 3) Monitoring Techniques
### Proactive Monitoring
- Detects early warning signs before failure.
- Example: CPU slowly rising over time.
- Benefit: fewer outages, faster prevention.
- Also helps with capacity planning before traffic peaks.

### Reactive Monitoring
- Responds after issue happens.
- Example: service crash alert.
- Benefit: quicker recovery from incidents.
- Works best when incident runbooks and ownership are clearly defined.

### Alerting Best Practices
- Set useful thresholds.
- Prioritize alerts by business impact.
- Reduce alert fatigue by removing noisy alerts.
- Prefer alerts that are actionable within minutes, not informational only.

Rule:
- Too many alerts = noise
- Too few alerts = missed incidents

## 4) Metrics Collection and Analysis
### Metric Types
- **Counter**: only increases (e.g., requests total).
- **Gauge**: current value up/down (e.g., memory usage).
- **Histogram/Summary**: distribution (e.g., response time percentiles).
- Histograms are useful for SLOs because percentiles show user experience better than averages.

### Collection Methods
- **Push**: app sends metrics.
- **Pull**: monitoring system scrapes metrics endpoint.
- **Agent-based**: side agent collects automatically.
- Pull model gives centralized control of scrape interval and target discovery.

### Prometheus Quick Notes
- Pull-based model.
- Scrapes `/metrics` endpoints.
- Uses labels for dimensions.
- Queries with PromQL.
- Scrape interval should balance freshness and overhead (often 15s to 60s).

### Analysis Focus
- Trend detection (up/down/stable).
- Anomaly detection (spikes/drops).
- Baselines (normal behavior).
- Compare current values against baseline before deciding severity.

## 5) Log Management Essentials
### Log Types
- Event logs: business actions.
- Error logs: failures/exceptions.
- Access logs: who accessed what.
- Debug logs: deep troubleshooting details.
- Structured logs (JSON-like fields) make searching and correlation much easier.

### Good Logging Practices
- Add timestamp, severity, service name, request/trace ID context.
- Centralize logs for easier search and correlation.
- Use retention rules (hot/warm/cold storage) to control cost.
- Never log sensitive secrets such as passwords, tokens, or private keys.

## 6) Distributed Tracing Essentials
- Each request gets a **trace ID**.
- Each service step creates a **span**.
- All spans together form one trace.
- Context propagation is required to keep trace complete.
- If one service drops trace context headers, the end-to-end view becomes incomplete.

### Why Tracing Helps
- Finds bottlenecks quickly.
- Shows exact failing service.
- Improves root-cause analysis speed.
- Waterfall timeline view makes latency hotspots obvious.

### Common Challenges
- Very high trace data volume.
- Missing context propagation causes broken traces.
- Complex traces need good visualization tools.
- Sampling strategies are needed to control cost at high traffic.

## 7) Microservices Security Essentials
### Core Risks
- Unauthorized access
- Data interception
- API vulnerabilities
- Service overload (DoS)
- Dependency vulnerabilities in third-party packages are also common.

### Core Protections
- **TLS** for encryption in transit.
- **Authentication**: verify identity (tokens, OAuth/OIDC).
- **Authorization**: control actions (RBAC).
- **Least privilege**: give minimum required access.
- **Defense in depth**: multiple security layers.
- **Continuous monitoring**: detect and respond fast.
- Add patch management and regular vulnerability scanning into CI/CD.

## 8) Observability Tools (Simple Map)
- **OpenTelemetry**: standard instrumentation and telemetry pipeline.
- **Prometheus**: metrics collection and storage.
- **Grafana**: dashboards and visualization.
- **ELK / Loki**: centralized logs.
- **Jaeger/Tempo**: distributed tracing backends.
- **Cloud managed tools**: CloudWatch, Azure Monitor, Google Cloud Operations.
- Many teams use a combined stack instead of one single tool.

## 9) GitOps for Observability
- Store monitoring configs in Git (dashboards, alerts, Prometheus config).
- Use operators/tools (Flux/ArgoCD) to auto-apply changes.
- Benefits include version history, rollback, and consistency across environments.
- It also improves review quality because config changes go through pull requests.

## 10) Fast Exam Recap
- Monitoring = known issue detection.
- Observability = deep investigation of unknown issues.
- Three pillars = metrics + logs + traces.
- Tracing key terms = trace ID, span, context propagation.
- Security basics = TLS + authn + authz + least privilege + vigilance.
- GitOps = observability config as code.
- For scenario questions, pick the option that improves visibility and actionable response.

## 11) 30-Second Revision Card
- Use M-L-T for observability.
- Combine proactive + reactive monitoring.
- Keep alerts actionable.
- Trace IDs connect cross-service request flow.
- Secure every service-to-service call.
- Use RBAC and least privilege everywhere.
- Remember: visibility without action is incomplete; always connect data to response steps.
