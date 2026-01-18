# Possible GitHub Copilot Settings

## GitHub.copilot-chat

https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat

Settings
ID Description Default
github.copilot.chat.agent.autoFix

Automatically fix diagnostics for edited files.

true
github.copilot.chat.agent.currentEditorContext.enabled

When enabled, Copilot will include the name of the current active editor in the context for agent mode.

true
github.copilot.chat.agent.temperature

Temperature setting for agent mode requests.

0
github.copilot.chat.agentHistorySummarizationForceGpt41

Force GPT-4.1 for agent history summarization.

false
github.copilot.chat.agentHistorySummarizationMode

Mode for agent history summarization.

""
github.copilot.chat.agentHistorySummarizationWithPromptCache

Use prompt caching for agent history summarization.

false
github.copilot.chat.alternateGeminiModelFPrompt.enabled

Enables an experimental alternate prompt for Gemini Model F instead of the default prompt.

false
github.copilot.chat.alternateGptPrompt.enabled

Enables an experimental alternate prompt for GPT models instead of the default prompt.

false
github.copilot.chat.anthropic.thinking.budgetTokens

Maximum number of tokens to allocate for extended thinking in Anthropic models. Setting this value enables extended thinking. Valid range is 1,024 to 32,000 tokens. Always capped at (max output tokens - 1).

Note: This is an experimental feature not yet activated for all users.

4000
github.copilot.chat.anthropic.tools.websearch.allowedDomains

List of domains to restrict web search results to (e.g., ["example.com", "docs.example.com"]). Domains should not include the HTTP/HTTPS scheme. Subdomains are automatically included. Cannot be used together with blocked domains.

[]
github.copilot.chat.anthropic.tools.websearch.blockedDomains

List of domains to exclude from web search results (e.g., ["untrustedsource.com"]). Domains should not include the HTTP/HTTPS scheme. Subdomains are automatically excluded. Cannot be used together with allowed domains.

[]
github.copilot.chat.anthropic.tools.websearch.enabled

Enable Anthropic's native web search tool for BYOK Claude models. When enabled, allows Claude to search the web for current information.

Note: This is an experimental feature only available for BYOK Anthropic Claude models.

false
github.copilot.chat.anthropic.tools.websearch.maxUses

Maximum number of web searches allowed per request. Valid range is 1 to 20. Prevents excessive API calls within a single interaction. If Claude exceeds this limit, the response returns an error.

5
github.copilot.chat.anthropic.tools.websearch.userLocation

User location for personalizing web search results based on geographic context. All fields (city, region, country, timezone) are optional. Example: {"city": "San Francisco", "region": "California", "country": "US", "timezone": "America/Los_Angeles"}

null
github.copilot.chat.anthropic.useMessagesApi

Use the Messages API instead of the Chat Completions API when supported.

Note: This is an experimental feature that is not yet activated for all users.

false
github.copilot.chat.azureAuthType

Authentication method for Azure OpenAI models. Entra ID is recommended for enterprise security and uses your Azure credentials.

"entraId"
github.copilot.chat.azureModels

Configure custom Azure OpenAI models. Each key should be a unique model ID, and the value should be an object with model configuration including name, url, toolCalling, vision, maxInputTokens, and maxOutputTokens properties.

{}
github.copilot.chat.backgroundAgent.enabled

Enable the Background Agent. When disabled, the Background Agent will not be available in 'Continue In' context menus.

true
github.copilot.chat.byok.ollamaEndpoint

The endpoint to use for the Ollama when accessed via bring your own key. Defaults to localhost.

"http://localhost:11434"
github.copilot.chat.claudeCode.debug

Enable debug mode for Claude Code agent.

false
github.copilot.chat.claudeCode.enabled

Enable Claude Code agent.

false
github.copilot.chat.cli.autoCommit.enabled

Enable automatic commit for Background Agents.

false
github.copilot.chat.cli.customAgents.enabled

Enable Custom Agents for Background Agents.

false
github.copilot.chat.cli.mcp.enabled

Enable Model Context Protocol (MCP) server for Background Agents.

false
github.copilot.chat.cloudAgent.enabled

Enable the Cloud Agent. When disabled, the Cloud Agent will not be available in 'Continue In' context menus.

true
github.copilot.chat.codeGeneration.instructions

A set of instructions that will be added to Copilot requests that generate code. Instructions can come from:

a file in the workspace: { "file": "fileName" }
text in natural language: { "text": "Use underscore for field names." }
Note: Keep your instructions short and precise. Poor instructions can degrade Copilot's quality and performance.

[]
github.copilot.chat.codeGeneration.useInstructionFiles

