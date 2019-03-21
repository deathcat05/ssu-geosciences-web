import React from 'react';
import axios from 'axios';
import './ImageUpload.css';

/*class Prediction extends React.Component {

}*/
class ImageUpload extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            file: null,
            imagePreviewUrl: null
        };

        this.handleImagePreview = this.handleImagePreview.bind(this);
        this.handleImageUpload = this.handleImageUpload.bind(this);
    }


    handleImageUpload(uploadEvent) {

        // console.log("image upload")
        uploadEvent.preventDefault();
        let fileToUpload = this.state.file;

        //console.log(fileToUpload);
        const formData = new FormData();

        formData.append('file', fileToUpload);
        console.log(formData)

        axios({
            method: 'post',
            url: 'http://localhost:5000/upload',
            data: formData,
            config: { headers: { 'Content-Type': 'multipart/form-data' } }
        })
            .then(response => console.log(response))
            .catch(errors => console.log(errors))

    }

    handleImagePreview(previewEvent) {
        console.log('in preview')

        let reader = new FileReader();
        let file = previewEvent.target.files[0];

        reader.onloadend = () => {
            this.setState({
                file: file,
                imagePreviewUrl: reader.result
            });
        }

        reader.readAsDataURL(file)
    }

    render() {
        return (
            <form method='post' action='http://localhost:5000/upload' encType="multipart/form-data" onSubmit={this.handleImageUpload}>    
                <div className="row row-margin-bot row-center">
                    <div className="col-md-5"> 
                        <input type="file" class="btn" onChange={this.handleImagePreview} />
                    </div>
                    <div className="col-md-2">
                        <button type="submit" className="btn btn-outline-dark" onClick={this.handleImageUpload}> Classify </button>
                    </div>
                </div>
                <div className="row row-margin-bot">
                    <div className="col-md-2" id="model-option">
                        Model
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline">
                        <input type="radio" className="custom-control-input" id="resnet-input"/>
                        <label className="custom-control-label" htmlFor="resnet-input">ResNet</label>
                    </div>
                    <div className="col-md-0.5 custom-radio custom-control custom-radio custom-control-inline" >
                        <input type="radio" className="custom-control-input" id="inception-input"/>
                        <label className="custom-control-label" htmlFor="inception-input">Inception</label>
                    </div>
                    <div className="col-md-3" id="other-option">
                        Other Options
                    </div>
                    <div className="col-md-1 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="ensembles-check"/>
                        <label className="custom-control-label" htmlFor="ensembles-check">Ensembles</label>
                    </div>
                    <div className="col-md-0.5 custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="fine-tuning-check"/>
                        <label className="custom-control-label" htmlFor="fine-tuning-check">Fine Tuning</label>

                    </div>
               </div>
               <div>
                    <img src={this.state.imagePreviewUrl} className="img-thumbnail img-responsive" alt="" />
               </div>
                
            </form>
        )
    }
}

export default ImageUpload;