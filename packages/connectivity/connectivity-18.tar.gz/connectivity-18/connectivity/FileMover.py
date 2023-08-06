from pathlib import Path
import os
import shutil

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
                changed = False
                
                while Path(newTargetPath).is_file():
                    changed = True
                    # Add number to fileName
                    tFileNameSplit = tFileName.split('.')
                    tFileName = tFileNameSplit[0] + '_1.' + tFileNameSplit[1]
                    newTargetPath = os.path.join(tPath, tFileName)
                
                if changed: print('Target file already exists! Saving the file as: ' + newTargetPath)
                
                # Move the file
                shutil.move(sourcePath, newTargetPath)

            elif not fSource.is_file():
                print('Source file does not exists!')
        else: 
            if not fSource.is_file():
                print('Source file does not exists!')
            else: shutil.move(sourcePath, targetPath)
            

    def removeTmpUserDir(self, uid):
        # Remove the temporary directory
        Path('tmp/' + str(uid) + '/').rmdir()