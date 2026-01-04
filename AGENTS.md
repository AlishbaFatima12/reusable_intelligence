# Agent Architecture

## Overview

This system consists of 3 microservice agents:

- **Concepts** (port 8000): FastAPI application for generating programming concept explanations.
- **Progress** (port 8000): FastAPI application for tracking student learning progress and mastery.
- **Triage** (port 8000): FastAPI application for query routing and intent classification.

Each agent is a FastAPI application with dedicated responsibilities and API contracts.

## Concepts

**Port**: 8000
**Purpose**: FastAPI application for generating programming concept explanations.
**Location**: `backend\agents\concepts`

### Dependencies

| Dependency | Type | Source |
|------------|------|--------|
| backend | PACKAGE | IMPORT |
| contextlib | PACKAGE | IMPORT |
| fastapi | PACKAGE | IMPORT |
| logging | PACKAGE | IMPORT |
| prometheus_client | PACKAGE | IMPORT |
| uvicorn | PACKAGE | IMPORT |

### API Contract

#### `GET /`

Root endpoint


### Pub/Sub Topics

No Kafka topics configured.

## Progress

**Port**: 8000
**Purpose**: FastAPI application for tracking student learning progress and mastery.
**Location**: `backend\agents\progress`

### Dependencies

| Dependency | Type | Source |
|------------|------|--------|
| backend | PACKAGE | IMPORT |
| contextlib | PACKAGE | IMPORT |
| fastapi | PACKAGE | IMPORT |
| logging | PACKAGE | IMPORT |
| prometheus_client | PACKAGE | IMPORT |
| uvicorn | PACKAGE | IMPORT |

### API Contract

#### `GET /`

Root endpoint


### Pub/Sub Topics

No Kafka topics configured.

## Triage

**Port**: 8000
**Purpose**: FastAPI application for query routing and intent classification.
**Location**: `backend\agents\triage`

### Dependencies

| Dependency | Type | Source |
|------------|------|--------|
| backend | PACKAGE | IMPORT |
| contextlib | PACKAGE | IMPORT |
| fastapi | PACKAGE | IMPORT |
| logging | PACKAGE | IMPORT |
| prometheus_client | PACKAGE | IMPORT |
| uvicorn | PACKAGE | IMPORT |

### API Contract

#### `GET /`

Root endpoint


### Pub/Sub Topics

No Kafka topics configured.