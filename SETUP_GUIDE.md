# LearnFlow Setup Guide

Complete guide for setting up authentication, Kafka, and Docker infrastructure for the LearnFlow platform.

---

## 1. Authentication with Better-Auth

### Why Better-Auth?
- ✅ Built for Next.js 15 and React 19
- ✅ Type-safe with TypeScript
- ✅ Multiple auth methods (email/password, OAuth, magic links)
- ✅ Session management built-in
- ✅ Easy integration with PostgreSQL/SQLite
- ✅ Built-in RBAC (Role-Based Access Control) for Student/Teacher roles

### Installation

```bash
cd mystery-skils-app-ui
npm install better-auth@latest
npm install @better-auth/react
```

### Setup Better-Auth

#### 1. Create Auth Configuration (`lib/auth.ts`)

```typescript
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"
import { prisma } from "./db"

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql" // or "sqlite" for development
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID || "",
      clientSecret: process.env.GITHUB_CLIENT_SECRET || "",
    }
  },
  user: {
    additionalFields: {
      role: {
        type: "string",
        defaultValue: "student", // student | teacher | admin
      },
      studentId: {
        type: "string",
        required: false,
      }
    }
  }
})
```

#### 2. Create Auth API Route (`app/api/auth/[...all]/route.ts`)

```typescript
import { auth } from "@/lib/auth"

export const { GET, POST } = auth.handler
```

#### 3. Create Auth Client (`lib/auth-client.ts`)

```typescript
import { createAuthClient } from "@better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:4000"
})

export const { signIn, signUp, signOut, useSession } = authClient
```

#### 4. Update Flash UI Auth Page

Replace the existing auth handshake with Better-Auth integration:

```typescript
// In mystery-skills-flash.html or create new Auth component

import { signIn, signUp } from "@/lib/auth-client"

async function handleLogin(email: string, password: string) {
  const result = await signIn.email({
    email,
    password,
  })

  if (result.data) {
    // Redirect to dashboard
    window.location.href = "/dashboard"
  }
}

async function handleSignup(email: string, password: string, role: "student" | "teacher") {
  const result = await signUp.email({
    email,
    password,
    name: email.split("@")[0],
    role, // Custom field
  })

  if (result.data) {
    // Auto-login after signup
    window.location.href = "/dashboard"
  }
}
```

#### 5. Protect Routes with Middleware (`middleware.ts`)

```typescript
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { auth } from "@/lib/auth"

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers
  })

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    if (!session) {
      return NextResponse.redirect(new URL("/auth", request.url))
    }
  }

  // Protect teacher-only routes
  if (request.nextUrl.pathname.startsWith("/teacher")) {
    if (!session || session.user.role !== "teacher") {
      return NextResponse.redirect(new URL("/dashboard", request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/teacher/:path*"]
}
```

#### 6. Use Session in Components

```typescript
"use client"

import { useSession, signOut } from "@/lib/auth-client"

export function UserProfile() {
  const { data: session, isPending } = useSession()

  if (isPending) return <div>Loading...</div>
  if (!session) return <div>Not logged in</div>

  return (
    <div>
      <p>Welcome, {session.user.name}</p>
      <p>Role: {session.user.role}</p>
      <p>Student ID: {session.user.studentId}</p>
      <button onClick={() => signOut()}>Logout</button>
    </div>
  )
}
```

---

## 2. Kafka Setup

### Option A: Local Kafka with Docker (Development)

#### 1. Create `docker-compose.kafka.yml`

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    hostname: zookeeper
    container_name: learnflow-zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - learnflow-network

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    hostname: kafka
    container_name: learnflow-kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "9101:9101"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_JMX_PORT: 9101
      KAFKA_JMX_HOSTNAME: localhost
    networks:
      - learnflow-network

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: learnflow-kafka-ui
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: learnflow-local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:29092
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
    networks:
      - learnflow-network

networks:
  learnflow-network:
    driver: bridge
```

#### 2. Start Kafka

```bash
docker-compose -f docker-compose.kafka.yml up -d
```

#### 3. Create Kafka Topics

```bash
# Install kafka-python
pip install kafka-python

# Create topics script
python infrastructure/scripts/create-kafka-topics.py
```

#### 4. Verify Kafka

```bash
# Check containers
docker ps

# Access Kafka UI
# Open http://localhost:8080
```

### Option B: Confluent Cloud (Production - Free Tier Available)

#### 1. Sign up at https://confluent.cloud
- Free tier: 30 days free + $400 credits

#### 2. Create Cluster
- Select "Basic" cluster (free tier eligible)
- Choose region closest to your users

#### 3. Get Connection Details
```bash
# Confluent Cloud will provide:
KAFKA_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
KAFKA_SASL_USERNAME=xxxxx
KAFKA_SASL_PASSWORD=xxxxx
```

#### 4. Update `.env`
```bash
# Add to .env
KAFKA_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
KAFKA_SASL_MECHANISM=PLAIN
KAFKA_SECURITY_PROTOCOL=SASL_SSL
KAFKA_SASL_USERNAME=xxxxx
KAFKA_SASL_PASSWORD=xxxxx
```

#### 5. Update Backend Kafka Client

```python
# backend/shared/kafka_client.py
from kafka import KafkaProducer, KafkaConsumer
import os

