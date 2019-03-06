import React from 'react';
import axios from 'axios';

class ImageUpload extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            file: null,
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
                <div class="form-group">
                    <input type="file" class="form-control-file" onChange={this.handleImagePreview} />
                    <img src={this.state.imagePreviewUrl} class="img-thumbnail" alt="" />
                    <button type="submit" class="btn btn-outline-dark" onClick={this.handleImageUpload}> Upload Photo </button>
                </div>
            </form>
        )
    }

}

export default ImageUpload;