Controls whether code instructions from .github/copilot-instructions.md are added to Copilot requests.

Note: Keep your instructions short and precise. Poor instructions can degrade Copilot's quality and performance. Learn more about customizing Copilot.

true
github.copilot.chat.codesearch.agent.enabled

Enable code search capabilities in agent mode.

true
github.copilot.chat.codesearch.enabled

Whether to enable agentic codesearch when using #codebase.

false
github.copilot.chat.commitMessageGeneration.instructions

A set of instructions that will be added to Copilot requests that generate commit messages. Instructions can come from:

a file in the workspace: { "file": "fileName" }
text in natural language: { "text": "Use conventional commit message format." }
Note: Keep your instructions short and precise. Poor instructions can degrade Copilot's quality and performance.

[]
github.copilot.chat.completionsFetcher

Sets the fetcher used for the inline completions.

""
github.copilot.chat.copilotDebugCommand.enabled

Whether the `copilot-debug` command is enabled in the terminal.

true
github.copilot.chat.customAgents.showOrganizationAndEnterpriseAgents

Enable custom agents from GitHub Enterprise and Organizations. When disabled, custom agents from your organization or enterprise will not be available in Copilot.

false
github.copilot.chat.customInstructionsInSystemMessage

When enabled, custom instructions and mode instructions will be appended to the system message instead of a user message.

true
github.copilot.chat.customOAIModels

Configure custom OpenAI-compatible models. Each key should be a unique model ID, and the value should be an object with model configuration including name, url, toolCalling, vision, maxInputTokens, and maxOutputTokens properties.

{}
github.copilot.chat.debug.overrideChatEngine

Override the chat model. This allows you to test with different models.

Note: This is an advanced debugging setting and should not be used while self-hosting as it may lead to a different experience compared to end-users.

""
github.copilot.chat.debug.requestLogger.maxEntries

Maximum number of entries to keep in the request logger for debugging purposes.

100
github.copilot.chat.debugTerminalCommandPatterns

A list of commands for which the "Debug Command" quick fix action should be shown in the debug terminal.

[]
github.copilot.chat.editRecording.enabled

Enable edit recording for analysis.

false
github.copilot.chat.edits.gemini3MultiReplaceString

Enable the modern multi_replace_string_in_file edit tool when generating edits with Gemini 3 models.

false
github.copilot.chat.edits.suggestRelatedFilesForTests

Whether to suggest source files from test files for the Copilot Edits working set.

true
github.copilot.chat.edits.suggestRelatedFilesFromGitHistory

Whether to suggest related files from git history for the Copilot Edits working set.

true
github.copilot.chat.enableUserPreferences

Enable remembering user preferences in agent mode.

false
github.copilot.chat.feedback.onChange

Enable feedback collection on configuration changes.

false
github.copilot.chat.generateTests.codeLens

Show 'Generate tests' code lens for symbols that are not covered by current test coverage information.

false
github.copilot.chat.githubMcpServer.enabled

Enable built-in support for the GitHub MCP Server.

false
github.copilot.chat.githubMcpServer.lockdown

Enable lockdown mode for the GitHub MCP Server. When enabled, hides public issue details created by users without push access. Learn more.

false
github.copilot.chat.githubMcpServer.readonly

Enable read-only mode for the GitHub MCP Server. When enabled, only read tools are available. Learn more.

false
github.copilot.chat.githubMcpServer.toolsets

Specify toolsets to use from the GitHub MCP Server. Learn more.

[
"default"
]
github.copilot.chat.gpt5AlternativePatch

Enable GPT-5 alternative patch format.

false
github.copilot.chat.imageUpload.enabled

Enables the use of image upload URLs in chat requests instead of raw base64 strings.

true
github.copilot.chat.inlineChat.selectionRatioThreshold

Threshold at which to switch editing strategies for inline chat. When a selection porition of code matches a parse tree node, only that is presented to the language model. This speeds up response times but might have lower quality results. Requires having a parse tree for the document and the inlineChat.enableV2 setting. Values must be between 0 and 1, where 0 means off and 1 means the selection perfectly matches a parse tree node.

0
github.copilot.chat.inlineEdits.diagnosticsContextProvider.enabled

Enable diagnostics context provider for next edit suggestions.

false
github.copilot.chat.inlineEdits.nextCursorPrediction.currentFileMaxTokens

Maximum tokens for current file in next cursor prediction.

2000
github.copilot.chat.inlineEdits.nextCursorPrediction.displayLine

Display predicted cursor line for next edit suggestions.

true
github.copilot.chat.inlineEdits.renameSymbolSuggestions

Enable rename symbol suggestions in inline edits.

true
github.copilot.chat.inlineEdits.triggerOnEditorChangeAfterSeconds

