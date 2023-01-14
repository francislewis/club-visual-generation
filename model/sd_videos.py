from model import Model
from stable_diffusion_videos import StableDiffusionWalkPipeline
import torch
import random
import os

class sd_videos(Model):
    def __init__(self, height=512, width=768, **kwargs):
        """
        Inputs:
            height, width - of output in pixels, default 512 x 768
            steps - Number of inference steps, lower is worse quality but faster
            interpolation steps
            platform - ['SLOW', 'CUDA', 'MPS', 'CoreML']
        """

        self.height = height
        self.width = width
        # Add valid kwargs
        kwargs['_valid_kwargs'] = kwargs.get('_valid_kwargs', tuple()) + ('steps', 'output_dir', 'interpolation_steps', 'platform',)
        super().__init__(**kwargs)
        self.steps = kwargs.pop('steps', '')
        self.output_dir = kwargs.pop('output_dir', '')
        self.interpolation_steps = kwargs.pop('interpolation_steps', '')
        self.platform = kwargs.pop('platform', 'SLOW')


    def gen_txt2vid(self, prompts, sub_directory):
        """
        prompts - list of strings to be used as prompts for video generation
        sub_directory - folder for videos to be saved under
        """

        self.is_running = True
        self.prompts = prompts
        self.sub_directory = sub_directory

        # TODO: this path is the path to the model from wherever the model instance it made, which is often outside the model directory
        path = os.getcwd()
        sd_model_path = os.path.join(path, 'model', 'stable-diffusion-v1-4')

        # Create different pipelines depending on target platform
        if self.platform == 'SLOW':
            # For low vram (very slow) - requires: 'pip install accelerate'
            pipe = StableDiffusionWalkPipeline.from_pretrained(sd_model_path)

        elif self.platform == 'CUDA':
            pipe = StableDiffusionWalkPipeline.from_pretrained(sd_model_path, torch_dtype=torch.float16, revision="fp16").to("cuda")

        elif self.platform == 'MPS':
            raise NotImplementedError

        elif self.platform == 'CoreML':
            raise NotImplementedError

        else:
            print(str(self.platform) + " is not a valid platform. Please try again with 'SLOW','CUDA' or 'MPS'")

        # Turn off NSFW filter
        def safety_checker(images, clip_input):
            return images, False
        pipe.safety_checker = safety_checker

        # Call SD_videos
        pipe.walk(
            prompts=self.prompts,
            seeds=random.sample(range(1, 100), len(prompts)),
            num_interpolation_steps=self.interpolation_steps,
            height=self.height,  # use multiples of 64 if > 512. Multiples of 8 if < 512.
            width=self.width,  # use multiples of 64 if > 512. Multiples of 8 if < 512.
            output_dir=self.output_dir,  # Where images/videos will be saved
            name=self.sub_directory,  # Subdirectory of output_dir where images/videos will be saved
            guidance_scale=5,  # Higher adheres to prompt more, lower lets model take the wheel
            num_inference_steps=self.steps,  # Number of diffusion steps per image generated. 50 is good default
        )

        self.is_running = False
        # return sub_directory

# ############ Example ############
# sd_videos_test_object = sd_videos(steps=3, output_dir='test_vid', self.interpolation_steps=3)
# print(sd_videos_test_object.gen_txt2vid(prompts=["Horse riding on an astronaut", "Astronaut riding on a horse"], sub_directory='2'))
