from __init__ import Model
from stable_diffusion_videos import StableDiffusionWalkPipeline
import torch
import random

class sd_videos(Model):
    def __init__(self, height=512, width=768, **kwargs):
        """
        steps - Number of inference steps, lower is worse quality but faster
        """
        self.height = height
        self.width = width
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('steps', 'output_dir', 'interpolation_steps',)
        super().__init__(**kwargs)
        self.steps = kwargs.pop('steps', '')
        self.output_dir = kwargs.pop('output_dir', '')
        self.interpolation_steps = kwargs.pop('interpolation_steps', '')


    def gen_txt2vid(self, prompts, sub_directory):
        """
        prompts - list of strings to be used as prompts for video generation
        output_dir
        """
        self.prompts = prompts
        self.sub_directory = sub_directory

        # For CUDA
        #pipe = StableDiffusionWalkPipeline.from_pretrained("./stable-diffusion-v1-4", torch_dtype=torch.float16, revision="fp16").to("cuda")

        # For low vram (very slow) - requires: 'pip install accelerate'
        pipe = StableDiffusionWalkPipeline.from_pretrained("./stable-diffusion-v1-4")

        # Turn off NSFW filter
        def safety_checker(images, clip_input):
            return images, False

        pipe.safety_checker = safety_checker
        pipe.walk(
            prompts=self.prompts,
            seeds=random.sample(range(1, 100), len(prompts)),
            num_interpolation_steps=self.interpolation_steps,
            height=self.height,  # use multiples of 64 if > 512. Multiples of 8 if < 512.
            width=self.width,  # use multiples of 64 if > 512. Multiples of 8 if < 512.
            output_dir=self.output_dir,  # Where images/videos will be saved
            name=self.sub_directory,  # Subdirectory of output_dir where images/videos will be saved
            guidance_scale=8.5,  # Higher adheres to prompt more, lower lets model take the wheel
            num_inference_steps=self.steps,  # Number of diffusion steps per image generated. 50 is good default
        )

        return sub_directory

# ############ Example ############
# sd_videos_test_object = sd_videos(steps=3, output_dir='test_vid', self.interpolation_steps=3)
# print(sd_videos_test_object.gen_txt2vid(prompts=["Horse riding on an astronaut", "Astronaut riding on a horse"], sub_directory='2'))
