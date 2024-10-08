import { useState, useRef } from "react";
import "./App.css";
import Webcam from "react-webcam";
import { isMobile } from "react-device-detect";

function App() {
  // Reference for the webcam output
  const webcamRef = useRef(null);
  // Reference for the file input
  const inputRef = useRef(null);
  // Flag to check if webcam is open
  const [openWebcam, setOpenWebcam] = useState(false);
  // Image file to be passed in base64 string
  const [imageFile, setImageFile] = useState(null);
  // Result image file after detection in base64 string
  const [resultImage, setResultImage] = useState(null);

  // When the CAPTURE button is clicked in webcam
  const capture = () => {
    // Get screenshot of webcam stream
    // Outputs base64 string of image
    const imageSrc = webcamRef.current.getScreenshot();
    // Set this screenshot as the imageFile
    setImageFile(imageSrc);
  };

  // When the UPLOAD IMAGE button is clicked
  const handleChange = (e) => {
    // Get the selected file in the file input
    const file = e.target.files[0];

    // Initialize reader that will convert file to base64 string
    const reader = new FileReader();

    reader.onloadend = () => {
      // reader.result is the base64 string
      setImageFile(reader.result);
    };

    // Convert file to base64 string
    reader.readAsDataURL(file);
  };

  // When the reset button is clicked
  const handleReset = () => {
    // Close webca,
    setOpenWebcam(false);
    // Clear input image
    setImageFile(null);
    // Clear result image, if there are any
    setResultImage(null);
    // Clear selected file in file input
    inputRef.current.value = "";
  };

  const handleDetect = async () => {
    // Checks if there is a input image file
    if (imageFile) {
      // Pass this image file (base64 string) to server
      const response = await fetch(
        import.meta.env.VITE_API_URL + "/yolo/detect",
        {
          method: "POST",
          body: JSON.stringify({ image_uri: imageFile }),
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Await result from server
      // Result is in base64 string
      const data = await response.json();

      // Display base64 string as an image
      setResultImage(data.result_image);
    }
  };
  return (
    <main>
      <div className="webcam-container">
        <div className="webcam-wrapper">
          <input
            type="file"
            name="upload-image"
            ref={inputRef}
            hidden
            onChange={handleChange}
            accept="image/*"
          />
          {imageFile ? (
            <div className="image-wrapper">
              <img src={imageFile} alt="image-file" />
            </div>
          ) : openWebcam ? (
            <div className="webcam-capture">
              <Webcam
                className="webcam"
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                videoConstraints={{
                  facingMode: isMobile ? { exact: "environment" } : "user",
                }}
              />
              <button onClick={capture}>CAPTURE</button>
            </div>
          ) : (
            <div className="choices">
              <button onClick={() => setOpenWebcam(true)}>Open Webcam</button>
              <button onClick={() => inputRef.current.click()}>
                Upload Image
              </button>
            </div>
          )}
        </div>
      </div>
      <div className="actions-container">
        <div className="actions-wrapper">
          <button onClick={handleDetect}>DETECT</button>
          <button onClick={handleReset}>RESET</button>
        </div>
      </div>
      <div className="prediction-container">
        <div className="prediction-wrapper">
          {resultImage && (
            <div className="image-wrapper">
              <img src={resultImage} alt="result-image" />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

export default App;
