# Sentiment Analysis Using AWS Lambda, Boto3, and Amazon Comprehend

## 📋 Project Overview

This project demonstrates automated sentiment analysis of user reviews using AWS Lambda, Boto3, and Amazon Comprehend. The Lambda function analyzes text input and determines whether the sentiment is positive, negative, neutral, or mixed.

## 🎯 Objectives

- Automate sentiment analysis using AI/ML services
- Utilize Amazon Comprehend for natural language processing
- Process user reviews and feedback automatically
- Practice serverless AI integration
- Understand sentiment analysis use cases

## 🏗️ Architecture

```
User Review (Text Input) → Lambda Function → Amazon Comprehend API
                                ↓
                          Sentiment Analysis
                                ↓
                    Result: Positive/Negative/Neutral/Mixed
                                ↓
                          CloudWatch Logs
```

## 📦 Prerequisites

- AWS Account (Free Tier eligible)
- Basic understanding of text analysis
- Python 3.x knowledge
- No additional AWS resources needed (just Lambda + Comprehend)

## 🚀 Features

- **Real-time sentiment analysis**: Instant results for text input
- **Multiple sentiment types**: Detects positive, negative, neutral, and mixed sentiments
- **Confidence scores**: Provides confidence percentage for each sentiment
- **Serverless**: No infrastructure to manage
- **Cost-effective**: Pay only for what you use
- **Easy integration**: Can be integrated with chatbots, review systems, etc.

## 📁 Repository Structure

```
assignment8-sentiment-analysis/
├── README.md                          # This file
├── lambda_function.py                 # Lambda function code
├── documentation.md                   # Detailed step-by-step guide
└── screenshots/                       # Project screenshots
```

## 🔧 Setup Instructions

### Step 1: Create IAM Role

1. Create IAM role: `Lambda-Comprehend-Role`
2. Attach policy: `ComprehendReadOnly`
3. Trust entity: Lambda service

### Step 2: Create Lambda Function

1. Function name: `Sentiment-Analyzer`
2. Runtime: Python 3.12
3. Execution role: `Lambda-Comprehend-Role`
4. Deploy the code from `lambda_function.py`

### Step 3: Test with Sample Reviews

1. Create test events with different sentiments
2. Execute the function
3. Review sentiment analysis results in response and logs

## 💻 Lambda Function Code

The Lambda function performs the following operations:

1. Extracts text from the event
2. Calls Amazon Comprehend's `detect_sentiment` API
3. Receives sentiment analysis results
4. Logs detailed findings
5. Returns sentiment and confidence scores

See `lambda_function.py` for complete implementation.

## 📊 Expected Results

### Positive Review Example
**Input:** "This product is amazing! I absolutely love it. Best purchase ever!"
**Output:**
```json
{
  "statusCode": 200,
  "body": {
    "message": "Sentiment analysis completed",
    "text": "This product is amazing! I absolutely love it. Best purchase ever!",
    "sentiment": "POSITIVE",
    "confidence_scores": {
      "Positive": 0.9987,
      "Negative": 0.0002,
      "Neutral": 0.0008,
      "Mixed": 0.0003
    }
  }
}
```

### Negative Review Example
**Input:** "Terrible product. Waste of money. Very disappointed."
**Output:**
```json
{
  "statusCode": 200,
  "body": {
    "sentiment": "NEGATIVE",
    "confidence_scores": {
      "Positive": 0.0001,
      "Negative": 0.9985,
      "Neutral": 0.0010,
      "Mixed": 0.0004
    }
  }
}
```

### Neutral Review Example
**Input:** "The product arrived on time. It works as described."
**Output:**
```json
{
  "statusCode": 200,
  "body": {
    "sentiment": "NEUTRAL",
    "confidence_scores": {
      "Positive": 0.2156,
      "Negative": 0.0234,
      "Neutral": 0.7543,
      "Mixed": 0.0067
    }
  }
}
```

## 📸 Screenshots

All screenshots documenting the implementation process are available in the `screenshots/` directory.

## 🔍 Testing

### Test Events

**Positive Sentiment:**
```json
{
  "text": "This product is amazing! I absolutely love it. Best purchase ever!"
}
```

**Negative Sentiment:**
```json
{
  "text": "Terrible product. Waste of money. Very disappointed."
}
```

**Neutral Sentiment:**
```json
{
  "text": "The product arrived on time. It works as described."
}
```

**Mixed Sentiment:**
```json
{
  "text": "The product quality is good but the customer service was terrible."
}
```

## 📝 CloudWatch Logs Sample

```
START RequestId: xxxxx
Analyzing sentiment for text: "This product is amazing! I absolutely love it. Best purchase ever!"
Sentiment detected: POSITIVE
Confidence scores:
  Positive: 99.87%
  Negative: 0.02%
  Neutral: 0.08%
  Mixed: 0.03%
END RequestId: xxxxx
```

## 🔐 Security Considerations

### Current Implementation
- Uses `ComprehendReadOnly` policy for read-only access

### Production Recommendations
- Use least privilege IAM policies
- Restrict to specific Comprehend operations
- Add input validation for text length
- Implement rate limiting
- Add encryption for sensitive data

### Recommended IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "comprehend:DetectSentiment"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🎓 Learning Outcomes

- Amazon Comprehend API usage
- Natural Language Processing (NLP) basics
- Sentiment analysis concepts
- Serverless AI/ML integration
- Real-time text analysis
- Confidence score interpretation

## 💡 Use Cases

- **Customer feedback analysis**: Analyze product reviews
- **Social media monitoring**: Track brand sentiment
- **Support ticket routing**: Prioritize negative feedback
- **Survey analysis**: Process open-ended responses
- **Content moderation**: Flag negative content
- **Market research**: Analyze customer opinions

## 🔄 Future Enhancements

- [ ] Add batch processing for multiple reviews
- [ ] Store results in DynamoDB
- [ ] Create dashboard for sentiment trends
- [ ] Add SNS notifications for negative sentiment
- [ ] Integrate with review platforms (Amazon, Yelp)
- [ ] Add language detection
- [ ] Implement sentiment tracking over time
- [ ] Create API Gateway endpoint for external access

## 🧹 Cleanup

To avoid unnecessary AWS charges:

```bash
# Delete Lambda function
# Delete IAM role
# Remove CloudWatch log groups
```

**Note:** Amazon Comprehend charges per request. Free tier includes 50,000 units per month for the first 12 months.

## 📚 References

- [Amazon Comprehend Documentation](https://docs.aws.amazon.com/comprehend/)
- [Boto3 Comprehend Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html)
- [Sentiment Analysis Overview](https://docs.aws.amazon.com/comprehend/latest/dg/how-sentiment.html)

## 💰 Pricing

**Amazon Comprehend Pricing:**
- Sentiment Analysis: $0.0001 per unit (100 characters = 1 unit)
- Free Tier: 50,000 units per month for 12 months
- Example: 1,000 reviews (avg 500 chars) = 5,000 units = $0.50

**AWS Lambda Pricing:**
- Free Tier: 1M requests per month
- This assignment: ~10 test requests = FREE

## 👤 Author

**Your Name**
- GitHub: [@PriyankP2](https://github.com/PriyankP2)

## 📄 License

This project is created for educational purposes as part of AWS Lambda automation assignment.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

---

**Note**: This is the simple project - perfect for understanding AI/ML service integration with Lambda!
