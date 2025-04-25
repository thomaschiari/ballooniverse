from dotenv import load_dotenv
from chain import BallooniverseChain

load_dotenv(override=True)

chain = BallooniverseChain(llm='gemini')
game = chain.get_game_code()

with open('result.md', 'w') as f:
    f.write(game)

try:
    html_code = game.split('```html')[1].split('```')[0]
    with open('index.html', 'w') as f:
        f.write(html_code)
except Exception as e:
    print(f"Unable to write index.html: {e}. Check for results in result.md")