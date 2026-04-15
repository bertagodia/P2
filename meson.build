project('P2', 'c')

exe = 'vad'
src = ['src/main_vad.c', 'src/vad.c', 'src/pav_analysis.c']

snd_dep = dependency('sndfile')

executable(exe, sources:src, dependencies: snd_dep, link_args: '-lm')
