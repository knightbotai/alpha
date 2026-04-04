---
name: direct-text-response
description: Handle simple conversational tasks with direct text responses, avoiding unnecessary tool invocations for efficiency.
---

# Direct Text Response Pattern

## Overview

This skill guides agents to handle simple, conversational tasks using direct text responses. When a task requires only basic interaction (like greetings, acknowledgments, or simple queries), invoking tools may be unnecessary overhead.

## When to Apply

Use this approach when:
- The task is conversational in nature (greetings, acknowledgments, simple Q&A)
- No file operations, code execution, or complex data processing is required
- The response can be delivered in a single message
- Tool invocation would add unnecessary complexity and latency

## Step-by-Step Instructions

1. **Analyze the task requirement**
   - Determine if the task can be completed with text alone
   - Check if no file, shell, or API operations are needed

2. **Craft a concise text response**
   - Keep the response focused and direct
   - Avoid over-complicating with tool calls when not needed

3. **Mark task completion**
   - Clearly indicate the task is complete after the text response
   - No follow-up tool execution required

## Example Scenarios

**Scenario 1: Simple Greeting**
```
User: "Please send a hello message."
Agent Response: "Hello! How can I assist you today?"
Status: Task complete (no tools invoked)
```

**Scenario 2: Acknowledgment**
```
User: "Confirm receipt of the document."
Agent Response: "Document received and acknowledged."
Status: Task complete (no tools invoked)
```

**Scenario 3: Simple Query**
```
User: "What is the current status?"
Agent Response: "The system is operational and ready for your requests."
Status: Task complete (no tools invoked)
```

## Best Practices

- **Keep it simple**: For conversational tasks, direct text is more efficient than tool orchestration
- **Avoid over-engineering**: Don't invoke tools for tasks that can be handled conversationally
- **Clear completion signal**: Always explicitly mark the task as complete after the text response

## When NOT to Use

Avoid this pattern when:
- File creation or modification is required
- Shell script execution is needed
- Data processing or API calls are necessary
- The task involves multiple steps requiring tool coordination

## Key Takeaway

For simple conversational tasks, a direct text response is often the most efficient approach, eliminating the overhead of tool invocation while maintaining clarity and responsiveness.