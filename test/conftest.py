import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
load_dotenv()

# import deepeval
# deepeval.login(api_key=os.environ.get("confident-api-key"))