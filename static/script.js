document.addEventListener("DOMContentLoaded", function() {
    const dropZone = document.getElementById("dropZone");
    const fileInput = dropZone.querySelector("input[type='file']");
    const preview = document.getElementById("preview");
    const form = document.getElementById("uploadForm");
    const loading = document.getElementById("loading");

    // Drag & Drop functionality
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.style.background = "rgba(255, 111, 97, 0.4)";
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.style.background = "transparent";
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.style.background = "transparent";
        fileInput.files = e.dataTransfer.files;
        showPreview(fileInput.files);
    });

    fileInput.addEventListener("change", () => {
        showPreview(fileInput.files);
    });

    function showPreview(files) {
        preview.innerHTML = "";
        for (let i = 0; i < files.length; i++) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                preview.appendChild(img);
            };
            reader.readAsDataURL(files[i]);
        }
    }
