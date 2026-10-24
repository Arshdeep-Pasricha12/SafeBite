# SafeBite — Evaluator Demonstration Guide

**Demonstration Version:** 1.0.0  
**Target Audience:** Academic Reviewers, Technical Evaluators, Industry Stakeholders  

---

## 1. Overview & Demonstration Goals

This guide provides a reproducible, click-through sequence to evaluate all key capabilities of SafeBite without requiring paid API keys, commercial delivery accounts, or external network access.

---

## 2. Pre-Demo Checklist

1. **Backend Server Running:** `http://127.0.0.1:8000` (`curl http://127.0.0.1:8000/api/health` returns `200 OK`).
2. **Frontend Running:** `http://127.0.0.1:5173`.
3. **Database Migrated & Populated:** `database/safebite.db` contains official FSSAI/NYC records and tagged benchmark fixtures.
4. **Demo Credentials Ready:**
   - **Admin:** `admin@safebite.demo` / `adminpassword`
   - **Customer:** `customer@safebite.demo` / `password123`
   - **Owner:** `owner@safebite.demo` / `password123`

---

## 3. Step-by-Step Evaluator Walkthrough

### Act 1: Customer Discovery & Data Provenance
1. **Open SafeBite Homepage:**
   - Navigate to `http://127.0.0.1:5173/`.
   - Observe the hero search bar, safety score transparency banner, and feature overview.
2. **Navigate to Restaurant Discovery:**
   - Click **Explore Restaurants** in the navbar (or visit `http://127.0.0.1:5173/restaurants`).
   - Notice the listing cards displaying safety score rings (e.g. 96, 92), letter grades (Grade A / Excellent), and data source badges.
3. **Filter by Data Provenance:**
   - Locate the **Data Provenance** dropdown filter on the left sidebar.
   - Select **Verified Official Only (FSSAI / NYC OpenData)**.
   - Observe the live filtered results: Only official government records (such as *Haldiram's*, *Shake Shack*, *Chipotle*) are displayed, each carrying a green verified shield icon.
   - Switch the filter to **Synthetic Benchmark Only** to demonstrate explicit synthetic segregation.

---

### Act 2: Explainable Food-Safety Assessment & Inspection Timeline
1. **Open Restaurant Detail Page:**
   - Click on **Haldiram's Sweets & Restaurant** (or open `http://127.0.0.1:5173/restaurants/R0001`).
2. **Inspect the Explainable Assessment Card:**
   - Scroll to the **Explainable Food-Safety Evaluation** section.
   - Review the factor breakdown:
     - **Base Compliance Score:** 100/100
     - **Positive Factors:** Active FSSAI FoSTaC License, certified sanitary staff.
     - **Deductions:** Minor equipment maintenance (-4 pts).
     - **Net Calculated Score:** 96 (Grade A: Excellent).
3. **Review Inspection History Timeline:**
   - Scroll down to the **Inspection Timeline**.
   - Notice the date, inspector credential ID (`INS001`), inspection score, and official government registry audit link (`Audit Registry Source`).

---

### Act 3: Owner Dispute & Data Correction Workflow
1. **Submit a Correction Request:**
   - On the restaurant detail page, click the **Submit Data Correction / Dispute** button.
   - The interactive modal appears. Fill in:
     - *Issue Type:* "Inaccurate Inspection Mapping"
     - *Reason / Discrepancy:* "Recent facility re-inspection on Oct 10 cleared the minor plumbing notice."
     - *Supporting Evidence URL:* `https://fostac.fssai.gov.in/audits/reinspection-cleared-oct2026.pdf`
   - Click **Submit Correction Request**. An alert confirms successful registration with the administrative moderation queue.

---

### Act 4: Administrator Governance & Approval
1. **Log in as Administrator:**
   - Click **Sign In** in the top navbar (or navigate to `http://127.0.0.1:5173/login`).
   - Click the quick-fill button **Admin (admin@safebite.demo)** or type `admin@safebite.demo` / `adminpassword`.
   - Click **Sign In**. You are redirected to `/admin/dashboard`.
2. **Review Pending Correction Requests:**
   - On the Admin Dashboard, click the **Correction Requests** tab.
   - View the correction request submitted in Act 3 with its supporting evidence link.
   - Click **Approve** (or **Reject** with moderator notes) to demonstrate the closed-loop governance workflow!

---

### Act 5: Companion Food Ordering Demonstration
1. **Navigate to the Companion Ordering Demo:**
   - Click **Demo: Order Food** in the navbar (or visit `http://127.0.0.1:5173/demo/order`).
2. **Select Restaurant and Browse Dishes:**
   - Select *Haldiram's Sweets & Restaurant* or *Chipotle Mexican Grill*.
   - Notice the prominent **SafeBite Injected Safety Pill** floating above the restaurant header.
3. **Add Items to Basket:**
   - Add "Special Chole Bhature" and "Raj Kachori" to the delivery basket.
   - Notice the order subtotal, delivery fee, and tax calculations update dynamically in real time.
4. **Trigger the Pre-Checkout Safety Audit Modal:**
   - Click **View Safety Audit Breakdown** on the floating SafeBite banner.
   - A pre-checkout modal appears explaining that the restaurant meets Grade A standards with zero critical foodborne pathogen risks.

---

### Act 6: Google Chrome Extension Demonstration (Optional)
1. In Google Chrome, go to `chrome://extensions/` $\rightarrow$ enable Developer Mode $\rightarrow$ **Load unpacked** $\rightarrow$ select the `extension/` directory.
2. Open `http://127.0.0.1:5173/demo/order`.
3. Notice the SafeBite Chrome Extension automatically detects the restaurant title from the DOM, matches it via `GET /api/restaurants/match`, and renders the floating extension pill!
