import React from 'react';
import axios from 'axios';
import './Prediction.css';
//import Radio from '@material-ui/core/Radio';

/*class Prediction extends React.Component {

}*/
class Prediction extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            image: null, //The image file to be classified
            confusionMatrix: '', //The confusion matrix image that will be returned once directory is classified
            directory: '', //The option to classify a directory
            imagePreviewUrl: null, //The image that will be classified
            selectedModelOption: '', //Which base model to use
            selectedOtherOptions: [], //Fine tuning, ensembles, etc.
            withSigmaPrediciton: '', //The with prediction confidence returned from classification
            withoutSigmaPrediction: '', //The without prediction confidence returned from classification
            predictions: [],
            checked: false
        };

        this.handleImagePreview = this.handleImagePreview.bind(this);
        this.classifyImage = this.classifyImage.bind(this);
        this.handleModelOptionChange = this.handleModelOptionChange.bind(this);
        this.handleOtherOptionsChange = this.handleOtherOptionsChange.bind(this);
        this.classifyDirectory = this.classifyDirectory.bind(this);
        this.classificationResults = this.classificationResults.bind(this);
    }

    /*The classification data returned by axios. */
    classificationResults (response){
        if(this.state.image !== null){
            let responseData = JSON.parse(JSON.stringify(response)); //Transform the response data into JSON
            console.log(responseData);
            //Single image classification is returned as a string, so split by ,.  
            let classification = responseData.data.split(',')
            let withSigma = classification[0]; 
            let withoutSigma = classification[1];
            this.setState({
                withSigmaPrediciton: withSigma,
                withoutSigmaPrediction: withoutSigma
            });
        }

        if(this.state.directory !== ''){
            let matrixData = response.data;
            //The confusion matrix image is sent as a base64 encoded string. 
            //Add data before string so that it can be rendered on the screen. 
            let srcData = "data:image/jpeg;base64," + matrixData;
            this.setState({
                confusionMatrix: srcData
            });
        }
    }

    //This function handles sending the data to Flask through axios so that the image or directory can be classified. 
    async classifyImage(uploadEvent) {
        if(this.state.selectedModelOption === ''){
            alert('Please choose a model to use');
        }
        console.log('inside classifyImage');
        console.log('the selectedModelOption is:', this.state.selectedModelOption);
        uploadEvent.preventDefault();

        //The data to include in the HTTP request 
        let imageToUpload = this.state.image;
        let modelOption = this.state.selectedModelOption;
        let otherOptions = this.state.selectedOtherOptions;
        let classifyDirectoryOption = this.state.directory;

        const formData = new FormData();

        //If the directory was chosen, don't send the image data. 
        if(this.state.image === null)
        {
            formData.append('model', modelOption);
            formData.append('options', otherOptions);
            formData.append('directory', classifyDirectoryOption);
        }

        //If the image was chosen, don't send the directory data.
        if(this.state.directory === '')
        {
            formData.append('image', imageToUpload);
            formData.append('directory', this.state.directory);
            formData.append('model', modelOption);
            formData.append('options', otherOptions);
            
        }
        //Send request to Flask 
        const response = await axios({
            method: 'post',
            url: 'http://localhost:5000/classify',
            data: formData,
            config: { headers: { 'Content-Type': 'multipart/form-data' } }
        });
        return this.classificationResults(response);

    }

    //This function will check to see if a user has already chosen to classify an image. 
    //If not, it sets the directory option which will be sent in the formData of the HTTP request. 
    classifyDirectory(changeEvent){
        console.log('inside classifyDirectory')
        if (this.state.image) {
            alert("You have already chosen to classify an image!");
            return
        }
       
        let directoryChosen = changeEvent.target.value;
        this.setState({
            directory: directoryChosen,
            checked: true
        });
    }

    //This function will check to see if a user has already chosen to classify a directory. 
    //If not, it sets the image option which will be sent in the formData of the HTTP request. 
    handleImagePreview(previewEvent) {
        if (this.state.directory !== '') {
            alert("You have already chosen to classify a directory!");
            previewEvent.target.value = null; //reset the value to null so that the filename doesn't change since the directory button is checked.
            return
        }

        //Use FileReader API to get image and display on screen. 
        let reader = new FileReader();
        let image = previewEvent.target.files[0];

        reader.onloadend = () => {
            this.setState({
                image: image,
                imagePreviewUrl: reader.result
            });
        }
            reader.readAsDataURL(image);
    }

    //This function will set the state of certain options based on which checkboxes were chosen. 
    //Input: strings i.e ensembles, fine-tuning. 
    //Output: an array containing the strings. This will be sent in formData of HTTP request. 
    handleOtherOptionsChange(changeEvent){
        console.log('inside handleOtherOptionsChange')
        console.log('selectedOtherOptions are', this.state.selectedOtherOptions);
        console.log(changeEvent.target.value)
     
        let newOtherOptions = this.state.selectedOtherOptions;
        newOtherOptions.push(changeEvent.target.value);

        console.log(newOtherOptions);
        this.setState({
            selectedOtherOptions: newOtherOptions
        })
    }
    
    //This function will set the state of the base model to use. 
    //Input: strings i.e resnet, inception, vgg16. 
    //Output: The string that corresponds to the model chosen 
    handleModelOptionChange(changeEvent){
        console.log('inside handleModelOptionChange')
        console.log('selectedModelOption is initially:', this.state.selectedModelOption);
        let newModelOption = changeEvent.target.value;
        console.log(newModelOption);
        this.setState({
            selectedModelOption: newModelOption
        });

        console.log('selectedModelOption is now:', this.state.newModelOption);
    }

    render() {
        return (
            <form method='post' action='http://localhost:5000/classify' encType="multipart/form-data" onSubmit={this.classifyImage}>    
                <div className="row row-margin-top choseImageDiv">
                    <div className="col-md-4"> 
                        <input type="file" id="image-to-upload" onChange={this.handleImagePreview} />
                    </div>
                    <div className="col-md-3 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="directory-input" value="directory" checked={this.state.checked} onChange={this.classifyDirectory} />
                        <label className="custom-control-label" htmlFor="directory-input">Classify a Directory</label>
                    </div>
                    <div className="col-md-0.1">
                        <button type="submit"  className="btn btn-outline-dark" onClick={this.classifyImage}> Classify </button>
                    </div>
                </div>
                <div className="row row-margin-top optionsDiv">
                    <div className="col-md-2" id="model-option">
                        Model
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline">
                        <input type="radio" className="custom-control-input" id="resnet-input" value="resnet" checked={this.state.selectedModelOption === 'resnet'} onChange={this.handleModelOptionChange} disabled/>
                        <label className="custom-control-label" htmlFor="resnet-input">ResNet</label>
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline" >
                        <input type="radio" className="custom-control-input" id="inception-input" value="inception" checked={this.state.selectedModelOption === 'inception'} onChange={this.handleModelOptionChange}/>
                        <label className="custom-control-label" htmlFor="inception-input">Inception</label>
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline" >
                        <input type="radio" className="custom-control-input" id="vgg16-input" value="vgg16" checked={this.state.selectedModelOption === 'vgg16'} onChange={this.handleModelOptionChange} disabled/>
                        <label className="custom-control-label " htmlFor="vgg16-input">VGG16</label>
                    </div>
                    <div className="col-md-3" id="other-option">
                        Other Options
                    </div>
                    <div className="col-md-1 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="ensembles-check" value="ensembles"  onChange={this.handleOtherOptionsChange} disabled/>
                        <label className="custom-control-label " htmlFor="ensembles-check">Ensembles</label>
                    </div>
                    <div className="col-md-0.5 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="fine-tuning-check" value="fine-tuning" onChange={this.handleOtherOptionsChange} disabled/>
                        <label className="custom-control-label" htmlFor="fine-tuning-check">Fine Tuning</label>

                    </div>
               </div>
                <div className="row row-margin-bot predictionDiv">
                    <div className="col-md-6 prediction-image">
                        <h5 id="image-to-predict">Image to Predict</h5>
                        <img id="image-preview"src={this.state.imagePreviewUrl} className="img-thumbnail" alt="" />
                    </div>

                    <div className="col-md-3">
                        <h5 id="prediction-confidence">Prediction Confidence: </h5>
                        <ol className="classificationList">
                            <li> {this.state.withSigmaPrediciton}</li>
                            <li> {this.state.withoutSigmaPrediction}</li>
                            <img id="confusion-matrix" src={this.state.confusionMatrix} alt="" />
                        </ol>   
                        
                    </div>
                </div>
            </form>
        )
    }
}

export default Prediction;