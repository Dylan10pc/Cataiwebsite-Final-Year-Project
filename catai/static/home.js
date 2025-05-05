console.log("JS Loaded");
document.addEventListener("DOMContentLoaded", function () { 
    const uploadedarea = document.getElementById('upload1');
    const inputimg = document.getElementById('file1');
    const imagepreview = document.getElementById('preview1');
    const textupload = uploadedarea.querySelector('p');
    const form = document.getElementById('uploadForm');
    const cropbtn = document.getElementById('crop');
    const modal = document.getElementById('Modal');
    const imgcrop = document.getElementById('cropimg');
    const closemodal = document.querySelector('.close');
    const savebtn = document.getElementById('save');
    const results = document.getElementById('results');
    const reversesearch = document.getElementById('reversesearch');
    let latestimgUrl = "";
    let cropper;
    let cropped = false;

    //event listener to trigger file upload when the user clicks on the upload area
    uploadedarea.addEventListener('click', () => inputimg.click());

    //when an image is uploaded, display the image in the preview area
    inputimg.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                imagepreview.src = reader.result;
                imagepreview.hidden = false;
                textupload.hidden = true;
                //reset the cropper and the cropped flag
                cropped = false;
                //destroy the cropper if it exists
                if (cropper) cropper.destroy();
                cropper = null;
            };
            //read the image file as a data URL
            reader.readAsDataURL(file);
        }
    });

    //event listener to trigger crop when the user clicks on the crop button
    cropbtn.addEventListener('click', () => {
        //set the imahge source of the crop image to the preview image
        imgcrop.src = imagepreview.src;
        modal.style.display = 'block';
        if (cropper) cropper.destroy();
        cropper = new Cropper(imgcrop, {
            aspectRatio: 1,
            viewMode: 2,
            dragMode: 'move',
            cropBoxResizable: true,
            cropBoxMovable: true,
            responsive: true,
        });
    });

    //event listener to save the cropped image when the user clicks on the save button
    savebtn.addEventListener('click', () => {
        if (cropper) {
            //get the cropped canvas and display it in the preview area
            const canvascrop = cropper.getCroppedCanvas();
            if (canvascrop) {
                imagepreview.src = canvascrop.toDataURL('image/jpeg'); 
                imagepreview.hidden = false;
                textupload.hidden = true;
                modal.style.display = 'none';
                //set the cropped flag to true
                cropped = true; 
            }
        }
    });

    //event listener to close the crop modal when the user clicks on the close button
    closemodal.addEventListener('click', () => {
        modal.style.display = 'none';
        if (cropper) cropper.destroy();
    });


    //event listener to submit the form when the user clicks on the submit button
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        //check if the image was cropped or not
        //and check if the image was uploaded or not
        if (!inputimg.files[0] && !cropped) {
            alert("Please upload an image before submitting.");
            return;
        }
        //display loading message while waiting for the response
        results.innerHTML = '<p>Loading...</p>'; 
    
        //create a new form data object and append the csrf token
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        //if the image was cropped then use the cropped image
        //we will also give the cropped image a unique name based on the time it was cropped
        if (cropped) {
            cropper.getCroppedCanvas().toBlob(async (blob) => {
                const uniqueFileName = `cropped_${Date.now()}.jpg`;
                formData.append('image', blob, uniqueFileName);
                await submitForm(formData);
            });
        } else {
            //if user didnt crop the image then use the original image
            const file = inputimg.files[0];
            if (file) {
                formData.append('image', file);
                await submitForm(formData);
            } else {
                alert("Please upload an image before submitting.");
            }
        }
    });

    async function submitForm(formData) {
        try {
            //connects to views.py send post request to the root url
            const response = await fetch('/', { 
                method: 'POST',
                //send the form data as the body of the request
                body: formData,
            });
    
            if (response.ok) {
                //recieve the data from the response
                const data = await response.json();
                //recieve the data from views.py
                const { predicted_breed, confidence, facts, image_url } = data;
    
                //display the results in the html template
                //display the image, predicted breed, confidence and facts
                results.innerHTML = `
                    <h2>Prediction Results</h2>
                    <img src="${image_url}" alt="Uploaded Image" style="max-width: 300px;">
                    <h3>Predicted Breed: ${predicted_breed}</h3>
                    <h3>Confidence: ${confidence.toFixed(2)}%</h3>
                    <h3>Facts:</h3>
                    <ul>
                        <li>Length: ${facts.Length || "Unknown"}</li>
                        <li>Child Friendly: ${facts["Children Friendly"] || "Unknown"}</li>
                        <li>General Health: ${facts["General Health"] || "Unknown"}</li>
                    </ul>
                `;
                //set the latest image url to the image url received from the server
                //this will be used for reverse search
                latestimgUrl = image_url;
                console.log("Image URL received from Django:", image_url);
                console.log("Image URL set to:", latestimgUrl);
                //display an error message if the request failed
            } else {
                const error = await response.json();
                results.innerHTML = `<p style="color: red;">${error.error || 'Error processing the image.'}</p>`;
            }
            //handle any errors that occur
        } catch (error) {
            console.error('Error:', error);
            results.innerHTML = '<p style="color: red;">An error occurred. Please try again later.</p>';
        }
        
    }

    //if the user clicks the reverse search button, open the google lens page with the image url
    if (reversesearch) {
        reversesearch.addEventListener("click", () => {
            //check if the latest image url is set
            //if it is set then open the google lens page with the image url
            if (latestimgUrl) {
                const lensurl = `https://lens.google.com/uploadbyurl?url=${encodeURIComponent(latestimgUrl)}`;
                window.open(lensurl, '_blank');
            } else {
                alert("Image not ready for reverse search yet.");
            }
        });
    } else {
        console.warn("Reverse search button not found in DOM.");
    }

});