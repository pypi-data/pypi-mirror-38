import os
import shutil
from pathlib import Path

from connectivity import Constants as Const


class FileMover():

    def moveFile(self, sourcePath, targetPath, override=False):
        fSource = Path(sourcePath)
        fTarget = Path(targetPath)

        # Evaluate target dir and target filename
        tPath, tFileName = os.path.split(targetPath)
        tPathObject = Path(tPath)
        if not tPathObject.is_dir():
            tPathObject.mkdir(parents=True, exist_ok=True)

        if not override:
            if fSource.is_file() and not fTarget.is_dir():
                newTargetPath = targetPath     
                while Path(newTargetPath).is_file():
                    # Add number to fileName
                    tFileNameSplit = tFileName.split('.')
                    tFileName = tFileNameSplit[0] + '_1.' + tFileNameSplit[1]
                    newTargetPath = os.path.join(tPath, tFileName)
                # Move the file
                shutil.move(sourcePath, newTargetPath)
            elif not fSource.is_file():
                raise FileNotFoundError('Source file does not exists!')
        else: 
            if not fSource.is_file():
                raise FileNotFoundError('Source file does not exists!')
            else: shutil.move(sourcePath, targetPath)
            

    def removeTmpUserDir(self, uid):
        # Remove the temporary directory
        Path(Const.DEFAULT_DIR + uid + '/').rmdir()
