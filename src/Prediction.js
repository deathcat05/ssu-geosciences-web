import React from 'react';
import axios from 'axios';
import './Prediction.css';

/*class Prediction extends React.Component {

}*/
class Prediction extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            image: null,
            directory: '',
            imagePreviewUrl: null,
            selectedModelOption: '',
            selectedOtherOptions: [],
            withSigmaPrediciton: '',
            withoutSigmaPrediction: '',
            predictions: [],
            checked: false
        };

        this.handleImagePreview = this.handleImagePreview.bind(this);
        this.classifyImage = this.classifyImage.bind(this);
        this.handleModelOptionChange = this.handleModelOptionChange.bind(this);
        this.handleOtherOptionsChange = this.handleOtherOptionsChange.bind(this);
        this.classifyDirectory = this.classifyDirectory.bind(this);
    }
    classificationResults (response){
        console.log(response);
        let responseData = JSON.parse(JSON.stringify(response));
        console.log(responseData);
        let classification = responseData.data.split(',')
        console.log(classification);
        let withSigma = classification[0];
        let withoutSigma = classification[1];
        this.setState({
            withSigmaPrediciton: withSigma,
            withoutSigmaPrediction: withoutSigma
        });
    }

    async classifyImage(uploadEvent) {

        console.log('inside classifyImage');
        console.log('the selectedModelOption is:', this.state.selectedModelOption);
        uploadEvent.preventDefault();
        let imageToUpload = this.state.image;
        let modelOption = this.state.selectedModelOption;
        let otherOptions = this.state.selectedOtherOptions;
        let classifyDirectoryOption = this.state.directory;

        console.log(modelOption);

        const formData = new FormData();
        //If the directory was chosen, don't send the image data. 
        if(this.state.image === null)
        {
            formData.append('image', this.state.image);
            formData.append('model', modelOption);
            formData.append('options', otherOptions);
            formData.append('directory', classifyDirectoryOption);
        }
        console.log(formData)
        //If the image was chosen, don't send the directory data.
        if(this.state.directory === '')
        {
            formData.append('image', imageToUpload);
            formData.append('model', modelOption);
            formData.append('options', otherOptions);
            formData.append('directory', this.state.directory);
        }
        console.log(formData)
        
       return axios({
            method: 'post',
            url: 'http://localhost:5000/classify',
            data: formData,
            config: { headers: { 'Content-Type': 'multipart/form-data' } }
        })
        .then(response => this.classificationResults(response))

    }
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
    handleImagePreview(previewEvent) {
        console.log('in preview')
        if(this.state.directory){
            alert("You have already chosen to classify a directory!");
            return
        }
        let reader = new FileReader();
        let image = previewEvent.target.files[0];

        reader.onloadend = () => {
            this.setState({
                image: image,
                imagePreviewUrl: reader.result
            });
        }

        reader.readAsDataURL(image)
    }

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
                <div className="row row-margin-bot choseImageDiv">
                    <div className="col-md-4"> 
                        <input type="file" className="btn" onChange={this.handleImagePreview} />
                    </div>
                    <div className="col-md-3 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="directory-input" value="directory" checked={this.state.checked} onChange={this.classifyDirectory} />
                        <label className="custom-control-label" htmlFor="directory-input">Classify a Directory</label>
                    </div>
                    <div className="col-md-0.1">
                        <button type="submit" className="btn btn-outline-dark" onClick={this.classifyImage}> Classify </button>
                    </div>
                </div>
                <div className="row row-margin-bot optionsDiv">
                    <div className="col-md-2" id="model-option">
                        Model
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline">
                        <input type="radio" className="custom-control-input" id="resnet-input" value="resnet" checked={this.state.selectedModelOption === 'resnet'} onChange={this.handleModelOptionChange}/>
                        <label className="custom-control-label" htmlFor="resnet-input">ResNet</label>
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline" >
                        <input type="radio" className="custom-control-input" id="inception-input" value="inception" checked={this.state.selectedModelOption === 'inception'} onChange={this.handleModelOptionChange}/>
                        <label className="custom-control-label" htmlFor="inception-input">Inception</label>
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline" >
                        <input type="radio" className="custom-control-input" id="vgg16-input" value="vgg16" checked={this.state.selectedModelOption === 'vgg16'} onChange={this.handleModelOptionChange} />
                        <label className="custom-control-label" htmlFor="vgg16-input">VGG16</label>
                    </div>
                    <div className="col-md-3" id="other-option">
                        Other Options
                    </div>
                    <div className="col-md-1 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="ensembles-check" value="ensembles"  onChange={this.handleOtherOptionsChange}/>
                        <label className="custom-control-label" htmlFor="ensembles-check">Ensembles</label>
                    </div>
                    <div className="col-md-0.5 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="fine-tuning-check" value="fine-tuning" onChange={this.handleOtherOptionsChange}/>
                        <label className="custom-control-label" htmlFor="fine-tuning-check">Fine Tuning</label>

                    </div>
               </div>
                <div className="row row-margin-bot predictionDiv">
                    <div className="col-md-6">
                        <img src={this.state.imagePreviewUrl} className="img-thumbnail img-responsive" alt="" />
                    </div>

                    <div className="col-md-2">
                        <h5>Prediction Confidence: </h5>
                        <ol className="classificationList">
                            <li> With Sigma: {this.state.withSigmaPrediciton}</li>
                            <li>Without Sigma: {this.state.withoutSigmaPrediction}</li>
                        </ol>
                    </div>
                </div>
            </form>
        )
    }
}

export default Prediction;