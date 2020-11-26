let detectedTextTextArea = document.getElementById("detected_text");
let typeTexRadio = document.getElementById('type-text');

function save() {
    if (typeTexRadio.checked) {
        // Saving file as text file
        saveAsTextFile(detectedTextTextArea.value, "detected-text.txt", "text/json");
    } else {
        saveAsPDF();
    }
}

function saveAsTextFile(text, filename, type) {
    var a = document.getElementById("a");
    var file = new Blob([text], { type: type });
    let url = URL.createObjectURL(file);
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

function saveAsPDF() {
    var doc = new jsPDF();

    doc.text(detectedTextTextArea.value, 10, 10);
    doc.save('detected-text.pdf');
}