from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentType
from langchain.agents import initialize_agent
import logging
import json
import time
import os
from langchain_core.messages import HumanMessage
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable not set")
    raise ValueError("OPENAI_API_KEY environment variable not set")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=OPENAI_API_KEY
)

def load_code_file(file_path: str) -> str:
    """
    Load code from a file.
    
    Args:
        file_path: Path to the code file
        
    Returns:
        String containing the code
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return f"Error: File not found: {file_path}"
            
        with open(file_path, 'r') as f:
            code = f.read()
        return code
    except Exception as e:
        logger.error(f"Error loading code file {file_path}: {e}")
        return f"Error loading code file: {str(e)}"

def analyze_code(code: str) -> Dict[str, Any]:
    """
    Analyze code and return structured markdown content.
    
    Args:
        code: The code to analyze
        
    Returns:
        Dictionary containing the analysis
    """
    prompt = (
        "You are an expert at writing documentation for Python code in markdown format. "
        "Analyze the following code and provide a comprehensive analysis including:\n"
        "1. Overall purpose and functionality\n"
        "2. Classes and their methods\n"
        "3. Functions and their parameters\n"
        "4. Dependencies and imports\n"
        "5. Usage examples\n\n"
        f"Code:\n{code}\n\n"
        "Return your analysis as content that can be directly used in markdown documentation."
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return {"content": response.content}
    except Exception as e:
        logger.error(f"Error analyzing code: {e}")
        return {"error": str(e)}

def write_doc(analysis: str) -> str:
    """
    Convert analysis into well-formatted markdown documentation.
    
    Args:
        analysis: The analysis to convert
        
    Returns:
        Markdown formatted documentation
    """
    prompt = (
        "You are a technical writer specializing in code documentation. "
        "Convert the following analysis into comprehensive markdown documentation. "
        "Include the following sections:\n"
        "- Title and description\n"
        "- Installation and setup\n"
        "- Usage examples\n"
        "- API reference with function and class details\n"
        "- Dependencies\n\n"
        "Format the documentation with proper markdown syntax including headings, "
        "code blocks, lists, and tables as appropriate.\n\n"
        f"Analysis:\n{analysis}"
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        logger.error(f"Error writing documentation: {e}")
        return f"Error generating documentation: {str(e)}"

def save_markdown_file(markdown_content: str, file_name: str = "untitled") -> str:
    """
    Save markdown content to a file.
    
    Args:
        markdown_content: The markdown content to save
        file_name: The name for the file (without .md extension)
        
    Returns:
        Path to the saved file
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "docs")
        os.makedirs(output_dir, exist_ok=True)

        # Create filename with timestamp
        timestamp = int(time.time())
        base_filename = f"{file_name}_{timestamp}.md"
        full_path = os.path.join(output_dir, base_filename)

        # Write content to file
        with open(full_path, "w") as f:
            f.write(markdown_content)

        logger.info(f"Successfully saved documentation to {full_path}")
        return full_path
    except Exception as e:
        error_msg = f"Error saving file: {e}"
        logger.error(error_msg)
        return error_msg

def document_code_file(file_path: str) -> str:
    """
    Generate documentation for a code file and save it.
    
    Args:
        file_path: Path to the code file
        
    Returns:
        Path to the saved documentation file
    """
    try:
        # Load the code
        code = load_code_file(file_path)
        if code.startswith("Error"):
            return code
            
        # Get the base filename without extension
        base_name = os.path.basename(file_path)
        file_name = os.path.splitext(base_name)[0]
        
        # Analyze the code
        analysis_result = analyze_code(code)
        if "error" in analysis_result:
            return f"Error analyzing code: {analysis_result['error']}"
            
        # Write documentation
        markdown_doc = write_doc(analysis_result["content"])
        
        # Save the documentation
        saved_path = save_markdown_file(markdown_doc, f"{file_name}_documentation")
        
        return f"Documentation generated and saved to {saved_path}"
    except Exception as e:
        logger.error(f"Error documenting code file: {e}")
        return f"Error documenting code file: {str(e)}"

# Define tools for the agent
tools = [
    Tool(
        name="load_code_file",
        func=load_code_file,
        description="Load code from a file. Provide the full path to the file."
    ),
    Tool(
        name="analyze_code", 
        func=analyze_code, 
        description="Analyze code and return structured markdown content"
    ),
    Tool(
        name="write_doc", 
        func=write_doc, 
        description="Convert analysis into well-formatted markdown documentation"
    ),
    Tool(
        name="save_markdown_file",
        func=save_markdown_file,
        description="Save markdown content which analysed from analyse_tool to a file . Provide the markdown content and optionally a file name."
    ),
    Tool(
        name="document_code_file",
        func=document_code_file,
        description="Generate documentation for a code file and save it. Provide the full path to the file."
    )
]

# Initialize the LLM for tools
tool_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

# Create the agent with AgentType enum
agent = initialize_agent(
    tools,
    tool_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example usage
if __name__ == "__main__":
    # Directly use the document_code_file function instead of the agent
    # file_path = "/home/hai/agent2agent/agent_document.py"
    # result = document_code_file(file_path)
    # print(result)
    
    # If you want to try the agent later, uncomment this:
    result = agent.run("Generate documentation for the file /home/hai/agent2agent/agent_document.py")
    # print(result)