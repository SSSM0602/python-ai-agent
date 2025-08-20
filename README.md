# AI Coding Agent

A Python-based AI coding agent that uses Google's Gemini 2.0 Flash model to analyze code, execute tasks, and provide direct technical responses. The agent can interact with files and directories to understand and work with codebases.

## Features

- **File System Operations**: List directories, read file contents, and write files
- **Code Execution**: Run Python scripts with optional arguments
- **Intelligent Analysis**: Uses Gemini 2.0 Flash to understand code structure and functionality
- **Task-Focused**: Provides direct, technical responses without conversational fluff
- **Function Call Handling**: Automatically executes tool calls and manages conversation state

## Prerequisites

- Python 3.7+
- Google Gemini API key
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aiagent
```

2. Install dependencies:
```bash
pip install google-genai python-dotenv
```

3. Set up your environment variables:
```bash
# Create a .env file in the root directory
GEMINI_API_KEY=your_gemini_api_key_here
```

## Project Structure

```
aiagent/
├── main.py                 # Main application entry point
├── .env                    # Environment variables (create this)
├── functions/              # Function modules
│   ├── get_file_content.py # Read file contents
│   ├── get_files_info.py   # List files and directories
│   ├── run_python.py       # Execute Python files
│   └── write_file.py       # Write/create files
└── calculator/             # Example working directory
    ├── main.py
    └── pkg/
        ├── calculator.py
        └── render.py
```

## Usage

### Basic Usage

Run the agent with a question or task:

```bash
python main.py "your question or task here"
```

### Verbose Mode

Get detailed information about function calls and token usage:

```bash
python main.py "your question" --verbose
```

### Examples

Analyze how code works:
```bash
python main.py "how does the calculator render results to the console?"
```

Examine file structure:
```bash
python main.py "what files are in this project?"
```

Run and analyze code:
```bash
python main.py "run the calculator with expression '2 + 3 * 4'"
```

## Available Functions

The agent has access to four main functions:

1. **get_files_info**: Lists files and directories in the working directory
2. **get_file_content**: Reads and returns the contents of specified files
3. **run_python_file**: Executes Python files with optional command-line arguments
4. **write_file**: Creates or overwrites files with specified content

## Configuration

### Working Directory

The agent operates within a specified working directory (default: `./calculator`). Modify the `working_directory` variable in `main.py` to change this:

```python
working_directory = "./your_project_directory"
```

### System Prompt

The agent's behavior is controlled by the system prompt. The current configuration makes it:
- Provide direct, factual responses
- Avoid conversational language
- Focus on technical analysis
- Complete tasks efficiently

### Function Schemas

Each function requires a schema definition that describes its parameters and return types. These are imported from the respective function modules:

- `schema_get_files_info`
- `schema_get_file_content` 
- `schema_run_python`
- `schema_write_file`

## How It Works

1. **User Input**: You provide a question or task via command line
2. **AI Planning**: Gemini analyzes the request and determines what functions to call
3. **Function Execution**: The agent executes necessary file operations or code runs
4. **Response Generation**: Based on the gathered information, provides a direct answer
5. **Conversation Management**: Maintains context across multiple function calls until task completion

## Error Handling

The application includes comprehensive error handling:

- **Function Call Errors**: Caught and reported, with execution continuing
- **API Errors**: Network and API issues are handled gracefully  
- **Iteration Limits**: Prevents infinite loops with a 20-iteration maximum
- **Validation Errors**: Function responses are validated and formatted correctly

## Limitations

- **Working Directory Scope**: All file operations are relative to the configured working directory
- **Python Execution Only**: Can only execute Python files directly
- **API Rate Limits**: Subject to Google Gemini API rate limiting
- **No Persistent State**: No memory between separate program runs

## Troubleshooting

### Common Issues

**"Need a cmd line argument"**: Provide a question or task as the first argument

**"validation error for FunctionResponse"**: Function returned non-dictionary data - this is handled automatically in the current version

**"Unknown function" errors**: Check that all function modules are properly imported and defined in `func_defs`

**API authentication errors**: Verify your `GEMINI_API_KEY` is correctly set in the `.env` file

### Debug Mode

Use the `--verbose` flag to see:
- Detailed function call information
- Token usage statistics
- Step-by-step execution flow

## Contributing

To add new functions:

1. Create a new function module in the `functions/` directory
2. Define both the function and its schema
3. Import and add to `func_defs` in `main.py`
4. Update the `available_functions` tool declaration

