import torch
from diffusers import StableDiffusionPipeline
from __init__ import Model


class SD_GPU_V1_4(Model):
    def __init__(self, height=512, width=768, **kwargs):
        """
        Use this for Google Colab
        steps - Number of inference steps, lower is worse quality but faster
        TODO: should this move to gen() in order to adjust quality depending on output speed?
        """
        self.height = height
        self.width = width
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('steps',)
        super().__init__(**kwargs)
        self.steps = kwargs.pop('steps','')


    def gen_txt2img(self, prompt):
        """
        prompt - string to be used as prompt for image generation
        """
        pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-4", revision="fp16",
                                                       torch_dtype=torch.float16, height=self.height, width=self.width, num_inference_steps=self.steps)
        # Note: revision="fp16" uses less VRAM
        #TODO: Ideally should be able to remove revision, torch_dtype and next CUDA line to run on CPU - something is wrong though.
        pipe = pipe.to("cuda")
        image = pipe(prompt).images[0]
        return image

# ############ Example ############
# GPU_img2img_test_object = SD_GPU_V1_4()
# print(GPU_img2img_test_object.gen_txt2img(prompt="Horse riding on an astronaut"))
