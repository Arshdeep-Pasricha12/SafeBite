#!/usr/bin/env python3
"""
Show SafeBite Inspection Data
"""

import pandas as pd
from pathlib import Path

def show_inspection_overview():
    """Show inspection history overview"""
    
    # Load the CSV data which contains inspection history
    csv_path = Path(__file__).parent / "SafeBite_Synthetic_Dataset_1000_Restaurants.csv"
    df = pd.read_csv(csv_path)
    
    print("🏥 SafeBite - Restaurant Inspection History")
    print("=" * 60)
    
    # Show summary statistics
    print(f"\n📊 INSPECTION OVERVIEW:")
    print(f"Total Restaurants: {len(df)}")
    
    # Inspection Results Summary
    inspection_results = df['InspectionResult'].value_counts()
    print(f"\n🔍 INSPECTION RESULTS:")
    for result, count in inspection_results.items():
        percentage = (count / len(df)) * 100
        print(f"  {result}: {count} ({percentage:.1f}%)")
    
    # Safety Ratings Summary
    safety_ratings = df['SafetyRating'].value_counts()
    print(f"\n⭐ SAFETY RATINGS:")
    for rating, count in safety_ratings.items():
        percentage = (count / len(df)) * 100
        print(f"  {rating}: {count} ({percentage:.1f}%)")
    
    # Violation Severity Summary
    violation_severity = df['ViolationSeverity'].value_counts()
    print(f"\n⚠️  VIOLATION SEVERITY:")
    for severity, count in violation_severity.items():
        percentage = (count / len(df)) * 100
        print(f"  {severity}: {count} ({percentage:.1f}%)")
    
    # Show some example inspection records
    print(f"\n📋 SAMPLE INSPECTION RECORDS:")
    print("-" * 80)
    
    # Show first 5 restaurants with inspection details
    examples = df.head(5)[['RestaurantID', 'RestaurantName', 'City', 'SafetyScore', 
                           'SafetyRating', 'LastInspectionDate', 'InspectionResult', 
                           'InspectionScore', 'LatestViolation', 'ViolationSeverity']]
    
    for _, row in examples.iterrows():
        print(f"\n🏪 {row['RestaurantName']} ({row['RestaurantID']})")
        print(f"   📍 Location: {row['City']}")
        print(f"   📊 Safety Score: {row['SafetyScore']}/100 ({row['SafetyRating']})")
        print(f"   🗓️  Last Inspection: {row['LastInspectionDate']}")
        print(f"   ✅ Result: {row['InspectionResult']} (Score: {row['InspectionScore']})")
        print(f"   ⚠️  Latest Violation: {row['LatestViolation']} ({row['ViolationSeverity']})")
    
    # Show restaurants with failed inspections
    print(f"\n❌ FAILED INSPECTIONS:")
    print("-" * 50)
    failed = df[df['InspectionResult'] == 'Failed'].head(3)
    
    for _, row in failed.iterrows():
        print(f"\n🚨 {row['RestaurantName']} ({row['RestaurantID']})")
        print(f"   📍 {row['City']}, {row['State']}")
        print(f"   📊 Safety Score: {row['SafetyScore']}/100")
        print(f"   🗓️  Last Inspection: {row['LastInspectionDate']}")
        print(f"   ❌ Failed with Score: {row['InspectionScore']}")
        print(f"   ⚠️  Critical Issue: {row['LatestViolation']} ({row['ViolationSeverity']})")
        print(f"   📞 Contact: {row['Phone']}")

if __name__ == "__main__":
    show_inspection_overview()