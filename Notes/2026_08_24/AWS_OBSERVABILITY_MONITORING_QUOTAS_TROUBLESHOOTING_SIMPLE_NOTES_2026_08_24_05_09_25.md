# AWS Observability, Monitoring, Quotas, and Troubleshooting

**Created:** 2026-08-24 05:09:25  
**Exam:** AWS Certified Solutions Architect - Associate (SAA-C03)

## Main Idea

- Observability helps a team understand what is happening inside a cloud system.
- The goal is to detect problems quickly, find the cause, and recover reliably.
- AWS monitoring is strongest when metrics, logs, traces, and events are used together.

## 1. Four Observability Signals

| Signal | Main question | Example use |
|---|---|---|
| **Metrics** | What is happening? | CPU, latency, errors, invocations |
| **Logs** | Why did it happen? | Error messages and request details |
| **Traces** | Where is the time spent? | The path from API Gateway to Lambda to DynamoDB |
| **Events** | What changed? | Deployments, scaling, configuration changes, AWS Health events |

### Common AWS Services

- **CloudWatch Metrics:** Stores time-series measurements and supports alarms.
- **CloudWatch Logs:** Stores logs from Lambda, EC2, ECS, and other services.
- **CloudWatch Logs Insights:** Queries and summarizes log data.
- **AWS X-Ray:** Follows requests across distributed services.
- **CloudTrail:** Records AWS API calls and configuration changes.
- **EventBridge:** Routes events to targets such as SNS, Lambda, and SSM Automation.
- **AWS Health:** Shows AWS events that specifically affect an account or resource.

## 2. CloudWatch Metrics and KPIs

Useful KPIs should represent user or business impact:

- **Availability:** Whether requests succeed.
- **Latency:** How long requests take. Use p90, p95, or p99 to reveal slow users.
- **Errors:** Error rate and important error types.
- **Saturation:** Concurrency, queue depth, throttles, and resource usage.
- **Business results:** Orders, checkouts, payments, or processed jobs.

### Metrics Design

- A **namespace** groups related metrics, such as `AWS/Lambda` or `AWS/EC2`.
- **Dimensions** add context, such as `FunctionName` or `InstanceId`.
- Avoid too many unique dimension values because high cardinality increases cost and noise.
- Use **Sum** for counts, such as total requests or errors.
- Use **percentiles** for latency instead of relying only on averages.
- Use short periods for fast detection, but use multiple evaluation periods to reduce false alarms.
- High-resolution metrics provide more frequent data but can cost more.

### Useful Metric Math

```text
Error rate = Errors / Invocations
Availability = 1 - (5XX errors / Total requests)
```

Custom metrics are useful for application KPIs, but they should be documented and created only when they support a real decision.

## 3. Dashboards and Alarms

### Dashboard Design

- Put availability, latency, and error rate at the top.
- Add saturation and dependency metrics to help explain problems.
- Use a top-level service view and separate deeper views for individual services.
- Review dashboards regularly as the system changes.

### Alarm Design

A CloudWatch alarm normally includes:

1. A metric and statistic.
2. A period and evaluation window.
3. A threshold.
4. A missing-data policy.
5. An action, such as SNS notification or automation.

### Reduce Alert Noise

- Page on user-impacting symptoms, such as high error rate or poor availability.
- Keep diagnostic alarms available for investigation, but give them lower severity.
- Use M-out-of-N evaluation so one short spike does not page someone.
- Use composite alarms to combine child alarms with `AND` or `OR` logic.
- Page once on the composite alarm and investigate the child alarms.
- Use static thresholds for stable limits, such as CPU above 80%.
- Use anomaly detection when normal behavior changes by hour, day, or season.
- Give every alarm an owner, escalation path, and runbook link.
- Remove alarms that are always noisy or no longer useful.

## 4. CloudWatch Logs

### Log Groups and Streams

- A **log group** is a container with shared retention, access, and monitoring settings.
- A **log stream** contains logs from one source, such as an instance or Lambda execution.
- Use consistent names, tags, and IAM policies to manage logs across teams.

### Logging Best Practices

- Set a retention period instead of keeping every log forever.
- Send long-term logs to lower-cost storage such as Amazon S3 when appropriate.
- Prefer structured JSON logs so fields can be queried reliably.
- Include fields such as log level, component, request ID, and trace ID.
- Never write passwords, secrets, or unnecessary personal information to logs.
- Save useful Logs Insights queries in incident runbooks.

### Metric and Subscription Filters

- **Metric filters** turn matching log patterns into CloudWatch metrics that can drive alarms.
- **Subscription filters** stream logs to services such as Lambda, Kinesis Data Streams, Kinesis Data Firehose, S3, or OpenSearch.
- CloudTrail explains control-plane changes; application logs explain runtime behavior.

