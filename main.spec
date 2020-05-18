# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['M:\\Proyectos\\Python\\Game_first_steps\\Game'],
             binaries=[],
             datas=[('./images/bg.jpg', 'images'), ('./images/bullet.png', 'images'), ('./images/monster.png', 'images'), ('./images/monster2.png', 'images'), ('./images/monster3.png', 'images'), ('./images/player_icon.png', 'images'), ('./images/player2_icon.png', 'images'), ('./images/space_ship.png', 'images'), ('./sounds/laser.wav', 'sounds'), ('./sounds/explosion.wav', 'sounds'), ('./sounds/bgs.wav', 'sounds'), ('./fonts/freesansbold.ttf', 'fonts')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