def create_producer():
    config = {
        'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'value_serializer': lambda v: json.dumps(v).encode('utf-8')
    }

    # Add SASL config for Confluent Cloud
    if os.getenv('KAFKA_SECURITY_PROTOCOL') == 'SASL_SSL':
        config.update({
            'security_protocol': 'SASL_SSL',
            'sasl_mechanism': 'PLAIN',
            'sasl_plain_username': os.getenv('KAFKA_SASL_USERNAME'),
            'sasl_plain_password': os.getenv('KAFKA_SASL_PASSWORD'),
        })

    return KafkaProducer(**config)
```

### Option C: Upstash Kafka (Serverless - Easiest)

#### 1. Sign up at https://upstash.com
- Free tier: 10,000 messages/day

#### 2. Create Kafka Cluster
- Click "Create Cluster"
- Select region

#### 3. Get Connection Details
```bash
UPSTASH_KAFKA_REST_URL=https://xxxxx.upstash.io
UPSTASH_KAFKA_REST_USERNAME=xxxxx
UPSTASH_KAFKA_REST_PASSWORD=xxxxx
```

#### 4. Use Upstash REST API (No Kafka client needed!)

```python
# backend/shared/upstash_kafka.py
import requests
import os
import base64

class UpstashKafka:
    def __init__(self):
        self.url = os.getenv('UPSTASH_KAFKA_REST_URL')
        username = os.getenv('UPSTASH_KAFKA_REST_USERNAME')
        password = os.getenv('UPSTASH_KAFKA_REST_PASSWORD')

        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded}',
            'Content-Type': 'application/json'
        }

    def produce(self, topic: str, message: dict):
        """Publish message to topic"""
        response = requests.post(
            f"{self.url}/produce/{topic}",
            headers=self.headers,
            json=message
        )
        return response.json()

    def consume(self, topic: str, consumer_group: str):
        """Consume messages from topic"""
        response = requests.get(
            f"{self.url}/consume/{consumer_group}/{topic}",
            headers=self.headers
        )
        return response.json()
```

---

## 3. PostgreSQL Setup (for Progress Tracker)

### Option A: Local PostgreSQL with Docker

```yaml
# Add to docker-compose.kafka.yml

  postgres:
    image: postgres:15-alpine
    container_name: learnflow-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: learnflow
      POSTGRES_PASSWORD: learnflow_dev_password
      POSTGRES_DB: learnflow_progress
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - learnflow-network

volumes:
  postgres_data:
```

### Option B: Supabase (Free Tier - Recommended)

1. Sign up at https://supabase.com
2. Create new project
3. Get connection string:
```bash
postgres://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

4. Update `.env`:
```bash
DATABASE_URL=postgres://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

---

## 4. Quick Start Commands

### Development (All Local)

```bash
# 1. Start infrastructure
docker-compose -f docker-compose.kafka.yml up -d

# 2. Install Better-Auth dependencies
cd mystery-skils-app-ui
npm install better-auth @better-auth/react
npx prisma init
npx prisma migrate dev

# 3. Start backend agents
cd ..
.\start-agents.bat

# 4. Start frontend
cd mystery-skils-app-ui
npm run dev
```

### Production (Managed Services)

```bash
# Use:
# - Confluent Cloud / Upstash for Kafka
# - Supabase for PostgreSQL
# - Vercel for Next.js deployment
# - Railway/Render for FastAPI agents

# Just update .env with production credentials
```

---

## 5. Environment Variables Summary

Create `.env` file in project root:

```bash
# Better-Auth
DATABASE_URL=postgresql://user:password@localhost:5432/learnflow
BETTER_AUTH_SECRET=your-32-char-secret-here
GOOGLE_CLIENT_ID=your-google-oauth-id
GITHUB_CLIENT_ID=your-github-oauth-id

# Kafka (Local)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Kafka (Confluent Cloud)
# KAFKA_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
# KAFKA_SECURITY_PROTOCOL=SASL_SSL
# KAFKA_SASL_MECHANISM=PLAIN
# KAFKA_SASL_USERNAME=xxxxx
# KAFKA_SASL_PASSWORD=xxxxx

# Kafka (Upstash - Easiest)
# UPSTASH_KAFKA_REST_URL=https://xxxxx.upstash.io
# UPSTASH_KAFKA_REST_USERNAME=xxxxx
# UPSTASH_KAFKA_REST_PASSWORD=xxxxx

# Claude API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Agent Ports
TRIAGE_PORT=8001
CONCEPTS_PORT=8002
CODE_REVIEW_PORT=8003
DEBUG_PORT=8004
EXERCISE_PORT=8005
PROGRESS_PORT=8006
```

---

## 6. Recommended Setup for Hackathon

**Quickest path to demo:**

1. ✅ **Auth**: Use Better-Auth with SQLite (no external DB needed)
2. ✅ **Kafka**: Use Upstash (serverless, no Docker needed)
3. ✅ **Database**: Use Supabase free tier
4. ✅ **Frontend**: Already on localhost:4000
5. ✅ **Backend**: Run agents locally with Python

This gives you a fully functional system in ~15 minutes with zero infrastructure setup!
