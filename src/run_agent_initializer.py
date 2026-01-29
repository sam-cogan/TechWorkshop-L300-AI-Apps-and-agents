"""
Wrapper script to run agent initializers with proper environment variable loading.
This ensures dotenv loads before any module imports that depend on environment variables.
"""
import os
import sys
from dotenv import load_dotenv

# Get the script directory (src)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from src/.env
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

# Verify environment variables are loaded
if not os.getenv('COSMOS_ENDPOINT'):
    print("ERROR: COSMOS_ENDPOINT not found after loading .env")
    sys.exit(1)

# Get the agent script name from command line argument
if len(sys.argv) < 2:
    print("Usage: python run_agent_initializer.py <agent_script_name>")
    sys.exit(1)

agent_script = sys.argv[1]

# Change to agents directory and run the script
agents_dir = os.path.join(script_dir, 'app', 'agents')
os.chdir(agents_dir)
sys.path.insert(0, agents_dir)

# Execute the agent initializer script
with open(agent_script, 'r') as f:
    exec(f.read())
