from model.sd_gpu_v1_4 import SD_GPU_V1_4

GPU_img2img_test_object = SD_GPU_V1_4(steps=5)
image = GPU_img2img_test_object.gen_txt2img(prompt="Horse riding on an astronaut")
display(image)

