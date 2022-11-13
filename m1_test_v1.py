import torch
from diffusers import StableDiffusionPipeline
from Model import SD_GPU_V1_4


GPU_img2img_test_object = SD_GPU_V1_4()
print(GPU_img2img_test_object.gen_txt2img(prompt="Horse riding on an astronaut"))
