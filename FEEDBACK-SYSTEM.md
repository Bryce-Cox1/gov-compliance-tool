# Feedback System

## Overview

The feedback system collects user feedback through a modal form accessible from the MVP banner at the top of the page.

## User Experience

1. **Banner**: Fixed at top of page: "This is an MVP, help us make it better by sharing your feedback"
2. **Form**: Click "sharing your feedback" to open modal with:
   - Text area for feedback
   - File upload for screenshots
   - Submit button

## Data Storage

All feedback is stored in the `feedback/` directory:

```
gov-compliance-tool/
  feedback/
    feedback.json           # Main feedback database
    screenshot_*.png        # Optional screenshots from users
```

### Feedback JSON Structure

```json
[
  {
    "timestamp": "2026-02-25T09:15:30.123456",
    "feedback": "User feedback text here...",
    "screenshot": "screenshot_20260225_091530.png"
  }
]
```

## Accessing Feedback

### Manual Review

```bash
cd gov-compliance-tool/feedback
cat feedback.json | jq .
```

### Agent Analysis

Create a cron job or manual task for Rook to:

1. Read `feedback/feedback.json`
2. Analyze feedback for:
   - Common themes
   - Bug reports
   - Feature requests
   - Usability issues
3. Generate recommendations
4. Prioritize improvements

### Example Agent Task

```
Hey Rook, analyze the feedback in gov-compliance-tool/feedback/feedback.json 
and give me:
- Top 3 themes
- Critical bugs (if any)
- Quick wins we should prioritize
- Long-term feature requests
```

## Integration Points

- **File**: `app.py` - `/api/feedback` endpoint
- **Template**: `templates/index.html` - Banner + modal + form
- **Styles**: `static/style.css` - Banner + modal styling
- **Storage**: `feedback/` directory (auto-created)

## Security Notes

- Screenshots are stored with timestamped filenames
- No user identification collected (anonymous feedback)
- Files stored locally in project directory
- Both human and AI can access via filesystem

## Future Enhancements

- Email notifications for new feedback
- Webhook integration (Slack, Discord)
- Sentiment analysis
- Auto-categorization
- Feedback dashboard/viewer
