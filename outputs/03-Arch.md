<reasoning>We need to produce a detailed system architecture, tech stack, API endpoints, DB schema, folder structure, deployment plan. Use markdown with diagrams (maybe mermaid). Provide clean sections. Let's craft.</reasoning># FitPulse – Technical Design Document  
*Version 1.0 – 2025‑11‑17*  

---

## Table of Contents
1. [System Architecture](#1-system-architecture)  
2. [Tech‑Stack Recommendation](#2-tech-stack-recommendation)  
3. [API Design (Endpoints & Contracts)](#3-api-design-endpoints--contracts)  
4. [Database Schema](#4-database-schema)  
5. [Codebase / Folder Structure](#5-codebase--folder-structure)  
6. [Deployment & Operations Plan (Docker + Cloud)](#6-deployment--operations-plan-docker--cloud)  

---  

## 1. System Architecture  

### 1.1 High‑Level Overview  

```
+-------------------+        +-------------------+        +-------------------+
|   Mobile Clients  | <----> |   API Gateway     | <----> |   Auth Service    |
| (iOS / Android)  |        | (Kong / AWS GW)   |        | (OAuth2 / OIDC)  |
+-------------------+        +-------------------+        +-------------------+
          |                           |                         |
          |                           |                         |
          v                           v                         v
+-------------------+   +-------------------+   +-------------------+
|   Edge Services   |   |   Core Services   |   |   ML/AI Service   |
| (Video/AR, CDN)   |   | (Workout Engine, |   | (TensorFlow‑Py   |
|                   |   |  Marketplace,    |   |  Torch, FastAPI) |
+-------------------+   |  Progress, etc.) |   +-------------------+
          |            +-------------------+            |
          |                     |                      |
          v                     v                      v
+-------------------+   +-------------------+   +-------------------+
|   Data Layer      |   |   Event Bus       |   |   Observability   |
| (PostgreSQL,      |   | (Kafka / Pulsar)  |   | (Prometheus,      |
|  MongoDB, Redis) |   +-------------------+   |  Grafana, Loki)   |
+-------------------+                           +-------------------+
```

### 1.2 Component Breakdown  

| Component | Responsibility | Tech (suggested) | Key Non‑Functional Concerns |
|-----------|----------------|------------------|-----------------------------|
| **Mobile Apps** | UI, camera/AR capture, local caching, offline mode | React Native (or Swift/Kotlin native) + TensorFlow Lite for on‑device inference (form‑correction) | Low latency, battery‑friendly, offline‑first |
| **API Gateway** | Single entry point, request routing, rate‑limiting, auth enforcement, TLS termination | Kong (open‑source) or AWS API Gateway (if on AWS) | Security, throttling, observability |
| **Auth Service** | OAuth2 / OIDC, social login, password‑less email, token revocation | Keycloak (self‑hosted) or AWS Cognito | GDPR‑compliant user consent, MFA |
| **Edge Services** | Video ingest, AR overlay streaming, CDN distribution, media transcoding | Cloudflare Workers + Cloudflare Stream OR AWS MediaConvert + CloudFront | 99.9 % availability, low‑latency media delivery |
| **Core Services** | Business logic (Workout Engine, Marketplace, Progress, Community) | FastAPI (Python) + gRPC for internal calls | Horizontal scaling, high throughput |
| **ML/AI Service** | Model training, inference (plan generation, form correction, recommendation) | TensorFlow / PyTorch, TorchServe, ONNX Runtime, GPU‑enabled nodes | Model versioning, A/B testing, latency < 150 ms |
| **Data Layer** | Persistent storage | PostgreSQL (relational), MongoDB (document for logs & events), Redis (caching, session store) | ACID compliance for financial data, eventual consistency for analytics |
| **Event Bus** | Asynchronous communication, activity streams, notifications | Apache Kafka (or Pulsar) | Exactly‑once semantics, replayability |
| **Observability** | Metrics, logs, tracing | Prometheus + Grafana, Loki, OpenTelemetry | SLA monitoring, alerting |
| **CI/CD** | Build, test, deploy pipelines | GitHub Actions / GitLab CI, Docker, Helm, ArgoCD | Automated security scans, blue‑green deploys |

### 1.3 Data Flow Example (Workout Session)

1. **User opens app → Auth token validated at API Gateway**.  
2. **App requests next workout** → `GET /v1/workouts/next`.  
3. **Core Service** queries **PostgreSQL** for user profile, pulls latest wearable data from **Redis** cache.  
4. **Core Service** calls **ML Service** (`POST /ml/plan`) with context → receives generated plan.  
5. **Core Service** stores plan in **PostgreSQL** and returns JSON to client.  
6. **Client** streams AR guidance video from **Edge Service** (signed URL).  
7. **During session**, client sends **frame‑level keypoints** to **Edge Service** → real‑time feedback (local inference) → optional server‑side validation via **ML Service**.  
8. **On completion**, client posts `POST /v1/workouts/{id}/complete`. Core Service updates progress, publishes `WorkoutCompleted` event to **Kafka**.  
9. **Notification Service** (consumer) sends push notification, updates leaderboard, triggers trainer report generation.  

---  

## 2. Tech‑Stack Recommendation  

| Layer | Primary Choice | Alternatives | Rationale |
|-------|----------------|--------------|----------|
| **Mobile** | **React Native** (TypeScript) + **TensorFlow Lite** | Native Swift / Kotlin | Single code‑base, fast iteration, community plugins for ARKit/ARCore. |
| **API Gateway** | **Kong** (Docker) | AWS API GW, NGINX | Open‑source, plugin ecosystem (rate‑limit, auth, logging). |
| **Auth** | **Keycloak** (Docker) | AWS Cognito, Auth0 | Full OIDC support, easy federation with Google/Apple, self‑hosted for GDPR. |
| **Backend Framework** | **FastAPI** (Python 3.11) | NestJS (Node), Spring Boot (Java) | Async‑first, excellent OpenAPI generation, easy integration with ML models. |
| **ML/AI** | **TensorFlow 2.x** + **TensorFlow Serving** (or **TorchServe** if PyTorch) | ONNX Runtime, SageMaker | Model versioning, GPU inference, can be containerised. |
| **Database** | **PostgreSQL 15** (RDS/Aurora) + **MongoDB Atlas** | MySQL, DynamoDB | Relational for financial & core data, document store for flexible logs. |
| **Cache** | **Redis 7** (Elasticache) | Memcached | Session store, rate‑limit counters, fast look‑ups. |
| **Message Bus** | **Apache Kafka** (Confluent Cloud) | Pulsar, RabbitMQ | High‑throughput, replay, stream processing for analytics. |
| **Observability** | **Prometheus + Grafana**, **OpenTelemetry**, **Loki** | Datadog, New Relic | Vendor‑agnostic, easy to self‑host. |
| **CI/CD** | **GitHub Actions** + **Docker** + **Helm** + **ArgoCD** | GitLab CI, Jenkins | Cloud‑native, GitOps deployment. |
| **Container Orchestration** | **Kubernetes** (EKS / GKE / AKS) | Docker Swarm | Autoscaling, service discovery, rolling updates. |
| **Infrastructure as Code** | **Terraform** (AWS) + **Helm** charts | Pulumi, CloudFormation | Declarative, multi‑cloud ready. |
| **CDN / Edge Media** | **Cloudflare Stream** + **Workers** | AWS CloudFront + MediaConvert | Low‑latency video, built‑in DRM. |
| **Payments** | **Stripe Connect** (for marketplace) | Braintree, Adyen | Global coverage, easy split‑payment for trainers. |

---  

## 3. API Design (Endpoints & Contracts)  

All APIs are versioned (`/v1/`). OpenAPI 3.0 spec will be generated automatically from FastAPI annotations.

### 3.1 Authentication  

| Method | Endpoint | Request | Response | Notes |
|--------|----------|---------|----------|-------|
| **OAuth2 Authorization Code** (PKCE) | `POST /auth/token` | `grant_type=authorization_code&code=...&code_verifier=...` | `{ access_token, refresh_token, expires_in, token_type }` | Tokens are JWT signed with RS256. |
| **Refresh Token** | `POST /auth/refresh` | `{ refresh_token }` | Same as above | Revoked on logout. |
| **Logout** | `POST /auth/logout` | `{ refresh_token }` | `204 No Content` | Blacklist token in Redis. |

### 3.2 User Profile  

| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| `GET