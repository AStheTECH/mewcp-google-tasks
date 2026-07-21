**Create, track, and manage Google Tasks and task lists — directly from your AI workflows.**

A Model Context Protocol (MCP) server that exposes Google Tasks' API for creating, listing, updating, completing, and deleting tasks and task lists.


## Overview

The Google Tasks MCP Server provides full programmatic access to Google Tasks through a stateless, multi-tenant interface:

- List, create, update, and delete task lists
- List, create, look up, update, complete, and delete individual tasks
- Every mutating tool that overwrites state (`update_task`, `update_tasklist`) returns both the before and after state of the resource

Perfect for:

- Automating to-do list management and task tracking from AI agents
- Building assistants that can create and complete tasks on a user's behalf
- Integrating Google Tasks actions into LLM-powered pipelines and reminders


## Tools

<details>
<summary><code>list_task_lists</code> — List all task lists</summary>

List all task lists accessible by the user. Returns task list IDs, titles, and metadata. Use the task list ID from the response to access tasks within a list.

**Inputs:**
```
(none)
```

**Output `data` schema:**

```typescript
{
  count: number;
  tasklists: {
    id: string;
    title: string | null;
    updated: string | null;
    etag: string | null;
    kind: string | null;
    selfLink: string | null;
  }[];
  next_page_token: string | null;
}
```

</details>


<details>
<summary><code>add_task</code> — Create a new task</summary>

Create a new task in a specific task list. Provide the task list ID, title, and optional notes and due date. Returns the created task with its assigned ID.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `title` (string, required) — The title of the new task.
- `notes` (string, optional, default: "") — Optional details or description for the task.
- `due` (string, optional, default: "") — Optional due date. MUST be an RFC 3339 timestamp (e.g., '2026-06-17T00:00:00.000Z').
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  notes: string | null;
  due: string | null;
  status: string | null;
  position: string | null;
  parent: string | null;
  links: { [key: string]: any }[] | null;
  webViewLink: string | null;
  hidden: boolean | null;
  completed: string | null;
  deleted: boolean | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>get_task</code> — Get a task's details</summary>

Gets the detail of a specific task from the task list. Returns the full task object including title, notes, due date, status, and position.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `task_id` (string, required) — The unique ID of the Google Task
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  notes: string | null;
  due: string | null;
  status: string | null;
  position: string | null;
  parent: string | null;
  links: { [key: string]: any }[] | null;
  webViewLink: string | null;
  hidden: boolean | null;
  completed: string | null;
  deleted: boolean | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>get_task_by_name</code> — Find a task by title</summary>

Get the task details from the name of the task. Searches a task list for a task by its title and returns the matching task details.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `task_title` (string, required) — The title of the task to search for.
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  notes: string | null;
  due: string | null;
  status: string | null;
  position: string | null;
  parent: string | null;
  links: { [key: string]: any }[] | null;
  webViewLink: string | null;
  hidden: boolean | null;
  completed: string | null;
  deleted: boolean | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>delete_task</code> — Permanently delete a task (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a specific task from the task list. This action is irreversible — the deleted task and all its data cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `task_id` (string, required) — The unique ID of the Google Task
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  notes: string | null;
  due: string | null;
  status: string | null;
  position: string | null;
  parent: string | null;
  links: { [key: string]: any }[] | null;
  webViewLink: string | null;
  hidden: boolean | null;
  completed: string | null;
  deleted: boolean | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>complete_task</code> — Mark a task as completed</summary>

Mark a specific task as completed from the task list. Sets the task status to 'completed'. Returns the updated task object.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `task_id` (string, required) — The unique ID of the Google Task
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  notes: string | null;
  due: string | null;
  status: string | null;
  position: string | null;
  parent: string | null;
  links: { [key: string]: any }[] | null;
  webViewLink: string | null;
  hidden: boolean | null;
  completed: string | null;
  deleted: boolean | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>update_task</code> — Update an existing task</summary>

Updates an existing task. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `task_id` (string, required) — The unique ID of the Google Task
- `task_title` (string, required) — The title of the task.
- `notes` (string, optional, default: "") — Optional details or description for the task.
- `due` (string, optional, default: "") — Optional due date. MUST be an RFC 3339 timestamp (e.g., '2026-06-17T00:00:00.000Z').
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string;
    title: string | null;
    notes: string | null;
    due: string | null;
    status: string | null;
    position: string | null;
    parent: string | null;
    links: { [key: string]: any }[] | null;
    webViewLink: string | null;
    hidden: boolean | null;
    completed: string | null;
    deleted: boolean | null;
    etag: string | null;
    kind: string | null;
    selfLink: string | null;
  };
  after: {
    id: string;
    title: string | null;
    notes: string | null;
    due: string | null;
    status: string | null;
    position: string | null;
    parent: string | null;
    links: { [key: string]: any }[] | null;
    webViewLink: string | null;
    hidden: boolean | null;
    completed: string | null;
    deleted: boolean | null;
    etag: string | null;
    kind: string | null;
    selfLink: string | null;
  };
}
```

</details>


<details>
<summary><code>create_tasklist</code> — Create a new task list</summary>

Create a brand new task list. Returns the created task list with its assigned ID and metadata.

**Inputs:**
```
- `tasklist_name` (string, required) — The name of the Google Tasks list.
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  updated: string | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>update_tasklist</code> — Rename an existing task list</summary>

