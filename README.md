# club-visual-generation

Software to generate interactive visuals in a club-night environment.

Currently all of the ML is done with [Stable Diffusion](https://github.com/CompVis/stable-diffusion).

## Development Overview
There are 3 different directions this can go in:
- ##### Manual pipeline
    - Choose a txt2img or img2img model to start
    - Choose a custom interpolater
      - Could be fast (OpenCV)
      - Or fancy like DAIN/DiffMorph
    - I'll leave the general framework of this in, but it will probably only ever be a priority if I run into a serious issue with DeForum 
    - Pros:
      - Very customisable/modular
    - Cons:
      - Have to write a lot of stuff from scratch 
- ##### [StableDiffusionVideos](https://github.com/nateraw/stable-diffusion-videos)
  - Library to create video from prompts using stable diffusion 
  - Already have a somewhat working implementation here
  - Pros:
    - Pretty easy to implement
  - Cons:
    - Not super customisable
    - May have to contribute upstream for features wanted here like initial image prompt
- ##### DeForum
  - This is the most mature solution in the SD Video generation space
  - Mostly notebook based but there is a [version](https://github.com/HelixNGC7293/DeforumStableDiffusionLocal) callable in Python (with some editing)
  - I think it's worth focusing some development effort here
  - Pros:
    - Likely has all the features we need
  - Cons:
    - Heavy reliance on a codebase which is getting more complex
    - Lot of dependencies
    - Quite a bit of a learning curve specific to DeForum



## Architecture Overview 
- ##### Model
  - Class containing all the models
    - Have methods like gentxt2img()
- ##### AbstractPipeline
  - To differentiate from generation/model pipelines
  - This is where the generation process is actually put together
  - A thread to take inputs is started, these are added to a queue object
  - Another thread is started for processing the actual generation
  - The sd_videos approach saves the outputs to file, this is useful to use as a pool to display from
- ##### Display
  - Not implemented yet
  - Link in with Rekordbox ProLink

### Plan / To-Do

- Find a way to abstract the images at a similiar rate
  -  Maybe img2img without current 'prompt hacking'
- Allow option for image or text input
- Integrate Rekordbox code for music sync and think about output methods 
- Control quality/speed trade off for a fixed generation time 
