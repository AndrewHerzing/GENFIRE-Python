# -*- mode: python -*-

block_cipher = None


a = Analysis(['GENFIRE_GUI_Launch.py'],
             pathex=['/Users/ajpryor/Documents/GENFIRE/temp/GENFIRE'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GENFIRE_GUI_Launch',
          debug=False,
          strip=False,
          upx=True,
          console=True )
