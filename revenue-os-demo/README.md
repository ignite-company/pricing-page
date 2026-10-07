# Ignite Revenue OS Demo

Sales demo environment for Ignite's AI implementation and revenue systems offer.

## Purpose

This project is designed for live sales calls with service businesses. It demonstrates:

- instant lead response
- missed-call recovery
- AI qualification
- appointment booking
- pipeline movement
- estimate follow-up
- database reactivation
- revenue-leak modeling
- the difference between the $3,500 implementation sprint and the $7,500 Revenue Operating System

## Architecture

- Frontend: static, zero-dependency sales interface hosted on Vercel
- Data: Supabase project `ignite-revenue-os-demo`
- Reliability: Supabase-backed read-only demo data with a built-in fallback dataset
- Security: only the Supabase publishable key is used in browser code; all demo tables have RLS enabled and are public-read only

## Sales reliability

The scenario player is intentionally deterministic. External AI, SMS, telephony, and CRM services should be connected in a separate Live Mode so a sales call never depends on third-party API timing.

## Source location

This source currently lives in the `revenue-os-demo` branch under `ignite-company/pricing-page` so it remains isolated from Ignite HQ production. It can be moved into a dedicated repository later without changing the Supabase backend.
