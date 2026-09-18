# AI Sales Inbox Agent

An AI-powered sales inbox assistant that reads incoming emails, identifies genuine sales leads, extracts key requirements, recommends the next action, and drafts a personalized reply for human review.

The system is designed as a lightweight Python agent connected to Gmail and Groq, without requiring a frontend or hosted application.

---

## Overview

Sales teams often spend significant time manually checking inboxes, identifying potential leads, understanding their requirements, and deciding how to respond.

This project automates the initial sales-email triage while keeping a human in control of the final response.

### Workflow

```text
Incoming Gmail Email
        ↓
Gmail API
        ↓
Email Extraction
        ↓
AI Analysis using Groq
        ↓
Lead / Non-Lead Classification
        ↓
Lead Information Extraction
        ↓
Recommended Next Action
        ↓
Personalized Reply Draft
        ↓
Guardrail Validation
        ↓
Human Review
        ↓
Approve / Edit / Reject