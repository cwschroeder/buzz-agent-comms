# Code-rendered motion

Claude cannot paint pixels, but it can write a program that draws every frame.
A browser renders those frames and ffmpeg turns them into an MP4 or a GIF.
Every frame is reproducible, a fix is a changed number, and Claude can inspect
its own frames before anyone else sees them. Use this for Buzz posts whenever
order or timing is the point. Background: the "Opus 5.5 Motion Lab" article
(Florence, X, 2026-09-30).

## When motion helps

Use a short animation when a still image would force the reader to replay the
sequence in their head:

- a handoff or pipeline where something moves between stages, agents or hosts
- a state that changes over time: a queue draining, a retry loop, a rollout
- a before/after where the difference is behaviour, not layout
- a decision path that is easier to follow one step at a time

Stay with a still diagram, a table or a list when the relationship is static.
Never animate a start message or a minor status update.

Motion explains; it does not prove. Delivery evidence for a UI stays a real
screenshot or screen recording from the canonical runtime. An animation built
from verified facts is an explanatory diagram. An animation of something not
built yet is a concept and its caption says `Konzept`.

## Engine

Default to one self-contained HTML file with inline SVG, CSS and JavaScript:
no network, no CDN, system fonts. It covers flows, timelines, cards and charts
under ten seconds. Reach for GSAP or three.js only when the piece needs a
timeline library or real 3D; vendor the pinned file next to the HTML instead of
loading it from the network. Remotion fits a series of data-driven videos.

## Render contract

Write these rules into the animation, or into the prompt that writes it:

- Every frame is a pure function of the frame number. No `Date.now()`, no
  `requestAnimationFrame` clock, no timers during capture.
- Randomness is seeded. Unseeded randomness makes shapes jitter between frames.
- The page exposes `?frame=N` and renders exactly frame N from it.
- A loop of N frames renders frames 0 to N-1, never N. Frame N is frame 0 again,
  and showing it twice is the hiccup at the seam.
- Frame 0 is a finished composition. It is what Buzz shows before playback.

The bundled [motion-example.html](motion-example.html) implements this contract
with synthetic content.

## Motion numbers

- Duration 4 to 10 seconds, 30 fps, 960x540 or 1280x720 (even dimensions).
- Enter with ease-out, exit with ease-in, exits 40 to 50 percent shorter than
  entrances. Linear only for rotation, progress bars and loop phase.
- One hero move at a time. Secondary moves travel 50 to 70 percent as far and
  start 100 to 200 ms later.
- Text never moves while it is meant to be read. Hold the final state at least
  one second.
- Springs: damping ratio 0.7 to 0.85 reads calm; position and size may
  overshoot, opacity and colour never do.

Avoid the defaults that read as generated: purple or blue gradients, glow, lens
flares, decorative particles, everything fading in at once, fade-and-slide-up
on every element, everything centred. After each first render, name any default
that slipped in and ban it explicitly in the next round.

## Capture

Headless Chrome and ffmpeg are enough. Check both exist; never install them
without the user's consent. On macOS:

```bash
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p frames
for i in $(seq 0 179); do
  "$chrome" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=960,540 \
    --screenshot="frames/$(printf %04d "$i").png" \
    "file://$PWD/anim.html?frame=$i" >/dev/null 2>&1
done
```

On Linux use `chromium` or `google-chrome`; on Windows use the full path to
`chrome.exe`. 180 frames take about 90 seconds this way. A Playwright script that
keeps one page open and calls `renderFrame(n)` is faster when it is installed.

Encode without metadata. The Buzz relay rejects MP4 files with metadata boxes
(HTTP 422, "media contains metadata or a non-canonical metadata channel"):

```bash
ffmpeg -framerate 30 -i frames/%04d.png -c:v libx264 -pix_fmt yuv420p \
  -crf 20 -movflags +faststart \
  -map_metadata -1 -fflags +bitexact -flags:v +bitexact anim.mp4
```

For a short loop as GIF, use one palette for the whole clip so colours do not
flicker. The relay accepts GIFs without comment or plain-text extensions:

```bash
ffmpeg -framerate 30 -i frames/%04d.png \
  -vf "fps=15,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" \
  -loop 0 anim.gif
```

## Look before you post

The first render is a draft. Before attaching anything:

1. Build a contact sheet of 12 frames and read it like a storyboard:

   ```bash
   ffmpeg -i frames/%04d.png \
     -vf "select='not(mod(n\,15))',scale=320:-1,tile=4x3:padding=4:color=white" \
     -frames:v 1 contact-sheet.png
   ```

2. Open the frames in between the sheet's samples, especially mid-transition
   and around the loop seam.
3. Write fixes against frame numbers, not feelings ("frame 84: the badge peaks
   two frames late"), change only that, and re-render only what changed.

Two to four rounds are normal. Check legibility at phone width, since Buzz
shows the clip small on mobile.

## Publish in Buzz

- Prefer MP4 (H.264): Buzz desktop and mobile play it inline. Use GIF only for
  loops of a few seconds.
- Keep it silent and small. A 6-second flow at 960x540 is well under 1 MB.
- Attach it top-level with `project-buzz attach`, like every other visual. The
  caption says what to watch and whether the content is verified or a concept.
- The post must still make sense without playing the clip.
- If Chrome or ffmpeg is missing, or the relay rejects the file, fall back to a
  static `project-buzz skizze` and state why.
