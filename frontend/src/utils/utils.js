import JSZip from "jszip"
import { toRaw } from "vue"
import { saveAs } from 'file-saver'


export async function downloadRom(rom, emitter, filesToDownload=[]) {
    emitter.emit('snackbarScan', {'msg': "Downloading "+rom.file_name+"...", 'icon': 'mdi-download', 'color': 'green'})
    if(rom.multi){
        const zip = new JSZip()
        var zipFilename = rom.file_name+".zip"
        var files = []
        toRaw(filesToDownload).forEach(f => {files.push(toRaw(f))})
        if (files.length == 0){ files = rom.files }
        var count = 0
        files.forEach(async function (file_part) {
            var file_full_path = "/assets"+rom.file_path+"/"+rom.file_name+"/"+file_part
            var file = await fetch(file_full_path)
            var fileBlob = await file.blob()
            var f = zip.folder(rom.file_name);
            f.file(file_part, fileBlob, { binary: true });
            count ++
            if (count == files.length) { zip.generateAsync({ type: 'blob' }).then(function (content) { saveAs(content, zipFilename); }); }
        })
    }
    else{
        var file_full_path = "/assets"+rom.file_path+"/"+rom.file_name
        var file = await fetch(file_full_path)
        var fileBlob = await file.blob()
        saveAs(fileBlob, rom.file_name)
    }
}

export async function downloadSave(rom, emitter) { console.log("Downloading "+rom.file_name+" save file") }
