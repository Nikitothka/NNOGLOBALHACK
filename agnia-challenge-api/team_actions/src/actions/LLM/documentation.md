# API Calls Documentation

## `request_llm_generation`

**Description**:
Sends a user message indicating a generation request to the LLM endpoint and returns the generated response.

**Parameters**:

- **user_message** (`UserMessage`):  
  A string message from the user, describing what needs to be generated by the LLM. This message will be sent directly to the LLM API.

**Returns**:

- **LLMResponse** (`LLMResponse`):  
  A response object containing the generated message from the LLM.

**Usage Example**

When a user provides a message like:

- "Generate a summary for the following article..." or "Suggest some creative ideas for marketing a new app."

The function should parse this to:

- **user_message**: The exact message from the user, e.g., "Generate a summary for the following article..."

## `request_daily_summary`

**Description**:
Generates a daily summary of messages from a conversation based on optional parameters like date, group name, and topic. Useful for reviewing important messages or discussions from specific groups.

**Parameters**:

- **date** (`Optional[DateParam]`):  
  The date for which the summary should be generated. If not provided, defaults to the current date.

- **group_name** (`Optional[GroupName]`):  
  The name of the group for which the summary should be generated. Useful if conversations are organized by group names.

- **topic** (`Optional[TopicName]`):  
  The specific subgroup or topic within the group for which the summary is generated.

**Returns**:

- **LLMResponse** (`LLMResponse`):  
  A response object containing the generated summary of messages.

**Usage Example**

When a user provides a message like:

- "Summarize today's conversation in the 'Product Development' group for the topic 'Feature Updates'."
  
The function should parse this to:

- **date**: `None` (defaults to today)
- **group_name**: `"Product Development"`
- **topic**: `"Feature Updates"`