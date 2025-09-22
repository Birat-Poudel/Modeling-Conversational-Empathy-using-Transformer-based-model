import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_intent_visualizations(df):
    """Create visualizations for intent data"""
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Query Intent Analysis', fontsize=16, fontweight='bold')
    
    # 1. Intent Distribution (Bar Chart)
    intent_counts = df['intent'].value_counts()
    axes[0, 0].bar(range(len(intent_counts)), intent_counts.values, color='skyblue')
    axes[0, 0].set_title('Intent Distribution')
    axes[0, 0].set_xlabel('Intent Categories')
    axes[0, 0].set_ylabel('Number of Queries')
    axes[0, 0].set_xticks(range(len(intent_counts)))
    axes[0, 0].set_xticklabels(intent_counts.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, v in enumerate(intent_counts.values):
        axes[0, 0].text(i, v + 50, str(v), ha='center', va='bottom')
    
    # 2. Query Length Distribution
    query_lengths = df['query'].str.len()
    axes[0, 1].hist(query_lengths, bins=30, color='lightgreen', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Query Length Distribution')
    axes[0, 1].set_xlabel('Query Length (characters)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].axvline(query_lengths.mean(), color='red', linestyle='--', 
                       label=f'Mean: {query_lengths.mean():.1f}')
    axes[0, 1].legend()
    
    # 3. Response Length Distribution
    response_lengths = df['response'].str.len()
    axes[1, 0].hist(response_lengths, bins=30, color='lightcoral', alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Response Length Distribution')
    axes[1, 0].set_xlabel('Response Length (characters)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].axvline(response_lengths.mean(), color='blue', linestyle='--', 
                       label=f'Mean: {response_lengths.mean():.1f}')
    axes[1, 0].legend()
    
    # 4. Intent Distribution (Pie Chart)
    top_intents = intent_counts.head(8)
    others = intent_counts.tail(len(intent_counts) - 8).sum()
    if others > 0:
        pie_data = list(top_intents.values) + [others]
        pie_labels = list(top_intents.index) + ['Others']
    else:
        pie_data = top_intents.values
        pie_labels = top_intents.index
    
    axes[1, 1].pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title('Intent Distribution (Percentage)')
    
    plt.tight_layout()
    plt.savefig('/home/leapfrog/Desktop/mce/data_visualizations/intent_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_sentiment_visualizations(df):
    """Create visualizations for sentiment data"""
    
    # Set style
    plt.style.use('default')
    sns.set_palette("Set2")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Query Sentiment Analysis', fontsize=16, fontweight='bold')
    
    # 1. Sentiment Distribution (Bar Chart)
    sentiment_counts = df['sentiment'].value_counts()
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    bars = axes[0, 0].bar(sentiment_counts.index, sentiment_counts.values, color=colors)
    axes[0, 0].set_title('Sentiment Distribution')
    axes[0, 0].set_xlabel('Sentiment')
    axes[0, 0].set_ylabel('Number of Queries')
    
    # Add value labels on bars
    for bar, value in zip(bars, sentiment_counts.values):
        axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                        str(value), ha='center', va='bottom')
    
    # 2. Query Length by Sentiment (Box Plot)
    df['query_length'] = df['query'].str.len()
    sns.boxplot(data=df, x='sentiment', y='query_length', ax=axes[0, 1])
    axes[0, 1].set_title('Query Length Distribution by Sentiment')
    axes[0, 1].set_xlabel('Sentiment')
    axes[0, 1].set_ylabel('Query Length (characters)')
    
    # 3. Query Length Distribution (Histogram)
    for sentiment in df['sentiment'].unique():
        sentiment_data = df[df['sentiment'] == sentiment]['query_length']
        axes[1, 0].hist(sentiment_data, alpha=0.6, label=sentiment, bins=30)
    
    axes[1, 0].set_title('Query Length Distribution by Sentiment')
    axes[1, 0].set_xlabel('Query Length (characters)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].legend()
    
    # 4. Sentiment Distribution (Pie Chart)
    axes[1, 1].pie(sentiment_counts.values, labels=sentiment_counts.index, 
                   autopct='%1.1f%%', startangle=90, colors=colors)
    axes[1, 1].set_title('Sentiment Distribution (Percentage)')
    
    plt.tight_layout()
    plt.savefig('/home/leapfrog/Desktop/mce/data_visualizations/sentiment_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_summary_stats():
    """Create a summary statistics visualization"""
    
    # Load both datasets
    intent_df = pd.read_csv('/home/leapfrog/Desktop/mce/data/query_intent_response.csv')
    sentiment_df = pd.read_csv('/home/leapfrog/Desktop/mce/data/query_sentiment.csv')
    
    # Create summary figure
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Dataset Overview', fontsize=16, fontweight='bold')
    
    # Dataset sizes
    datasets = ['Intent Dataset', 'Sentiment Dataset']
    sizes = [len(intent_df), len(sentiment_df)]
    
    axes[0].bar(datasets, sizes, color=['lightblue', 'lightgreen'])
    axes[0].set_title('Dataset Sizes')
    axes[0].set_ylabel('Number of Records')
    
    # Add value labels
    for i, v in enumerate(sizes):
        axes[0].text(i, v + 500, f'{v:,}', ha='center', va='bottom')
    
    # Categories comparison
    categories = ['Intent Categories', 'Sentiment Categories']
    cat_counts = [intent_df['intent'].nunique(), sentiment_df['sentiment'].nunique()]
    
    axes[1].bar(categories, cat_counts, color=['orange', 'purple'])
    axes[1].set_title('Number of Categories')
    axes[1].set_ylabel('Number of Unique Categories')
    
    # Add value labels
    for i, v in enumerate(cat_counts):
        axes[1].text(i, v + 0.2, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('/home/leapfrog/Desktop/mce/data_visualizations/dataset_overview.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Main function to create all visualizations"""
    try:
        print("Loading datasets...")
        intent_df = pd.read_csv('/home/leapfrog/Desktop/mce/data/query_intent_response.csv')
        sentiment_df = pd.read_csv('/home/leapfrog/Desktop/mce/data/query_sentiment.csv')
        
        print("Creating intent visualizations...")
        create_intent_visualizations(intent_df)
        
        print("Creating sentiment visualizations...")
        create_sentiment_visualizations(sentiment_df)
        
        print("Creating summary statistics...")
        create_summary_stats()
        
        print("All visualizations created successfully!")
        print("Generated files:")
        print("- intent_analysis.png")
        print("- sentiment_analysis.png") 
        print("- dataset_overview.png")
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    main()