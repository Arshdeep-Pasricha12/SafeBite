import datetime
from typing import List, Optional, Dict, Any

class FoodSafetyAssessmentEngine:
    """
    Explainable, deterministic food-safety risk assessment engine for SafeBite.
    
    Evaluates:
    - Critical vs non-critical violations
    - Repeat violations with escalating penalties
    - Inspection recency and data freshness decay
    - Verified complaint history
    - License status
    - Data provenance transparency
    """

    CRITICAL_PENALTY = 18
    MAJOR_PENALTY = 8
    MINOR_PENALTY = 3
    REPEAT_MULTIPLIER = 1.5
    VERIFIED_COMPLAINT_PENALTY = 6
    STALE_DAYS_THRESHOLD = 365
    EXPIRED_DAYS_THRESHOLD = 730

    @classmethod
    def evaluate(
        cls,
        restaurant_data: Dict[str, Any],
        inspections_data: Optional[List[Dict[str, Any]]] = None,
        complaints_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate food safety and return deterministic score, rating, grade,
        and human-readable explainability factors.
        """
        inspections = inspections_data or []
        complaints = complaints_data or []
        
        # Sort inspections descending by inspection_date
        def get_date(insp):
            d = insp.get("inspection_date")
            if isinstance(d, datetime.date):
                return d
            if isinstance(d, str):
                try:
                    return datetime.date.fromisoformat(d.split("T")[0])
                except Exception:
                    return datetime.date.min
            return datetime.date.min

        sorted_inspections = sorted(inspections, key=get_date, reverse=True)
        latest_inspection = sorted_inspections[0] if sorted_inspections else None
        
        score = 100
        risk_factors: List[str] = []
        positive_factors: List[str] = []
        
        today = datetime.date.today()
        days_since_inspection: Optional[int] = None
        data_freshness_status = "Unknown"
        confidence_score = 0.50

        # 1. Inspection Recency & Staleness Evaluation
        if latest_inspection and latest_inspection.get("inspection_date"):
            insp_date = get_date(latest_inspection)
            days_since_inspection = (today - insp_date).days
            
            if days_since_inspection <= 180:
                data_freshness_status = "Current"
                confidence_score = 0.95
                positive_factors.append(f"Recent inspection conducted {days_since_inspection} days ago.")
            elif days_since_inspection <= cls.STALE_DAYS_THRESHOLD:
                data_freshness_status = "Current"
                confidence_score = 0.85
                positive_factors.append(f"Inspected within the past year ({days_since_inspection} days ago).")
            elif days_since_inspection <= cls.EXPIRED_DAYS_THRESHOLD:
                data_freshness_status = "Stale"
                confidence_score = 0.60
                score -= 5
                risk_factors.append(f"Inspection is {days_since_inspection} days old (>1 year). Safety conditions may have changed.")
            else:
                data_freshness_status = "Expired"
                confidence_score = 0.35
                score -= 12
                risk_factors.append(f"Data is expired ({days_since_inspection} days since last inspection). Re-audit strongly recommended.")
        else:
            data_freshness_status = "Uninspected"
            confidence_score = 0.20
            risk_factors.append("No official inspection record available on file.")

        # 2. License Status Check
        license_status = str(restaurant_data.get("license_status", "Active")).strip()
        if license_status.lower() == "suspended":
            score = min(score, 35)
            risk_factors.append("Health license is currently SUSPENDED by authorities.")
        elif license_status.lower() == "expired":
            score -= 20
            risk_factors.append("Health license is EXPIRED. Operating without current certification.")
        elif license_status.lower() == "under review":
            score -= 10
            risk_factors.append("Health license is currently under administrative review.")
        else:
            positive_factors.append("Active and verified food safety operating license.")

        # 3. Violation Deductions (from latest inspection or restaurant summaries)
        critical_count = 0
        non_critical_count = 0
        repeat_count = 0

        if latest_inspection and "violations" in latest_inspection:
            violations = latest_inspection.get("violations", [])
            for v in violations:
                severity = str(v.get("severity", "") or v.get("severity_level", "")).lower()
                desc = v.get("description", "Safety infraction")
                is_repeat = bool(v.get("repeat_violation", False))
                points_deducted = v.get("points_deducted", 0)

                mult = cls.REPEAT_MULTIPLIER if is_repeat else 1.0
                if is_repeat:
                    repeat_count += 1

                if severity == "critical":
                    critical_count += 1
                    penalty = int(cls.CRITICAL_PENALTY * mult)
                    score -= penalty
                    rep_text = " [REPEAT OFFENSE]" if is_repeat else ""
                    risk_factors.append(f"Critical Violation (-{penalty} pts): {desc}{rep_text}")
                elif severity in ["major", "medium"]:
                    non_critical_count += 1
                    penalty = int(cls.MAJOR_PENALTY * mult)
                    score -= penalty
                    rep_text = " [REPEAT OFFENSE]" if is_repeat else ""
                    risk_factors.append(f"Major Violation (-{penalty} pts): {desc}{rep_text}")
                else:
                    non_critical_count += 1
                    penalty = int(cls.MINOR_PENALTY * mult)
                    score -= penalty
                    risk_factors.append(f"Minor Violation (-{penalty} pts): {desc}")

        elif restaurant_data.get("previous_violations"):
            # Fallback to restaurant summary violation data
            prev_viol = int(restaurant_data.get("previous_violations", 0))
            severity = str(restaurant_data.get("violation_severity", "")).lower()
            latest_v = restaurant_data.get("latest_violation") or "Standard sanitation notice"
            if severity == "critical":
                critical_count += 1
                penalty = cls.CRITICAL_PENALTY
                score -= penalty
                risk_factors.append(f"Critical Violation (-{penalty} pts): {latest_v}")
            elif severity == "major":
                non_critical_count += 1
                penalty = cls.MAJOR_PENALTY
                score -= penalty
                risk_factors.append(f"Major Violation (-{penalty} pts): {latest_v}")
            elif prev_viol > 0:
                non_critical_count += prev_viol
                penalty = min(prev_viol * cls.MINOR_PENALTY, 15)
                score -= penalty
                risk_factors.append(f"Past Violations (-{penalty} pts): {latest_v}")

        if critical_count == 0:
            positive_factors.append("Zero critical food safety violations recorded on latest inspection.")
        if repeat_count == 0:
            positive_factors.append("No repeated violations identified.")

        # 4. Complaints Check
        verified_complaints = [
            c for c in complaints 
            if str(c.get("status", "")).lower() in ["verified", "resolved"]
        ]
        pending_complaints = [
            c for c in complaints 
            if str(c.get("status", "")).lower() in ["submitted", "under investigation"]
        ]
        
        active_complaints_count = len(verified_complaints) + len(pending_complaints)
        if verified_complaints:
            comp_penalty = len(verified_complaints) * cls.VERIFIED_COMPLAINT_PENALTY
            score -= comp_penalty
            risk_factors.append(f"Verified Food Safety Complaints (-{comp_penalty} pts): {len(verified_complaints)} substantiated complaints on record.")
        if pending_complaints:
            risk_factors.append(f"Active Complaints: {len(pending_complaints)} unresolved consumer complaints currently under investigation.")

        # Clamp Score
        score = max(0, min(100, score))

        # 5. Determine Rating & Grade Label
        if license_status.lower() == "suspended":
            safety_rating = "Poor"
            grade_label = "High Risk / Alert"
            risk_level = "Critical"
            summary_explanation = "Health operating license is SUSPENDED by regulatory authorities due to safety infractions."
            consumer_advice = "DO NOT ORDER. Operating privileges have been suspended."
        elif data_freshness_status == "Uninspected":
            safety_rating = "Fair"
            grade_label = "Uninspected / Pending"
            risk_level = "Medium"
            summary_explanation = "This restaurant has not yet received an official on-site inspection in our database."
            consumer_advice = "Check restaurant licensing before ordering; official compliance verification is pending."
        elif score < 60 or critical_count >= 2:
            safety_rating = "Poor"
            grade_label = "High Risk / Alert"
            risk_level = "Critical" if score < 50 else "High"
            summary_explanation = f"High food safety risk identified with a compliance score of {score}/100 and {critical_count} critical citation(s)."
            consumer_advice = "Avoid ordering until a verified re-inspection confirms corrective action on sanitation."
        elif score < 75 or critical_count == 1:
            safety_rating = "Fair"
            grade_label = "Needs Improvement"
            risk_level = "Medium"
            summary_explanation = f"Moderate compliance score of {score}/100. Notable citations require corrective oversight."
            consumer_advice = "Exercise discretion. Inquire about food preparation hygiene or choose fully cleared items."
        elif score < 90:
            safety_rating = "Good"
            grade_label = "Good / Low Risk"
            risk_level = "Low"
            summary_explanation = f"Good food safety standards with a score of {score}/100 and no critical violations."
            consumer_advice = "Safe dining choice with routine compliance standards verified."
        else:
            safety_rating = "Excellent"
            grade_label = "Pass / Excellent"
            risk_level = "Low"
            summary_explanation = f"Exemplary food hygiene and safety compliance ({score}/100) with complete regulatory adherence."
            consumer_advice = "Highly recommended for safe dining and ordering."

        # Append stale warning to grade label if applicable
        if data_freshness_status == "Stale" and grade_label not in ["Uninspected / Pending"]:
            grade_label += " (Stale Data)"

        # 6. Provenance Disclaimer
        is_synthetic = bool(restaurant_data.get("is_synthetic", True))
        source_name = restaurant_data.get("source_name") or "SafeBite Synthetic Benchmark"
        verification_status = restaurant_data.get("verification_status") or ("Synthetic Demonstration" if is_synthetic else "Verified Official")

        if is_synthetic or verification_status == "Synthetic Demonstration":
            provenance_disclaimer = f"DEMONSTRATION RECORD: This score is calculated from simulated benchmark data ({source_name}) for testing and demonstration purposes. It does not represent real government audit findings."
        else:
            provenance_disclaimer = f"OFFICIAL DATA: Sourced from verified public health records ({source_name}). Verification status: {verification_status}."

        return {
            "safety_score": score,
            "safety_rating": safety_rating,
            "grade_label": grade_label,
            "risk_level": risk_level,
            "confidence_score": round(confidence_score, 2),
            "data_freshness_status": data_freshness_status,
            "days_since_inspection": days_since_inspection,
            "critical_violations_count": critical_count,
            "non_critical_violations_count": non_critical_count,
            "repeat_violations_count": repeat_count,
            "active_complaints_count": active_complaints_count,
            "risk_factors": risk_factors,
            "positive_factors": positive_factors,
            "summary_explanation": summary_explanation,
            "consumer_advice": consumer_advice,
            "provenance_disclaimer": provenance_disclaimer
        }
