# 參考111010515林弘杰同學
# 參考https://github.com/ccc112b/py2cs/blob/master/03-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/06-%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92/01-%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92/01-gym/04-run/cartpole_human_run.py
import gym

env = gym.make("CartPole-v1", render_mode = "human")
observation = env.reset(seed=42)

score = 0
for _ in range(1000):
    env.render()
    
    if observation[2] < 0:
        action = 0  # 向左移動
    else:
        action = 1  # 向右移動
    
    observation, reward, done, info = env.step(action)
    score += reward
    
    if done:
        observation = env.reset()
        print(f"Done, Score: {score}")
        score = 0
        
env.close()