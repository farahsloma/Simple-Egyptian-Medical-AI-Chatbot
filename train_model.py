from models import State
from dotenv import load_dotenv
from workflow import WorkFlow
load_dotenv()

intial_state = State({
    'query' : 'give me 4 exmples about egyptian medical',
    'messages':[],
    'content':None,
    'response':None,
    'rewritten_query':None
})
WorkFlow = WorkFlow()
results = WorkFlow.run(intial_state)
print(f'Rewrriten_Query: {results.get('rewritten_query')}')
print('=' * 50)
print(f'Response: {results.get('response')}')
print('='*50)
