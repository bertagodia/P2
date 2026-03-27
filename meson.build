project('P2', 'c')

exe = 'vad'
src = ['src/main_vad.c', 'src/vad.c', 'src/pav_analysis.c']
#lib = ['-lm', '-lsndfile']

# Esta línea es la clave: busca la librería y sus rutas de cabecera
snd_dep = dependency('sndfile')

executable(exe, sources:src, dependencies: snd_dep)