Updates the name of a specific task list. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
- `title` (string, required) — The title or name of the Google Tasks list
```

**Output `data` schema:**

```typescript
{
  before: {
    id: string;
    title: string | null;
    updated: string | null;
    etag: string | null;
    kind: string | null;
    selfLink: string | null;
  };
  after: {
    id: string;
    title: string | null;
    updated: string | null;
    etag: string | null;
    kind: string | null;
    selfLink: string | null;
  };
}
```

</details>


<details>
<summary><code>list_tasks</code> — List all tasks in a task list</summary>

List all the tasks present in the specific task list. Returns task IDs, titles, statuses, and other metadata for all tasks in the list.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
```

**Output `data` schema:**

```typescript
{
  count: number;
  tasks: {
    id: string;
    title: string | null;
    notes: string | null;
    due: string | null;
    status: string | null;
    position: string | null;
    parent: string | null;
    links: { [key: string]: any }[] | null;
    webViewLink: string | null;
    hidden: boolean | null;
    completed: string | null;
    deleted: boolean | null;
    etag: string | null;
    kind: string | null;
    selfLink: string | null;
  }[];
  next_page_token: string | null;
}
```

</details>


<details>
<summary><code>get_tasklist</code> — Get a task list's details</summary>

Get the details or metadata of a specific task list. Returns the task list ID, title, and last updated timestamp.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  updated: string | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


<details>
<summary><code>delete_tasklist</code> — Permanently delete a task list (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes an entire task list with all tasks in it. This action is irreversible — the task list and all its tasks cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `tasklist_id` (string, required) — The unique ID of the Google Tasks list.
```

**Output `data` schema:**

```typescript
{
  id: string;
  title: string | null;
  updated: string | null;
  etag: string | null;
  kind: string | null;
  selfLink: string | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 404,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "NOT_FOUND", "message": "No task found with the title {task_title}", "details": null },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for auth, not-found, and other non-transient errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `NOT_FOUND` (`get_task_by_name` found no match), `AUTH_ERROR` (no OAuth access token available), `UPSTREAM_ERROR` (the Google Tasks API returned an HTTP error), `SERVER_ERROR` (unexpected server-side failure).

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `tasklist_id` — The unique ID of a Google Tasks list. Obtain it from `list_task_lists`, `create_tasklist`, or any task list response's `id` field. Required by every task-level and task-list-level tool.
- `task_id` — The unique ID of a Google Task within a task list. Obtain it from `list_tasks`, `add_task`, or any task response's `id` field.
- `next_page_token` — Returned by `list_task_lists` and `list_tasks` when the underlying Google Tasks API indicates more results exist. This server currently passes through a single page from the upstream API and does not expose an input parameter to request subsequent pages.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Task List ID (`tasklist_id`):**

```
Opaque identifier assigned by the Google Tasks API, or the literal value `@default` for the user's default task list.
Example: MDAxMjM0NTY3ODkwMTIzNDU2Nzo6MA
```

**Task ID (`task_id`):**

```
Opaque identifier assigned by the Google Tasks API when a task is created.
Example: MTIzNDU2Nzg5MDEyMzQ1Njc4OTA
```

**Due Date (`due`):**

```
RFC 3339 timestamp.
Example: 2026-06-17T00:00:00.000Z
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Google Tasks credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Google Tasks API Error</strong></summary>

- **Cause:** Upstream Google Tasks API returned an error
- **Solution:**
  1. Check Google service status at [Google Workspace Status Page](https://www.google.com/appsstatus)
  2. Verify your credential has the required Google Tasks permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Google Tasks API Documentation](https://developers.google.com/tasks)** — Official API reference
- **[Google Tasks API Reference](https://developers.google.com/tasks/reference/rest)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
