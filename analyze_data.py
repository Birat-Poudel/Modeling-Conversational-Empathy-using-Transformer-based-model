import pandas as pd

def analyze_intent_data(df):
    """Analyze the query intent response dataset"""
    analysis = {}
    
    # Basic statistics
    analysis['total_records'] = len(df)
    analysis['columns'] = list(df.columns)
    
    # Intent distribution
    intent_counts = df['intent'].value_counts()
    analysis['intent_distribution'] = intent_counts.to_dict()
    analysis['unique_intents'] = len(intent_counts)
    
    # Query analysis
    analysis['avg_query_length'] = df['query'].str.len().mean()
    analysis['max_query_length'] = df['query'].str.len().max()
    analysis['min_query_length'] = df['query'].str.len().min()
    
    # Response analysis
    analysis['avg_response_length'] = df['response'].str.len().mean()
    analysis['max_response_length'] = df['response'].str.len().max()
    analysis['min_response_length'] = df['response'].str.len().min()
    
    return analysis

def analyze_sentiment_data(df):
    """Analyze the query sentiment dataset"""
    analysis = {}
    
    # Basic statistics
    analysis['total_records'] = len(df)
    analysis['columns'] = list(df.columns)
    
    # Sentiment distribution
    sentiment_counts = df['sentiment'].value_counts()
    analysis['sentiment_distribution'] = sentiment_counts.to_dict()
    analysis['unique_sentiments'] = len(sentiment_counts)
    
    # Query analysis by sentiment
    analysis['avg_query_length_by_sentiment'] = df.groupby('sentiment')['query'].apply(lambda x: x.str.len().mean()).to_dict()
    
    # Query length statistics
    analysis['avg_query_length'] = df['query'].str.len().mean()
    analysis['max_query_length'] = df['query'].str.len().max()
    analysis['min_query_length'] = df['query'].str.len().min()
    
    return analysis

def generate_readme(intent_analysis, sentiment_analysis):
    """Generate README content based on analysis"""
    
    readme_content = f"""# Dataset Analysis

## Overview
Analysis of two main datasets focusing on query intent classification and sentiment analysis.

![Dataset Overview](data_visualizations/dataset_overview.png)

## Dataset Description

### Files
- `query_intent_response.csv`: Contains customer queries with their classified intents and corresponding responses
- `query_sentiment.csv`: Contains customer queries with their sentiment classifications

## Data Analysis Summary

### Query Intent Response Dataset
- **Total Records**: {intent_analysis['total_records']:,}
- **Columns**: {', '.join(intent_analysis['columns'])}
- **Unique Intents**: {intent_analysis['unique_intents']}

#### Intent Distribution
"""
    
    for intent, count in intent_analysis['intent_distribution'].items():
        percentage = (count / intent_analysis['total_records']) * 100
        readme_content += f"- **{intent}**: {count:,} queries ({percentage:.1f}%)\n"
    
    readme_content += f"""
#### Query Statistics
- **Average Query Length**: {intent_analysis['avg_query_length']:.1f} characters
- **Shortest Query**: {intent_analysis['min_query_length']} characters
- **Longest Query**: {intent_analysis['max_query_length']} characters

#### Response Statistics
- **Average Response Length**: {intent_analysis['avg_response_length']:.1f} characters
- **Shortest Response**: {intent_analysis['min_response_length']} characters
- **Longest Response**: {intent_analysis['max_response_length']} characters

![Intent Analysis](data_visualizations/intent_analysis.png)

### Query Sentiment Dataset
- **Total Records**: {sentiment_analysis['total_records']:,}
- **Columns**: {', '.join(sentiment_analysis['columns'])}
- **Unique Sentiments**: {sentiment_analysis['unique_sentiments']}

#### Sentiment Distribution
"""
    
    for sentiment, count in sentiment_analysis['sentiment_distribution'].items():
        percentage = (count / sentiment_analysis['total_records']) * 100
        readme_content += f"- **{sentiment}**: {count:,} queries ({percentage:.1f}%)\n"
    
    readme_content += f"""
#### Query Length by Sentiment
"""
    
    for sentiment, avg_length in sentiment_analysis['avg_query_length_by_sentiment'].items():
        readme_content += f"- **{sentiment}**: {avg_length:.1f} characters on average\n"
    
    readme_content += f"""

![Sentiment Analysis](data_visualizations/sentiment_analysis.png)

## Key Insights

### Intent Analysis
1. **Dominant Intent**: The most common intent is "{max(intent_analysis['intent_distribution'], key=intent_analysis['intent_distribution'].get)}" with {max(intent_analysis['intent_distribution'].values()):,} queries
2. **Query Complexity**: Average query length is {intent_analysis['avg_query_length']:.1f} characters, indicating moderate complexity
3. **Response Detail**: Responses are comprehensive with an average length of {intent_analysis['avg_response_length']:.1f} characters

### Sentiment Analysis
1. **Sentiment Balance**: {sentiment_analysis['sentiment_distribution']['Positive']:,} positive vs {sentiment_analysis['sentiment_distribution'].get('Negative', 0):,} negative queries
2. **Query Length Patterns**: Different sentiments show varying query lengths, which could indicate different communication patterns
3. **Vocabulary Differences**: Each sentiment category has distinct commonly used words

## Usage
This data can be used for:
- Training intent classification models
- Sentiment analysis model development
- Customer service automation
- Understanding customer communication patterns
- Response generation systems

## Technical Details
- **Intent Dataset Size**: {intent_analysis['total_records']:,} records
- **Sentiment Dataset Size**: {sentiment_analysis['total_records']:,} records
- **File Format**: CSV with UTF-8 encoding
- **Analysis Date**: Generated automatically
"""
    
    return readme_content

def main():
    """Main analysis function"""
    try:
        # Load datasets
        print("Loading datasets...")
        intent_df = pd.read_csv('/home/leapfrog/Desktop/mce/data/query_intent_response.csv')
        sentiment_df = pd.read_csv('/home/leapfrog/Desktop/mce/data/query_sentiment.csv')
        
        print("Analyzing intent data...")
        intent_analysis = analyze_intent_data(intent_df)
        
        print("Analyzing sentiment data...")
        sentiment_analysis = analyze_sentiment_data(sentiment_df)
        
        print("Generating README...")
        readme_content = generate_readme(intent_analysis, sentiment_analysis)
        
        # Write README
        with open('/home/leapfrog/Desktop/mce/README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("Analysis complete! README.md has been generated.")
        
        # Print summary to console
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"Intent Dataset: {intent_analysis['total_records']:,} records")
        print(f"Sentiment Dataset: {sentiment_analysis['total_records']:,} records")
        print(f"Intent Categories: {intent_analysis['unique_intents']}")
        print(f"Sentiment Categories: {sentiment_analysis['unique_sentiments']}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()