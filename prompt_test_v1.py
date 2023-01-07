import random

orig_prompt = "devinantart contemporary art psychedelic jungle mushroom with multicolour lines DMT elves"
iteration_limit = 60  # Max number of iterations, will likely be less than this for equal splits

init_split = orig_prompt.split()
len_split = len(init_split)
iterations = (iteration_limit // len_split) * len_split  # True number of iterations
prompt_list = []  # Where the prompts to be run are saved
for i in range(iterations):
    if i != 0:
        if i % (iterations / len_split) == 0:
            if len(init_split) > 1:
                init_split.pop(random.randrange(len(init_split)))
        prompt = ' '.join(init_split)
        prompt_list.append(prompt)

print(len(prompt_list))
