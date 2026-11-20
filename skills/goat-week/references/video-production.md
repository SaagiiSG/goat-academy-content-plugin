# Videos: production with the GOAT video skills

Videos are produced by the GOAT video skills bundled in this plugin (video editing styles
plus a 3D animation skill). They create the Mongolian voice-over with ElevenLabs, using the
key in `~/.goat-academy/keys.env` (load it into the environment for the command; never
print it).

## Which skill for which post

<!-- GOAT_VIDEO_SKILLS: fill in when the video skills are added to skills/ -->
The video skills are not bundled yet. Until they are:
- `video-ai` posts → make them as carousels instead and note it in `plan.md`.
- `video-member` posts → write the filming card; the member films and posts, or drops the
  clip into `inbox/` for scheduling as-is.

## Inputs every video skill gets

- `script.md` (spoken lines in Mongolian, timing, on-screen text, visual notes)
- The chosen format's example link from `formats.md` (for pacing and style)
- Brand colors and font from `profile.md`; voice choice (cloned / stock voice name)
- Output: `post-NN/video.mp4`, 9:16, 1080×1920, 15–60 s unless the format needs longer,
  burned-in Mongolian captions (most people watch on mute), hook text on screen in the first
  second.

## Check after rendering

Watch-check by extracting 3 frames (start, middle, end) with ffmpeg if available and reading
them: hook visible at 0 s, captions readable and not covering faces, nothing cut off.
Confirm the audio is Mongolian and matches the script.
