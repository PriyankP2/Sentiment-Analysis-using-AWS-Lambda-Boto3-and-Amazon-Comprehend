import boto3
import json

def lambda_handler(event, context):
    """
    Lambda function to analyze sentiment of user reviews using Amazon Comprehend.
    
    This function performs the following operations:
    - Extracts text from the event
    - Sends text to Amazon Comprehend for sentiment analysis
    - Returns sentiment (POSITIVE, NEGATIVE, NEUTRAL, MIXED) and confidence scores
    - Logs detailed results to CloudWatch
    
    Args:
        event (dict): Lambda event object containing 'text' field with review text
        context (object): Lambda context object
    
    Returns:
        dict: Response containing status code and sentiment analysis results
    
    Example event:
    {
        "text": "This product is amazing! I absolutely love it."
    }
    """
    
    # Initialize Amazon Comprehend client
    comprehend_client = boto3.client('comprehend')
    
    try:
        # Extract text from event
        if 'text' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Error: No text provided in event',
                    'error': 'Missing required field: text'
                })
            }
        
        review_text = event['text']
        
        # Validate text is not empty
        if not review_text or not review_text.strip():
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Error: Text cannot be empty',
                    'error': 'Empty text provided'
                })
            }
        
        # Log the text being analyzed
        print(f"Analyzing sentiment for text: \"{review_text}\"")
        
        # Call Amazon Comprehend to detect sentiment
        response = comprehend_client.detect_sentiment(
            Text=review_text,
            LanguageCode='en'  # English language
        )
        
        # Extract sentiment and confidence scores
        sentiment = response['Sentiment']
        sentiment_scores = response['SentimentScore']
        
        # Log results
        print(f"Sentiment detected: {sentiment}")
        print("Confidence scores:")
        print(f"  Positive: {sentiment_scores['Positive'] * 100:.2f}%")
        print(f"  Negative: {sentiment_scores['Negative'] * 100:.2f}%")
        print(f"  Neutral: {sentiment_scores['Neutral'] * 100:.2f}%")
        print(f"  Mixed: {sentiment_scores['Mixed'] * 100:.2f}%")
        
        # Return success response with sentiment analysis
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Sentiment analysis completed successfully',
                'text': review_text,
                'sentiment': sentiment,
                'confidence_scores': {
                    'Positive': round(sentiment_scores['Positive'], 4),
                    'Negative': round(sentiment_scores['Negative'], 4),
                    'Neutral': round(sentiment_scores['Neutral'], 4),
                    'Mixed': round(sentiment_scores['Mixed'], 4)
                },
                'interpretation': get_sentiment_interpretation(sentiment, sentiment_scores)
            })
        }
        
    except Exception as e:
        # Log and return error
        print(f"Error analyzing sentiment: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error analyzing sentiment',
                'error': str(e)
            })
        }


def get_sentiment_interpretation(sentiment, scores):
    """
    Helper function to provide human-readable interpretation of sentiment.
    
    Args:
        sentiment (str): The detected sentiment (POSITIVE, NEGATIVE, NEUTRAL, MIXED)
        scores (dict): Confidence scores for each sentiment
    
    Returns:
        str: Human-readable interpretation
    """
    confidence = max(scores.values()) * 100
    
    interpretations = {
        'POSITIVE': f"This text expresses positive sentiment with {confidence:.1f}% confidence. "
                   "The content indicates satisfaction, happiness, or approval.",
        
        'NEGATIVE': f"This text expresses negative sentiment with {confidence:.1f}% confidence. "
                   "The content indicates dissatisfaction, disappointment, or disapproval.",
        
        'NEUTRAL': f"This text expresses neutral sentiment with {confidence:.1f}% confidence. "
                  "The content is factual or objective without strong positive or negative emotion.",
        
        'MIXED': f"This text expresses mixed sentiment with {confidence:.1f}% confidence. "
                "The content contains both positive and negative elements."
    }
    
    return interpretations.get(sentiment, "Unable to interpret sentiment")
