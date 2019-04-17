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
            imagePreviewUrl: null,
            selectedModelOption: '',
            selectedOtherOptions: [],
            prediciton: []
        };

        this.handleImagePreview = this.handleImagePreview.bind(this);
        this.classifyImage = this.classifyImage.bind(this);
        this.handleModelOptionChange = this.handleModelOptionChange.bind(this);
        this.handleOtherOptionsChange = this.handleOtherOptionsChange.bind(this);
    }
    classificationResults (response){
        console.log(response);
        let responseData = JSON.parse(JSON.stringify(response));
        console.log(responseData);
        let classification = responseData.data.replace(/[^a-zA-Z0-9 , _]/g, "");
        console.log(classification);
        let individualClassification = classification.split(',');
        this.setState({
            prediciton: individualClassification
        });
    }

    async classifyImage(uploadEvent) {

        console.log('inside classifyImage');
        console.log('the selectedModelOption is:', this.state.selectedModelOption);
        uploadEvent.preventDefault();
        let imageToUpload = this.state.image;
        let modelOption = this.state.selectedModelOption;
        let otherOptions = this.state.selectedOtherOptions;

        console.log(modelOption);

        const formData = new FormData();

        formData.append('image', imageToUpload);
        formData.append('model', modelOption);
        formData.append('options', otherOptions);
        console.log(formData);
       return axios({
            method: 'post',
            url: 'http://localhost:5000/classify',
            data: formData,
            config: { headers: { 'Content-Type': 'multipart/form-data' } }
        })
        .then(response => this.classificationResults(response))

    }

    handleImagePreview(previewEvent) {
        console.log('in preview')

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
                    <div className="col-md-5"> 
                        <input type="file" className="btn" onChange={this.handleImagePreview} />
                    </div>
                    <div className="col-md-0.1">
                        <button type="submit" className="btn btn-outline-dark" onClick={this.classifyImage}> Classify </button>
                    </div>
                    <div className="">
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
                    <div className="col-md-0.5 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="other-check" value="other" onChange={this.handleOtherOptionsChange} />
                        <label className="custom-control-label" htmlFor="other-check">Another Option</label>

                    </div>
               </div>
                <div className="row row-margin-bot predictionDiv">
                    <div className="col-md-2">
                        <h5>Prediction: </h5>
                        <ol className="classificationList">
                            {this.state.prediciton.map((element, idx) => <li key={idx}>{element}</li>)}
                        </ol>
                    </div>
                    <div className="col-md-10">
                        <img src={this.state.imagePreviewUrl} className="img-thumbnail img-responsive" alt="" />
                    </div>
                </div>
            </form>
        )
    }
}

export default Prediction;