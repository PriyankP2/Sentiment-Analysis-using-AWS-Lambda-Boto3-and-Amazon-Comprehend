# Sentiment Analysis - Complete Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Code Explanation](#code-explanation)
6. [Testing and Verification](#testing-and-verification)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Introduction

### Project Goal
Create an automated sentiment analysis system using AWS Lambda and Amazon Comprehend. The function analyzes user reviews and feedback to determine if the sentiment is positive, negative, neutral, or mixed.

### What is Sentiment Analysis?
Sentiment analysis (also called opinion mining) is a natural language processing (NLP) technique that identifies the emotional tone behind text. It helps understand whether the writer's attitude is:
- **Positive** - expressing satisfaction, happiness, approval
- **Negative** - expressing dissatisfaction, disappointment, disapproval
- **Neutral** - factual, objective, without strong emotion
- **Mixed** - containing both positive and negative elements

### Real-World Use Cases
- **E-commerce**: Analyze product reviews to understand customer satisfaction
- **Customer Support**: Automatically prioritize negative feedback
- **Social Media**: Monitor brand sentiment across platforms
- **Market Research**: Analyze survey responses
- **Content Moderation**: Flag potentially negative or harmful content

### Technologies Used
- **AWS Lambda**: Serverless compute service
- **Amazon Comprehend**: Natural language processing (NLP) service
- **Boto3**: AWS SDK for Python
- **AWS IAM**: Identity and Access Management
- **CloudWatch Logs**: Logging and monitoring

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                               │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         User Input / Test Event                    │    │
│  │                                                     │    │
│  │  {                                                  │    │
│  │    "text": "This product is amazing!"              │    │
│  │  }                                                  │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │      Lambda Function: Sentiment-Analyzer           │    │
│  │                                                     │    │
│  │  1. Extract text from event                        │    │
│  │  2. Validate text input                            │    │
│  │  3. Call Amazon Comprehend API                     │    │
│  │  4. Receive sentiment analysis                     │    │
│  │  5. Log results                                    │    │
│  │  6. Return response                                │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Amazon Comprehend                          │    │
│  │                                                     │    │
│  │  - Natural Language Processing                     │    │
│  │  - Sentiment Detection                             │    │
│  │  - Confidence Score Calculation                    │    │
│  │  - Multi-language Support (using English)          │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Response                               │    │
│  │                                                     │    │
│  │  {                                                  │    │
│  │    "sentiment": "POSITIVE",                        │    │
│  │    "confidence_scores": {                          │    │
│  │      "Positive": 0.9987,                           │    │
│  │      "Negative": 0.0002,                           │    │
│  │      "Neutral": 0.0008,                            │    │
│  │      "Mixed": 0.0003                               │    │
│  │    }                                                │    │
│  │  }                                                  │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │           CloudWatch Logs                          │    │
│  │                                                     │    │
│  │  - Input text logged                               │    │
│  │  - Sentiment result logged                         │    │
│  │  - Confidence scores logged                        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Workflow:**
1. User provides text input (review, feedback, comment)
2. Lambda function receives the text
3. Function calls Amazon Comprehend's sentiment detection API
4. Comprehend analyzes the text and returns sentiment + confidence scores
5. Lambda logs the results
6. Response is returned to the user

---

## Prerequisites

### AWS Account Requirements
- Active AWS account with console access
- No additional resources needed (just Lambda and Comprehend)
- Amazon Comprehend is available in most regions

### Knowledge Requirements
- Basic understanding of text analysis
- Familiarity with AWS Lambda
- Python basics
- Understanding of JSON format

### Cost Considerations
**Amazon Comprehend Pricing:**
- **Free Tier**: 50,000 units per month for first 12 months
- **After Free Tier**: $0.0001 per unit (100 characters = 1 unit)
- **This Assignment**: ~10-20 test requests = FREE (well within free tier)

**AWS Lambda Pricing:**
- **Free Tier**: 1 million requests per month
- **This Assignment**: ~10 requests = FREE

---

## Step-by-Step Implementation

### Step 1: Create IAM Role for Lambda

#### 1.1 Navigate to IAM Service

1. Log in to [AWS Management Console](https://console.aws.amazon.com)
2. In the search bar at the top, type **"IAM"**
3. Click on **"IAM"** under Services

#### 1.2 Create New Role

1. In the left sidebar, click **"Roles"**
2. Click **"Create role"** button

#### 1.3 Select Trusted Entity

1. **Trusted entity type**: Select **"AWS service"**
2. **Use case**: Select **"Lambda"**
3. Click **"Next"**

#### 1.4 Attach Permissions Policy

1. In the search box, type: `ComprehendReadOnly`

2. **Check the checkbox** next to **"ComprehendReadOnly"**
   - This policy allows read-only access to Amazon Comprehend
   - Includes `comprehend:DetectSentiment` permission

3. Click **"Next"**

**Note**: This is a read-only policy which is perfect for sentiment analysis.

#### 1.5 Name and Create Role

1. **Role name**: `Lambda-Comprehend-Role`
2. **Description**: `Allows Lambda to use Amazon Comprehend for sentiment analysis`
3. Review settings:
   - Trusted entities: lambda.amazonaws.com
   - Permissions: ComprehendReadOnly
4. Click **"Create role"**

#### 1.6 Verify Role

1. Search for your role: `Lambda-Comprehend-Role`
2. Click on the role name
3. Verify:
   - **Permissions tab**: Shows ComprehendReadOnly
   - **Trust relationships tab**: Shows lambda.amazonaws.com

**✅ Checkpoint**: 
- ✓ IAM role created with Comprehend permissions
- ✓ Trust relationship configured for Lambda

---

### Step 2: Create Lambda Function

#### 2.1 Navigate to Lambda Service

1. In AWS Console search bar, type **"Lambda"**
2. Click on **"Lambda"** under Services

#### 2.2 Create Function

1. Click **"Create function"** button
2. Select **"Author from scratch"**

#### 2.3 Configure Basic Settings

1. **Function name**: `Sentiment-Analyzer`

2. **Runtime**: Select **"Python 3.12"** (or latest Python 3.x)

3. **Architecture**: x86_64 (default)

4. Expand **"Change default execution role"**

5. Select **"Use an existing role"**

6. **Existing role**: Select `Lambda-Comprehend-Role`

7. Click **"Create function"**

#### 2.4 Function Created

Wait for: "Successfully created the function Sentiment-Analyzer"

**✅ Checkpoint**:
- ✓ Lambda function created: Sentiment-Analyzer
- ✓ Python 3.12 runtime
- ✓ IAM role with Comprehend access attached

---

### Step 3: Add Lambda Function Code

#### 3.1 Access Code Editor

1. You should be on the Lambda function page
2. Scroll down to **"Code source"** section
3. You'll see `lambda_function.py` with default code

#### 3.2 Copy the Code

**Copy this entire code:**

```python
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
```

#### 3.3 Paste the Code

1. Select all default code in the editor (Ctrl+A or Cmd+A)
2. Delete it
3. Paste the code above (Ctrl+V or Cmd+V)
4. Verify the code looks correct

#### 3.4 Deploy the Code

1. Click **"Deploy"** button (orange button above editor)
2. Wait for "Changes deployed" success message

**✅ Checkpoint**:
- ✓ Lambda code deployed
- ✓ Ready for testing

---

### Step 4: Test with Positive Sentiment

#### 4.1 Create Test Event - Positive Review

1. Click **"Test"** tab (next to Code tab)
2. Click **"Create new event"**
3. Configure:
   - **Event name**: `PositiveReview`
   - **Event sharing settings**: Private
   - **Template**: hello-world
4. **Replace the JSON** with:

```json
{
  "text": "This product is amazing! I absolutely love it. Best purchase ever! Highly recommended!"
}
```

5. Click **"Save"**

#### 4.2 Execute Test

1. Make sure **"PositiveReview"** is selected
2. Click **"Test"** button (orange)
3. Wait for execution to complete

#### 4.3 Review Results

**Expected Response:**
```json
{
  "statusCode": 200,
  "body": "{\"message\": \"Sentiment analysis completed successfully\", \"text\": \"This product is amazing! I absolutely love it. Best purchase ever! Highly recommended!\", \"sentiment\": \"POSITIVE\", \"confidence_scores\": {\"Positive\": 0.9987, \"Negative\": 0.0002, \"Neutral\": 0.0008, \"Mixed\": 0.0003}, \"interpretation\": \"This text expresses positive sentiment with 99.9% confidence. The content indicates satisfaction, happiness, or approval.\"}"
}
```

**Expected Logs:**
```
START RequestId: xxxxx
Analyzing sentiment for text: "This product is amazing! I absolutely love it. Best purchase ever! Highly recommended!"
Sentiment detected: POSITIVE
Confidence scores:
  Positive: 99.87%
  Negative: 0.02%
  Neutral: 0.08%
  Mixed: 0.03%
END RequestId: xxxxx
```

---

### Step 5: Test with Negative Sentiment

#### 5.1 Create Test Event - Negative Review

1. Click **"Test"** tab
2. Click dropdown next to test event name
3. Click **"Create new event"**
4. Configure:
   - **Event name**: `NegativeReview`
5. **Event JSON**:

```json
{
  "text": "Terrible product! Complete waste of money. Very disappointed and frustrated. Would not recommend to anyone."
}
```

6. Click **"Save"**

#### 5.2 Execute Test

1. Select **"NegativeReview"** from dropdown
2. Click **"Test"** button
3. Review results

**Expected Response:**
- **sentiment**: "NEGATIVE"
- **Positive**: ~0.0001 (0.01%)
- **Negative**: ~0.9985 (99.85%)

---

### Step 6: Test with Neutral Sentiment

#### 6.1 Create Test Event - Neutral Review

1. Create new test event: `NeutralReview`
2. **Event JSON**:

```json
{
  "text": "The product arrived on time. It works as described in the specifications. Standard packaging."
}
```

3. Save and execute

**Expected Response:**
- **sentiment**: "NEUTRAL"
- **Neutral**: ~0.75-0.85 (75-85%)

---

### Step 7: Test with Mixed Sentiment

#### 7.1 Create Test Event - Mixed Review

1. Create new test event: `MixedReview`
2. **Event JSON**:

```json
{
  "text": "The product quality is excellent and works great, but the customer service was absolutely terrible and shipping took forever."
}
```

3. Save and execute

**Expected Response:**
- **sentiment**: "MIXED" or "NEGATIVE" (depends on which aspect weighs more)
- Multiple sentiment scores will be relatively high

---

### Step 8: Review CloudWatch Logs

#### 8.1 Access CloudWatch Logs

1. Click **"Monitor"** tab
2. Click **"View CloudWatch logs"**
3. Click on the latest log stream

#### 8.2 Review Detailed Logs

You should see logs for all your test executions showing:
- Input text
- Detected sentiment
- Confidence scores for all four categories

**✅ Final Checkpoint**:
- ✓ Lambda function works correctly
- ✓ Positive sentiment detected accurately
- ✓ Negative sentiment detected accurately
- ✓ Neutral sentiment detected accurately
- ✓ Mixed sentiment detected accurately
- ✓ All results logged to CloudWatch

---

## Code Explanation

### Imports

```python
import boto3
import json
```

- **boto3**: AWS SDK for Python (pre-installed in Lambda)
- **json**: For JSON serialization/deserialization

### Comprehend Client Initialization

```python
comprehend_client = boto3.client('comprehend')
```

- Creates a client to interact with Amazon Comprehend service
- Uses Lambda's IAM role for authentication

### Input Validation

```python
if 'text' not in event:
    return {
        'statusCode': 400,
        'body': json.dumps({
            'message': 'Error: No text provided in event',
            'error': 'Missing required field: text'
        })
    }
```

- Checks if 'text' field exists in event
- Returns HTTP 400 (Bad Request) if missing
- Good practice: Always validate input

### Empty Text Check

```python
if not review_text or not review_text.strip():
    return {
        'statusCode': 400,
        'body': json.dumps({
            'message': 'Error: Text cannot be empty',
            'error': 'Empty text provided'
        })
    }
```

- Validates text is not empty or whitespace only
- `.strip()` removes leading/trailing whitespace

### Sentiment Detection API Call

```python
response = comprehend_client.detect_sentiment(
    Text=review_text,
    LanguageCode='en'  # English language
)
```

**Key parameters:**
- **Text**: The input text to analyze (up to 5,000 bytes)
- **LanguageCode**: Language of the text ('en' for English)
  - Supports: en, es, fr, de, it, pt, ar, hi, ja, ko, zh, zh-TW

**Response structure:**
```python
{
    'Sentiment': 'POSITIVE',  # or NEGATIVE, NEUTRAL, MIXED
    'SentimentScore': {
        'Positive': 0.9987,
        'Negative': 0.0002,
        'Neutral': 0.0008,
        'Mixed': 0.0003
    }
}
```

### Extracting Results

```python
sentiment = response['Sentiment']
sentiment_scores = response['SentimentScore']
```

- **sentiment**: Overall sentiment classification
- **sentiment_scores**: Confidence score for each category (0 to 1)

### Logging Results

```python
print(f"Sentiment detected: {sentiment}")
print("Confidence scores:")
print(f"  Positive: {sentiment_scores['Positive'] * 100:.2f}%")
print(f"  Negative: {sentiment_scores['Negative'] * 100:.2f}%")
print(f"  Neutral: {sentiment_scores['Neutral'] * 100:.2f}%")
print(f"  Mixed: {sentiment_scores['Mixed'] * 100:.2f}%")
```

- Logs to CloudWatch for monitoring
- Multiplies by 100 to show as percentage
- `.2f` formats to 2 decimal places

### Response Structure

```python
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
```

- Returns HTTP 200 (success)
- Includes original text, sentiment, and scores
- Rounds scores to 4 decimal places
- Adds human-readable interpretation

### Helper Function: Interpretation

```python
def get_sentiment_interpretation(sentiment, scores):
    confidence = max(scores.values()) * 100
    
    interpretations = {
        'POSITIVE': f"This text expresses positive sentiment with {confidence:.1f}% confidence...",
        'NEGATIVE': f"This text expresses negative sentiment with {confidence:.1f}% confidence...",
        # etc.
    }
    
    return interpretations.get(sentiment, "Unable to interpret sentiment")
```

- Provides user-friendly explanation
- Calculates highest confidence score
- Maps sentiment to description

---

## Testing and Verification

### Test Cases Summary

| Test Case | Input | Expected Sentiment | Expected Confidence |
|-----------|-------|-------------------|---------------------|
| Positive Review | "Amazing product! Love it!" | POSITIVE | > 95% |
| Negative Review | "Terrible! Waste of money!" | NEGATIVE | > 95% |
| Neutral Review | "Product arrived on time." | NEUTRAL | > 70% |
| Mixed Review | "Good quality but bad service" | MIXED or NEGATIVE | Varies |

### Verification Checklist

- [ ] Function deploys without errors
- [ ] Positive sentiment detected correctly
- [ ] Negative sentiment detected correctly
- [ ] Neutral sentiment detected correctly
- [ ] Mixed sentiment handled appropriately
- [ ] Confidence scores make sense (sum ~ 1.0)
- [ ] CloudWatch logs show detailed results
- [ ] Status code 200 returned
- [ ] Error handling works (empty text, missing field)

---

## Troubleshooting

### Issue 1: "Access Denied" Error

**Symptoms**: Cannot call Comprehend API

**Solutions**:
1. Verify IAM role has `ComprehendReadOnly` policy
2. Check Lambda is using correct role
3. Ensure Comprehend is available in your region

### Issue 2: "Invalid Language Code"

**Symptoms**: Error about language code

**Solutions**:
1. Verify `LanguageCode='en'` in the code
2. Check text is actually in English
3. For other languages, change code (e.g., 'es' for Spanish)

### Issue 3: All Sentiments Show Low Confidence

**Symptoms**: No clear sentiment winner

**Solutions**:
1. This is normal for truly ambiguous text
2. Text might be too short
3. Text might genuinely be mixed sentiment

### Issue 4: "Text too long" Error

**Symptoms**: Error about text size

**Solutions**:
1. Comprehend limit: 5,000 bytes (UTF-8)
2. Shorten the input text
3. For longer text, split into chunks

---

## Best Practices

### Input Validation

1. **Always validate input**:
```python
if not review_text or len(review_text) > 5000:
    return error_response
```

2. **Handle edge cases**:
   - Empty strings
   - Very short text (< 10 characters)
   - Special characters
   - Non-English text

### Error Handling

1. **Specific error messages**:
```python
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'TextSizeLimitExceededException':
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Text too long (max 5000 bytes)'})
        }
```

### Production Enhancements

1. **Add batch processing**:
```python
# Process multiple reviews at once
response = comprehend_client.batch_detect_sentiment(
    TextList=[review1, review2, review3],
    LanguageCode='en'
)
```

2. **Store results in DynamoDB**:
```python
dynamodb.put_item(
    TableName='SentimentResults',
    Item={
        'review_id': review_id,
        'sentiment': sentiment,
        'timestamp': datetime.now().isoformat()
    }
)
```

3. **Add SNS notifications for negative sentiment**:
```python
if sentiment == 'NEGATIVE' and sentiment_scores['Negative'] > 0.9:
    sns_client.publish(
        TopicArn='arn:aws:sns:region:account:negative-reviews',
        Message=f'Highly negative review detected: {review_text}'
    )
```

4. **Language detection**:
```python
# Auto-detect language
lang_response = comprehend_client.detect_dominant_language(Text=review_text)
language_code = lang_response['Languages'][0]['LanguageCode']

# Use detected language
sentiment_response = comprehend_client.detect_sentiment(
    Text=review_text,
    LanguageCode=language_code
)
```

---

## Summary

### What We Built
- ✅ Automated sentiment analysis system
- ✅ Integration with Amazon Comprehend AI service
- ✅ Support for all four sentiment types
- ✅ Confidence scoring
- ✅ Human-readable interpretations
- ✅ Comprehensive logging

### Skills Learned
- Amazon Comprehend API usage
- Sentiment analysis concepts
- AI/ML service integration with Lambda
- Natural Language Processing basics
- Input validation best practices
- Error handling for AI services

### Real-World Applications
- Customer feedback analysis
- Social media monitoring
- Support ticket prioritization
- Product review analysis
- Brand reputation management

### Production Enhancements
- Batch processing for multiple reviews
- DynamoDB storage for historical data
- SNS notifications for critical sentiments
- API Gateway for external access
- Multi-language support
- Sentiment trend dashboards

---

**Congratulations!** You've completed Assignment 8. This is a practical implementation of AI-powered text analysis that can be used in real production systems!

**Next Steps:**
- Try with your own text samples
- Experiment with different languages
- Integrate with a real review system
- Build a dashboard for sentiment trends
