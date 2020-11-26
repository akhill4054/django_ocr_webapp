var src = document.getElementById("upload_image");
var target = document.getElementById("chosen_image");

function showImage(src, target) {
    var fr = new FileReader();
    // When image is loaded, set the src of the image where you want to display it
    fr.onload = function (e) { target.src = this.result; };
    src.addEventListener("change", function () {
        // fill fr with image data    
        fr.readAsDataURL(src.files[0]);
        document.getElementById('warn_no_img').innerHTML = "";
    });
}

showImage(src, target);