Trigger inline edits after editor has been idle for this many seconds.

0
github.copilot.chat.instantApply.shortContextLimit

Token limit for short context instant apply.

8000
github.copilot.chat.instantApply.shortContextModelName

Model name for short context instant apply.

"gpt-4o-instant-apply-full-ft-v66-short"
github.copilot.chat.languageContext.fix.typescript.enabled

Enables the TypeScript language context provider for /fix commands

false
github.copilot.chat.languageContext.inline.typescript.enabled

Enables the TypeScript language context provider for inline chats (both generate and edit)

false
github.copilot.chat.languageContext.typescript.cacheTimeout

The cache population timeout for the TypeScript language context provider in milliseconds. The default is 500 milliseconds.

500
github.copilot.chat.languageContext.typescript.enabled

Enables the TypeScript language context provider for inline suggestions

false
github.copilot.chat.languageContext.typescript.includeDocumentation

Controls whether to include documentation comments in the generated code snippets.

false
github.copilot.chat.languageContext.typescript.items

Controls which kind of items are included in the TypeScript language context provider.

"double"
github.copilot.chat.localeOverride

Specify a locale that Copilot should respond in, e.g. en or fr. By default, Copilot will respond using VS Code's configured display language locale.

"auto"
github.copilot.chat.localWorkspaceRecording.enabled

Enable local workspace recording for analysis.

false
github.copilot.chat.nesFetcher

Sets the fetcher used for the next edit suggestions.

""
github.copilot.chat.newWorkspace.useContext7

Whether to use the Context7 tools to scaffold project for new workspace creation.

false
github.copilot.chat.newWorkspaceCreation.enabled

Whether to enable new agentic workspace creation.

true
github.copilot.chat.notebook.alternativeFormat

Alternative document format for notebooks.

"xml"
github.copilot.chat.notebook.alternativeNESFormat.enabled

Enable alternative format for Next Edit Suggestions in notebooks.

false
github.copilot.chat.notebook.enhancedNextEditSuggestions.enabled

Controls whether to use an enhanced approach for generating next edit suggestions in notebook cells.

false
github.copilot.chat.notebook.followCellExecution.enabled

Controls whether the currently executing cell is revealed into the viewport upon execution from Copilot.

false
github.copilot.chat.notebook.summaryExperimentEnabled

Enable the notebook summary experiment.

false
github.copilot.chat.notebook.variableFilteringEnabled

Enable filtering variables by cell document symbols.

false
github.copilot.chat.omitBaseAgentInstructions

Omit base agent instructions from prompts.

false
github.copilot.chat.projectLabels.chat

Add project labels in chat requests.

false
github.copilot.chat.projectLabels.expanded

Use the expanded format for project labels in prompts.

false
github.copilot.chat.projectLabels.inline

Add project labels in inline edit requests.

false
github.copilot.chat.promptFileContextProvider.enabled

Enable prompt file context provider.

true
github.copilot.chat.pullRequestDescriptionGeneration.instructions

A set of instructions that will be added to Copilot requests that generate pull request titles and descriptions. Instructions can come from:

a file in the workspace: { "file": "fileName" }
text in natural language: { "text": "Always include a list of key changes." }
Note: Keep your instructions short and precise. Poor instructions can degrade Copilot's quality and performance.

[]
github.copilot.chat.responsesApiReasoningEffort

Sets the reasoning effort used for the Responses API. Requires #github.copilot.chat.useResponsesApi#.

"default"
github.copilot.chat.responsesApiReasoningSummary

Sets the reasoning summary style used for the Responses API. Requires #github.copilot.chat.useResponsesApi#.

"detailed"
github.copilot.chat.review.intent

Enable intent detection for code review.

false
github.copilot.chat.reviewAgent.enabled

Enables the code review agent.

true
github.copilot.chat.reviewSelection.enabled

Enables code review on current selection.

true
github.copilot.chat.reviewSelection.instructions

A set of instructions that will be added to Copilot requests that provide code review for the current selection. Instructions can come from:

a file in the workspace: { "file": "fileName" }
text in natural language: { "text": "Use underscore for field names." }
Note: Keep your instructions short and precise. Poor instructions can degrade Copilot's effectiveness.

[]
github.copilot.chat.scopeSelection

Whether to prompt the user to select a specific symbol scope if the user uses /explain and the active editor has no selection.

false
github.copilot.chat.setupTests.enabled

Enables the /setupTests intent and prompting in /tests generation.

true
github.copilot.chat.suggestRelatedFilesFromGitHistory.useEmbeddings

Use embeddings to suggest related files from git history.

