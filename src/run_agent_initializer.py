"""
Wrapper script to run agent initializers with proper environment variable loading.
This ensures dotenv loads before any module imports that depend on environment variables.
"""
import os
import sys
from dotenv import load_dotenv, dotenv_values

# Get the script directory (src)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from src/.env
env_path = os.path.join(script_dir, '.env')

# Check if .env file exists
if not os.path.exists(env_path):
    print(f"ERROR: .env file not found at {env_path}")
    sys.exit(1)

# Load and explicitly set environment variables
print(f"Loading environment from: {env_path}")
env_vars = dotenv_values(env_path)
print(f"Loaded {len(env_vars)} environment variables")

# Explicitly set each variable in os.environ
for key, value in env_vars.items():
    if value:  # Only set non-empty values
        os.environ[key] = value

# Also call load_dotenv for good measure
load_dotenv(env_path, override=True)

# Verify environment variables are loaded
if not os.getenv('COSMOS_ENDPOINT'):
    print("ERROR: COSMOS_ENDPOINT not found after loading .env")
    print(f"Available env vars starting with 'COSMOS': {[k for k in os.environ.keys() if k.startswith('COSMOS')]}")
    sys.exit(1)

print(f"Environment loaded successfully. COSMOS_ENDPOINT: {os.getenv('COSMOS_ENDPOINT')[:50]}...")

# Get the agent script name from command line argument
if len(sys.argv) < 2:
    print("Usage: python run_agent_initializer.py <agent_script_name>")
    sys.exit(1)

agent_script = sys.argv[1]

# Change to agents directory
agents_dir = os.path.join(script_dir, 'app', 'agents')
os.chdir(agents_dir)
sys.path.insert(0, agents_dir)

# Get the full path to the agent script
agent_script_path = os.path.join(agents_dir, agent_script)

# Execute the agent initializer script with proper globals including __file__
print(f"Executing {agent_script}...")
exec_globals = {
    '__file__': agent_script_path,
    '__name__': '__main__',
    '__builtins__': __builtins__,
}
with open(agent_script, 'r') as f:
    exec(f.read(), exec_globals)
