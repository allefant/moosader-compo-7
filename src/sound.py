import main

class Envelope:
    float attack # Seconds from 0 to max volume.
    float decay # Seconds from max volume to sustain volume.
    float hold # Seconds to hold sustain volume.
    float release # Seconds from sustain volume to 0.

    float volume # Maximum volume [0..1].
    float sustain # Sustain volume [0..1].

static float def wave_square(float x):
    return 1 - 2 * ((int)(x * 2) & 1)

static float def envelope(Envelope *e, float x):
    float v = 0
    if x < e->attack:
        v = e->volume * x / e->attack
    else:
        float x_ = x - e->attack
        if x_ < e->decay:
            v = e->volume + (e->sustain - e->volume) * x_ / e->decay
        else:
            v = e->sustain
            x_ -= e->decay
            if x_ > e->hold:
                x_ -= e->hold
                if x_ < e->release:
                    v = e->sustain - e->sustain * x_ / e->release
                else:
                    v = 0
                
    return v

static int16_t def float_to_signed_16(float s):
    int c = (s + 1) * 32767.5 - 32768
    if c < -32768: c = -32768
    elif c > 32767: c = 32767
    return c

LandSound *def sound_synthesize(Envelope *e, int note):
    float duration = e->attack
    duration += e->decay
    duration += e->hold
    duration += e->release
    
    float frequency = 48000

    int length = duration * frequency

    LandSound *sound = land_sound_new(length, frequency, 16, 2)
    
    uint16_t *data = land_sound_sample_pointer(sound)

    float x = 0
    for int i = 0 while i < length with i++:
        float t = i
        t *= 1 / frequency # Convert to seconds.
        float v = envelope(e, t)

        float tone_frequency = 440 * pow (2.0, (note - 69) / 12.0)

        float y = wave_square(x)

        y *= v

        data[i * 2] = float_to_signed_16(y)
        data[i * 2 + 1] = float_to_signed_16(y)

        x += tone_frequency / frequency

    return sound