false
github.copilot.chat.summarizeAgentConversationHistory.enabled

Whether to auto-summarize agent conversation history once the context window is filled.

true
github.copilot.chat.summarizeAgentConversationHistoryThreshold

Threshold for summarizing agent conversation history.

0
github.copilot.chat.terminalChatLocation

Controls where chat queries from the terminal should be opened.

"chatView"
github.copilot.chat.testGeneration.instructions

A set of instructions that will be added to Copilot requests that generate tests. Instructions can come from:

a file in the workspace: { "file": "fileName" }
text in natural language: { "text": "Use underscore for field names." }
Note: Keep your instructions short and precise. Poor instructions can degrade Copilot's quality and performance.

[]
github.copilot.chat.tools.defaultToolsGrouped

Group default tools in prompts.

false
github.copilot.chat.tools.memory.enabled

Enable memory tool to allow models to store and retrieve information across conversations.

Note: This is an experimental feature.

false
github.copilot.chat.useProjectTemplates

Use relevant GitHub projects as starter projects when using /new

true
github.copilot.chat.useResponsesApi

Use the Responses API instead of the Chat Completions API when supported. Enables reasoning and reasoning summaries.

Note: This is an experimental feature that is not yet activated for all users.

Important: URL API path resolution for custom OpenAI-compatible and Azure models is independent of this setting and fully determined by url property of #github.copilot.chat.customOAIModels# or #github.copilot.chat.azureModels# respectively.

true
github.copilot.chat.useResponsesApiTruncation

Use Responses API for truncation.

false
github.copilot.chat.virtualTools.threshold

This setting defines the tool count over which virtual tools should be used. Virtual tools group similar sets of tools together and they allow the model to activate them on-demand. Certain tool groups will optimistically be pre-activated. We are actively developing this feature and you experience degraded tool calling once the threshold is hit.

May be set to 0 to disable virtual tools.

128
github.copilot.chat.workspace.enableCodeSearch

Enable code search in workspace context.

true
github.copilot.chat.workspace.enableEmbeddingsSearch

Enable embeddings-based search in workspace context.

true
github.copilot.chat.workspace.enableFullWorkspace

Enable full workspace context analysis.

true
github.copilot.chat.workspace.maxLocalIndexSize

Maximum size of the local workspace index.

100000
github.copilot.chat.workspace.preferredEmbeddingsModel

Preferred embeddings model for semantic search.

""
github.copilot.chat.workspace.prototypeAdoCodeSearchEndpointOverride

Override endpoint for Azure DevOps code search prototype.

""
github.copilot.editor.enableCodeActions

Controls if Copilot commands are shown as Code Actions when available

true
github.copilot.enable

Enable or disable auto triggering of Copilot completions for specified languages. You can still trigger suggestions manually using Alt + \

{
"\*": true,
"plaintext": false,
"markdown": false,
"scminput": false
}
github.copilot.nextEditSuggestions.allowWhitespaceOnlyChanges

Whether to allow whitespace-only changes be proposed by next edit suggestions (NES).

true
github.copilot.nextEditSuggestions.enabled

Whether to enable next edit suggestions (NES).

NES can propose a next edit based on your recent changes. Learn more about next edit suggestions.

false
github.copilot.nextEditSuggestions.extendedRange

Whether to allow next edit suggestions (NES) to modify code farther away from the cursor position.

false
github.copilot.nextEditSuggestions.fixes

Whether to offer fixes for diagnostics via next edit suggestions (NES).

true
github.copilot.nextEditSuggestions.preferredModel

Preferred model for next edit suggestions.

"none"
github.copilot.renameSuggestions.triggerAutomatically

Controls whether Copilot generates suggestions for renaming

true
github.copilot.selectedCompletionModel

The currently selected completion model ID. To select from a list of available models, use the "Change Completions Model" command or open the model picker (from the Copilot menu in the VS Code title bar, select "Configure Code Completions" then "Change Completions Model". The value must be a valid model ID. An empty value indicates that the default model will be used.

---

## GitHub.copilot

https://marketplace.visualstudio.com/items?itemName=GitHub.copilot

Settings
ID Description Default
github.copilot.advanced

{}
github.copilot.enable

Enable or disable auto triggering of Copilot completions for specified languages. You can still trigger suggestions manually using Alt + \

{
"\*": true,
"plaintext": false,
"markdown": false,
"scminput": false
}
github.copilot.selectedCompletionModel

The currently selected completion model ID. To select from a list of available models, use the "Change Completions Model" command or open the model picker (from the Copilot menu in the VS Code title bar, select "Configure Code Completions" then "Change Completions Model". The value must be a valid model ID. An empty value indicates that the default model will be used.
