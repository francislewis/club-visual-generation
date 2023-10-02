from model.sd_v1_4 import sd_v1_4

GPU_img2img_test_object = sd_v1_4(steps=5)
image = GPU_img2img_test_object.gen_txt2img(prompt="Horse riding on an astronaut")
display(image)

