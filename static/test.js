document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const uploadBtn = document.getElementById("upload-btn");
    const uploadedImage = document.getElementById("uploaded-image");

    fileInput.addEventListener("change", handleFileSelect);
    uploadBtn.addEventListener("click", handleUpload);

    function handleFileSelect(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            uploadedImage.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }

    function handleUpload() {
        const fileInput = document.getElementById("file-input");

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        fetch("/classify", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                const result = data;
                const resultText = document.getElementById("result-text");
                console.log(result);
                console.log(result);

                resultText.innerHTML = JSON.stringify(result, undefined, 2);
            })
            .catch((error) => console.error("Error uploading image:", error));
    }
});
