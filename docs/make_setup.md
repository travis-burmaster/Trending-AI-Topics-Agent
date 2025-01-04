# Make.com Configuration Guide

## Prerequisites
- A Make.com account (sign up at make.com)
- API access tokens for:
  - LinkedIn API (Developer Portal)
  - GitHub API (Personal Access Token)
  - Google Custom Search API

## 1. LinkedIn Scenario Setup

1. Create New Scenario
   - Click "Create a new scenario"
   - Search for "LinkedIn" in the module picker

2. Configure LinkedIn Module
   - Add "Watch LinkedIn Posts" module
   - Click to configure the module
   - Authenticate with your LinkedIn account
   - Set up filters:
     - Keywords: "artificial intelligence project"
     - Post types: All
     - Time range: Past week
     - Max results: 10

3. Add Data Processing
   - Add a "Tools > Set Variable" module
   - Map the following fields:
     ```json
     {
       "title": "{{1.post.title}}",
       "url": "{{1.post.url}}",
       "engagement": {
         "likes": "{{1.post.likeCount}}",
         "comments": "{{1.post.commentCount}}",
         "shares": "{{1.post.shareCount}}"
       },
       "timestamp": "{{1.post.created}}"
     }
     ```

4. Add Webhook Output
   - Add "HTTP > Make a request" module
   - Configure as POST request
   - Response will be sent to your application

## 2. GitHub Scenario Setup

1. Create New Scenario
   - Click "Create a new scenario"
   - Search for "GitHub" in the module picker

2. Configure GitHub Module
   - Add "Watch Repositories" module
   - Connect your GitHub account
   - Configure filters:
     - Topic: "artificial-intelligence"
     - Language: All
     - Sort: Stars
     - Time range: Past week

3. Add Data Processing
   - Add a "Tools > Set Variable" module
   - Map the following fields:
     ```json
     {
       "repo_name": "{{1.repository.full_name}}",
       "description": "{{1.repository.description}}",
       "url": "{{1.repository.html_url}}",
       "metrics": {
         "stars": "{{1.repository.stargazers_count}}",
         "forks": "{{1.repository.forks_count}}",
         "issues": "{{1.repository.open_issues_count}}"
       },
       "last_updated": "{{1.repository.updated_at}}"
     }
     ```

4. Add Webhook Output
   - Add "HTTP > Make a request" module
   - Configure as POST request
   - Response will be sent to your application

## 3. Google Search Scenario Setup

1. Create New Scenario
   - Click "Create a new scenario"
   - Search for "Google" in the module picker

2. Configure Google Search Module
   - Add "Google Custom Search API" module
   - Connect your Google API account
   - Configure search parameters:
     - Query: "new artificial intelligence projects"
     - Time range: Past week
     - Result count: 10

3. Add Data Processing
   - Add a "Tools > Set Variable" module
   - Map the following fields:
     ```json
     {
       "title": "{{1.title}}",
       "snippet": "{{1.snippet}}",
       "url": "{{1.link}}",
       "source": "{{1.displayLink}}",
       "published": "{{1.pagemap.metatags[0]['article:published_time']}}"
     }
     ```

4. Add Webhook Output
   - Add "HTTP > Make a request" module
   - Configure as POST request
   - Response will be sent to your application

## 4. Testing and Deployment

1. Test Each Scenario
   - Click "Run Once" to test
   - Check webhook responses
   - Verify data format matches expected schema

2. Configure Scheduling
   - Set each scenario to run weekly
   - Stagger execution times to avoid rate limits
   - Enable error notifications

## Security Considerations

1. API Credentials
   - Store API keys securely in Make.com
   - Use environment variables for sensitive data
   - Rotate credentials regularly

2. Webhook Security
   - Use HTTPS endpoints only
   - Implement authentication for webhooks
   - Set up IP restrictions if possible

## Troubleshooting

1. Common Issues
   - Rate limiting: Adjust scenario scheduling
   - Data format mismatches: Check mapping
   - Authentication errors: Verify credentials

2. Monitoring
   - Enable execution history
   - Set up error notifications
   - Monitor API usage
