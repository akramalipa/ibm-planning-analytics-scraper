#!/usr/bin/env python3
"""
Data Visualization Script for IBM Planning Analytics Features
Creates charts and graphs from the scraped data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def load_latest_csv():
    """Load the most recent CSV file"""
    csv_files = list(Path('.').glob('ibm_features_*.csv'))
    if not csv_files:
        print("Error: No CSV files found!")
        sys.exit(1)
    
    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
    print(f"Loading data from: {latest_file}")
    return pd.read_csv(latest_file)

def create_visualizations(df):
    """Create multiple visualizations"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 14))
    
    # 1. Features by Functional Area (Top 10 for clarity)
    ax1 = plt.subplot(2, 2, 1)
    functional_area_counts = df['Functional area'].value_counts().head(10)
    bars = functional_area_counts.plot(kind='barh', ax=ax1, color='steelblue', edgecolor='black', linewidth=1.2)
    ax1.set_title('Top 10 Functional Areas by Feature Count', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Number of Features', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Functional Area', fontsize=13, fontweight='bold')
    ax1.tick_params(axis='both', labelsize=11)
    # Add value labels on bars
    for i, v in enumerate(functional_area_counts.values):
        ax1.text(v + 2, i, str(v), va='center', fontsize=11, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. Feature Distribution Pie Chart (Top 7 - all unique areas)
    ax2 = plt.subplot(2, 2, 2)
    top_areas = df['Functional area'].value_counts()
    colors = plt.cm.Set3(range(len(top_areas)))
    wedges, texts, autotexts = ax2.pie(top_areas.values, labels=None, autopct='%1.1f%%',
            startangle=90, colors=colors, textprops={'fontsize': 12, 'fontweight': 'bold'},
            pctdistance=0.85, explode=[0.05] * len(top_areas))
    ax2.set_title('Functional Areas Distribution', fontsize=16, fontweight='bold', pad=20)
    # Create legend with clear labels
    legend_labels = [f'{area} ({count})' for area, count in top_areas.items()]
    ax2.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
               fontsize=11, frameon=True, shadow=True)
    
    # 3. Features Over Time (Top 15 for better readability)
    ax3 = plt.subplot(2, 2, 3)
    version_counts = df['Release dateVersion number'].value_counts().head(15)
    bars = version_counts.plot(kind='bar', ax=ax3, color='coral', edgecolor='black', linewidth=1.2)
    ax3.set_title('Features by Release Version (Top 15)', fontsize=16, fontweight='bold', pad=20)
    ax3.set_xlabel('Release Version', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Number of Features', fontsize=13, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45, labelsize=10)
    ax3.tick_params(axis='y', labelsize=11)
    # Add value labels on bars
    for i, (idx, v) in enumerate(version_counts.items()):
        ax3.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Summary Statistics
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    
    stats_text = f"""
    📊 DATA SUMMARY
    {'═'*50}
    
    📈 Total Features: {len(df):,}
    
    🏷️  Unique Functional Areas: {df['Functional area'].nunique()}
    
    📅 Unique Release Versions: {df['Release dateVersion number'].nunique()}
    
    🔝 Top 5 Functional Areas:
    """
    
    for i, (area, count) in enumerate(df['Functional area'].value_counts().head(5).items(), 1):
        percentage = (count / len(df)) * 100
        stats_text += f"\n    {i}. {area[:35]:35s} : {count:3d} ({percentage:5.1f}%)"
    
    stats_text += f"\n\n    {'─'*50}\n    Latest Release: {df['Release dateVersion number'].value_counts().index[0]}"
    
    ax4.text(0.05, 0.5, stats_text, fontsize=13, family='monospace',
             verticalalignment='center', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout(pad=3.0)
    
    # Save the figure
    output_file = 'ibm_features_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Visualization saved to: {output_file}")
    
    # Show the plot
    plt.show()
    
    return output_file

def print_summary(df):
    """Print detailed summary statistics"""
    print("\n" + "="*60)
    print("DETAILED DATA ANALYSIS")
    print("="*60)
    
    print(f"\nTotal Records: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"\nColumn Names: {', '.join(df.columns)}")
    
    print("\n--- Functional Area Statistics ---")
    print(f"Unique Functional Areas: {df['Functional area'].nunique()}")
    print("\nTop 10 Functional Areas:")
    for i, (area, count) in enumerate(df['Functional area'].value_counts().head(10).items(), 1):
        percentage = (count / len(df)) * 100
        print(f"  {i:2d}. {area:40s} : {count:3d} ({percentage:5.2f}%)")
    
    print("\n--- Release Version Statistics ---")
    print(f"Unique Release Versions: {df['Release dateVersion number'].nunique()}")
    print("\nTop 10 Release Versions:")
    for i, (version, count) in enumerate(df['Release dateVersion number'].value_counts().head(10).items(), 1):
        print(f"  {i:2d}. {version:30s} : {count:3d}")
    
    print("\n" + "="*60)

def main():
    """Main execution function"""
    print("IBM Planning Analytics Features - Data Visualization")
    print("="*60)
    
    # Load data
    df = load_latest_csv()
    
    # Print summary
    print_summary(df)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_visualizations(df)
    
    print("\n✓ Analysis complete!")

if __name__ == "__main__":
    main()

# Made with Bob
