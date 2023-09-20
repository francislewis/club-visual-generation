# import random
# import threading
#
# orig_prompt = "devinantart contemporary art psychedelic jungle mushroom with multicolour lines DMT elves"
# iteration_limit = 60  # Max number of iterations, will likely be less than this for equal splits
#
# init_split = orig_prompt.split()
# len_split = len(init_split)
# iterations = (iteration_limit // len_split) * len_split  # True number of iterations
# prompt_list = []  # Where the prompts to be run are saved
# for i in range(iterations):
#     if i != 0:
#         if i % (iterations / len_split) == 0:
#             if len(init_split) > 1:
#                 init_split.pop(random.randrange(len(init_split)))
#         prompt = ' '.join(init_split)
#         prompt_list.append(prompt)
#
# print(len(prompt_list))
#
# # Generate a test video:
# from model.sd_videos import sd_videos
#
# sd_videos_test_object = sd_videos(steps=3, output_dir='test_vid', interpolation_steps=5)
# sd_videos_test_object.gen_txt2vid(prompts=prompt_list, sub_directory='1')



