#!/usr/bin/env python3
"""
SafeBite Inspection History Viewer
View detailed inspection history and violation data for restaurants
"""

import pandas as pd
import sqlite3
from pathlib import Path

def view_restaurant_inspections():
    """View inspection history for restaurants"""
    
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
    
    # Show restaurants with different inspection results
    examples = df.head(10)[['RestaurantID', 'RestaurantName', 'City', 'SafetyScore', 
                           'SafetyRating', 'LastInspectionDate', 'InspectionResult', 
                           'InspectionScore', 'LatestViolation', 'ViolationSeverity']]
    
    for _, row in examples.iterrows():
        print(f"\n🏪 {row['RestaurantName']} ({row['RestaurantID']})")
        print(f"   📍 Location: {row['City']}")
        print(f"   📊 Safety Score: {row['SafetyScore']}/100 ({row['SafetyRating']})")
        print(f"   🗓️  Last Inspection: {row['LastInspectionDate']}")
        print(f"   ✅ Result: {row['InspectionResult']} (Score: {row['InspectionScore']})")
        print(f"   ⚠️  Latest Violation: {row['LatestViolation']} ({row['ViolationSeverity']})")

def search_restaurant_by_id():
    """Search for specific restaurant inspection history"""
    csv_path = Path(__file__).parent / "SafeBite_Synthetic_Dataset_1000_Restaurants.csv"
    df = pd.read_csv(csv_path)
    
    print("\n" + "=" * 60)
    print("🔍 SEARCH RESTAURANT INSPECTION HISTORY")
    print("=" * 60)
    
    restaurant_id = input("\nEnter Restaurant ID (e.g., R0001): ").strip().upper()
    
    restaurant = df[df['RestaurantID'] == restaurant_id]
    
    if restaurant.empty:
        print(f"❌ Restaurant {restaurant_id} not found!")
        return
    
    row = restaurant.iloc[0]
    
    print(f"\n🏪 DETAILED INSPECTION HISTORY FOR {row['RestaurantName']}")
    print("-" * 50)
    print(f"📍 Location: {row['Address']}, {row['City']}, {row['State']}")
    print(f"📞 Contact: {row['Phone']} | {row['Email']}")
    print(f"🍽️  Cuisine: {row['Cuisine']}")
    print(f"📜 License: {row['LicenseNumber']} ({row['LicenseStatus']})")
    print(f"🏪 Status: {row['RestaurantStatus']}")
    
    print(f"\n📊 SAFETY & INSPECTION DATA:")
    print(f"   Overall Safety Score: {row['SafetyScore']}/100")
    print(f"   Safety Rating: {row['SafetyRating']}")
    print(f"   Last Inspection Date: {row['LastInspectionDate']}")
    print(f"   Inspection Result: {row['InspectionResult']}")
    print(f"   Inspection Score: {row['InspectionScore']}/100")
    
    print(f"\n⚠️  VIOLATIONS HISTORY:")
    print(f"   Previous Violations Count: {row['PreviousViolations']}")
    print(f"   Latest Violation: {row['LatestViolation']}")
    print(f"   Violation Severity: {row['ViolationSeverity']}")
    
    print(f"\n📝 COMPLAINTS DATA:")
    print(f"   Total Complaints: {row['ComplaintCount']}")
    print(f"   Latest Complaint: {row['LatestComplaint']}")
    print(f"   Complaint Status: {row['ComplaintStatus']}")
    
    print(f"\n⭐ PUBLIC ENGAGEMENT:")
    print(f"   Bookmark Count: {row['BookmarkCount']}")

def show_worst_performers():
    """Show restaurants with poor inspection results"""
    csv_path = Path(__file__).parent / "SafeBite_Synthetic_Dataset_1000_Restaurants.csv"
    df = pd.read_csv(csv_path)
    
    print("\n" + "=" * 60)
    print("⚠️  RESTAURANTS REQUIRING ATTENTION")
    print("=" * 60)
    
    # Failed inspections
    failed = df[df['InspectionResult'] == 'Failed'].sort_values('SafetyScore')
    print(f"\n❌ FAILED INSPECTIONS ({len(failed)} restaurants):")
    for _, row in failed.head(5).iterrows():
        print(f"   {row['RestaurantID']}: {row['RestaurantName']} - Score: {row['SafetyScore']}")
        print(f"      Latest Violation: {row['LatestViolation']} ({row['ViolationSeverity']})")
    
    # Critical violations
    critical = df[df['ViolationSeverity'] == 'Critical'].sort_values('SafetyScore')
    print(f"\n🚨 CRITICAL VIOLATIONS ({len(critical)} restaurants):")
    for _, row in critical.head(5).iterrows():
        print(f"   {row['RestaurantID']}: {row['RestaurantName']} - Score: {row['SafetyScore']}")
        print(f"      Critical Issue: {row['LatestViolation']}")

def main():
    """Main menu for inspection history viewer"""
    while True:
        print("\n🏥 SafeBite Inspection History Viewer")
        print("=" * 40)
        print("1. View Overall Inspection Statistics")
        print("2. Search Specific Restaurant")
        print("3. View Worst Performers")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            view_restaurant_inspections()
        elif choice == '2':
            search_restaurant_by_id()
        elif choice == '3':
            show_worst_performers()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-4.")

if __name__ == "__main__":
    main()