## 5. CloudWatch Logs Insights Queries

Use a narrow time range and only the log groups needed. This reduces scan volume and query cost.

### Find Errors

```text
fields @timestamp, @message
| filter @message like /ERROR|Exception|Failed/
| sort @timestamp desc
| limit 20
```

### Count Errors Over Time

```text
filter @message like /ERROR/
| stats count() as error_count by bin(5m)
| sort @timestamp desc
```

### Investigate Slow Requests

```text
filter @message like /Duration/
| parse @message /Duration: (?<duration_ms>[0-9.]+) ms/
| stats avg(duration_ms) as average_ms, max(duration_ms) as maximum_ms by bin(5m)
```

Important commands:

- `filter` narrows the events.
- `fields` chooses the displayed data.
- `stats` aggregates data.
- `bin()` groups data into time periods.
- `sort` ranks results.
- `limit` keeps results readable.

## 6. AWS X-Ray Distributed Tracing

- A **trace** represents one request from beginning to end.
- A **segment** represents work done by one service.
- A **subsegment** records a downstream call, such as a database or API request.
- **Annotations** are indexed fields used to search traces.
- **Metadata** stores extra details but is not indexed for searching.
- A **service map** shows services as nodes and calls as edges.
- Latency and fault indicators help identify bottlenecks.

### Tracing Workflow

1. Start with metrics to notice the problem.
2. Use logs to understand the error or runtime details.
3. Use X-Ray to locate the slow or failing dependency.
4. Correlate the trace ID with logs and other signals.

Sampling lowers cost by tracing only some requests. Critical routes and errors may need higher sampling. Trace context must be passed between services so one request remains connected across the system.

For Lambda, enable active tracing. For API Gateway REST APIs, tracing is configured at the stage level.

## 7. Service Quotas and Throttling

**Throttling** happens when a service reaches a request, throughput, concurrency, or other limit.

### Common Symptoms

- HTTP `429` or `TooManyRequests` errors.
- `Rate exceeded` messages.
- DynamoDB `ProvisionedThroughputExceeded` errors.
- Spiky latency caused by retries and backoff.
- Growing queues, timeouts, and cascading failures.

Quotas may be account-level, resource-level, or Region-specific. Some quotas can be increased, while others are fixed architectural limits.

### Detection and Mitigation

Monitor throttles, errors, latency, queue depth, and application logs. Use CloudTrail to identify callers and configuration changes.

Useful mitigation patterns include:

- Buffer bursts with SQS or another queue.
- Scale horizontally with concurrency or partitioning.
- Cache repeated reads.
- Batch operations to reduce API calls.
- Apply per-client or per-tenant rate limits.
- Use asynchronous processing for bursty workloads.
- Retry only transient errors and throttles.
- Use exponential backoff with jitter.
- Make writes idempotent so retries do not duplicate effects.
- Set maximum attempts, timeouts, and circuit breakers.

Use the AWS Service Quotas console to request increases for adjustable quotas. Plan early, because approval can take time. Verify the new quota in the correct Region after approval.

## 8. AWS Health and EventBridge

- AWS Health provides account-specific information about service issues, scheduled changes, and advisories.
- Events can be regional or global.
- EventBridge can receive Health events and route them to an operational target.
- SNS can notify many people or systems at once.
- Lambda can enrich an event with dashboards and runbook links.
- SSM Automation can execute approved remediation steps.
- ChatOps and ticketing systems improve team communication and audit history.

For multi-account and multi-Region environments:

- Centralize important events in an operations account.
- Configure routing for every Region in use.
- Standardize EventBridge rules and targets.
- Test notifications and automation before a real incident.

## 9. Simple Troubleshooting Process

```text
Detect with metrics or alarms
        -> Check AWS Health and recent CloudTrail changes
        -> Search logs for errors and patterns
        -> Use X-Ray to locate dependency latency or failure
        -> Apply the runbook or mitigation
        -> Confirm recovery with metrics
        -> Record lessons learned and improve the alarms
```

## Quick Exam Recap

- Metrics show trends and trigger alarms; logs provide detailed evidence.
- X-Ray follows one request across services and helps locate bottlenecks.
- CloudTrail records AWS API activity and configuration changes.
- EventBridge routes operational events to notifications and automation.
- Use percentiles for latency, rates for errors, and business KPIs for user outcomes.
- Reduce alert fatigue with evaluation windows, composite alarms, and clear ownership.
- Treat throttling as a quota or capacity signal; use queues, caching, batching, and backoff.
- Check AWS Health when an AWS service problem may explain an incident.
